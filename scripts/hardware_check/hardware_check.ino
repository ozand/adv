#include <M5Cardputer.h>

static bool ready = false;

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
