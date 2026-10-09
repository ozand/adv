"""Fake-serial coverage for proposed, explicitly opt-in audio host commands."""
import json
import unittest
from unittest.mock import patch

from scripts import adv_diagnostic_cli as cli


def frame(value):
    return json.dumps(value, separators=(",", ":")).encode("ascii") + bytes((13, 10))


def status(build=cli.AUDIO_BUILD, ready=True):
    return frame({
        "v": 1, "type": "status", "firmware_build": build,
        "board_ready": ready, "imu_ready": ready,
        "sd": {"state": "not_run", "stage": "idle", "reason": "none",
               "bytes_verified": 0, "cleanup": "not_attempted"},
    })


def result(command="mic_test", operation_id="A1"):
    family = "mic_test" if command.startswith("mic_") else "tone_test"
    value = {"v": 1, "type": family, "firmware_build": cli.AUDIO_BUILD,
             "operation_id": operation_id, "state": "INCONCLUSIVE",
             "reason": "owner_observation_required",
             "cleanup": "quiescent" if family == "mic_test" else "software_stopped_codec_unknown"}
    if family == "mic_test":
        value.update({"mic_rms": 123, "mic_peak": 456})
    return frame(value)


class FakePort:
    def __init__(self, replies):
        self.replies = bytearray(replies)
        self.writes = []
        self.timeout = 0.1

    def write(self, value):
        self.writes.append(value)
        return len(value)

    def read(self, count):
        value = self.replies[:count]
        del self.replies[:count]
        return bytes(value)


