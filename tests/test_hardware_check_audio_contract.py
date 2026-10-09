"""Source-backed contract tests for opt-in firmware audio diagnostics."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).parents[1]
SKETCH = ROOT / "scripts" / "hardware_check" / "hardware_check.ino"


def test_emitter_templates_are_bounded_json_with_actual_crlf():
    source = SKETCH.read_text(encoding="utf-8")
    mic_template = json.loads(re.search(r'n = snprintf\(frame, sizeof\(frame\), (".*mic_rms.*")', source).group(1))
    formatted = mic_template % ("ABCDEFGHIJKL", "owner_observation_required", "quiescent", 32768, 32768)
    mic = json.loads(formatted)
    assert mic["mic_peak"] == 32768 and mic["state"] == "INCONCLUSIVE"
    assert len(formatted.encode()) <= 256
    assert "\\\\r\\\\n" not in mic_template
    assert "\r\n" in formatted
    assert "samples" not in mic and "waveform" not in mic

    error_source = source[source.index('if (strcmp(type, "error") == 0)') : source.index('else if (mic)', source.index('if (strcmp(type, "error") == 0)'))]
    error_template = json.loads(re.search(r'n = snprintf\(frame, sizeof\(frame\), (".*operation.*")', error_source).group(1))
    result_pairs = {
        "mic_test": [("owner_observation_required", "quiescent"), ("zero_signal", "quiescent"), ("begin_failed", "quiescent"), ("record_failed", "quiescent"), ("capture_timeout", "quiescent"), ("cleanup_unknown", "unknown"), ("not_ready", "not_attempted"), ("audio_busy", "not_attempted"), ("run_id_busy", "not_attempted"), ("run_not_found", "not_attempted"), ("invalid_command", "not_attempted")],
        "tone_test": [("owner_observation_required", "software_stopped_codec_unknown"), ("play_failed", "software_stopped_codec_unknown"), ("playback_timeout", "software_stopped_codec_unknown"), ("cleanup_unknown", "unknown"), ("not_ready", "not_attempted"), ("audio_busy", "not_attempted"), ("run_id_busy", "not_attempted"), ("run_not_found", "not_attempted"), ("invalid_command", "not_attempted")],
    }
    for operation, pairs in result_pairs.items():
        for reason, cleanup in pairs:
            if operation == "mic_test":
                frame = formatted if (reason, cleanup) == ("owner_observation_required", "quiescent") else mic_template % ("ABCDEFGHIJKL", reason, cleanup, 0, 0)
            else:
                tone_template = json.loads(re.search(r'n = snprintf\(frame, sizeof\(frame\), (".*tone_test.*")', source).group(1))
                frame = tone_template % ("ABCDEFGHIJKL", reason, cleanup)
            assert len(frame.encode("ascii")) <= 256
            assert json.loads(frame)["reason"] == reason
    errors = {"mic_test": ["not_ready", "audio_busy", "run_id_busy", "run_not_found", "invalid_command"], "tone_test": ["not_ready", "audio_busy", "run_id_busy", "run_not_found", "invalid_command"]}
    for operation, reasons in errors.items():
        for reason in reasons:
            frame = error_template % (operation, "ABCDEFGHIJKL", reason, "not_attempted")
            assert len(frame.encode("ascii")) <= 256
            assert json.loads(frame)["operation"] == operation


def test_capture_callback_is_the_only_metrics_gate_and_end_is_join_boundary():
    source = SKETCH.read_text(encoding="utf-8")
    callback = source[source.index("static void micReleaseCallback") : source.index("static const char *const kAudioReasons")]
    assert "data == micSamples && length == kMicSamples" in callback
    assert "store(true, std::memory_order_release)" in callback
    mic = source[source.index("static void executeMicTest() {") : source.index("static void executeToneTest() {")]
    assert "record(micSamples, kMicSamples, kMicSampleRate, false)" in mic
    assert "isRecording() == 0" not in mic[:mic.index("for (size_t i = 0; i < kMicSamples")]
    assert mic.index("micCaptureComplete.load(std::memory_order_acquire)") < mic.index("for (size_t i = 0; i < kMicSamples")
    assert "M5.Mic.end();" in mic
    assert mic.index("M5.Mic.end();") < mic.index("memset(micSamples")
    assert "static_cast<uint32_t>(millis() - started)" in mic
    assert "micRms = micPeak = 0" in mic
    assert "bool recordQueued = false" in mic
    assert "if (recordQueued) micResultReason = \"capture_timeout\"" in mic
    assert "overrideReason ? overrideReason" in source
    assert "responseRms" in source and "responsePeak" in source
    assert "Serial.write(reinterpret_cast<const uint8_t *>(frame), static_cast<size_t>(n)) != static_cast<size_t>(n)" in source
    assert "Serial.end();  // Never append another frame after a partial audio response." in source
    tone = source[source.index("static void executeToneTest() {") : source.index("void loop()")]
    assert "M5.Speaker.end();" in tone
    assert tone.index("M5.Speaker.end();") < tone.index("memset(toneSamples")
    assert "emitAudioJson(\"error\", \"mic_test\", id, true, \"run_not_found\", \"not_attempted\")" in source
    assert "emitAudioJson(\"error\", \"tone_test\", id, false, \"run_not_found\", \"not_attempted\")" in source


def test_operations_are_explicit_cached_and_not_boot_or_aggregate_side_effects():
    source = SKETCH.read_text(encoding="utf-8")
    assert 'memcmp(commandBuffer, "mic_test ", 9)' in source
    assert 'memcmp(commandBuffer, "tone_test ", 10)' in source
    assert 'memcmp(commandBuffer, "mic_result ", 11)' in source
    assert 'memcmp(commandBuffer, "tone_result ", 12)' in source
    setup = source[source.index("void setup()") : source.index("static constexpr size_t kCommandMaxBytes")]
    assert "executeMicTest" not in setup and "executeToneTest" not in setup
    aggregate = source[source.index("static void executeRun") : source.index("static void executeMicTest")]
    assert "Mic." not in aggregate and "Speaker." not in aggregate
    assert "if (strcmp(micResultId, id) == 0)" in source
    assert "if (strcmp(toneResultId, id) == 0)" in source
    assert "toneResultReady || audioLifecycleUncertain" in source
    assert "micResultReady || audioLifecycleUncertain" in source


def test_mic_lifecycle_source_guards():
    source = SKETCH.read_text(encoding="utf-8")
    mic = source[source.index("static void executeMicTest() {") : source.index("static void executeToneTest() {")]
    callback = source[source.index("static void micReleaseCallback") : source.index("static const char *const kAudioReasons")]
    assert "data == micSamples && length == kMicSamples" in callback
    assert "std::memory_order_release" in callback and "std::memory_order_acquire" in mic
    assert "if (M5.Mic.record" in mic and "bool recordQueued = false" in mic
    assert mic.index("M5.Mic.end();") < mic.index("memset(micSamples")
    assert "static_cast<uint32_t>(millis() - started)" in mic
    assert "micResultReason = \"capture_timeout\"" in mic
    assert "micRms = micPeak = 0" in mic


def test_tone_is_fixed_bounded_and_uncertainty_is_not_pass():
    source = SKETCH.read_text(encoding="utf-8")
    tone = source[source.index("static void executeToneTest() {") : source.index("void loop()")]
    assert "kToneSamples = 1600" in source and "kToneSampleRate = 16000" in source
    assert "2.0 * PI * 440.0" in tone
    assert "M5.Speaker.setVolume(8)" in tone
    assert "software_stopped_codec_unknown" in tone
    assert "INCONCLUSIVE" in source[source.index("static void emitAudioJson") : source.index("static void emitJson")]
    assert "tone_test_result" not in source
    assert "cfg.internal_mic = true;" in source and "cfg.internal_spk = true;" in source
    assert 'firmware_build\\\":\\\"adv-diagnostic-3-audio-proposal' in source
    host = (ROOT / "scripts" / "adv_diagnostic_cli.py").read_text(encoding="utf-8")
    assert "AUDIO_BUILD = \"adv-diagnostic-3-audio-proposal\"" in host
