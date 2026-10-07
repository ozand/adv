import json
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
    return json.dumps(value, separators=(",", ":")).encode() + b"\r\n"


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

    def test_status_mismatch_or_not_ready_never_sends_sd_test(self):
        wrong = json.loads(response())
        wrong["firmware_build"] = "wrong"
        port = FakeSerial(json.dumps(wrong).encode() + b"\r\n")
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "firmware_mismatch"):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"status\n"])
        self.assertTrue(port.closed)

        not_ready = json.loads(response())
        not_ready["board_ready"] = False
        port = FakeSerial(json.dumps(not_ready).encode() + b"\r\n")
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
        result, port = self.run_fake(json.dumps(payload).encode() + b"\r\n")
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

    def test_success_requires_full_verification_and_cleanup(self):
        inconsistent = response("sd_test_result", "pass", stage="complete", cleanup="failed", count=65536)
        with self.assertRaisesRegex(ValueError, "inconsistent_sd_result"):
            cli.validate_response(inconsistent.rstrip(), "sd_test_result")

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
        with patch.object(cli.time, "monotonic", side_effect=[0] * 2000):
            with self.assertRaisesRegex(ValueError, "response_too_large"):
                cli.read_line(port, 1)

    def test_crlf_frame_is_read(self):
        port = FakeSerial(b"{\"v\":1}\r\n")
        self.assertEqual(cli.read_line(port, cli.time.monotonic() + 1), b"{\"v\":1}")


if __name__ == "__main__":
    unittest.main()
