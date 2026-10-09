"""Sanitized bounded host client for the ADV hardware-check JSON protocol."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from types import SimpleNamespace
from typing import Any

try:
    import serial
except ImportError:  # Allows protocol tests without installing host dependencies.
    serial = SimpleNamespace(Serial=None)

LEGACY_BUILD = "adv-diagnostic-1"
CURRENT_BUILD = "adv-diagnostic-2"
AUDIO_BUILD = "adv-diagnostic-3-audio-proposal"
MAX_AUDIO_FRAME_BYTES = 256
AUDIO_TIMEOUT_SECONDS = 20
PROTOCOL_BUILD = LEGACY_BUILD
RUN_CHECKS = (
    "mcu", "ram_scratch", "imu_data", "motion", "display", "keyboard",
    "audio", "ir", "radio", "battery", "connectors", "sd",
)
REPORT_ONLY_CHECKS = (
    "usb_transport", "flash_health", "gnss", "lora",
    "microphone", "speaker", "headphones",
)
RUN_STATES = {"PASS", "FAIL", "NOT_TESTED", "INCONCLUSIVE"}
RUN_REASONS = {
    "none", "owner_observation_required", "unavailable", "not_requested",
    "nonfinite_sample", "pattern_mismatch", "unsupported_board", "imu_unavailable",
    "run_id_busy", "run_not_found", "invalid_id", "not_ready", "invalid_command",
    "accessory_unknown",
}
RUN_ID_PATTERN = re.compile(r"[A-Z0-9]{1,12}\Z")
MAX_RESPONSE_BYTES = 1024
MAX_V1_RESPONSE_BYTES = 512
RUN_TIMEOUT_SECONDS = 20
MAX_LINE_BYTES = 64
IDLE_REPLY_SECONDS = 3
SD_RESULT_SECONDS = 40
IO_OPERATION_SECONDS = 0.5


def read_line(port: Any, deadline: float, *, max_bytes: int = MAX_V1_RESPONSE_BYTES) -> bytes:
    """Read one bounded newline frame before the monotonic deadline."""
    data = bytearray()
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        port.timeout = min(IO_OPERATION_SECONDS, remaining)
        part = port.read(1)
        if not part:
            continue
        if part == b"\n":
            return bytes(data).removesuffix(b"\r")
        data.extend(part)
        if len(data) > max_bytes:
            raise ValueError("response_too_large")
    raise TimeoutError("response_timeout")


def validate_response(
    raw: bytes, expected_type: str, *, allowed_builds: set[str] | None = None
) -> dict[str, Any]:
    """Parse only the exact bounded JSON schema; never return raw serial text."""
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        parsed: dict[str, Any] = {}
        for key, value in pairs:
            if key in parsed:
                raise ValueError("duplicate_json_key")
            parsed[key] = value
        return parsed

    def reject_nonfinite(value: str) -> None:
        raise ValueError("invalid_json_number")

    if len(raw) > MAX_V1_RESPONSE_BYTES:
        raise ValueError("response_too_large")
    try:
        obj = json.loads(
            raw.decode("ascii"), object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid_json") from exc
    if not isinstance(obj, dict):
        raise ValueError("invalid_response")
    if obj.get("v") != 1 or obj.get("type") not in {expected_type, "error"}:
        raise ValueError("protocol_mismatch")
    default_builds = {LEGACY_BUILD, CURRENT_BUILD}
    if expected_type == "status":
        default_builds.add(AUDIO_BUILD)
    if obj.get("firmware_build") not in (allowed_builds or default_builds):
        raise ValueError("firmware_mismatch")
    if set(obj) != {"v", "type", "firmware_build", "board_ready", "imu_ready", "sd"}:
        raise ValueError("unexpected_fields")
    if type(obj["board_ready"]) is not bool or type(obj["imu_ready"]) is not bool:
        raise ValueError("invalid_status")
    sd = obj["sd"]
    if not isinstance(sd, dict) or set(sd) != {
        "state", "stage", "reason", "bytes_verified", "cleanup"
    }:
        raise ValueError("invalid_sd_status")
    allowed = {
        "state": {"not_run", "running", "pass", "fail"},
        "stage": {"idle", "mount", "write", "read", "cleanup", "complete", "error"},
        "reason": {"none", "invalid_command", "not_ready", "unsupported_pin_map",
                   "mount_failed", "invalid_or_small", "test_path_exists", "create_failed",
                   "write_failed_or_timeout", "read_open_or_size_failed",
                   "read_failed_or_timeout", "verify_mismatch", "verify_failed_or_timeout"},
        "cleanup": {"not_attempted", "removed", "failed", "retained"},
    }
    for key, values in allowed.items():
        if not isinstance(sd.get(key), str) or sd[key] not in values:
            raise ValueError("invalid_sd_status")
    count = sd.get("bytes_verified")
    if type(count) is not int or not 0 <= count <= 65536:
        raise ValueError("invalid_sd_status")
    if obj["type"] == "error":
        if sd["reason"] not in {"invalid_command", "not_ready"}:
            raise ValueError("invalid_error_reason")
    elif sd["reason"] in {"invalid_command", "not_ready"}:
        raise ValueError("invalid_error_reason")
    if sd["state"] == "pass" and not (
        sd["stage"] == "complete" and sd["reason"] == "none"
        and sd["bytes_verified"] == 65536
        and sd["cleanup"] in {"removed", "failed"}
    ):
        raise ValueError("inconsistent_sd_result")
    return obj


def validate_run_response(
    raw: bytes, expected_type: str, expected_id: str
) -> dict[str, Any]:
    """Validate a fixed v2 run envelope and its bounded check arrays."""
    def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = value
        return result

    def reject_nonfinite(value: str) -> None:
        raise ValueError("invalid_json_number")

    if len(raw) > MAX_RESPONSE_BYTES:
        raise ValueError("response_too_large")
    try:
        obj = json.loads(
            raw.decode("ascii"), object_pairs_hook=reject_pairs,
            parse_constant=reject_nonfinite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        if str(exc) in {"duplicate_json_key", "invalid_json_number"}:
            raise ValueError(str(exc)) from exc
        raise ValueError("invalid_json") from exc
    fields = {"v", "type", "firmware_build", "run_id", "overall", "check_names", "checks", "reasons", "metrics", "reason"}
    if not isinstance(obj, dict) or set(obj) != fields:
        raise ValueError("unexpected_run_fields")
    allowed_types = {expected_type, "error"}
    if expected_type == "run_ack":
        allowed_types.update({"run_result", "result"})
    if obj["v"] != 2 or obj["type"] not in allowed_types:
        raise ValueError("run_protocol_mismatch")
    if obj["firmware_build"] != CURRENT_BUILD:
        raise ValueError("firmware_mismatch")
    if obj["type"] == "error":
        valid_error_id = (
            obj["reason"] == "invalid_id" and obj["run_id"] == ""
        ) or (
            obj["reason"] != "invalid_id" and obj["run_id"] == expected_id
        )
        if not valid_error_id:
            raise ValueError("run_id_mismatch")
    elif obj["run_id"] != expected_id:
        raise ValueError("run_id_mismatch")
    if not isinstance(obj["overall"], str) or obj["overall"] not in RUN_STATES:
        raise ValueError("invalid_run_overall")
    if obj["type"] == "error" and obj["reason"] not in {
        "invalid_id", "run_id_busy", "run_not_found", "not_ready", "invalid_command"
    }:
        raise ValueError("invalid_run_error")
    if obj["check_names"] != list(RUN_CHECKS):
        raise ValueError("invalid_run_check_names")
    checks, reasons = obj["checks"], obj["reasons"]
    if not isinstance(checks, list) or len(checks) != 12 or any(x not in RUN_STATES for x in checks):
        raise ValueError("invalid_run_checks")
    if not isinstance(reasons, list) or len(reasons) != 12 or any(x not in RUN_REASONS for x in reasons):
        raise ValueError("invalid_run_reasons")
    metrics = obj["metrics"]
    if not isinstance(metrics, dict) or set(metrics) != {"free_heap_bytes", "ram_bytes_verified", "imu_samples"}:
        raise ValueError("invalid_run_metrics")
    bounds = {"free_heap_bytes": 0xFFFFFFFF, "ram_bytes_verified": 256, "imu_samples": 8}
    if any(type(metrics[k]) is not int or not 0 <= metrics[k] <= limit for k, limit in bounds.items()):
        raise ValueError("invalid_run_metrics")
    if obj["reason"] not in RUN_REASONS:
        raise ValueError("invalid_run_reason")
    if obj["type"] != "error" and obj["reason"] != "none":
        raise ValueError("invalid_run_reason")
    if obj["type"] == "run_ack" and obj["overall"] != "INCONCLUSIVE":
        raise ValueError("invalid_run_ack")
    if obj["type"] == "run_result" and obj["run_id"] != expected_id:
        raise ValueError("run_id_mismatch")
    if obj["type"] in {"run_result", "result"}:
        expected_overall = (
            "FAIL" if "FAIL" in checks
            else "INCONCLUSIVE" if any(state in {"NOT_TESTED", "INCONCLUSIVE"} for state in checks)
            else "PASS"
        )
        if obj["overall"] != expected_overall:
            raise ValueError("inconsistent_run_overall")
    return obj


def run_v2(
    port: Any, command: str, run_id: str, trace: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Send one run or read-only result command; never retry a run."""
    if command not in {"run", "result"} or not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("invalid_run_id")
    frame = f"{command} {run_id}\n".encode("ascii")
    phase = "run" if command == "run" else "result"
    if trace is not None:
        trace["phase"] = f"{phase}_write"
        trace[f"{phase}_write_attempted"] = True
    if len(frame) > MAX_LINE_BYTES or port.write(frame) != len(frame):
        raise ValueError("run_command_write_failed")
    if trace is not None:
        trace[f"{phase}_write_returned_full_length"] = True
        trace["phase"] = f"{phase}_response"
    deadline = time.monotonic() + RUN_TIMEOUT_SECONDS
    first = validate_run_response(read_line(port, deadline, max_bytes=MAX_RESPONSE_BYTES), "run_ack" if command == "run" else "result", run_id)
    if first["type"] == "error":
        if first["reason"] == "run_id_busy":
            raise ValueError("run_id_busy")
        return first
    if command == "result":
        return first
    if first["type"] in {"run_result", "result"}:
        return first
    if first["type"] != "run_ack":
        raise ValueError("invalid_run_ack")
    if trace is not None:
        trace["phase"] = "run_result_response"
    return validate_run_response(read_line(port, deadline, max_bytes=MAX_RESPONSE_BYTES), "run_result", run_id)


