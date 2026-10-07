"""Sanitized bounded host client for the ADV hardware-check JSON protocol."""
from __future__ import annotations

import argparse
import json
import sys
import time
from types import SimpleNamespace
from typing import Any

try:
    import serial
except ImportError:  # Allows protocol tests without installing host dependencies.
    serial = SimpleNamespace(Serial=None)

PROTOCOL_BUILD = "adv-diagnostic-1"
MAX_RESPONSE_BYTES = 512
MAX_LINE_BYTES = 64
IDLE_REPLY_SECONDS = 3
SD_RESULT_SECONDS = 40
IO_OPERATION_SECONDS = 0.5


def read_line(port: Any, deadline: float) -> bytes:
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
        if len(data) > MAX_RESPONSE_BYTES:
            raise ValueError("response_too_large")
    raise TimeoutError("response_timeout")


def validate_response(raw: bytes, expected_type: str) -> dict[str, Any]:
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
    if obj.get("firmware_build") != PROTOCOL_BUILD:
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


def run(port_name: str, command: str) -> dict[str, Any]:
    """Perform exactly one bounded request; never retry an uncertain SD test."""
    if command not in {"status", "sd_test"}:
        raise ValueError("invalid_command")
    if serial.Serial is None:
        raise RuntimeError("pyserial_required")
    port = serial.Serial(port=None, baudrate=115200, timeout=0.1, write_timeout=1)
    port.dtr = False
    port.rts = False
    port.port = port_name
    try:
        port.open()
        status_frame = b"status\n"
        if len(status_frame) > MAX_LINE_BYTES:
            raise ValueError("command_too_large")
        if port.write(status_frame) != len(status_frame):
            raise OSError("incomplete_command_write")
        deadline = time.monotonic() + IDLE_REPLY_SECONDS
        status = validate_response(read_line(port, deadline), "status")
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
        if port.write(sd_frame) != len(sd_frame):
            raise OSError("incomplete_command_write")
        deadline = time.monotonic() + SD_RESULT_SECONDS
        ack = validate_response(read_line(port, deadline), "sd_test")
        if ack["type"] == "error":
            return ack
        if not ack["board_ready"] or not ack["imu_ready"]:
            raise ValueError("firmware_not_ready")
        if ack["sd"]["state"] in {"pass", "fail"}:
            raise ValueError("invalid_sd_ack")
        if ack["sd"]["state"] != "running":
            raise ValueError("invalid_sd_ack")
        result = validate_response(read_line(port, deadline), "sd_test_result")
        if result["type"] == "error":
            return result
        if result["sd"]["state"] == "pass" and result["sd"]["cleanup"] == "failed":
            raise ValueError("cleanup_failed")
        if not result["board_ready"] or not result["imu_ready"]:
            raise ValueError("firmware_not_ready")
        if result["sd"]["state"] not in {"pass", "fail"}:
            raise ValueError("invalid_sd_result")
        return result
    finally:
        port.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--command", choices=("status", "sd_test"), required=True)
    args = parser.parse_args()
    try:
        result = run(args.port, args.command)
    except (OSError, TimeoutError, ValueError, RuntimeError) as exc:
        code = str(exc) if str(exc) in {
            "response_timeout", "response_too_large", "invalid_json", "invalid_response",
            "protocol_mismatch", "firmware_mismatch", "unexpected_fields", "invalid_status",
            "invalid_sd_status", "invalid_sd_ack", "invalid_sd_result", "firmware_not_ready",
            "invalid_command", "command_too_large",
            "incomplete_command_write", "cleanup_failed", "invalid_cached_terminal",
        } else "serial_error_or_indeterminate"
        print(json.dumps({"ok": False, "error": code}, separators=(",", ":")))
        return 2
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
