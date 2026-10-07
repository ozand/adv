import json
import unittest
from unittest.mock import patch

from scripts import adv_diagnostic_cli as cli


def v1(kind="status", state="not_run", build=cli.CURRENT_BUILD):
    return {
        "v": 1, "type": kind, "firmware_build": build,
        "board_ready": True, "imu_ready": True,
        "sd": {"state": state, "stage": "idle", "reason": "none",
               "bytes_verified": 0, "cleanup": "not_attempted"},
    }


def v2(kind="run_result", run_id="RUN1", overall="INCONCLUSIVE"):
    return {
        "v": 2, "type": kind, "firmware_build": "adv-diagnostic-2", "run_id": run_id,
        "overall": overall,
        "check_names": list(cli.RUN_CHECKS),
        "checks": ["PASS", "PASS", "PASS"] + ["NOT_TESTED"] * 9,
        "reasons": ["none"] * 3 + ["owner_observation_required"] * 9,
        "metrics": {"free_heap_bytes": 123456, "ram_bytes_verified": 256, "imu_samples": 8},
        "reason": "none",
    }


def line(value):
    return json.dumps(value, separators=(",", ":")).encode("ascii") + b"\r\n"


class FakeSerial:
    def __init__(self, data):
        self.data = bytearray(data)
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

    def read(self, size):
        if not self.data:
            return b""
        result = self.data[:size]
        del self.data[:size]
        return bytes(result)