def build_report(
    run_result: dict[str, Any], sd_result: dict[str, Any] | None,
    *, usb_handshake: bool = False,
) -> dict[str, Any]:
    """Expose fixed check names and coverage counts without upgrading evidence."""
    failed_lookup = run_result.get("type") == "error"
    checks = (
        ["INCONCLUSIVE"] * len(RUN_CHECKS) if failed_lookup
        else run_result.get("checks", ["NOT_TESTED"] * len(RUN_CHECKS))
    )
    reasons = (
        [run_result.get("reason", "run_not_found")] * len(RUN_CHECKS) if failed_lookup
        else run_result.get("reasons", ["run_not_found"] * len(RUN_CHECKS))
    )
    named_checks = [
        {"name": name, "status": checks[i], "reason": reasons[i]}
        for i, name in enumerate(RUN_CHECKS)
    ] if len(checks) == len(RUN_CHECKS) and len(reasons) == len(RUN_CHECKS) else [
        {"name": name, "status": "INCONCLUSIVE", "reason": "run_not_found"}
        for name in RUN_CHECKS
    ]
    report_only = [
        {"name": name, "status": "NOT_TESTED", "reason": reason}
        for name, reason in zip(REPORT_ONLY_CHECKS, (
            "not_independently_tested", "firmware_reports_metadata_only",
            "unknown_module", "unknown_module", "not_independently_tested",
            "not_independently_tested", "not_independently_tested",
        ))
    ]
    usb_status, usb_reason = (
        ("PASS", "status_handshake_succeeded") if usb_handshake
        else ("INCONCLUSIVE", "handshake_not_completed")
    )
    report_only[0] = {"name": "usb_transport", "status": usb_status, "reason": usb_reason}
    named_checks.extend(report_only)
    coverage = {state.lower(): sum(item["status"] == state for item in named_checks) for state in RUN_STATES}
    return {
        "run_id": run_result.get("run_id"),
        "overall": run_result.get("overall", "INCONCLUSIVE"),
        "checks": named_checks,
        "coverage": coverage,
        "metrics": run_result.get("metrics", {}),
        "error": run_result.get("reason") if run_result.get("type") == "error" else None,
        "sd_test": sd_result,
    }


