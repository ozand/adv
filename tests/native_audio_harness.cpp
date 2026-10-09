// Bound to firmware source commit de59f24ac5032e968b6725d7f7ea212937a20f17.
// Exact validator/emitter/audio command branches extracted from committed .ino.
// Hardware-facing M5 calls and audio executors are stubbed. This extracted-code
// harness does not compile or execute the complete firmware sketch.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
struct SerialStub { std::string bytes; bool ended=false; size_t limit=static_cast<size_t>(-1); size_t write(const uint8_t*p,size_t n){size_t k=n<limit?n:limit;bytes.append(reinterpret_cast<const char*>(p),k);return k;} void end(){ended=true;} };
static SerialStub Serial;
static constexpr size_t kAudioFrameMaxBytes=256, kMicSamples=256;
static uint32_t micRms=0; static uint16_t micPeak=0;
static const char *micResultReason="run_not_found", *micCleanupState="not_attempted";
static const char *toneResultReason="run_not_found", *toneCleanupState="not_attempted";
static bool micResultReady=false, toneResultReady=false, audioLifecycleUncertain=false, ready=true;
static char micResultId[13]="", toneResultId[13]="";
static int micExecutions=0, toneExecutions=0;
static bool micRunning=false, speakerRunning=false;
struct DeviceStub { bool *running; bool isEnabled() const { return true; } bool isRunning() const { return *running; } int isRecording() const { return *running ? 1 : 0; } bool isPlaying() const { return *running; } };

struct M5Stub { DeviceStub Mic{&micRunning}, Speaker{&speakerRunning}; };
static M5Stub M5;
static void strlcpy(char*d,const char*s,size_t n){if(n){std::strncpy(d,s,n-1);d[n-1]=0;}}
static void emitJson(const char*,const char*){}
static void executeMicTest(){++micExecutions;micRunning=true;micResultReason="owner_observation_required";micCleanupState="quiescent";micRms=321;micPeak=654;micRunning=false;}
static void executeToneTest(){++toneExecutions;speakerRunning=true;toneResultReason="owner_observation_required";toneCleanupState="software_stopped_codec_unknown";speakerRunning=false;}
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
static bool validRunId(const char *value, size_t length) {
  if (length < 1 || length > 12) return false;
  for (size_t i = 0; i < length; ++i) {
    if (!((value[i] >= 'A' && value[i] <= 'Z') ||
          (value[i] >= '0' && value[i] <= '9'))) return false;
  }
  return true;
}

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


static char commandBuffer[64]; static size_t commandLength=0; static bool commandOverflow=false;
static void handleAudioCommandLine(){
 commandBuffer[commandLength < 64 ? commandLength : 63]='\0';
 if(commandOverflow || commandLength==0) { emitJson("error","invalid_command"); }
 else {
  if (commandLength > 9 && memcmp(commandBuffer, "mic_test ", 9) == 0) {
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
  } else { emitJson("error","invalid_command"); }
 }
 commandLength=0; commandOverflow=false;
}
static void resetHarnessState(){
 Serial=SerialStub{}; micResultReady=false; toneResultReady=false; audioLifecycleUncertain=false; ready=true;
 micResultId[0]='\0'; toneResultId[0]='\0'; micExecutions=0; toneExecutions=0;
 micRms=0; micPeak=0; micResultReason="run_not_found"; micCleanupState="not_attempted";
 toneResultReason="run_not_found"; toneCleanupState="not_attempted"; micRunning=false; speakerRunning=false;
}
int main(){
 const std::string expectedMic = "{\"v\":1,\"type\":\"mic_test\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation_id\":\"ABCDEFGHIJKL\",\"state\":\"INCONCLUSIVE\",\"reason\":\"owner_observation_required\",\"cleanup\":\"quiescent\",\"mic_rms\":32768,\"mic_peak\":32768}\r\n";
 micResultReason="owner_observation_required"; micCleanupState="quiescent"; micRms=32768; micPeak=32768;
 emitAudioJson("mic_test","mic_test","ABCDEFGHIJKL",true,nullptr,nullptr);
 if(Serial.bytes != expectedMic || Serial.bytes.size()>256) return 1;
 Serial.bytes.clear();
 const std::string expectedTone = "{\"v\":1,\"type\":\"tone_test\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation_id\":\"A1\",\"state\":\"INCONCLUSIVE\",\"reason\":\"owner_observation_required\",\"cleanup\":\"software_stopped_codec_unknown\"}\r\n";
 emitAudioJson("tone_test","tone_test","A1",false,"owner_observation_required","software_stopped_codec_unknown");
 if(Serial.bytes != expectedTone || Serial.bytes.find("mic_rms") != std::string::npos) return 2;
 Serial.bytes.clear();
 const std::string expectedError = "{\"v\":1,\"type\":\"error\",\"firmware_build\":\"adv-diagnostic-3-audio-proposal\",\"operation\":\"unknown\",\"operation_id\":\"\",\"state\":\"INCONCLUSIVE\",\"reason\":\"invalid_command\",\"cleanup\":\"not_attempted\"}\r\n";
 emitAudioJson("error","unknown","",false,"invalid_command","not_attempted");
 if(Serial.bytes != expectedError || Serial.bytes.find("mic_peak") != std::string::npos) return 3;
 Serial.bytes.clear(); Serial.limit=4;
 emitAudioJson("tone_test","tone_test","A1",false,"owner_observation_required","software_stopped_codec_unknown");
 if(!Serial.ended || Serial.bytes.size()!=4) return 4;
 Serial=SerialStub{};
 auto send=[&](const char*cmd){std::strncpy(commandBuffer,cmd,sizeof(commandBuffer));commandLength=std::strlen(cmd);handleAudioCommandLine();};
 send("mic_test A1"); std::string original=Serial.bytes; if(micExecutions!=1 || original.empty()) return 5;
 Serial.bytes.clear(); send("mic_result ZZ"); if(micExecutions!=1) return 6;
 Serial.bytes.clear(); send("mic_test B2"); if(micExecutions!=1) return 7;
 Serial.bytes.clear(); send("mic_result A1"); if(Serial.bytes!=original || micExecutions!=1) return 8;
 Serial.bytes.clear(); send("tone_test T1"); if(toneExecutions!=1 || Serial.bytes.empty()) return 9;
 Serial.bytes.clear(); send("mic_test M3"); if(micExecutions!=1 || Serial.bytes.find("run_id_busy")==std::string::npos) return 10;
 Serial.bytes.clear(); send("tone_test T2"); if(toneExecutions!=1 || Serial.bytes.find("run_id_busy")==std::string::npos) return 11;
 resetHarnessState();
 Serial.bytes.clear(); send("tone_test T1"); if(toneExecutions!=1 || Serial.bytes.empty()) return 12;
 Serial.bytes.clear(); send("mic_test M1"); if(micExecutions!=1 || Serial.bytes.empty()) return 13;
 Serial.bytes.clear(); send("tone_test T2"); if(toneExecutions!=1 || Serial.bytes.find("run_id_busy")==std::string::npos) return 14;
 Serial.bytes.clear(); send("mic_test M2"); if(micExecutions!=1 || Serial.bytes.find("run_id_busy")==std::string::npos) return 15;
 return 0;
}
