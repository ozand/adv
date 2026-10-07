#include <M5Cardputer.h>
#include <SD.h>

static constexpr char kSdTestPath[] = "/ADV_DIAGNOSTIC_SD_TEST.BIN";
static constexpr size_t kSdTestBytes = 64 * 1024;
static constexpr size_t kSdChunkBytes = 512;
static bool ready = false;
static bool sdDone = false;

static uint8_t patternByte(size_t offset) {
  return static_cast<uint8_t>((offset * 37u + 0x5Au) & 0xFFu);
}

static void runSdSelfTest() {
  sdDone = true;
  M5.Display.println("SD: checking card...");

  const int cs = M5.getPin(m5::pin_name_t::sd_spi_cs);
  const int sck = M5.getPin(m5::pin_name_t::sd_spi_sclk);
  const int miso = M5.getPin(m5::pin_name_t::sd_spi_miso);
  const int mosi = M5.getPin(m5::pin_name_t::sd_spi_mosi);
  if (cs < 0 || sck < 0 || miso < 0 || mosi < 0) {
    M5.Display.println("SD: unsupported pin map");
    return;
  }

  SPI.begin(sck, miso, mosi, cs);
  if (!SD.begin(cs, SPI, 4000000, "/sdcard", 2, false)) {
    M5.Display.println("SD: mount failed; no format attempted");
    return;
  }

  M5.Display.printf("SD: type %d, capacity %llu MiB\n",
                    static_cast<int>(SD.cardType()),
                    static_cast<unsigned long long>(SD.cardSize() / (1024 * 1024)));
  if (SD.cardType() == CARD_NONE || SD.cardSize() < kSdTestBytes) {
    M5.Display.println("SD: invalid/too small; no test file created");
    SD.end();
    return;
  }

  if (SD.exists(kSdTestPath)) {
    M5.Display.println("SD: reserved test path exists; refusing overwrite");
    SD.end();
    return;
  }

  File testFile = SD.open(kSdTestPath, FILE_WRITE);
  if (!testFile) {
    M5.Display.println("SD: test file create failed");
    SD.end();
    return;
  }

  bool writeOk = true;
  uint8_t buffer[kSdChunkBytes];
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
    M5.Display.println("SD: write failed/timeout; test file retained");
    SD.end();
    return;
  }

  testFile = SD.open(kSdTestPath, FILE_READ);
  if (!testFile || testFile.size() != kSdTestBytes) {
    if (testFile) testFile.close();
    M5.Display.println("SD: read open/size failed; test file retained");
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
      match = false;
      break;
    }
    for (size_t i = 0; i < count; ++i) {
      if (buffer[i] != patternByte(checked + i)) {
        match = false;
        break;
      }
    }
    if (!match) break;
    checked += count;
  }
  testFile.close();
  match = match && checked == kSdTestBytes;

  const bool removed = match && SD.remove(kSdTestPath);
  M5.Display.printf("SD: verify %s; owned test file %s\n",
                    match ? "PASS" : "FAIL",
                    match ? (removed ? "removed" : "cleanup failed") : "retained for inspection");
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

  if (M5.getBoard() != m5::board_t::board_M5CardputerADV) {
    M5.Display.setTextSize(1);
    M5.Display.println("Unsupported board; stopping.");
    return;
  }

  M5Cardputer.Keyboard.begin();
  if (!M5.Imu.begin(&M5.In_I2C, M5.getBoard())) {
    M5.Display.println("BMI270 init failed.");
    return;
  }

  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.fillRect(0, 0, 40, 18, TFT_RED);
  M5.Display.fillRect(45, 0, 40, 18, TFT_GREEN);
  M5.Display.fillRect(90, 0, 40, 18, TFT_BLUE);
  M5.Display.setCursor(0, 24);
  M5.Display.println("ADV diagnostic / keys + IMU");
  M5.Display.println("Press S to run bounded SD test");
  ready = true;
}

void loop() {
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
  M5.Display.print("Keys: ");
  for (char key : M5Cardputer.Keyboard.keysState().word) {
    M5.Display.write(static_cast<uint8_t>(key));
  }
  M5.Display.println();
  delay(100);
}
