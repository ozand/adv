#include <M5Cardputer.h>
#include <SD.h>

static constexpr char kSdTestPath[] = "/ADV_DIAGNOSTIC_SD_TEST.BIN";
static constexpr size_t kSdTestBytes = 64 * 1024;
static constexpr size_t kSdChunkBytes = 512;
static bool ready = false;
static bool boardReady = false;
static bool imuReady = false;
static bool sdDone = false;
static char lastRunId[13] = "";
static bool runRecordValid = false;
static char runOverall[16] = "NOT_TESTED";
static char runChecks[12][16];
static char runReasons[12][32];
static uint32_t runHeapBytes = 0;
static uint16_t runRamBytesVerified = 0;
static uint8_t runImuSamples = 0;
static const char *const kCheckNames[12] = {"mcu", "ram_scratch", "imu_data", "motion", "display", "keyboard", "audio", "ir", "radio", "battery", "connectors", "sd"};
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
  const char *safeType = (strcmp(type, "status") == 0 || strcmp(type, "sd_test") == 0 ||
                          strcmp(type, "sd_test_result") == 0 || strcmp(type, "error") == 0)
                             ? type : "error";
  static const char *const safeReasons[] = {
      "none", "invalid_command", "not_ready", "unsupported_pin_map", "mount_failed",
      "invalid_or_small", "test_path_exists", "create_failed", "write_failed_or_timeout",
      "read_open_or_size_failed", "read_failed_or_timeout", "verify_mismatch",
      "verify_failed_or_timeout"};
  bool reasonAllowed = false;
  for (const char *safeReason : safeReasons) {
    if (strcmp(reason, safeReason) == 0) reasonAllowed = true;
  }
  const char *safeReason = reasonAllowed ? reason : "invalid_command";
  const int length = snprintf(json, sizeof(json),
      "{\"v\":1,\"type\":\"%s\",\"firmware_build\":\"adv-diagnostic-2\",\"board_ready\":%s,\"imu_ready\":%s,\"sd\":{\"state\":\"%s\",\"stage\":\"%s\",\"reason\":\"%s\",\"bytes_verified\":%u,\"cleanup\":\"%s\"}}\r\n",
      safeType, boardReady ? "true" : "false", imuReady ? "true" : "false",
      stateName(), stageName(), safeReason, static_cast<unsigned>(sdBytesVerified), cleanupName());
  if (length > 0 && static_cast<size_t>(length) < sizeof(json)) {
    Serial.write(reinterpret_cast<const uint8_t *>(json), static_cast<size_t>(length));
  }
}

static constexpr size_t kRunFrameMaxBytes = 1024;
static const char *responseRunId(const char *requestedId) {
  if (runRecordValid && strcmp(lastRunId, requestedId) == 0) return lastRunId;
  return requestedId;
}
static void emitRunJson(const char *type, const char *errorReason, const char *requestedId) {
  const char *responseId = responseRunId(requestedId);
  char json[kRunFrameMaxBytes];
  const char *safeType = (strcmp(type, "run_ack") == 0 || strcmp(type, "run_result") == 0 ||
                          strcmp(type, "result") == 0 || strcmp(type, "error") == 0) ? type : "error";
  size_t used = 0;
  int n = snprintf(json, sizeof(json), "{\"v\":2,\"type\":\"%s\",\"firmware_build\":\"adv-diagnostic-2\",\"run_id\":\"%s\",\"overall\":\"%s\",\"check_names\":[", safeType, responseId, runOverall);
  if (n < 0 || static_cast<size_t>(n) >= sizeof(json)) return;
  used = static_cast<size_t>(n);
  for (size_t i = 0; i < 12; ++i) {
    n = snprintf(json + used, sizeof(json) - used, "%s\"%s\"", i ? "," : "", kCheckNames[i]);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
    used += static_cast<size_t>(n);
  }
  n = snprintf(json + used, sizeof(json) - used, "],\"checks\":[");
  if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
  used += static_cast<size_t>(n);
  for (size_t i = 0; i < 12; ++i) {
    n = snprintf(json + used, sizeof(json) - used, "%s\"%s\"", i ? "," : "", runChecks[i]);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
    used += static_cast<size_t>(n);
  }
  n = snprintf(json + used, sizeof(json) - used, "],\"reasons\":[");
  if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
  used += static_cast<size_t>(n);
  for (size_t i = 0; i < 12; ++i) {
    n = snprintf(json + used, sizeof(json) - used, "%s\"%s\"", i ? "," : "", runReasons[i]);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
    used += static_cast<size_t>(n);
  }
  n = snprintf(json + used, sizeof(json) - used, ",\"metrics\":{\"free_heap_bytes\":%lu,\"ram_bytes_verified\":%u,\"imu_samples\":%u},\"reason\":\"%s\"}\r\n",
      static_cast<unsigned long>(runHeapBytes), static_cast<unsigned>(runRamBytesVerified),
      static_cast<unsigned>(runImuSamples), errorReason);
  if (n < 0 || static_cast<size_t>(n) >= sizeof(json) - used) return;
  used += static_cast<size_t>(n);
  if (used > kRunFrameMaxBytes || Serial.write(reinterpret_cast<const uint8_t *>(json), used) != used) {
    Serial.end();  // A partial protocol frame must not be followed by another response.
  }
}

