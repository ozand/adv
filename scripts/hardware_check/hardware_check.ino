#include <M5Cardputer.h>
#include <SD.h>
#include <atomic>
#include <math.h>

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
static constexpr size_t kMicSamples = 256;
static constexpr uint32_t kMicSampleRate = 16000, kMicWarmupMs = 1000, kMicWaitMs = 1000;
static constexpr size_t kToneSamples = 1600;
static constexpr uint32_t kToneSampleRate = 16000, kToneWaitMs = 500;
static constexpr size_t kAudioFrameMaxBytes = 256;
static int16_t micSamples[kMicSamples], toneSamples[kToneSamples];
static std::atomic<bool> micCaptureComplete{false};
static bool micResultReady = false, toneResultReady = false, audioLifecycleUncertain = false;
static char micResultId[13] = "", toneResultId[13] = "";
static uint32_t micRms = 0;
static uint16_t micPeak = 0;
static const char *micResultReason = "run_not_found", *micCleanupState = "not_attempted";
static const char *toneResultReason = "run_not_found", *toneCleanupState = "not_attempted";
enum class AudioUiStage { Idle, Starting, Warmup, Capture, Cleanup, Playback, Complete, Unavailable, Unknown };
static AudioUiStage audioUiStage = AudioUiStage::Idle;
static char audioUiResult[48] = "Audio: idle";
static char micUiId[13] = "", toneUiId[13] = "";
static bool micKeyLatched = false, toneKeyLatched = false, sdKeyLatched = false, yKeyLatched = false;
static bool micUiPending = false, toneUiPending = false;
static constexpr uint32_t kToneConsentMs = 5000;
static uint32_t toneConsentStarted = 0;
static bool toneConsentPending = false, toneConsentReady = false;
static bool audioUiBlockKeysUntilRelease = false;
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

