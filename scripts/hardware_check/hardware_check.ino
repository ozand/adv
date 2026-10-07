#include <M5Cardputer.h>
#include <SD.h>

static constexpr char kSdTestPath[] = "/ADV_DIAGNOSTIC_SD_TEST.BIN";
static constexpr size_t kSdTestBytes = 64 * 1024;
static constexpr size_t kSdChunkBytes = 512;
static bool ready = false;
static bool boardReady = false;
static bool imuReady = false;
static bool sdDone = false;
enum class SdState { NotRun, Running, Pass, Fail };
enum class SdStage { Idle, Mount, Write, Read, Cleanup, Complete, Error };
enum class SdCleanup { NotAttempted, Removed, Failed, Retained };
static SdState sdState = SdState::NotRun;
static SdStage sdStage = SdStage::Idle;
static SdCleanup sdCleanup = SdCleanup::NotAttempted;
static const char *sdReason = "none";
static size_t sdBytesVerified = 0;
static char sdStatus[48] = "SD: press S to test";

static const char *stateName() {
  switch (sdState) {
    case SdState::NotRun: return "not_run";
    case SdState::Running: return "running";
    case SdState::Pass: return "pass";
    case SdState::Fail: return "fail";
  }
  return "fail";
}

static const char *stageName() {
  switch (sdStage) {
    case SdStage::Idle: return "idle";
    case SdStage::Mount: return "mount";
    case SdStage::Write: return "write";
    case SdStage::Read: return "read";
    case SdStage::Cleanup: return "cleanup";
    case SdStage::Complete: return "complete";
    case SdStage::Error: return "error";
  }
  return "error";
}

static const char *cleanupName() {
  switch (sdCleanup) {
    case SdCleanup::NotAttempted: return "not_attempted";
    case SdCleanup::Removed: return "removed";
    case SdCleanup::Failed: return "failed";
    case SdCleanup::Retained: return "retained";
  }
  return "failed";
}

static void emitJson(const char *type, const char *reason) {
  char json[384];
  const int length = snprintf(json, sizeof(json),
      "{\"v\":1,\"type\":\"%s\",\"firmware_build\":\"adv-diagnostic-1\",\"board_ready\":%s,\"imu_ready\":%s,\"sd\":{\"state\":\"%s\",\"stage\":\"%s\",\"reason\":\"%s\",\"bytes_verified\":%u,\"cleanup\":\"%s\"}}\r\n",
      type, boardReady ? "true" : "false", imuReady ? "true" : "false",
      stateName(), stageName(), reason, static_cast<unsigned>(sdBytesVerified), cleanupName());
  if (length > 0 && static_cast<size_t>(length) < sizeof(json)) {
    Serial.write(reinterpret_cast<const uint8_t *>(json), static_cast<size_t>(length));
  }
}

static uint8_t patternByte(size_t offset) {
  return static_cast<uint8_t>((offset * 37u + 0x5Au) & 0xFFu);
}

static void runSdSelfTest() {
  sdDone = true;
  sdState = SdState::Running;
  sdStage = SdStage::Mount;
  sdReason = "none";
  sdCleanup = SdCleanup::NotAttempted;
  sdBytesVerified = 0;
  snprintf(sdStatus, sizeof(sdStatus), "SD: checking card...");

  const int cs = M5.getPin(m5::pin_name_t::sd_spi_cs);
  const int sck = M5.getPin(m5::pin_name_t::sd_spi_sclk);
  const int miso = M5.getPin(m5::pin_name_t::sd_spi_miso);
  const int mosi = M5.getPin(m5::pin_name_t::sd_spi_mosi);
  if (cs < 0 || sck < 0 || miso < 0 || mosi < 0) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "unsupported_pin_map";
    snprintf(sdStatus, sizeof(sdStatus), "SD: unsupported pin map");
    return;
  }

  SPI.begin(sck, miso, mosi, cs);
  if (!SD.begin(cs, SPI, 4000000, "/sdcard", 2, false)) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "mount_failed";
    snprintf(sdStatus, sizeof(sdStatus), "SD: mount failed; no format");
    return;
  }

  if (SD.cardType() == CARD_NONE || SD.cardSize() < kSdTestBytes) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "invalid_or_small";
    sdCleanup = SdCleanup::NotAttempted;
    snprintf(sdStatus, sizeof(sdStatus), "SD: invalid/too small");
    SD.end();
    return;
  }

  if (SD.exists(kSdTestPath)) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "test_path_exists";
    snprintf(sdStatus, sizeof(sdStatus), "SD: test path exists");
    SD.end();
    return;
  }

  File testFile = SD.open(kSdTestPath, FILE_WRITE);
  if (!testFile) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "create_failed";
    snprintf(sdStatus, sizeof(sdStatus), "SD: create failed");
    SD.end();
    return;
  }

  sdStage = SdStage::Write;
  uint8_t buffer[kSdChunkBytes];
  bool writeOk = true;
  size_t written = 0;
  const uint32_t writeStart = millis();
  while (written < kSdTestBytes && millis() - writeStart < 15000) {
    const size_t remaining = kSdTestBytes - written;
    const size_t count = remaining < kSdChunkBytes ? remaining : kSdChunkBytes;
    for (size_t i = 0; i < count; ++i) buffer[i] = patternByte(written + i);
    if (testFile.write(buffer, count) != count) {
      writeOk = false;
      break;
    }
    written += count;
  }
  testFile.flush();
  testFile.close();
  writeOk = writeOk && written == kSdTestBytes;
  if (!writeOk) {
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "write_failed_or_timeout"; sdCleanup = SdCleanup::Retained;
    snprintf(sdStatus, sizeof(sdStatus), "SD: write fail; file retained");
    SD.end();
    return;
  }

  sdStage = SdStage::Read;
  testFile = SD.open(kSdTestPath, FILE_READ);
  if (!testFile || testFile.size() != kSdTestBytes) {
    if (testFile) testFile.close();
    sdState = SdState::Fail; sdStage = SdStage::Error; sdReason = "read_open_or_size_failed"; sdCleanup = SdCleanup::Retained;
    snprintf(sdStatus, sizeof(sdStatus), "SD: read open/size fail; retained");
    SD.end();
    return;
  }

  bool match = true;
  size_t checked = 0;
  const uint32_t readStart = millis();
  while (checked < kSdTestBytes && millis() - readStart < 15000) {
    const size_t remaining = kSdTestBytes - checked;
    const size_t count = remaining < kSdChunkBytes ? remaining : kSdChunkBytes;
    if (testFile.read(buffer, count) != count) {
      sdReason = "read_failed_or_timeout";
      match = false;
      break;
    }
    for (size_t i = 0; i < count; ++i) {
      if (buffer[i] != patternByte(checked + i)) {
        sdReason = "verify_mismatch";
        match = false;
        break;
      }
    }
    if (!match) break;
    checked += count;
    sdBytesVerified = checked;
  }
  testFile.close();
  match = match && checked == kSdTestBytes;

  sdStage = SdStage::Cleanup;
  const bool removed = match && SD.remove(kSdTestPath);
  sdState = match ? SdState::Pass : SdState::Fail;
  sdStage = SdStage::Complete;
  if (match) sdReason = "none";
  else if (strcmp(sdReason, "none") == 0) sdReason = "verify_failed_or_timeout";
  sdCleanup = match ? (removed ? SdCleanup::Removed : SdCleanup::Failed) : SdCleanup::Retained;
  snprintf(sdStatus, sizeof(sdStatus), "SD: %s; file %s",
           match ? "PASS" : "FAIL",
           match ? (removed ? "removed" : "cleanup fail") : "retained");
  SD.end();
}