static bool validRunId(const char *value, size_t length) {
  if (length < 1 || length > 12) return false;
  for (size_t i = 0; i < length; ++i) {
    if (!((value[i] >= 'A' && value[i] <= 'Z') ||
          (value[i] >= '0' && value[i] <= '9'))) return false;
  }
  return true;
}

static uint8_t patternByte(size_t offset) {
  return static_cast<uint8_t>((offset * 37u + 0x5Au) & 0xFFu);
}

static void markSdTestStarted() {
  sdDone = true;
  sdState = SdState::Running;
  sdStage = SdStage::Mount;
  sdReason = "none";
  sdCleanup = SdCleanup::NotAttempted;
  sdBytesVerified = 0;
  snprintf(sdStatus, sizeof(sdStatus), "SD: checking card...");
}

static void runSdSelfTest() {
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
  commandBuffer[commandLength < kCommandMaxBytes ? commandLength : kCommandMaxBytes - 1] = '\0';
  if (commandOverflow || commandLength == 0) {
    emitJson("error", "invalid_command");
  } else if (commandLength == 6 && memcmp(commandBuffer, "status", 6) == 0) {
    emitJson("status", sdReason);
  } else if (commandLength == 7 && memcmp(commandBuffer, "sd_test", 7) == 0) {
    if (!ready && !sdDone) {
      emitJson("error", "not_ready");
    } else if (!sdDone) {
      markSdTestStarted();
      emitJson("sd_test", "none");
      runSdSelfTest();
      emitJson("sd_test_result", sdReason);
    } else {
      emitJson("sd_test_result", sdReason);
    }
  } else if (commandLength > 4 && memcmp(commandBuffer, "run ", 4) == 0) {
    const size_t idLength = commandLength - 4;
    if (!validRunId(commandBuffer + 4, idLength)) {
      emitRunJson("error", "invalid_id", "");
    } else if (runRecordValid && strncmp(lastRunId, commandBuffer + 4, idLength) == 0 && strlen(lastRunId) == idLength) {
      emitRunJson("result", "none", commandBuffer + 4);
    } else if (runRecordValid) {
      emitRunJson("error", "run_id_busy", commandBuffer + 4);
    } else if (!ready) {
      emitRunJson("error", "not_ready", commandBuffer + 4);
    } else {
      strlcpy(lastRunId, commandBuffer + 4, sizeof(lastRunId));
      for (size_t i = 0; i < 12; ++i) { strlcpy(runChecks[i], "NOT_TESTED", sizeof(runChecks[i])); strlcpy(runReasons[i], "unavailable", sizeof(runReasons[i])); }
      strlcpy(runOverall, "INCONCLUSIVE", sizeof(runOverall));
      emitRunJson("run_ack", "none", lastRunId);
      executeRun(commandBuffer + 4);
      emitRunJson("run_result", "none", lastRunId);
    }
  } else if (commandLength > 7 && memcmp(commandBuffer, "result ", 7) == 0) {
    const size_t idLength = commandLength - 7;
    if (!validRunId(commandBuffer + 7, idLength)) {
      emitRunJson("error", "invalid_id", "");
    } else if (!runRecordValid || strncmp(lastRunId, commandBuffer + 7, idLength) != 0 || strlen(lastRunId) != idLength) {
      emitRunJson("error", "run_not_found", commandBuffer + 7);
    } else {
      emitRunJson("result", "none", lastRunId);
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
      if ((value < 0x20 && value != '\r') || value > 0x7E || commandLength == kCommandMaxBytes) {
        commandOverflow = true;
      } else {
        commandBuffer[commandLength++] = static_cast<char>(value);
      }
    }
  }
}

