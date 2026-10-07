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
    try:
        obj = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid_json") from exc
    if not isinstance(obj, dict):
        raise ValueError("invalid_response")
    if obj.get("v") != 1 or obj.get("type") != expected_type:
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
        "reason": {"none", "mount_failed", "unsupported_board", "card_invalid",
                   "path_exists", "create_failed", "write_failed", "read_failed",
                   "verify_failed", "cleanup_failed"},
        "cleanup": {"not_attempted", "removed", "failed", "retained"},
    }
    for key, values in allowed.items():
        if not isinstance(sd.get(key), str) or sd[key] not in values:
            raise ValueError("invalid_sd_status")
    count = sd.get("bytes_verified")
    if type(count) is not int or not 0 <= count <= 65536:
        raise ValueError("invalid_sd_status")
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
        frame = (command + "\n").encode("ascii")
        if len(frame) > MAX_LINE_BYTES:
            raise ValueError("command_too_large")
        if port.write(frame) != len(frame):
            raise OSError("incomplete_command_write")
        deadline = time.monotonic() + (
            SD_RESULT_SECONDS if command == "sd_test" else IDLE_REPLY_SECONDS
        )
        if command == "status":
            result = validate_response(read_line(port, deadline), "status")
            if not result["board_ready"] or not result["imu_ready"]:
                raise ValueError("firmware_not_ready")
            return result
        ack = validate_response(read_line(port, deadline), "sd_test")
        if not ack["board_ready"] or not ack["imu_ready"]:
            raise ValueError("firmware_not_ready")
        if ack["sd"]["reason"] == "not_ready":
            return ack
        if ack["sd"]["state"] in {"pass", "fail"}:
            return ack
        if ack["sd"]["state"] != "running":
            raise ValueError("invalid_sd_ack")
        result = validate_response(read_line(port, deadline), "sd_test_result")
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
            "incomplete_command_write",
        } else "serial_error_or_indeterminate"
        print(json.dumps({"ok": False, "error": code}, separators=(",", ":")))
        return 2
    print(json.dumps({"ok": True, "result": result}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