void setup() {
  auto cfg = M5.config();
  cfg.output_power = false;
  cfg.internal_mic = false;
  cfg.internal_spk = false;
  cfg.internal_rtc = false;
  cfg.external_imu = false;
  cfg.internal_imu = false;
  cfg.clear_display = true;
  M5.begin(cfg);  // Display auto-detection/init occurs before board gate.
  Serial.begin(115200);

  if (M5.getBoard() != m5::board_t::board_M5CardputerADV) {
    M5.Display.setTextSize(1);
    M5.Display.println("Unsupported board; stopping.");
    return;
  }

  boardReady = true;
  M5Cardputer.Keyboard.begin();
  if (!M5.Imu.begin(&M5.In_I2C, M5.getBoard())) {
    M5.Display.println("ADV OK; BMI270 init failed.");
    return;
  }

  imuReady = true;
  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.fillRect(0, 0, 40, 18, TFT_RED);
  M5.Display.fillRect(45, 0, 40, 18, TFT_GREEN);
  M5.Display.fillRect(90, 0, 40, 18, TFT_BLUE);
  M5.Display.setCursor(0, 24);
  M5.Display.println("ADV OK / BMI270 OK");
  M5.Display.println("Press S to run bounded SD test");
  ready = true;
}

static constexpr size_t kCommandMaxBytes = 64;
static char commandBuffer[kCommandMaxBytes];
static size_t commandLength = 0;
static bool commandOverflow = false;

static void handleCommandLine() {
  if (commandOverflow || commandLength == 0) {
    emitJson("error", "invalid_command");
  } else if (commandLength == 6 && memcmp(commandBuffer, "status", 6) == 0) {
    emitJson("status", "none");
  } else if (commandLength == 7 && memcmp(commandBuffer, "sd_test", 7) == 0) {
    if (!ready && !sdDone) emitJson("sd_test", "not_ready");
    else {
      if (!sdDone) runSdSelfTest();
      emitJson("sd_test", sdReason);
    }
  } else {
    emitJson("error", "invalid_command");
  }
  commandLength = 0;
  commandOverflow = false;
}

static void pollSerialCommands() {
  while (Serial.available() > 0) {
    const int value = Serial.read();
    if (value == '\n') {
      if (commandLength > 0 && commandBuffer[commandLength - 1] == '\r') --commandLength;
      handleCommandLine();
    } else if (!commandOverflow) {
      if (value < 0x20 || value > 0x7E || commandLength == kCommandMaxBytes) {
        commandOverflow = true;
      } else {
        commandBuffer[commandLength++] = static_cast<char>(value);
      }
    }
  }
}

void loop() {
  pollSerialCommands();
  if (!ready) {
    delay(1000);
    return;
  }

  M5.update();
  M5Cardputer.Keyboard.updateKeyList();
  M5Cardputer.Keyboard.updateKeysState();
  for (char key : M5Cardputer.Keyboard.keysState().word) {
    if ((key == 's' || key == 'S') && !sdDone) runSdSelfTest();
  }
  M5.Imu.update();
  const auto data = M5.Imu.getImuData();

  M5.Display.fillRect(0, 42, 240, 95, TFT_BLACK);
  M5.Display.setCursor(0, 42);
  M5.Display.printf("G: %.2f %.2f %.2f\n", data.gyro.x, data.gyro.y, data.gyro.z);
  M5.Display.printf("A: %.2f %.2f %.2f\n", data.accel.x, data.accel.y, data.accel.z);
  M5.Display.setCursor(0, 103);
  M5.Display.print(sdStatus);
  M5.Display.setCursor(0, 119);
  M5.Display.print("Keys: ");
  for (char key : M5Cardputer.Keyboard.keysState().word) {
    M5.Display.write(static_cast<uint8_t>(key));
  }
  M5.Display.println();
  delay(100);
}
