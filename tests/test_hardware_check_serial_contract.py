from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]
SKETCH = ROOT / "scripts" / "hardware_check" / "hardware_check.ino"
README = ROOT / "scripts" / "hardware_check" / "README.md"


class SerialContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SKETCH.read_text(encoding="utf-8")
        cls.docs = README.read_text(encoding="utf-8")

    def test_command_allowlist_and_bounded_line(self):
        self.assertIn('memcmp(commandBuffer, "status", 6)', self.source)
        self.assertIn('memcmp(commandBuffer, "sd_test", 7)', self.source)
        self.assertIn("kCommandMaxBytes = 64", self.source)
        self.assertIn("commandOverflow = true", self.source)
        self.assertIn('emitJson("error", "invalid_command")', self.source)

    def test_status_path_is_cached_and_sd_test_is_one_shot(self):
        command = self.source[self.source.index("static void handleCommandLine") : self.source.index("static void pollSerialCommands")]
        self.assertNotIn("SD.", command.split('memcmp(commandBuffer, "status"')[1].split("} else if")[0])
        self.assertIn("if (!sdDone) {", command)
        self.assertIn('emitJson("sd_test", "none");', command)
        self.assertLess(command.index('emitJson("sd_test", "none");'), command.index("runSdSelfTest();"))
        self.assertIn("if ((key == 's' || key == 'S') && !sdDone)", self.source)
        self.assertIn("runSdSelfTest();", self.source)
        self.assertIn("sdDone = true;", self.source)

    def test_response_is_fixed_bounded_json_and_no_raw_echo(self):
        self.assertIn("char json[384];", self.source)
        self.assertIn('strcmp(type, "sd_test_result") == 0', self.source)
        self.assertIn('emitJson("sd_test_result", sdReason);', self.source)
        self.assertIn('emitJson("status", sdReason);', self.source)
        self.assertNotIn('emitJson("status", "none")', self.source)
        self.assertIn('\\"firmware_build\\":\\"adv-diagnostic-2\\"', self.source)
        self.assertIn('\\"bytes_verified\\":%u', self.source)
        self.assertIn('"verify_mismatch"', self.source)
        self.assertIn('"invalid_command"', self.source)
        self.assertIn('"not_ready"', self.source)
        self.assertNotIn("Serial.print(command", self.source)
        self.assertNotIn("Serial.write(command", self.source)

    def test_sd_terminal_paths_record_failure_or_result(self):
        body = self.source[self.source.index("static void runSdSelfTest") : self.source.index("void setup()")]
        returns = [m.start() for m in re.finditer(r"\breturn;", body)]
        self.assertGreaterEqual(len(returns), 6)
        for end in returns:
            prefix = body[max(0, end - 360) : end]
            self.assertRegex(prefix, r"sdState = SdState::(Fail|Pass)")

    def test_documented_contract_matches_bounds(self):
        self.assertIn("64 printable command bytes", self.docs)
        self.assertIn("status` reads cached state only", self.docs)
        self.assertIn("physical `S` key uses the same one-shot guard", self.docs)

    def test_runner_is_bounded_idempotent_and_excludes_sd_side_effects(self):
        self.assertIn('commandLength > 4 && memcmp(commandBuffer, "run ", 4)', self.source)
        self.assertIn('commandLength > 7 && memcmp(commandBuffer, "result ", 7)', self.source)
        self.assertIn('emitRunJson("run_ack", "none", lastRunId);', self.source)
        self.assertIn('executeRun(commandBuffer + 4);', self.source)
        self.assertIn('emitRunJson("run_result", "none", lastRunId);', self.source)
        self.assertIn('emitRunJson("result", "none", lastRunId);', self.source)
        run_block = self.source[self.source.index("static void executeRun") : self.source.index("void loop()")]
        self.assertNotIn("SD.", run_block)
        self.assertIn("uint8_t scratch[256]", run_block)
        self.assertIn("i < 8", run_block)
        self.assertIn("runReasons[11], " + '"not_requested"', run_block)
        self.assertIn("kRunFrameMaxBytes = 1024", self.source)
        self.assertIn("run data is volatile", self.docs.lower())
        expected = ["mcu", "ram_scratch", "imu_data", "motion", "display", "keyboard", "audio", "ir", "radio", "battery", "connectors", "sd"]
        names = re.search(r"kCheckNames\[12\] = \{([^}]+)\}", self.source)
        self.assertEqual(expected, re.findall(r'"([a-z_]+)"', names.group(1)))
        self.assertIn('adv-diagnostic-2', self.source)
        self.assertIn("accessory_unknown", self.source)
        self.assertIn("responseRunId(const char *requestedId)", self.source)
        self.assertIn("kCheckNames[12]", self.source)
        self.assertIn("kRunFrameMaxBytes = 1024", self.source)
        self.assertIn('adv-diagnostic-2', self.source)
        self.assertIn('runReasons[10], "accessory_unknown"', self.source)
        self.assertIn('runReasons[11], "not_requested"', self.source)
        self.assertIn('emitRunJson("error", "run_not_found", commandBuffer + 7);', self.source)
        self.assertIn('emitRunJson("error", "run_id_busy", commandBuffer + 4);', self.source)
        self.assertNotIn('firmware_build\\":\\"adv-diagnostic-1', self.source)
        self.assertIn('return requestedId;', self.source)
        self.assertIn('emitRunJson("error", "run_not_found", commandBuffer + 7);', self.source)
        self.assertIn('emitRunJson("error", "run_id_busy", commandBuffer + 4);', self.source)


if __name__ == "__main__":
    unittest.main()