def run_full_port(
    port: Any, run_id: str, with_sd: bool = False,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Handshake, run v2 checks once, then optionally report separate cached SD evidence."""
    status_frame = b"status\n"
    if trace is not None:
        trace["phase"] = "status_write"
        trace["status_write_attempted"] = True
    if port.write(status_frame) != len(status_frame):
        raise OSError("incomplete_command_write")
    if trace is not None:
        trace["status_write_returned_full_length"] = True
        trace["phase"] = "status_response"
    status = validate_response(
        read_line(port, time.monotonic() + IDLE_REPLY_SECONDS), "status",
        allowed_builds={CURRENT_BUILD},
    )
    if status["type"] == "error" or not status["board_ready"] or not status["imu_ready"]:
        raise ValueError("firmware_not_ready")
    run_result = run_v2(port, "run", run_id, trace=trace)
    sd_result = (
        run_v1(port, "sd_test", allowed_builds={CURRENT_BUILD}, trace=trace)
        if with_sd and run_result["type"] != "error" else None
    )
    return build_report(run_result, sd_result, usb_handshake=True)


def open_port(port_name: str) -> Any:
    if serial.Serial is None:
        raise RuntimeError("pyserial_required")
    port = serial.Serial(port=None, baudrate=115200, timeout=0.1, write_timeout=1)
    port.dtr = False
    port.rts = False
    port.port = port_name
    port.open()
    return port


def run_v1(
    port: Any, command: str, *, allowed_builds: set[str] | None = None,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Perform one v1 operation on an already-open serial port."""
    if command not in {"status", "sd_test"}:
        raise ValueError("invalid_command")
    status_frame = b"status\n"
    if len(status_frame) > MAX_LINE_BYTES:
        raise ValueError("command_too_large")
    status_phase = "sd_status" if command == "sd_test" else "status"
    if trace is not None:
        trace["phase"] = f"{status_phase}_write"
        trace["status_write_attempted"] = True
    if port.write(status_frame) != len(status_frame):
        raise OSError("incomplete_command_write")
    if trace is not None:
        trace["status_write_returned_full_length"] = True
        trace["phase"] = f"{status_phase}_response"
    deadline = time.monotonic() + IDLE_REPLY_SECONDS
    builds = allowed_builds or {LEGACY_BUILD, CURRENT_BUILD}
    status = validate_response(read_line(port, deadline), "status", allowed_builds=builds)
    if status["type"] == "error":
        return status
    if command == "status":
        if not status["board_ready"] or not status["imu_ready"]:
            raise ValueError("firmware_not_ready")
        return status
    if not status["board_ready"] or not status["imu_ready"]:
        raise ValueError("firmware_not_ready")
    if status["sd"]["state"] in {"pass", "fail"}:
        if status["type"] != "status":
            raise ValueError("invalid_cached_terminal")
        return status
    sd_frame = b"sd_test\n"
    if len(sd_frame) > MAX_LINE_BYTES:
        raise ValueError("command_too_large")
    if trace is not None:
        trace["phase"] = "sd_test_write"
        trace["sd_test_write_attempted"] = True
    if port.write(sd_frame) != len(sd_frame):
        raise OSError("incomplete_command_write")
    if trace is not None:
        trace["sd_test_write_returned_full_length"] = True
        trace["phase"] = "sd_test_response"
    deadline = time.monotonic() + SD_RESULT_SECONDS
    ack = validate_response(read_line(port, deadline), "sd_test", allowed_builds=builds)
    if ack["type"] == "error":
        return ack
    if not ack["board_ready"] or not ack["imu_ready"]:
        raise ValueError("firmware_not_ready")
    if ack["sd"]["state"] in {"pass", "fail"} or ack["sd"]["state"] != "running":
        raise ValueError("invalid_sd_ack")
    result = validate_response(read_line(port, deadline), "sd_test_result", allowed_builds=builds)
    if result["type"] == "error":
        return result
    if result["sd"]["state"] == "pass" and result["sd"]["cleanup"] == "failed":
        raise ValueError("cleanup_failed")
    if not result["board_ready"] or not result["imu_ready"]:
        raise ValueError("firmware_not_ready")
    if result["sd"]["state"] not in {"pass", "fail"}:
        raise ValueError("invalid_sd_result")
    return result


def run(
    port_name: str, command: str, trace: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Open a bounded serial session for one status or explicit SD command."""
    if serial.Serial is None:
        raise RuntimeError("pyserial_required")
    port = serial.Serial(port=None, baudrate=115200, timeout=0.1, write_timeout=1)
    port.dtr = False
    port.rts = False
    port.port = port_name
    try:
        port.open()
        return run_v1(port, command, trace=trace)
    finally:
        port.close()


def build_error_report(
    error: str, run_id: str | None, execution: dict[str, Any]
) -> dict[str, Any]:
    """Return sanitized command-phase flags without retaining serial bytes."""
    report: dict[str, Any] = {"ok": False, "error": error}
    if run_id and RUN_ID_PATTERN.fullmatch(run_id):
        report["run_id"] = run_id
        report["execution"] = dict(execution)
    return report


AUDIO_REASONS = {
    "none", "not_ready", "audio_busy", "run_id_busy", "run_not_found",
    "unsupported_board", "begin_failed", "record_failed", "capture_timeout",
    "cleanup_unknown", "zero_signal", "owner_observation_required", "invalid_command",
    "play_failed", "playback_timeout",
}
AUDIO_STATES = {"NOT_TESTED", "PASS", "FAIL", "INCONCLUSIVE"}
AUDIO_CLEANUP = {
    "mic_test": {"not_attempted", "quiescent", "unknown"},
    "tone_test": {"not_attempted", "software_stopped_codec_unknown", "unknown"},
}
AUDIO_RESULT_PAIRS = {
    "mic_test": {
        ("unsupported_board", "not_attempted"), ("not_ready", "not_attempted"),
        ("audio_busy", "not_attempted"), ("begin_failed", "quiescent"),
        ("record_failed", "quiescent"), ("capture_timeout", "quiescent"),
        ("cleanup_unknown", "unknown"), ("zero_signal", "quiescent"),
        ("owner_observation_required", "quiescent"),
    },
    "tone_test": {
        ("unsupported_board", "not_attempted"), ("not_ready", "not_attempted"),
        ("audio_busy", "not_attempted"),
        ("play_failed", "software_stopped_codec_unknown"),
        ("playback_timeout", "software_stopped_codec_unknown"),
        ("cleanup_unknown", "unknown"),
        ("owner_observation_required", "software_stopped_codec_unknown"),
    },
}
AUDIO_ERROR_PAIRS = {
    "mic_test": {
        ("invalid_command", "not_attempted"), ("not_ready", "not_attempted"),
        ("audio_busy", "not_attempted"), ("run_id_busy", "not_attempted"),
        ("run_not_found", "not_attempted"), ("unsupported_board", "not_attempted"),
    },
    "tone_test": {
        ("invalid_command", "not_attempted"), ("not_ready", "not_attempted"),
        ("audio_busy", "not_attempted"), ("run_id_busy", "not_attempted"),
        ("run_not_found", "not_attempted"), ("unsupported_board", "not_attempted"),
    },
    "unknown": {("invalid_command", "not_attempted")},
}
AUDIO_COMMANDS = {"mic_test", "mic_result", "tone_test", "tone_result"}


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for key, value in pairs:
        if key in parsed:
            raise ValueError("duplicate_json_key")
        parsed[key] = value
    return parsed


def _reject_nonfinite_json_number(value: str) -> None:
    raise ValueError("invalid_json_number")


def _audio_family(command: str) -> str:
    return "mic_test" if command.startswith("mic_") else "tone_test"


def validate_audio_status(raw: bytes) -> dict[str, Any]:
    """Strictly validate read-only status before any audio command write."""
    if len(raw) > MAX_V1_RESPONSE_BYTES:
        raise ValueError("response_too_large")
    try:
        status = json.loads(
            raw.decode("ascii"), object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite_json_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        if str(exc) in {"duplicate_json_key", "invalid_json_number"}:
            raise ValueError(str(exc)) from exc
        raise ValueError("invalid_json") from exc
    if not isinstance(status, dict) or set(status) != {
        "v", "type", "firmware_build", "board_ready", "imu_ready", "sd"
    }:
        raise ValueError("invalid_audio_status")
    if type(status["v"]) is not int or status["v"] != 1:
        raise ValueError("invalid_audio_status")
    if status["type"] not in {"status", "error"}:
        raise ValueError("invalid_audio_status")
    if status["firmware_build"] != AUDIO_BUILD:
        raise ValueError("firmware_mismatch")
    if status["type"] != "status":
        raise ValueError("invalid_audio_status")
    if type(status["board_ready"]) is not bool or type(status["imu_ready"]) is not bool:
        raise ValueError("invalid_status")
    sd = status["sd"]
    if not isinstance(sd, dict) or set(sd) != {
        "state", "stage", "reason", "bytes_verified", "cleanup"
    }:
        raise ValueError("invalid_sd_status")
    if any(type(sd[key]) is not str for key in ("state", "stage", "reason", "cleanup")):
        raise ValueError("invalid_sd_status")
    if type(sd["bytes_verified"]) is not int or not 0 <= sd["bytes_verified"] <= 65536:
        raise ValueError("invalid_sd_status")
    status = validate_response(raw, "status", allowed_builds={AUDIO_BUILD})
    if not status["board_ready"] or not status["imu_ready"]:
        raise ValueError("firmware_not_ready")
    return status


def validate_audio_response(
    raw: bytes, command: str, operation_id: str
) -> dict[str, Any]:
    """Validate one bounded, operation-specific audio result without raw samples."""
    if command not in AUDIO_COMMANDS:
        raise ValueError("invalid_audio_command")
    if not RUN_ID_PATTERN.fullmatch(operation_id):
        raise ValueError("invalid_run_id")
    if len(raw) + 2 > MAX_AUDIO_FRAME_BYTES:
        raise ValueError("response_too_large")
    try:
        obj = json.loads(
            raw.decode("ascii"), object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite_json_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        if str(exc) in {"duplicate_json_key", "invalid_json_number"}:
            raise ValueError(str(exc)) from exc
        raise ValueError("invalid_json") from exc
    if (
        not isinstance(obj, dict)
        or type(obj.get("v")) is not int
        or obj["v"] != 1
        or obj.get("firmware_build") != AUDIO_BUILD
    ):
        raise ValueError("audio_protocol_mismatch")
    family = _audio_family(command)
    if obj.get("type") == "error":
        fields = {
            "v", "type", "firmware_build", "operation", "operation_id",
            "state", "reason", "cleanup",
        }
        if set(obj) != fields or obj["operation"] not in {"mic_test", "tone_test", "unknown"}:
            raise ValueError("unexpected_audio_fields")
        if obj["operation_id"] != ("" if obj["reason"] == "invalid_command" else operation_id):
            raise ValueError("audio_id_mismatch")
    else:
        fields = {
            "v", "type", "firmware_build", "operation_id", "state", "reason",
            "cleanup",
        }
        if family == "mic_test":
            fields.update({"mic_rms", "mic_peak"})
        if set(obj) != fields or obj["type"] != family:
            raise ValueError("unexpected_audio_fields")
        if obj["operation_id"] != operation_id:
            raise ValueError("audio_id_mismatch")
    if obj.get("state") not in AUDIO_STATES:
        raise ValueError("invalid_audio_state")
    if obj.get("reason") not in AUDIO_REASONS:
        raise ValueError("invalid_audio_reason")
    cleanup_operation = obj.get("operation", family)
    cleanup_family = cleanup_operation if cleanup_operation in AUDIO_CLEANUP else family
    if obj.get("cleanup") not in AUDIO_CLEANUP[cleanup_family]:
        raise ValueError("invalid_audio_cleanup")
    if obj["state"] != "INCONCLUSIVE":
        raise ValueError("invalid_audio_state")
    result_family = obj.get("operation", family) if obj["type"] == "error" else family
    if obj["type"] == "error":
        if (obj["reason"], obj["cleanup"]) not in AUDIO_ERROR_PAIRS[result_family]:
            raise ValueError("invalid_audio_reason")
    elif (obj["reason"], obj["cleanup"]) not in AUDIO_RESULT_PAIRS[family]:
        raise ValueError("invalid_audio_reason")
    if obj["type"] != "error" and family == "mic_test":
        if obj["reason"] in {"unsupported_board", "not_ready", "audio_busy",
                              "begin_failed", "record_failed", "capture_timeout",
                              "cleanup_unknown", "zero_signal"} and (
            obj["mic_rms"] != 0 or obj["mic_peak"] != 0
        ):
            raise ValueError("invalid_audio_metrics")
        if type(obj["mic_rms"]) is not int or not 0 <= obj["mic_rms"] <= 32768:
            raise ValueError("invalid_audio_metrics")
        if type(obj["mic_peak"]) is not int or not 0 <= obj["mic_peak"] <= 32768:
            raise ValueError("invalid_audio_metrics")
        if obj["mic_rms"] > obj["mic_peak"]:
            raise ValueError("invalid_audio_metrics")
    return obj


def run_audio_port(
    port: Any, command: str, operation_id: str,
    trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Handshake read-only, then send one explicit audio request at most once."""
    if command not in AUDIO_COMMANDS:
        raise ValueError("invalid_audio_command")
    if not RUN_ID_PATTERN.fullmatch(operation_id):
        raise ValueError("invalid_run_id")
    if trace is not None:
        trace["phase"] = "status_write"
        trace["status_write_attempted"] = True
    if port.write(b"status\n") != len(b"status\n"):
        raise OSError("incomplete_command_write")
    if trace is not None:
        trace["status_write_returned_full_length"] = True
        trace["phase"] = "status_response"
    validate_audio_status(read_line(port, time.monotonic() + IDLE_REPLY_SECONDS))
    frame = f"{command} {operation_id}\n".encode("ascii")
    if len(frame) > MAX_LINE_BYTES:
        raise ValueError("command_too_large")
    if trace is not None:
        trace["phase"] = f"{command}_write"
        trace["audio_write_attempted"] = True
    if port.write(frame) != len(frame):
        raise OSError("audio_command_write_failed")
    if trace is not None:
        trace["audio_write_returned_full_length"] = True
        trace["phase"] = f"{command}_response"
    raw = read_line(
        port, time.monotonic() + AUDIO_TIMEOUT_SECONDS,
        max_bytes=MAX_AUDIO_FRAME_BYTES - 2,
    )
    return validate_audio_response(raw, command, operation_id)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument(
        "--command",
        choices=(
            "status", "sd_test", "run", "result", "mic_test", "mic_result",
            "tone_test", "tone_result",
        ),
        required=True,
    )
    parser.add_argument("--run-id")
    parser.add_argument("--with-sd", action="store_true")
    args = parser.parse_args()
    if args.with_sd and args.command != "run":
        parser.error("--with-sd is valid only with --command run")
    if args.command in AUDIO_COMMANDS and args.with_sd:
        parser.error("--with-sd cannot be combined with audio commands")
    try:
        trace = {
            "phase": "validation",
            "status_write_attempted": False,
            "status_write_returned_full_length": False,
            "run_write_attempted": False,
            "run_write_returned_full_length": False,
            "result_write_attempted": False,
            "result_write_returned_full_length": False,
            "sd_test_write_attempted": False,
            "sd_test_write_returned_full_length": False,
            "audio_write_attempted": False,
            "audio_write_returned_full_length": False,
        }
        if args.command in {"run", "result"}:
            if not args.run_id or not RUN_ID_PATTERN.fullmatch(args.run_id):
                raise ValueError("invalid_run_id")
            port = open_port(args.port)
            try:
                if args.command == "result":
                    result = build_report(run_v2(port, "result", args.run_id, trace=trace), None)
                else:
                    result = run_full_port(port, args.run_id, with_sd=args.with_sd, trace=trace)
            finally:
                port.close()
        elif args.command in AUDIO_COMMANDS:
            if not args.run_id or not RUN_ID_PATTERN.fullmatch(args.run_id):
                raise ValueError("invalid_run_id")
            port = open_port(args.port)
            try:
                result = run_audio_port(port, args.command, args.run_id, trace=trace)
            finally:
                port.close()
        else:
            result = run(args.port, args.command, trace=trace)
    except (OSError, TimeoutError, ValueError, RuntimeError) as exc:
        code = str(exc) if str(exc) in {
            "response_timeout", "response_too_large", "invalid_json", "invalid_response",
            "protocol_mismatch", "firmware_mismatch", "unexpected_fields", "invalid_status",
            "invalid_sd_status", "invalid_sd_ack", "invalid_sd_result", "firmware_not_ready",
            "invalid_command", "command_too_large",
            "incomplete_command_write", "cleanup_failed", "invalid_cached_terminal",
            "invalid_run_id", "run_command_write_failed", "run_protocol_mismatch",
            "unexpected_run_fields", "run_id_mismatch", "invalid_run_overall",
            "invalid_run_checks", "invalid_run_reasons", "invalid_run_metrics",
            "invalid_run_reason", "invalid_run_error", "invalid_run_ack",
            "inconsistent_run_overall", "run_id_busy", "invalid_audio_command",
            "invalid_audio_status", "audio_protocol_mismatch", "unexpected_audio_fields",
            "audio_id_mismatch", "invalid_audio_state", "invalid_audio_reason",
            "invalid_audio_cleanup", "invalid_audio_metrics", "audio_command_write_failed",
        } else "serial_error_or_indeterminate"
        print(json.dumps(build_error_report(code, args.run_id, trace), separators=(",", ":")))
        return 2
    if isinstance(result, dict) and result.get("type") in {"mic_test", "tone_test", "error"}:
        print(json.dumps({"ok": False, "result": result}, separators=(",", ":")))
        return 2
    if isinstance(result, dict) and "checks" in result and "coverage" in result:
        overall_ok = result["overall"] == "PASS"
        sd_result = result["sd_test"]
        if sd_result and (sd_result.get("type") == "error" or sd_result["sd"]["state"] != "pass" or sd_result["sd"]["cleanup"] != "removed"):
            print(json.dumps({"ok": False, "error": "sd_test_not_passed", "result": result}, separators=(",", ":")))
            return 2
        print(json.dumps({"ok": overall_ok, "result": result}, separators=(",", ":")))
        return 0 if overall_ok else 2
    if result["type"] == "error":
        print(json.dumps(
            {"ok": False, "error": result["sd"]["reason"], "result": result},
            separators=(",", ":"),
        ))
        return 2
    if result["sd"]["state"] == "pass" and result["sd"]["cleanup"] == "failed":
        print(json.dumps(
            {"ok": False, "error": "cleanup_failed", "result": result},
            separators=(",", ":"),
        ))
        return 2
    print(json.dumps({"ok": True, "result": result}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