class RunnerContractTests(unittest.TestCase):
    def test_id_validation(self):
        for value in ("A", "ABC123", "Z" * 12):
            self.assertTrue(cli.RUN_ID_PATTERN.fullmatch(value))
        for value in ("", "a", "A-B", "A" * 13, "é"):
            self.assertIsNone(cli.RUN_ID_PATTERN.fullmatch(value))

    def test_v1_build_allowlist_is_exact(self):
        self.assertEqual(cli.validate_response(line(v1(build=cli.LEGACY_BUILD)), "status")["firmware_build"], cli.LEGACY_BUILD)
        self.assertEqual(cli.validate_response(line(v1()), "status")["firmware_build"], cli.CURRENT_BUILD)
        with self.assertRaisesRegex(ValueError, "firmware_mismatch"):
            cli.validate_response(line(v1(build="adv-diagnostic-3")), "status")

    def test_firmware_error_envelopes_and_accessory_reason(self):
        for reason, request_id, response_id in (
            ("invalid_id", "RUN1", ""), ("run_id_busy", "RUN2", "RUN2"),
            ("not_ready", "RUN1", "RUN1"), ("run_not_found", "RUN1", "RUN1"),
        ):
            frame = v2("error", response_id, "INCONCLUSIVE")
            frame["reason"] = reason
            self.assertEqual(
                cli.validate_run_response(line(frame), "result", request_id)["reason"],
                reason,
            )
        frame = v2()
        frame["reasons"][10] = "accessory_unknown"
        self.assertEqual(
            cli.validate_run_response(line(frame), "run_result", "RUN1")["reasons"][10],
            "accessory_unknown",
        )

    def test_v2_schema_bounds_and_fixed_slots(self):
        result = cli.validate_run_response(line(v2()), "run_result", "RUN1")
        self.assertEqual(len(result["checks"]), 12)
        bad_names = v2()
        bad_names["check_names"][0] = "usb_transport"
        with self.assertRaisesRegex(ValueError, "invalid_run_check_names"):
            cli.validate_run_response(line(bad_names), "run_result", "RUN1")
        bad = v2()
        bad["checks"].pop()
        with self.assertRaisesRegex(ValueError, "invalid_run_checks"):
            cli.validate_run_response(line(bad), "run_result", "RUN1")
        bad = v2()
        bad["metrics"]["imu_samples"] = 9
        with self.assertRaisesRegex(ValueError, "invalid_run_metrics"):
            cli.validate_run_response(line(bad), "run_result", "RUN1")

    def test_run_ack_then_result_no_retry(self):
        ack = v2("run_ack")
        result = v2("run_result")
        port = FakeSerial(line(ack) + line(result))
        with patch.object(cli.serial, "Serial", return_value=port):
            actual = cli.run_v2(port, "run", "RUN1")
        self.assertEqual(actual["type"], "run_result")
        self.assertEqual(port.writes, [b"run RUN1\n"])

    def test_cached_result_type_is_accepted_for_explicit_same_id_run(self):
        cached = v2("result")
        port = FakeSerial(line(cached))
        result = cli.run_v2(port, "run", "RUN1")
        self.assertEqual(result["type"], "result")
        self.assertEqual(port.writes, [b"run RUN1\n"])

    def test_result_query_is_read_only(self):
        port = FakeSerial(line(v2("result")))
        with patch.object(cli.serial, "Serial", return_value=port):
            cli.run_v2(port, "result", "RUN1")
        self.assertEqual(port.writes, [b"result RUN1\n"])

    def test_lost_run_ack_never_retries(self):
        port = FakeSerial(b"")
        with patch.object(cli.serial, "Serial", return_value=port), patch.object(
            cli, "RUN_TIMEOUT_SECONDS", 0.01
        ):
            with self.assertRaises(TimeoutError):
                cli.run_v2(port, "run", "RUN1")
        self.assertEqual(port.writes, [b"run RUN1\n"])

    def test_cached_same_id_terminal_and_busy(self):
        terminal = v2("run_result")
        port = FakeSerial(line(terminal))
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run_v2(port, "run", "RUN1")
        self.assertEqual(result["type"], "run_result")
        self.assertEqual(port.writes, [b"run RUN1\n"])
        busy = v2("error", "RUN2")
        busy["reason"] = "run_id_busy"
        port = FakeSerial(line(busy))
        with patch.object(cli.serial, "Serial", return_value=port):
            with self.assertRaisesRegex(ValueError, "run_id_busy"):
                cli.run_v2(port, "run", "RUN2")

    def test_error_run_not_found_is_inconclusive(self):
        missing = v2("error")
        missing["reason"] = "run_not_found"
        port = FakeSerial(line(missing))
        with patch.object(cli.serial, "Serial", return_value=port):
            result = cli.run_v2(port, "result", "RUN1")
        self.assertEqual(result["reason"], "run_not_found")
        report = cli.build_report(result, None, usb_handshake=True)
        self.assertEqual(report["overall"], "INCONCLUSIVE")
        self.assertEqual(len(report["checks"]), 19)
        self.assertTrue(all(item["status"] == "INCONCLUSIVE" for item in report["checks"][:12]))
        self.assertEqual(report["coverage"]["inconclusive"], 12)
        self.assertEqual(report["checks"][12]["name"], "usb_transport")
        self.assertEqual(report["checks"][12]["status"], "PASS")
        self.assertEqual(report["error"], "run_not_found")

    def test_with_sd_is_explicit_separate_v1_phase(self):
        calls = []
        port = FakeSerial(line(v1()))
        with patch.object(cli, "run_v2", return_value=v2()), patch.object(
            cli, "run_v1", side_effect=lambda p, cmd, **kwargs: calls.append(cmd) or v1("sd_test_result", "pass")
        ):
            cli.run_full_port(port, "RUN1", with_sd=True)
        self.assertEqual(calls, ["sd_test"])
        calls.clear()
        port = FakeSerial(line(v1()))
        with patch.object(cli, "run_v2", return_value=v2()), patch.object(
            cli, "run_v1", side_effect=lambda p, cmd, **kwargs: calls.append(cmd) or v1()
        ):
            cli.run_full_port(port, "RUN1", with_sd=False)
        self.assertEqual(calls, [])

    def test_lost_run_ack_never_retries_and_result_recovery_is_read_only(self):
        port = FakeSerial(b"")
        with patch.object(cli, "RUN_TIMEOUT_SECONDS", 0.01):
            with self.assertRaises(TimeoutError):
                cli.run_v2(port, "run", "RUN1")
        self.assertEqual(port.writes, [b"run RUN1\n"])
        port = FakeSerial(line(v2("result")))
        recovered = cli.run_v2(port, "result", "RUN1")
        self.assertEqual(recovered["type"], "result")
        self.assertEqual(port.writes, [b"result RUN1\n"])

    def test_report_coverage_maps_all_fixed_check_positions(self):
        report = cli.build_report(v2(), None, usb_handshake=True)
        self.assertEqual(
            [item["name"] for item in report["checks"]],
            list(cli.RUN_CHECKS) + list(cli.REPORT_ONLY_CHECKS),
        )
        self.assertEqual(report["coverage"]["pass"], 4)
        self.assertEqual(report["coverage"]["not_tested"], 15)
        self.assertEqual(report["checks"][12], {
            "name": "usb_transport", "status": "PASS", "reason": "status_handshake_succeeded"
        })
        self.assertTrue(all(item["status"] == "NOT_TESTED" for item in report["checks"][13:]))
        self.assertEqual(report["sd_test"], None)

    def test_fake_v2_frame_matches_firmware_slots_and_is_bounded(self):
        frame = line(v2())
        self.assertLessEqual(len(frame), cli.MAX_RESPONSE_BYTES)
        parsed = cli.validate_run_response(frame.rstrip(), "run_result", "RUN1")
        self.assertEqual(parsed["check_names"], list(cli.RUN_CHECKS))
        self.assertEqual(parsed["reasons"][10], "owner_observation_required")
        unknown = v2("error", "MISSING1", "INCONCLUSIVE")
        unknown["reason"] = "run_not_found"
        accepted = cli.validate_run_response(line(unknown), "result", "MISSING1")
        self.assertEqual(accepted["run_id"], "MISSING1")
        self.assertEqual(accepted["reason"], "run_not_found")

    def test_v2_cap_is_1024_and_1025_rejected(self):
        payload = v2("error", "Z" * 12)
        payload["reason"] = "run_id_busy"
        encoded = line(payload)
        self.assertLessEqual(len(encoded), cli.MAX_RESPONSE_BYTES)
        oversized = b" " * (cli.MAX_RESPONSE_BYTES - 1) + b"x\n"
        with self.assertRaisesRegex(ValueError, "response_too_large"):
            cli.validate_run_response(oversized, "run_result", "RUN1")

    def test_unknown_fields_duplicate_keys_and_overlong_response_rejected(self):
        bad = v2()
        bad["extra"] = 1
        with self.assertRaisesRegex(ValueError, "unexpected_run_fields"):
            cli.validate_run_response(line(bad), "run_result", "RUN1")
        with self.assertRaisesRegex(ValueError, "duplicate_json_key"):
            cli.validate_run_response(b'{"v":2,"v":2}', "run_result", "RUN1")
        nonfinite = line(v2()).replace(b'"free_heap_bytes":123456', b'"free_heap_bytes":NaN')
        with self.assertRaisesRegex(ValueError, "invalid_json"):
            cli.validate_run_response(nonfinite, "run_result", "RUN1")
        port = FakeSerial(b"x" * (cli.MAX_RESPONSE_BYTES + 1) + b"\n")
        with self.assertRaisesRegex(ValueError, "response_too_large"):
            cli.read_line(port, cli.time.monotonic() + 1, max_bytes=cli.MAX_RESPONSE_BYTES)


if __name__ == "__main__":
    unittest.main()
