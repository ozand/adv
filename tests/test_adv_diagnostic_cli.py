import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch

from scripts import adv_diagnostic_cli as cli


def response(kind="status", state="not_run", reason="none", stage="idle", cleanup="not_attempted", count=0):
    value = {
        "v": 1, "type": kind, "firmware_build": cli.PROTOCOL_BUILD,
        "board_ready": True, "imu_ready": True,
        "sd": {"state": state, "stage": stage, "reason": reason,
               "bytes_verified": count, "cleanup": cleanup},
    }
    return json.dumps(value, separators=(",", ":")).encode() + bytes((13, 10))


class FakeSerial:
    def __init__(self, replies):
        self.replies = bytearray(replies)
        self.writes = []
        self.closed = False
        self.dtr = True
        self.rts = True
        self.timeout = 0.1

    def open(self):
        pass

    def close(self):
        self.closed = True

    def write(self, data):
        self.writes.append(data)
        return len(data)

    def read(self, count):
        if not self.replies:
            return b""
        result = self.replies[:count]
        del self.replies[:count]
        return bytes(result)


class DiagnosticCliTests(unittest.TestCase):
    def test_legacy_error_main_preserves_output_and_audio_error_stays_wrapped(self):
        for command, replies, expected_error, writes in (
            ("status", response("error", reason="not_ready"), "not_ready",
             [b"status\n"]),
            ("sd_test", response() + response("error", reason="not_ready"), "not_ready",
             [b"status\n", b"sd_test\n"]),
        ):
            with self.subTest(command=command):
                port = FakeSerial(replies)
                output = io.StringIO()
                with patch.object(cli.serial, "Serial", return_value=port), \
                     patch.object(sys, "argv", ["cli", "--port", "COM-test", "--command", command]), \
                     contextlib.redirect_stdout(output):
                    exit_code = cli.main()
                self.assertEqual(exit_code, 2)
                report = json.loads(output.getvalue())
                self.assertEqual(report["error"], expected_error)
                self.assertEqual(report["result"]["type"], "error")
                self.assertNotIn("execution", report)
                self.assertEqual(port.writes, writes)

    def test_audio_error_main_uses_audio_wrapper(self):
        status_obj = json.loads(response())
        status_obj["firmware_build"] = cli.AUDIO_BUILD
        audio_error = {
            "v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
            "operation": "mic_test", "operation_id": "A1", "state": "INCONCLUSIVE",
            "reason": "audio_busy", "cleanup": "not_attempted",
        }
        port = FakeSerial(
            json.dumps(status_obj).encode() + bytes((13, 10))
            + json.dumps(audio_error).encode() + bytes((13, 10))
        )
        output = io.StringIO()
        with patch.object(cli.serial, "Serial", return_value=port), \
             patch.object(sys, "argv", ["cli", "--port", "COM-test", "--command",
                                          "mic_test", "--run-id", "A1"]), \
             contextlib.redirect_stdout(output):
            exit_code = cli.main()
        report = json.loads(output.getvalue())
        self.assertEqual(exit_code, 2)
        self.assertFalse(report["ok"])
        self.assertEqual(report["result"], audio_error)
        self.assertEqual(port.writes, [bytes((115, 116, 97, 116, 117, 115, 10)), bytes((109, 105, 99, 95, 116, 101, 115, 116, 32, 65, 49, 10))])

    def test_legacy_error_responses_keep_legacy_cli_shape(self):
        status_error = json.loads(response("error", reason="not_ready"))
        sd_error = json.loads(response("error", reason="not_ready"))
        cases = (
            ("status", status_error, [b"status\n"], response("error", reason="not_ready")),
            ("sd_test", sd_error, [b"status\n", b"sd_test\n"],
             response() + response("error", reason="not_ready")),
        )
        for command, expected_result, expected_writes, replies in cases:
            with self.subTest(command=command):
                port = FakeSerial(replies)
                output = io.StringIO()
                with patch.object(cli.serial, "Serial", return_value=port), \
                     patch.object(sys, "argv", ["adv_diagnostic_cli.py", "--port", "COM-test",
                                                   "--command", command]), \
                     contextlib.redirect_stdout(output):
                    exit_code = cli.main()
                payload = json.loads(output.getvalue())
                self.assertEqual(exit_code, 2)
                self.assertEqual(payload["error"], expected_result["sd"]["reason"])
                self.assertEqual(payload["result"], expected_result)
                self.assertNotIn("execution", payload)
                self.assertEqual(port.writes, expected_writes)

    def test_audio_error_dispatch_keeps_audio_wrapper_and_inconclusive_state(self):
        audio_error = {
            "v": 1, "type": "error", "firmware_build": cli.AUDIO_BUILD,
            "operation": "mic_test", "operation_id": "A1", "state": "INCONCLUSIVE",
            "reason": "audio_busy", "cleanup": "not_attempted",
        }
        audio_status = json.loads(response())
        audio_status["firmware_build"] = cli.AUDIO_BUILD
        port = FakeSerial(
            json.dumps(audio_status).encode() + bytes((13, 10))
            + json.dumps(audio_error).encode() + bytes((13, 10))
        )
        output = io.StringIO()
        with patch.object(cli.serial, "Serial", return_value=port), \
             patch.object(sys, "argv", ["adv_diagnostic_cli.py", "--port", "COM-test",
                                           "--command", "mic_test", "--run-id", "A1"]), \
             contextlib.redirect_stdout(output):
            exit_code = cli.main()
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["result"], audio_error)
        self.assertEqual(port.writes, [b"status" + bytes((10,)), b"mic_test A1" + bytes((10,))])

    def test_legacy_status_and_sd_accept_audio_build_without_changing_wire_version(self):
        payload = response().replace(cli.PROTOCOL_BUILD.encode(), cli.AUDIO_BUILD.encode())
        cli.validate_response(
            payload.rstrip(), "status", allowed_builds={cli.CURRENT_BUILD, cli.AUDIO_BUILD}
        )
        ack = response("sd_test", "running", stage="mount").replace(
            cli.PROTOCOL_BUILD.encode(), cli.AUDIO_BUILD.encode()
        )
        result_frame = response(
            "sd_test_result", "pass", stage="complete", count=65536, cleanup="removed"
        ).replace(cli.PROTOCOL_BUILD.encode(), cli.AUDIO_BUILD.encode())
        port = FakeSerial(payload + ack + result_frame)
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", "sd_test")
        self.assertEqual(result["type"], "sd_test_result")
        self.assertEqual(port.writes, [b"status" + bytes((10,)), b"sd_test" + bytes((10,))])
        self.assertEqual(result["v"], 1)

    def test_run_v2_accepts_audio_build_with_existing_v2_schema(self):
        value = {
            "v": 2, "type": "result", "firmware_build": cli.AUDIO_BUILD,
            "run_id": "A1", "overall": "INCONCLUSIVE",
            "check_names": list(cli.RUN_CHECKS),
            "checks": ["NOT_TESTED"] * 12,
            "reasons": ["unavailable"] * 12,
            "metrics": {"free_heap_bytes": 0, "ram_bytes_verified": 0, "imu_samples": 0},
            "reason": "none",
        }
        for build in (cli.AUDIO_BUILD, cli.CURRENT_BUILD):
            value["firmware_build"] = build
            payload = json.dumps(value, separators=(",", ":")).encode()
            self.assertEqual(cli.validate_run_response(payload, "result", "A1")["v"], 2)

    def run_fake(self, replies, command="sd_test"):
        port = FakeSerial(replies)
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", command)
        return result, port

    def test_status_is_one_cached_request(self):
        result, port = self.run_fake(response(), "status")
        self.assertEqual(result["type"], "status")
        self.assertEqual(port.writes, [b"status\n"])
        self.assertTrue(port.closed)
        self.assertFalse(port.dtr)
        self.assertFalse(port.rts)

    def test_sd_test_handshakes_before_explicit_command(self):
        ack = response("sd_test", "running", stage="mount")
        terminal = response("sd_test_result", "pass", stage="complete", count=65536, cleanup="removed")
        result, port = self.run_fake(response() + ack + terminal)
        self.assertEqual(result["type"], "sd_test_result")
        self.assertEqual(port.writes, [b"status\n", b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_not_ready_error_from_status_is_returned_without_sd_request(self):
        payload = json.loads(response("error", reason="not_ready"))
        port = FakeSerial(json.dumps(payload).encode() + bytes((13, 10)))
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", "sd_test")
        self.assertEqual(result["sd"]["reason"], "not_ready")
        self.assertEqual(port.writes, [b"status\n"])
        self.assertTrue(port.closed)

    def test_sd_test_mislabelled_terminal_ack_is_rejected(self):
        malformed_terminal = response("sd_test", "fail", reason="mount_failed", stage="error")
        port = FakeSerial(response() + malformed_terminal)
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "invalid_sd_ack"):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n", b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_status_mismatch_or_not_ready_never_sends_sd_test(self):
        wrong = json.loads(response())
        wrong["firmware_build"] = "wrong"
        port = FakeSerial(json.dumps(wrong).encode() + bytes((13, 10)))
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "firmware_mismatch"):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n"])
        self.assertTrue(port.closed)

        not_ready = json.loads(response())
        not_ready["board_ready"] = False
        port = FakeSerial(json.dumps(not_ready).encode() + bytes((13, 10)))
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "firmware_not_ready"):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n"])

    def test_cached_terminal_is_returned_without_sd_command(self):
        terminal = response("status", "pass", stage="complete", count=65536, cleanup="removed")
        result, port = self.run_fake(terminal)
        self.assertEqual(result["sd"]["state"], "pass")
        self.assertEqual(port.writes, [b"status\n"])

    def test_error_snapshot_is_validated_and_returned(self):
        payload = json.loads(response("error", reason="not_ready"))
        result, port = self.run_fake(json.dumps(payload).encode() + bytes((13, 10)))
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["sd"]["reason"], "not_ready")
        self.assertEqual(port.writes, [b"status\n"])

    def test_timeout_after_sd_command_never_retries(self):
        port = FakeSerial(response() + response("sd_test", "running", stage="mount"))
        with patch.object(cli.serial, "Serial", return_value=port), patch.object(
            cli, "SD_RESULT_SECONDS", 0.01
        ):
            with self.assertRaises(TimeoutError):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n", b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_duplicate_json_keys_and_nonfinite_numbers_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate_json_key"):
            cli.validate_response(b'{"v":1,"v":1}', "status")
        with self.assertRaisesRegex(ValueError, "invalid_json_number"):
            cli.validate_response(b'{"v":NaN}', "status")

    def test_data_pass_with_cleanup_failure_is_not_cli_success(self):
        cleanup_failed = response(
            "sd_test_result", "pass", stage="complete", reason="none",
            cleanup="failed", count=65536,
        )
        port = FakeSerial(
            response() + response("sd_test", "running", stage="mount") + cleanup_failed
        )
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "cleanup_failed"):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n", b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_all_firmware_reasons_are_allowed(self):
        reasons = {
            "none", "invalid_command", "not_ready", "unsupported_pin_map", "mount_failed",
            "invalid_or_small", "test_path_exists", "create_failed", "write_failed_or_timeout",
            "read_open_or_size_failed", "read_failed_or_timeout", "verify_mismatch",
            "verify_failed_or_timeout",
        }
        for reason in reasons:
            kind = "error" if reason in {"invalid_command", "not_ready"} else "status"
            cli.validate_response(response(kind, reason=reason).rstrip(), "status")

    def test_overlong_frame_is_rejected(self):
        port = FakeSerial(b"x" * (cli.MAX_RESPONSE_BYTES + 1) + b"\n")
        with patch.object(cli.time, "monotonic", side_effect=[0] * 3000):
            with self.assertRaisesRegex(ValueError, "response_too_large"):
                cli.read_line(port, 1)

    def test_crlf_frame_is_read(self):
        port = FakeSerial(b"{\"v\":1}\r\n")
        self.assertEqual(cli.read_line(port, cli.time.monotonic() + 1), b"{\"v\":1}")


if __name__ == "__main__":
    unittest.main()
