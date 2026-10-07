# Cardputer-Adv diagnostic — Issue #2

Status: partial diagnostic, not a hardware certification. This report records sanitized
observations, source-backed interpretations, limitations, and safe follow-up tests.

## Measured host and Launcher observations

- Host inventory at 2026-10-07 05:55 UTC found the Espressif USB JTAG/serial unit and
  `USB Serial Device (COM5)` present with status OK. No removable volume or USB disk
  was exposed. USB enumeration does not by itself identify running firmware or prove
  SD presence/health.
- One passive RX on COM5 (115200 baud, 8 seconds, DTR/RTS disabled, no TX) received
  zero bytes. Silence alone does not identify boot state or imply a firmware fault.
- A subsequent bounded probe (12-second cap, 1094 bytes) sent only `help`, `version`,
  `whoami`, `partitions`, then `help`; the serial handle closed in `finally`.
- Responses identified Launcher 2.9.1 and compiled name “M5Stack Cardputer & ADV”.
  The partition table reported 8 MiB flash; `app0` at 0x010000/0x150000;
  `wifibl` at 0x170000/0x150000 and marked boot-selected; NVS, OTA metadata and
  coredump partitions; 5376 KiB free. Partition metadata is not application identity
  or health, and NVS/coredump contents were not read.
- Initial `help` returned “unknown command”; final `help` returned the command list.
  This is retained as an observed response, not diagnosed as a firmware defect.
- No reset, settings/credential query, Wi-Fi operation, flash dump/write/erase,
  partition mutation, or SD write/format was performed. Probe output was not retained
  as raw evidence.

## Source verification and safe command boundary

The Launcher tag [2.9.1](https://github.com/bmorcelli/Launcher/tree/2.9.1) was
reviewed, especially `src/serial_console.cpp`. `version` prints the Launcher version
macro; `whoami` prints the compiled device name; `help` prints command descriptions.
`partitions` reads the current partition table and reads two OTA metadata entries to
identify the selected boot partition. These handlers do not write or erase flash.

The probe allowlist is limited to `help`, `version`, `whoami`, and `partitions`. Do
not use `settings get` (may expose private configuration), Wi-Fi commands, `reboot`,
`nav` (software-injected input only), partition mutation, or firmware commands as a
hardware test. Do not run esptool merely to recover a silent console: its configured
post-command behavior can leave the chip in ROM download mode and may interrupt the
application.

## Hardware, storage, and software test matrix

| Area | Status and evidence | Safe next test / limitation |
|---|---|---|
| USB/JTAG serial | Measured: COM5 enumerated; Launcher information probe responded. | Repeat host inventory only if needed; do not infer board identity solely from VID/PID. |
| Firmware/Launcher | Measured: Launcher 2.9.1, compiled Cardputer & ADV name. | Capture bounded boot text on a future authorized session; no app-version command was verified. |
| Flash/partitions | Measured metadata only; `wifibl` marked boot-selected. | No content reads; metadata does not certify app integrity or health. |
| Keyboard controller | Not physically tested. Launcher source initializes TCA8418 at I2C 0x34 on SDA 8/SCL 9. | Future boot log may show init/ACK; owner must press keys to verify physical response. `nav` is not a physical test. |
| Display | Not physically inspected. | Owner visually confirms boot/menu/pixels; serial output is not proof of rendering. |
| SD card | Unknown; host showed no removable volume or USB disk. | Owner confirms card presence. Launcher USB MSC uses a raw SD write callback; never expose it to a host as a read-only diagnostic. Any later SD test must be source-reviewed and demonstrably read-only. |
| IMU | Not tested. | Owner-authorized build/test may initialize the board's BMI270 driver and sample movement; no Launcher serial query is documented. |
| Microphone / speaker / buzzer | Not tested. | Require a bounded test with owner-observed audio/input; no serial command is documented. |
| IR | Not tested. | Requires source-reviewed send/receive test and a known external target; no Launcher serial command documented. |
| Battery / charging | Not tested. | Requires suitable measurement equipment and physical observation; software metadata is insufficient. |
| Expansion connectors | Not tested. | Requires a known compatible peripheral and owner observation; do not probe pins blindly. |

## Firmware-port research boundary

The official [MicroPython repository](https://github.com/micropython/micropython),
including its [ESP32 board definitions](https://github.com/micropython/micropython/tree/master/ports/esp32/boards),
was checked for Cardputer-specific support. At the recorded review, the inspected board listing
contained `ESP32_GENERIC_S3` but no Cardputer/Cardputer-Adv board definition; guessed
Cardputer-specific paths returned not found. This is a bounded check of that listing,
not proof that no third-party port exists. Generic ESP32-S3 support is not proof of
Cardputer-Adv board support, correct peripheral pins/drivers, or installed firmware.
No MicroPython image was downloaded or installed.

## Safe follow-up and residuals

Keep future device checks bounded, read-only, and separate from public evidence. Stop if
USB behavior is unstable or command effects are unclear. Physical module checks need
owner observation; do not report untested modules as passing. The prior diagnostic
notes describe an earlier disconnect after an authorized reboot; that event is not
reproduced here and does not establish current USB state or cause.

Relevant sources: [Launcher 2.9.1](https://github.com/bmorcelli/Launcher/tree/2.9.1),
[M5Cardputer examples](https://github.com/m5stack/M5Cardputer/tree/master/examples/Basic),
[M5Unified IMU example](https://github.com/m5stack/M5Unified/tree/master/examples/Basic/Imu),
and [M5Unified IMU implementation](https://github.com/m5stack/M5Unified/tree/master/src/utility/imu).