static void executeMicTest();
static void executeToneTest();
static void emitAudioJson(const char *, const char *, const char *, bool, const char *, const char *);
static const char kAudioFirmwareBuild[] = "adv-diagnostic-3-audio-proposal";
static void micReleaseCallback(void *, void *data, size_t length) {
  if (data == micSamples && length == kMicSamples) micCaptureComplete.store(true, std::memory_order_release);
}
static const char *audioUiStageName() {
  switch (audioUiStage) {
    case AudioUiStage::Idle: return "IDLE";
    case AudioUiStage::Starting: return "STARTING";
    case AudioUiStage::Warmup: return "WARMUP";
    case AudioUiStage::Capture: return "CAPTURE";
    case AudioUiStage::Cleanup: return "CLEANUP";
    case AudioUiStage::Playback: return "PLAYBACK";
    case AudioUiStage::Complete: return "DONE";
    case AudioUiStage::Unavailable: return "UNAVAILABLE";
    case AudioUiStage::Unknown: return "UNKNOWN";
  }
  return "UNKNOWN";
}
static void showAudioUiStage() {
  M5.Display.setCursor(0, 108);
  M5.Display.printf("A:%-8s %.27s", audioUiStageName(), audioUiResult);
  M5.Display.display();
}
static const char *const kAudioReasons[] = {"none", "invalid_command", "not_ready", "audio_busy", "run_id_busy", "run_not_found", "unsupported_board", "begin_failed", "record_failed", "capture_timeout", "cleanup_unknown", "zero_signal", "play_failed", "playback_timeout", "owner_observation_required"};
static bool audioReasonAllowed(const char *reason) {
  for (const char *allowed : kAudioReasons) if (strcmp(reason, allowed) == 0) return true;
  return false;
}
static bool audioResultPairValid(const char *operation, const char *reason, const char *cleanup) {
  if (strcmp(operation, "mic_test") == 0) {
    if (strcmp(cleanup, "not_attempted") == 0) return strcmp(reason, "not_ready") == 0 || strcmp(reason, "unsupported_board") == 0 || strcmp(reason, "audio_busy") == 0 || strcmp(reason, "run_id_busy") == 0 || strcmp(reason, "run_not_found") == 0 || strcmp(reason, "invalid_command") == 0;
    if (strcmp(reason, "cleanup_unknown") == 0) return strcmp(cleanup, "unknown") == 0;
    if (strcmp(cleanup, "quiescent") != 0) return false;
    if (strcmp(reason, "owner_observation_required") == 0) return micRms <= micPeak && micPeak <= 32768;
    if (strcmp(reason, "zero_signal") == 0) return micRms == 0 && micPeak == 0;
    return (strcmp(reason, "begin_failed") == 0 || strcmp(reason, "record_failed") == 0 || strcmp(reason, "capture_timeout") == 0) && micRms == 0 && micPeak == 0;
  }
  if (strcmp(cleanup, "not_attempted") == 0) return strcmp(reason, "not_ready") == 0 || strcmp(reason, "audio_busy") == 0 || strcmp(reason, "run_id_busy") == 0 || strcmp(reason, "run_not_found") == 0 || strcmp(reason, "invalid_command") == 0;
  if (strcmp(reason, "cleanup_unknown") == 0) return strcmp(cleanup, "unknown") == 0;
  return strcmp(cleanup, "software_stopped_codec_unknown") == 0 && (strcmp(reason, "owner_observation_required") == 0 || strcmp(reason, "play_failed") == 0 || strcmp(reason, "playback_timeout") == 0);
}
static bool validRunId(const char *value, size_t length);
static void emitAudioJson(const char *type, const char *operation, const char *operationId, bool mic,
                          const char *overrideReason, const char *overrideCleanup) {
  char frame[kAudioFrameMaxBytes];
  const char *reason = overrideReason ? overrideReason : mic ? micResultReason : toneResultReason;
  const char *cleanup = overrideCleanup ? overrideCleanup : mic ? micCleanupState : toneCleanupState;
  const char *id = operationId && validRunId(operationId, strlen(operationId)) ? operationId : "";
  if (!audioReasonAllowed(reason) || !audioResultPairValid(operation, reason, cleanup)) { reason = "cleanup_unknown"; cleanup = "unknown"; }
  const uint32_t responseRms = mic && !overrideReason ? micRms : 0;
  const uint16_t responsePeak = mic && !overrideReason ? micPeak : 0;
  int n;
  if (strcmp(type, "error") == 0)
    n = snprintf(frame, sizeof(frame), "{\"v\":1,\"type\":\"error\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation\":\"%s\",\"operation_id\":\"%s\",\"state\":\"INCONCLUSIVE\",\"reason\":\"%s\",\"cleanup\":\"%s\"}\r\n", operation, id, reason, cleanup);
  else if (mic)
    n = snprintf(frame, sizeof(frame), "{\"v\":1,\"type\":\"mic_test\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation_id\":\"%s\",\"state\":\"INCONCLUSIVE\",\"reason\":\"%s\",\"cleanup\":\"%s\",\"mic_rms\":%lu,\"mic_peak\":%u}\r\n", id, reason, cleanup, static_cast<unsigned long>(responseRms), static_cast<unsigned>(responsePeak));
  else
    n = snprintf(frame, sizeof(frame), "{\"v\":1,\"type\":\"tone_test\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation_id\":\"%s\",\"state\":\"INCONCLUSIVE\",\"reason\":\"%s\",\"cleanup\":\"%s\"}\r\n", id, reason, cleanup);
  if (n > 0 && static_cast<size_t>(n) < sizeof(frame) &&
      Serial.write(reinterpret_cast<const uint8_t *>(frame), static_cast<size_t>(n)) != static_cast<size_t>(n)) {
    Serial.end();  // Never append another frame after a partial audio response.
  }
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
      "{\"v\":1,\"type\":\"%s\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"board_ready\":%s,\"imu_ready\":%s,\"sd\":{\"state\":\"%s\",\"stage\":\"%s\",\"reason\":\"%s\",\"bytes_verified\":%u,\"cleanup\":\"%s\"}}\r\n",
      safeType, boardReady ? "true" : "false", imuReady ? "true" : "false",
      stateName(), stageName(), safeReason, static_cast<unsigned>(sdBytesVerified), cleanupName());
  if (length > 0 && static_cast<size_t>(length) < sizeof(json)) {
    Serial.write(reinterpret_cast<const uint8_t *>(json), static_cast<size_t>(length));
  }
}