class AudioHostTests(unittest.TestCase):
    def test_audio_commands_handshake_then_write_once(self):
        for command in sorted(cli.AUDIO_COMMANDS):
            with self.subTest(command=command):
                port = FakePort(status() + result(command))
                got = cli.run_audio_port(port, command, "A1")
                family = "mic_test" if command.startswith("mic_") else "tone_test"
                self.assertEqual(got["type"], family)
                self.assertEqual(port.writes, [b"status\n", f"{command} A1\n".encode()])

    def test_old_or_unready_firmware_never_receives_audio_command(self):
        for reply in (status(build=cli.CURRENT_BUILD), status(ready=False)):
            port = FakePort(reply)
            with self.assertRaises(ValueError):
                cli.run_audio_port(port, "mic_test", "A1")
            self.assertEqual(port.writes, [b"status\n"])

    def test_status_accepts_audio_candidate_marker_only_on_status_path(self):
        parsed = cli.validate_response(
            status(), "status", allowed_builds={cli.AUDIO_BUILD}
        )
        self.assertEqual(parsed["firmware_build"], cli.AUDIO_BUILD)
        with self.assertRaisesRegex(ValueError, "firmware_mismatch"):
            cli.validate_response(
                status(), "status", allowed_builds={cli.CURRENT_BUILD}
            )

    def test_audio_frame_cap_counts_crlf_bytes(self):
        encoded = result()[:-2]
        at_limit = encoded + b" " * (cli.MAX_AUDIO_FRAME_BYTES - len(encoded) - 2)
        self.assertEqual(
            cli.validate_audio_response(at_limit, "mic_test", "A1")["type"],
            "mic_test",
        )
        over_limit = at_limit + b" "
        with self.assertRaisesRegex(ValueError, "response_too_large"):
            cli.validate_audio_response(over_limit, "mic_test", "A1")

    def test_terminal_frames_cannot_claim_pass_or_fail(self):
        value = json.loads(result().decode("ascii"))
        for state in ("PASS", "FAIL", "NOT_TESTED"):
            value["state"] = state
            with self.subTest(state=state), self.assertRaisesRegex(
                ValueError, "invalid_audio_state"
            ):
                cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")

    def test_mic_result_reason_cleanup_pairs_are_finite_and_failure_metrics_zero(self):
        valid_pairs = (
            ("unsupported_board", "not_attempted"), ("not_ready", "not_attempted"),
            ("audio_busy", "not_attempted"), ("begin_failed", "quiescent"),
            ("record_failed", "quiescent"), ("capture_timeout", "quiescent"),
            ("cleanup_unknown", "unknown"), ("zero_signal", "quiescent"),
            ("owner_observation_required", "quiescent"),
        )
        for reason, cleanup in valid_pairs:
            value = json.loads(result().decode("ascii"))
            value.update(reason=reason, cleanup=cleanup, mic_rms=0, mic_peak=0)
            with self.subTest(reason=reason, cleanup=cleanup):
                cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")
        invalid = json.loads(result().decode("ascii"))
        invalid.update(reason="capture_timeout", cleanup="quiescent", mic_rms=1)
        with self.assertRaisesRegex(ValueError, "invalid_audio_metrics"):
            cli.validate_audio_response(frame(invalid)[:-2], "mic_test", "A1")
        invalid.update(reason="audio_busy", cleanup="unknown", mic_rms=0, mic_peak=0)
        with self.assertRaisesRegex(ValueError, "invalid_audio_reason"):
            cli.validate_audio_response(frame(invalid)[:-2], "mic_test", "A1")

    def test_tone_result_reason_cleanup_pairs_are_finite(self):
        valid_pairs = (
            ("unsupported_board", "not_attempted"), ("not_ready", "not_attempted"),
            ("audio_busy", "not_attempted"),
            ("play_failed", "software_stopped_codec_unknown"),
            ("playback_timeout", "software_stopped_codec_unknown"),
            ("cleanup_unknown", "unknown"),
            ("owner_observation_required", "software_stopped_codec_unknown"),
        )
        for reason, cleanup in valid_pairs:
            value = json.loads(result("tone_test").decode("ascii"))
            value.update(reason=reason, cleanup=cleanup)
            with self.subTest(reason=reason, cleanup=cleanup):
                cli.validate_audio_response(frame(value)[:-2], "tone_test", "A1")
        value.update(reason="play_failed", cleanup="unknown")
        with self.assertRaisesRegex(ValueError, "invalid_audio_reason"):
            cli.validate_audio_response(frame(value)[:-2], "tone_test", "A1")

    def test_schema_is_operation_discriminated_and_bounded(self):
        mic = json.loads(result().decode("ascii"))
        self.assertEqual(cli.validate_audio_response(frame(mic)[:-2], "mic_test", "A1"), mic)
        tone = json.loads(result("tone_test").decode("ascii"))
        self.assertNotIn("mic_rms", tone)
        self.assertEqual(cli.validate_audio_response(frame(tone)[:-2], "tone_test", "A1"), tone)
        tone["mic_rms"] = 10
        with self.assertRaisesRegex(ValueError, "unexpected_audio_fields"):
            cli.validate_audio_response(frame(tone)[:-2], "tone_test", "A1")

    def test_unrecognized_operation_error_is_fixed_and_inconclusive(self):
        error = {"v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
                 "operation": "unknown", "operation_id": "", "state": "INCONCLUSIVE",
                 "reason": "invalid_command", "cleanup": "not_attempted"}
        got = cli.validate_audio_response(frame(error)[:-2], "mic_test", "A1")
        self.assertEqual(got, error)
        error["state"] = "PASS"
        with self.assertRaisesRegex(ValueError, "invalid_audio_state"):
            cli.validate_audio_response(frame(error)[:-2], "mic_test", "A1")

    def test_wrong_operation_error_is_rejected_for_requested_family(self):
        for command, other in (
            ("mic_test", "tone_test"), ("tone_test", "mic_test"),
            ("mic_result", "tone_test"), ("tone_result", "mic_test"),
        ):
            with self.subTest(command=command):
                error = {"v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
                         "operation": other, "operation_id": "A1", "state": "INCONCLUSIVE",
                         "reason": "not_ready" if command.endswith("test") else "run_not_found",
                         "cleanup": "not_attempted"}
                with self.assertRaisesRegex(ValueError, "audio_operation_mismatch"):
                    cli.validate_audio_response(frame(error)[:-2], command, "A1")

    def test_unknown_operation_error_requires_invalid_command_reason(self):
        error = {"v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
                 "operation": "unknown", "operation_id": "A1", "state": "INCONCLUSIVE",
                 "reason": "run_not_found", "cleanup": "not_attempted"}
        with self.assertRaisesRegex(ValueError, "audio_operation_mismatch"):
            cli.validate_audio_response(frame(error)[:-2], "mic_test", "A1")

    def test_invalid_command_has_empty_id_and_fixed_error_shape(self):
        error = {"v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
                 "operation": "mic_test", "operation_id": "", "state": "INCONCLUSIVE",
                 "reason": "invalid_command", "cleanup": "not_attempted"}
        got = cli.validate_audio_response(frame(error)[:-2], "mic_test", "A1")
        self.assertEqual(got, error)

    def test_errors_for_result_commands_use_operation_specific_cleanup(self):
        error = {"v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
                 "operation": "tone_test", "operation_id": "A1", "state": "INCONCLUSIVE",
                 "reason": "run_not_found", "cleanup": "not_attempted"}
        got = cli.validate_audio_response(frame(error)[:-2], "tone_result", "A1")
        self.assertEqual(got, error)
        error["cleanup"] = "unknown"
        with self.assertRaisesRegex(ValueError, "invalid_audio_reason"):
            cli.validate_audio_response(frame(error)[:-2], "tone_result", "A1")

    def test_bounds_include_twelve_character_id_and_max_metrics(self):
        payload = result(operation_id="A" * 12)
        value = json.loads(payload.decode("ascii"))
        value["mic_rms"] = 32767
        value["mic_peak"] = 32768
        self.assertEqual(
            cli.validate_audio_response(frame(value)[:-2], "mic_test", "A" * 12),
            value,
        )

    def test_mic_metrics_accept_signed_int16_peak_and_reject_rms_above_peak(self):
        value = json.loads(result().decode("ascii"))
        value["mic_rms"] = 32768
        value["mic_peak"] = 32768
        accepted = cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")
        self.assertEqual(accepted["mic_rms"], 32768)
        value["mic_rms"] = 100
        value["mic_peak"] = 99
        with self.assertRaisesRegex(ValueError, "invalid_audio_metrics"):
            cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")
        for value_type in (True, 1.5):
            value["mic_rms"] = value_type
            value["mic_peak"] = 32768
            with self.subTest(value_type=value_type), self.assertRaisesRegex(
                ValueError, "invalid_audio_metrics"
            ):
                cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")

    def test_audio_json_rejects_bool_and_float_protocol_versions(self):
        for version in (True, 1.0):
            value = json.loads(result().decode("ascii"))
            value["v"] = version
            with self.subTest(version=version), self.assertRaisesRegex(
                ValueError, "audio_protocol_mismatch"
            ):
                cli.validate_audio_response(frame(value)[:-2], "mic_test", "A1")

    def test_malformed_or_wrong_typed_audio_handshake_never_sends_audio(self):
        replies = []
        for version in (True, 1.0, 2):
            value = json.loads(status().decode("ascii"))
            value["v"] = version
            replies.append(frame(value))
        duplicate = b'{"v":1,"v":1}' + bytes((13, 10))
        nonfinite = b'{"v":NaN}' + bytes((13, 10))
        wrong_ready_type = json.loads(status().decode("ascii"))
        wrong_ready_type["board_ready"] = 1
        replies.extend((duplicate, nonfinite, frame(wrong_ready_type)))
        for reply in replies:
            port = FakePort(reply)
            with self.subTest(reply=reply[:32]), self.assertRaises(ValueError):
                cli.run_audio_port(port, "mic_test", "A1")
            self.assertEqual(port.writes, [b"status" + bytes((10,))])

    def test_invalid_host_id_is_rejected_before_any_serial_write(self):
        for operation_id in ("bad-id", "", "lower", "A" * 13):
            port = FakePort(status() + result())
            with self.subTest(operation_id=operation_id), self.assertRaisesRegex(
                ValueError, "invalid_run_id"
            ):
                cli.run_audio_port(port, "mic_test", operation_id)
            self.assertEqual(port.writes, [])

    def test_lost_audio_reply_is_never_retried(self):
        port = FakePort(status())
        with patch.object(cli, "AUDIO_TIMEOUT_SECONDS", 0.01):
            with self.assertRaises(TimeoutError):
                cli.run_audio_port(port, "tone_test", "A1")
        self.assertEqual(port.writes, [b"status\n", b"tone_test A1\n"])


if __name__ == "__main__":
    unittest.main()