static void executeRun(const char *runId) {
  strlcpy(lastRunId, runId, sizeof(lastRunId));
  runRecordValid = true;
  runHeapBytes = ESP.getFreeHeap();
  runRamBytesVerified = 0;
  runImuSamples = 0;
  for (size_t i = 0; i < 12; ++i) {
    strlcpy(runChecks[i], "NOT_TESTED", sizeof(runChecks[i]));
    strlcpy(runReasons[i], "unavailable", sizeof(runReasons[i]));
  }
  if (boardReady) { strlcpy(runChecks[0], "PASS", sizeof(runChecks[0])); strlcpy(runReasons[0], "none", sizeof(runReasons[0])); }
  else { strlcpy(runChecks[0], "FAIL", sizeof(runChecks[0])); strlcpy(runReasons[0], "unsupported_board", sizeof(runReasons[0])); }

  uint8_t scratch[256];
  for (size_t i = 0; i < sizeof(scratch); ++i) scratch[i] = static_cast<uint8_t>((i * 73u + 0x5Au) & 0xFFu);
  bool ramOk = true;
  for (size_t i = 0; i < sizeof(scratch); ++i) {
    if (scratch[i] != static_cast<uint8_t>((i * 73u + 0x5Au) & 0xFFu)) { ramOk = false; break; }
    ++runRamBytesVerified;
  }
  strlcpy(runChecks[1], ramOk ? "PASS" : "FAIL", sizeof(runChecks[1]));
  strlcpy(runReasons[1], ramOk ? "none" : "pattern_mismatch", sizeof(runReasons[1]));

  if (!imuReady) {
    strlcpy(runChecks[2], "FAIL", sizeof(runChecks[2]));
    strlcpy(runReasons[2], "imu_unavailable", sizeof(runReasons[2]));
  } else {
    bool finite = true;
    for (uint8_t i = 0; i < 8; ++i) {
      M5.Imu.update();
      const auto sample = M5.Imu.getImuData();
      const float values[] = {sample.gyro.x, sample.gyro.y, sample.gyro.z,
                              sample.accel.x, sample.accel.y, sample.accel.z};
      for (float value : values) if (!isfinite(value)) finite = false;
      if (!finite) break;
      ++runImuSamples;
      delay(5);
    }
    strlcpy(runChecks[2], finite && runImuSamples == 8 ? "PASS" : "FAIL", sizeof(runChecks[2]));
    strlcpy(runReasons[2], finite && runImuSamples == 8 ? "none" : "nonfinite_sample", sizeof(runReasons[2]));
  }
  strlcpy(runReasons[3], "owner_observation_required", sizeof(runReasons[3]));
  strlcpy(runReasons[4], "owner_observation_required", sizeof(runReasons[4]));
  strlcpy(runReasons[5], "owner_observation_required", sizeof(runReasons[5]));
  strlcpy(runReasons[6], "owner_observation_required", sizeof(runReasons[6]));
  strlcpy(runReasons[7], "unavailable", sizeof(runReasons[7]));
  strlcpy(runReasons[8], "not_requested", sizeof(runReasons[8]));
  strlcpy(runReasons[9], "unavailable", sizeof(runReasons[9]));
  strlcpy(runReasons[10], "accessory_unknown", sizeof(runReasons[10]));
  strlcpy(runReasons[11], "not_requested", sizeof(runReasons[11]));

  bool failed = false;
  bool incomplete = false;
  for (size_t i = 0; i < 12; ++i) {
    if (strcmp(runChecks[i], "FAIL") == 0) failed = true;
    if (strcmp(runChecks[i], "NOT_TESTED") == 0 || strcmp(runChecks[i], "INCONCLUSIVE") == 0) incomplete = true;
  }
  strlcpy(runOverall, failed ? "FAIL" : incomplete ? "INCONCLUSIVE" : "PASS", sizeof(runOverall));
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
    if ((key == 's' || key == 'S') && !sdDone) {
      markSdTestStarted();
      runSdSelfTest();
    }
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