static constexpr size_t kRunFrameMaxBytes = 1024;
static bool validRunId(const char *value, size_t length);
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
  int n = snprintf(json, sizeof(json), "{\"v\":2,\"type\":\"%s\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"run_id\":\"%s\",\"overall\":\"%s\",\"check_names\":[", safeType, responseId, runOverall);
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
  n = snprintf(json + used, sizeof(json) - used, "],\"metrics\":{\"free_heap_bytes\":%lu,\"ram_bytes_verified\":%u,\"imu_samples\":%u},\"reason\":\"%s\"}\r\n",
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
  cfg.internal_mic = true;
  cfg.internal_spk = true;
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
  M5.Display.println("S:SD M:MIC T:TONE");
  M5.Display.println("T then Y after earphones out");
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
  } else if (commandLength > 9 && memcmp(commandBuffer, "mic_test ", 9) == 0) {
    const size_t idLength = commandLength - 9; const char *id = commandBuffer + 9;
    if (!validRunId(id, idLength)) emitAudioJson("error", "mic_test", "", true, "invalid_command", "not_attempted");
    else if (micResultReady) {
      if (strcmp(micResultId, id) == 0) emitAudioJson("mic_test", "mic_test", id, true, nullptr, nullptr);
      else emitAudioJson("error", "mic_test", id, true, "run_id_busy", "not_attempted");
    } else if (audioLifecycleUncertain || M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) emitAudioJson("error", "mic_test", id, true, "audio_busy", "not_attempted");
    else if (!ready || !M5.Mic.isEnabled()) emitAudioJson("error", "mic_test", id, true, "not_ready", "not_attempted");
    else { strlcpy(micResultId, id, sizeof(micResultId)); micResultReady = true; executeMicTest(); if (micResultReady) emitAudioJson("mic_test", "mic_test", id, true, nullptr, nullptr); else { strlcpy(micResultId, "", sizeof(micResultId)); emitAudioJson("error", "mic_test", id, true, micResultReason, micCleanupState); } }
  } else if (commandLength > 10 && memcmp(commandBuffer, "tone_test ", 10) == 0) {
    const size_t idLength = commandLength - 10; const char *id = commandBuffer + 10;
    if (!validRunId(id, idLength)) emitAudioJson("error", "tone_test", "", false, "invalid_command", "not_attempted");
    else if (toneResultReady) {
      if (strcmp(toneResultId, id) == 0) emitAudioJson("tone_test", "tone_test", id, false, nullptr, nullptr);
      else emitAudioJson("error", "tone_test", id, false, "run_id_busy", "not_attempted");
    } else if (audioLifecycleUncertain || M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) emitAudioJson("error", "tone_test", id, false, "audio_busy", "not_attempted");
    else if (!ready || !M5.Speaker.isEnabled()) emitAudioJson("error", "tone_test", id, false, "not_ready", "not_attempted");
    else { strlcpy(toneResultId, id, sizeof(toneResultId)); toneResultReady = true; executeToneTest(); if (toneResultReady) emitAudioJson("tone_test", "tone_test", id, false, nullptr, nullptr); else { strlcpy(toneResultId, "", sizeof(toneResultId)); emitAudioJson("error", "tone_test", id, false, toneResultReason, toneCleanupState); } }
  } else if (commandLength > 11 && memcmp(commandBuffer, "mic_result ", 11) == 0) {
    const size_t idLength = commandLength - 11; const char *id = commandBuffer + 11;
    if (!validRunId(id, idLength)) emitAudioJson("error", "mic_test", "", true, "invalid_command", "not_attempted");
    else if (!micResultReady || strcmp(micResultId, id) != 0) emitAudioJson("error", "mic_test", id, true, "run_not_found", "not_attempted");
    else emitAudioJson("mic_test", "mic_test", id, true, nullptr, nullptr);
  } else if (commandLength > 12 && memcmp(commandBuffer, "tone_result ", 12) == 0) {
    const size_t idLength = commandLength - 12; const char *id = commandBuffer + 12;
    if (!validRunId(id, idLength)) emitAudioJson("error", "tone_test", "", false, "invalid_command", "not_attempted");
    else if (!toneResultReady || strcmp(toneResultId, id) != 0) emitAudioJson("error", "tone_test", id, false, "run_not_found", "not_attempted");
    else emitAudioJson("tone_test", "tone_test", id, false, nullptr, nullptr);
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

static void executeMicTest() {
  micResultReason = "begin_failed"; micCleanupState = "unknown"; micRms = 0; micPeak = 0;
  audioUiStage = AudioUiStage::Starting; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: starting"); showAudioUiStage();
  if (M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) { micResultReason = "audio_busy"; micCleanupState = "not_attempted"; micResultReady = false; audioUiStage = AudioUiStage::Unknown; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: audio busy/unknown"); audioUiBlockKeysUntilRelease = true; return; }
  const uint8_t priorVolume = M5.Speaker.getVolume(); M5.Speaker.setVolume(0);
  M5.Mic.setBufferReleaseCallback(nullptr, micReleaseCallback);
  bool recordQueued = false;
  if (M5.Mic.begin()) {
    audioUiStage = AudioUiStage::Warmup; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: warmup"); showAudioUiStage();
    delay(kMicWarmupMs); audioUiStage = AudioUiStage::Capture; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: capture"); showAudioUiStage();
    micCaptureComplete.store(false, std::memory_order_release);
    if (M5.Mic.record(micSamples, kMicSamples, kMicSampleRate, false)) {
      recordQueued = true;
      const uint32_t started = millis();
      while (!micCaptureComplete.load(std::memory_order_acquire) && static_cast<uint32_t>(millis() - started) < kMicWaitMs) delay(1);
      if (!micCaptureComplete.load(std::memory_order_acquire)) micResultReason = "capture_timeout";
      else {
        uint64_t squares = 0;
        for (size_t i = 0; i < kMicSamples; ++i) {
          const int32_t sample = micSamples[i]; const uint32_t magnitude = static_cast<uint32_t>(sample < 0 ? -sample : sample);
          if (magnitude > micPeak) micPeak = static_cast<uint16_t>(magnitude);
          squares += static_cast<uint64_t>(static_cast<int64_t>(sample) * sample);
        }
        micRms = static_cast<uint32_t>(sqrt(static_cast<double>(squares) / kMicSamples));
        micResultReason = micPeak == 0 ? "zero_signal" : "owner_observation_required";
      }
    } else micResultReason = "record_failed";
  }
  audioUiStage = AudioUiStage::Cleanup; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: cleanup"); showAudioUiStage();
  M5.Mic.end();
  if (!M5.Mic.isRunning() && M5.Mic.isRecording() == 0) {
    if (micCaptureComplete.load(std::memory_order_acquire)) { memset(micSamples, 0, sizeof(micSamples)); M5.Mic.setBufferReleaseCallback(nullptr, nullptr); micCleanupState = "quiescent"; }
    else {
      memset(micSamples, 0, sizeof(micSamples)); M5.Mic.setBufferReleaseCallback(nullptr, nullptr); micCleanupState = "quiescent";
      if (recordQueued) micResultReason = "capture_timeout";
      micRms = micPeak = 0;
    }
  } else { audioLifecycleUncertain = true; micResultReason = "cleanup_unknown"; micCleanupState = "unknown"; }
  M5.Speaker.setVolume(priorVolume);
  audioUiStage = micCleanupState && strcmp(micCleanupState, "unknown") == 0 ? AudioUiStage::Unknown : AudioUiStage::Complete;
  const char *shortReason = strcmp(micResultReason, "owner_observation_required") == 0 ? "observe" :
                            strcmp(micResultReason, "zero_signal") == 0 ? "zero" :
                            strcmp(micResultReason, "capture_timeout") == 0 ? "timeout" :
                            strcmp(micResultReason, "begin_failed") == 0 ? "begin_fail" :
                            strcmp(micResultReason, "record_failed") == 0 ? "record_fail" : micResultReason;
  snprintf(audioUiResult, sizeof(audioUiResult), "MIC INC %s R%lu P%u", shortReason, static_cast<unsigned long>(micRms), static_cast<unsigned>(micPeak));
  audioUiBlockKeysUntilRelease = true;
}

static void executeToneTest() {
  toneResultReason = "play_failed"; toneCleanupState = "unknown";
  audioUiStage = AudioUiStage::Starting; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: checking"); showAudioUiStage();
  if (audioLifecycleUncertain || M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) { toneResultReason = "audio_busy"; toneCleanupState = "not_attempted"; toneResultReady = false; audioUiStage = AudioUiStage::Unknown; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: audio busy/unknown"); audioUiBlockKeysUntilRelease = true; return; }
  const uint8_t priorVolume = M5.Speaker.getVolume();
  for (size_t i = 0; i < kToneSamples; ++i) toneSamples[i] = (i < 32 || i >= kToneSamples - 32) ? 0 : static_cast<int16_t>(1600.0 * sin(2.0 * PI * 440.0 * i / kToneSampleRate));
  M5.Speaker.setVolume(8);
  audioUiStage = AudioUiStage::Playback; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: request <=100ms"); showAudioUiStage();
  const bool queued = M5.Speaker.playRaw(toneSamples, kToneSamples, kToneSampleRate, false, 1, 0, true);
  if (queued) { const uint32_t started = millis(); while (M5.Speaker.isPlaying(0) && static_cast<uint32_t>(millis() - started) < kToneWaitMs) delay(1); toneResultReason = M5.Speaker.isPlaying(0) ? "playback_timeout" : "owner_observation_required"; }
  audioUiStage = AudioUiStage::Cleanup; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: cleanup"); showAudioUiStage();
  M5.Speaker.end();
  if (!M5.Speaker.isRunning() && !M5.Speaker.isPlaying()) { memset(toneSamples, 0, sizeof(toneSamples)); toneCleanupState = "software_stopped_codec_unknown"; }
  else { audioLifecycleUncertain = true; toneResultReason = "cleanup_unknown"; toneCleanupState = "unknown"; }
  M5.Speaker.setVolume(priorVolume);
  audioUiStage = toneCleanupState && strcmp(toneCleanupState, "unknown") == 0 ? AudioUiStage::Unknown : AudioUiStage::Complete;
  const char *shortReason = strcmp(toneResultReason, "owner_observation_required") == 0 ? "observe" :
                            strcmp(toneResultReason, "playback_timeout") == 0 ? "timeout" :
                            strcmp(toneResultReason, "play_failed") == 0 ? "play_fail" : toneResultReason;
  snprintf(audioUiResult, sizeof(audioUiResult), "TONE INC %s", shortReason);
  audioUiBlockKeysUntilRelease = true;
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
  const bool sPressed = M5Cardputer.Keyboard.isKeyPressed('s') || M5Cardputer.Keyboard.isKeyPressed('S');
  const bool mPressed = M5Cardputer.Keyboard.isKeyPressed('m') || M5Cardputer.Keyboard.isKeyPressed('M');
  const bool tPressed = M5Cardputer.Keyboard.isKeyPressed('t') || M5Cardputer.Keyboard.isKeyPressed('T');
  const bool yPressed = M5Cardputer.Keyboard.isKeyPressed('y') || M5Cardputer.Keyboard.isKeyPressed('Y');
  if (audioUiBlockKeysUntilRelease) {
    sdKeyLatched = sPressed; micKeyLatched = mPressed; toneKeyLatched = tPressed; yKeyLatched = yPressed;
    toneConsentPending = false; toneConsentReady = false; micUiPending = false; toneUiPending = false;
    if (!sPressed && !mPressed && !tPressed && !yPressed) audioUiBlockKeysUntilRelease = false;
  }
  const bool wasAudioUiBlocked = audioUiBlockKeysUntilRelease;
  const bool sdEdge = sPressed && !sdKeyLatched;
  const bool micEdge = mPressed && !micKeyLatched;
  const bool toneEdge = tPressed && !toneKeyLatched;
  if (!audioUiBlockKeysUntilRelease) {
    sdKeyLatched = sPressed; micKeyLatched = mPressed; toneKeyLatched = tPressed;
    if (sdEdge) { if (!sdDone) { markSdTestStarted(); runSdSelfTest(); } }
    else if (micEdge) micUiPending = true;
    else if (toneEdge && !toneConsentPending) {
      toneConsentPending = true; toneConsentReady = false; toneConsentStarted = millis();
      audioUiStage = AudioUiStage::Starting; snprintf(audioUiResult, sizeof(audioUiResult), "EAR OUT THEN PRESS Y");
    }
  }
  if (toneConsentPending && static_cast<uint32_t>(millis() - toneConsentStarted) >= kToneConsentMs) {
    toneConsentPending = false; toneConsentReady = false; audioUiStage = AudioUiStage::Idle; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: cancelled");
  }
  if (toneConsentPending && !audioUiBlockKeysUntilRelease) {
    if (!yPressed) toneConsentReady = true;
    audioUiStage = AudioUiStage::Starting; snprintf(audioUiResult, sizeof(audioUiResult), "EAR OUT THEN PRESS Y");
  }
  const bool yEdge = yPressed && !yKeyLatched;
  yKeyLatched = yPressed;
  if (!wasAudioUiBlocked && yEdge && toneConsentPending && toneConsentReady) {
    toneConsentPending = false; toneConsentReady = false; toneUiPending = true;
  }
  if (micUiPending) {
    micUiPending = false;
    if (!ready || !M5.Mic.isEnabled()) { audioUiStage = AudioUiStage::Unavailable; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: not ready"); }
    else if (audioLifecycleUncertain || M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) { micUiId[0] = '\0'; audioUiStage = AudioUiStage::Unknown; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: audio busy/unknown"); }
    else if (!micResultReady) {
      strlcpy(micUiId, "UI1", sizeof(micUiId)); strlcpy(micResultId, micUiId, sizeof(micResultId)); micResultReady = true;
      audioUiStage = AudioUiStage::Starting; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: starting"); showAudioUiStage();
      executeMicTest();
    }
    else if (micResultReady && micUiId[0] != '\0' && strcmp(micUiId, micResultId) == 0) { audioUiStage = micCleanupState && strcmp(micCleanupState, "unknown") == 0 ? AudioUiStage::Unknown : AudioUiStage::Complete; const char *shortReason = strcmp(micResultReason, "owner_observation_required") == 0 ? "observe" : strcmp(micResultReason, "zero_signal") == 0 ? "zero" : micResultReason; snprintf(audioUiResult, sizeof(audioUiResult), "MIC INC %s R%lu P%u", shortReason, static_cast<unsigned long>(micRms), static_cast<unsigned>(micPeak)); }
    else { audioUiStage = AudioUiStage::Unavailable; snprintf(audioUiResult, sizeof(audioUiResult), "Mic: slot busy"); }
  }
  if (toneUiPending) {
    toneUiPending = false;
    if (!ready || !M5.Speaker.isEnabled()) { audioUiStage = AudioUiStage::Unavailable; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: not ready"); }
    else if (audioLifecycleUncertain || M5.Mic.isRunning() || M5.Mic.isRecording() != 0 || M5.Speaker.isRunning() || M5.Speaker.isPlaying()) { toneUiId[0] = '\0'; audioUiStage = AudioUiStage::Unknown; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: audio busy/unknown"); }
    else if (!toneResultReady) {
      strlcpy(toneUiId, "UI1", sizeof(toneUiId)); strlcpy(toneResultId, toneUiId, sizeof(toneResultId)); toneResultReady = true;
      audioUiStage = AudioUiStage::Playback; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: playing <=100ms"); showAudioUiStage();
      executeToneTest();
    }
    else if (toneResultReady && toneUiId[0] != '\0' && strcmp(toneUiId, toneResultId) == 0) { audioUiStage = toneCleanupState && strcmp(toneCleanupState, "unknown") == 0 ? AudioUiStage::Unknown : AudioUiStage::Complete; const char *shortReason = strcmp(toneResultReason, "owner_observation_required") == 0 ? "observe" : toneResultReason; snprintf(audioUiResult, sizeof(audioUiResult), "TONE INC %s", shortReason); }
    else { audioUiStage = AudioUiStage::Unavailable; snprintf(audioUiResult, sizeof(audioUiResult), "Tone: slot busy"); }
  }
  M5.Imu.update();
  const auto data = M5.Imu.getImuData();

  M5.Display.fillRect(0, 42, 240, 55, TFT_BLACK);
  M5.Display.setCursor(0, 42);
  M5.Display.printf("G: %.2f %.2f %.2f\n", data.gyro.x, data.gyro.y, data.gyro.z);
  M5.Display.printf("A: %.2f %.2f %.2f\n", data.accel.x, data.accel.y, data.accel.z);
  M5.Display.setCursor(0, 96);
  M5.Display.print(sdStatus);
  M5.Display.setCursor(0, 108);
  M5.Display.printf("A:%-8s %.21s", audioUiStageName(), audioUiResult);
  M5.Display.setCursor(0, 120);
  M5.Display.print("S:SD M:MIC T:TONE Y:EAR OUT");
  delay(100);
}
