"""Source-backed checks for firmware v1/v2 JSON fragment bounds and parsing."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKETCH = ROOT / "scripts" / "hardware_check" / "hardware_check.ino"


def test_emitter_fragments_form_parseable_v1_and_v2_responses():
    source = SKETCH.read_text(encoding="utf-8")
    v1_source = source[source.index("static void emitJson") : source.index("static constexpr size_t kRunFrameMaxBytes")]
    v1_line = next(line for line in v1_source.splitlines() if "bytes_verified" in line)
    v1_template = ast.literal_eval(v1_line.strip().rstrip(","))
    v1_frame = v1_template % (
        "status", "true", "true", "not_run", "idle", "none", 0, "not_attempted"
    )
    v1_encoded = v1_frame.encode("ascii")
    assert len(v1_encoded) <= 512
    v1 = json.loads(v1_encoded)
    assert v1["v"] == 1 and v1["type"] == "status"
    assert v1["sd"]["bytes_verified"] == 0

    emitter = source[source.index("static void emitRunJson") : source.index("static uint8_t patternByte")]
    prefix_line = next(line for line in emitter.splitlines() if "check_names" in line)
    suffix_line = next(line for line in emitter.splitlines() if "free_heap_bytes" in line)
    prefix_literal = prefix_line.split("snprintf(json, sizeof(json), ", 1)[1].split(", safeType", 1)[0]
    suffix_literal = suffix_line.split("- used, ", 1)[1].rsplit(",", 1)[0]
    prefix = ast.literal_eval(prefix_literal)
    suffix = ast.literal_eval(suffix_literal)
    names = ["mcu", "ram_scratch", "imu_data", "motion", "display", "keyboard",
             "audio", "ir", "radio", "battery", "connectors", "sd"]
    checks = ["PASS", "PASS", "PASS"] + ["NOT_TESTED"] * 9
    reasons = ["none"] * 3 + ["owner_observation_required"] * 9
    metrics = {"free_heap_bytes": 345028, "ram_bytes_verified": 256, "imu_samples": 8}

    for response_type in ("run_ack", "run_result", "result", "error"):
        run_id = "Z" * 12
        reason = "run_not_found" if response_type == "error" else "none"
        frame = prefix % (response_type, run_id, "INCONCLUSIVE")
        frame += ",".join(json.dumps(value) for value in names)
        frame += "],\"checks\":[" + ",".join(json.dumps(value) for value in checks)
        frame += "],\"reasons\":[" + ",".join(json.dumps(value) for value in reasons)
        frame += suffix % (metrics["free_heap_bytes"], metrics["ram_bytes_verified"],
                           metrics["imu_samples"], reason)
        encoded = frame.encode("ascii")
        assert len(encoded) <= 1024
        parsed = json.loads(encoded)
        assert parsed["type"] == response_type
        assert parsed["run_id"] == run_id
        assert len(parsed["check_names"]) == len(parsed["checks"]) == len(parsed["reasons"]) == 12
        assert parsed["metrics"] == metrics
        assert parsed["reason"] == reason
