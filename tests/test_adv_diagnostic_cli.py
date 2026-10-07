import json
import unittest
from unittest.mock import patch

from scripts import adv_diagnostic_cli as cli


def response(kind="status", state="not_run", **extra):
    value = {
        "v": 1, "type": kind, "firmware_build": cli.PROTOCOL_BUILD,
        "board_ready": True, "imu_ready": True,
        "sd": {
            "state": state, "stage": "idle", "reason": "none",
            "bytes_verified": 0, "cleanup": "not_attempted",
        },
    }
    value.update(extra)
    return json.dumps(value, separators=(",", ":")).encode() + b"\n"


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

    def reset_input_buffer(self):
        pass

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
    def test_status_sends_only_status_and_closes(self):
        port = FakeSerial(response())
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", "status")
        self.assertTrue(result["board_ready"])
        self.assertEqual(port.writes, [b"status\n"])
        self.assertTrue(port.closed)
        self.assertFalse(port.dtr)
        self.assertFalse(port.rts)

    def test_sd_test_is_single_request_and_returns_result(self):
        port = FakeSerial(response("sd_test", "running") + response("sd_test_result", "pass"))
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", "sd_test")
        self.assertEqual(result["type"], "sd_test_result")
        self.assertEqual(port.writes, [b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_repeated_sd_request_returns_retained_terminal_without_retest(self):
        port = FakeSerial(response("sd_test", "pass"))
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run("COM-test", "sd_test")
        self.assertEqual(result["sd"]["state"], "pass")
        self.assertEqual(port.writes, [b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_timeout_does_not_retry_and_closes(self):
        port = FakeSerial(b"")
        with patch.object(cli.serial, "Serial", return_value=port), patch.object(
            cli.time, "monotonic", side_effect=[0, 100]
        ):
            with self.assertRaises(TimeoutError):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_rejects_unknown_field_and_firmware(self):
        with self.assertRaisesRegex(ValueError, "unexpected_fields"):
            cli.validate_response(response(extra="forbidden"), "status")
        wrong = json.loads(response())
        wrong["firmware_build"] = "other"
        with self.assertRaisesRegex(ValueError, "firmware_mismatch"):
            cli.validate_response(json.dumps(wrong).encode(), "status")

    def test_sd_ack_timeout_never_resends(self):
        port = FakeSerial(response("sd_test", "running"))
        with patch.object(cli.serial, "Serial", return_value=port), patch.object(
            cli.time, "monotonic", side_effect=[0, 0, 0, 0, 0, 100]
        ):
            with self.assertRaises(TimeoutError):
                cli.run("COM-test", "sd_test")
        self.assertEqual(port.writes, [b"sd_test\n"])
        self.assertTrue(port.closed)

    def test_rejects_overlong_frame(self):
        port = FakeSerial(b"x" * (cli.MAX_RESPONSE_BYTES + 1) + b"\n")
        with patch.object(cli.time, "monotonic", side_effect=[0] * 2000):
            with self.assertRaisesRegex(ValueError, "response_too_large"):
                cli.read_line(port, 1)

    def test_read_line_handles_split_frames_and_crlf(self):
        port = FakeSerial(b"{\"v\":1}\r\n")
        self.assertEqual(cli.read_line(port, time_deadline()), b"{\"v\":1}")


def time_deadline():
    import time
    return time.monotonic() + 1


if __name__ == "__main__":
    unittest.main()
