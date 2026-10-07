import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "adv_launcher_probe.py"
spec = importlib.util.spec_from_file_location("adv_launcher_probe", MODULE_PATH)
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


class FakeSerial:
    def __init__(self, chunks):
        self.chunks = iter(chunks)
        self.writes = []

    def write(self, data):
        self.writes.append(data)

    def read(self, size):
        try:
            return next(self.chunks)
        except StopIteration:
            return b""


class Tick:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        self.value += 0.5
        return self.value


class LauncherProbeTests(unittest.TestCase):
    def test_extracts_only_validated_known_fields(self):
        raw = (
            b"Launcher 2.9.1\r\nM5Stack Cardputer & ADV\r\n"
            b"Flash size: 8MB\r\n<free> offset=0x2C0000 size=0x540000 (5376KB)\r\n"
            b"app0 type=app subtype=0x20 offset=0x010000 size=0x150000 (1344KB)\r\n"
            b"wifi ssid: private-network\r\nrandom serial bytes\r\n"
        )
        parsed = probe.parse_response(raw)
        rendered = probe.format_report(parsed, len(raw), 4)
        self.assertEqual(parsed["version"], "2.9.1")
        self.assertEqual(parsed["device"], "M5Stack Cardputer & ADV")
        self.assertEqual(parsed["flash"], "8MB")
        self.assertEqual(parsed["free"], "5376KB")
        self.assertEqual(parsed["partitions"][0]["label"], "app0")
        self.assertNotIn("private-network", rendered)
        self.assertNotIn("random serial bytes", rendered)

    def test_suppresses_malformed_and_oversized_values(self):
        raw = (
            b"Launcher 2.9.1\r\nM5Stack Cardputer & ADV\r\n"
            b"wifi ssid: hidden\r\n"
            b"app0 type=app subtype=../../token offset=secret size=1KB\r\n"
            b"Launcher 2.9.1" + b"X" * 100 + b"\r\n"
        )
        rendered = probe.format_report(probe.parse_response(raw), len(raw), 0)
        self.assertNotIn("hidden", rendered)
        self.assertNotIn("../../token", rendered)
        self.assertNotIn("secret", rendered)
        self.assertEqual(rendered.count("version:"), 1)

    def test_command_allowlist_and_output_cap(self):
        serial = FakeSerial([b"X" * 600] * 40)
        parsed, count, sent = probe.run_probe(serial, 12, clock=Tick(), sleeper=lambda _: None)
        self.assertLessEqual(count, probe.MAX_BYTES)
        self.assertLessEqual(len(serial.writes), len(probe.COMMANDS))
        self.assertTrue(all(write.rstrip() in {c.encode() for c in probe.COMMANDS} for write in serial.writes))
        self.assertEqual(sent, len(serial.writes))

    def test_empty_reads_terminate_at_deadline(self):
        serial = FakeSerial([])
        parsed, count, sent = probe.run_probe(serial, 1, clock=Tick(), sleeper=lambda _: None)
        self.assertEqual(count, 0)
        self.assertLessEqual(sent, len(probe.COMMANDS))

    def test_port_closes_if_probe_raises(self):
        class Port:
            closed = False
            dtr = False
            rts = False
            port = None

            def open(self):
                pass

            def close(self):
                self.closed = True

        port = Port()

        def fail_probe(*args, **kwargs):
            raise RuntimeError("probe failure")

        fake_serial_module = type("SerialModule", (), {"Serial": lambda **_: port})
        with patch.dict(sys.modules, {"serial": fake_serial_module}):
            with patch.object(probe, "run_probe", side_effect=fail_probe):
                with patch.object(probe, "parse_args", return_value=type("Args", (), {"port": "COM5", "seconds": 1})()):
                    with self.assertRaises(RuntimeError):
                        probe.main()
        self.assertTrue(port.closed)


if __name__ == "__main__":
    unittest.main()
