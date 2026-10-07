# Cardputer-Adv hardware check (compile-only)

Minimal local test sketch for an owner-approved diagnostic session. It uses the official M5Stack M5Cardputer, M5Unified, M5GFX, and Arduino SD libraries. It shows display color bars, reports key activity, samples BMI270 IMU values, and offers a manually triggered bounded SD self-test. This sketch has been compiled only; it has **not** been flashed or run on hardware. It does not test audio, IR, battery, or peripherals.

## Pinned build environment

- Arduino CLI 1.3.1, downloaded from the official Arduino download endpoint.
- Espressif Arduino-ESP32 core 3.2.1 (`esp32:esp32`). Its indexed ESP-IDF base is 5.4.2.
- Official board FQBN: `esp32:esp32:m5stack_cardputer` (generic Cardputer board definition; runtime guard requires Cardputer-Adv).
- M5Cardputer 1.1.1, source tag commit [`f1392858b9994c3547120e602a57d3553d16ab01`](https://github.com/m5stack/M5Cardputer/tree/f1392858b9994c3547120e602a57d3553d16ab01).
- M5Unified 0.2.25, source tag commit [`fd40d58b8405ad1e7ed7afab548dab5e7cec5bbb`](https://github.com/m5stack/M5Unified/tree/fd40d58b8405ad1e7ed7afab548dab5e7cec5bbb).
- M5GFX 0.2.32, source tag commit [`c5a3fefad0b38a52cc750e2c4761e339a69a7208`](https://github.com/m5stack/M5GFX/tree/c5a3fefad0b38a52cc750e2c4761e339a69a7208).

M5Cardputer depends on M5Unified, M5GFX, IRremote, and LibSSH-ESP32; Arduino Library Manager resolved IRremote 4.7.1 and LibSSH-ESP32 5.9.0. M5Unified requires M5GFX >=0.2.31. Install the exact versions above in an isolated Arduino CLI user/data directory; do not install libraries globally.

## Compile only

```text
arduino-cli compile --fqbn esp32:esp32:m5stack_cardputer:FlashSize=8M,PartitionScheme=default_8MB scripts/hardware_check
```

Use the same pinned CLI/core/library versions. This command compiles only. Do not append `upload`, `burn-bootloader`, erase, or any flash command without the separate owner approval and verified recovery/partition plan required by Issue #2. Do not use the merged image as a recovery image; the default Arduino partition table is not the installed Launcher partition layout.

## Bounded serial JSON protocol (candidate)

After USB CDC is available, send exactly one newline-terminated ASCII command per line: `status` or `sd_test`. The parser accepts at most 64 printable command bytes; an overlong, empty, non-ASCII/control, or unknown line is discarded through its newline and returns a bounded `{"v":1,"type":"error","reason":"invalid_command"}` response. The device does not wait for a host at boot. Each accepted line returns one JSON object (CRLF terminated) with fixed fields: `v` (1), `type` (`status`, `sd_test`, or `error`), `firmware_build` (`adv-diagnostic-1`), `board_ready`, `imu_ready`, and `sd` (`state`, `stage`, `reason`, `bytes_verified`, `cleanup`). SD state is `not_run|running|pass|fail`; stage is `idle|mount|write|read|cleanup|complete|error`; cleanup is `not_attempted|removed|failed|retained`; reasons are fixed enum-like strings in source. `status` reads cached state only and never mounts or accesses SD. `sd_test` runs only when ready and not already attempted; the physical `S` key uses the same one-shot guard. Repeated requests return retained outcome without retry. Output contains no raw input, keys, paths, serial/MAC, card identity, or free-form device errors. USB serial access is still device interaction and requires separate authorization. This protocol implementation remains compile-only until independently reviewed and explicitly approved for device use.

## Runtime effects and limitations

`M5.begin(cfg)` probes and initializes the display before the runtime board identity check; `clear_display=true` visibly clears the display. It disables external output power, microphone, speaker, RTC, external IMU, and automatic internal IMU. After checking `M5.getBoard() == board_M5CardputerADV`, the sketch initializes the TCA8418 keyboard and BMI270 internal IMU. These initialize/configure peripherals in volatile device/sensor state. SD is untouched at boot; pressing `S` once after the ADV identity check calls `SD.begin` with the M5Unified Cardputer-ADV SPI pin map, 4 MHz, and `format_if_empty=false`. It reports card type/capacity, refuses if the reserved `/ADV_DIAGNOSTIC_SD_TEST.BIN` path already exists, writes at most 64 KiB in 512-byte chunks with a 15-second write deadline, reads and verifies a deterministic pattern with a 15-second deadline, then attempts to delete only that exact file it created. The last SD result remains visible on the display after the sample area refreshes. A failed/incomplete write or read leaves that uniquely named test file in place for inspection; cleanup failure is reported. It does not list/read existing files, overwrite an existing path, format/repair, use USB mass storage, or access other files. SD initialization/mount still performs card and filesystem I/O and is not a guarantee of zero incidental metadata writes; a filesystem-level read-only mount is not provided here. Do not run on another board; require separate runtime authorization and owner confirmation that writing a temporary test file is acceptable. Keyboard initialization has no success return; actual key response requires owner observation. BMI270 initialization failure is shown and stops sensor/key loop. Compiled success is not hardware validation.
