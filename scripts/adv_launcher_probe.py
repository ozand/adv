"""Bounded, allowlisted read-only Launcher information queries."""
import argparse
import re
import time

import serial

COMMANDS = ("help", "version", "whoami", "partitions")
MAX_SECONDS = 12
MAX_BYTES = 16384


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--seconds", type=int, default=12, choices=range(1, MAX_SECONDS + 1))
    return parser.parse_args()


def redact(text):
    text = re.sub(r"(?i)(password|passwd|token|api[_ -]?key|ssid)\s*[:=]\s*\S+", r"\1=[REDACTED]", text)
    text = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP]", text)
    return re.sub(r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", "[MAC]", text)


def main():
    args = parse_args()
    port = serial.Serial(port=None, baudrate=115200, timeout=0.2, write_timeout=1)
    port.dtr = False
    port.rts = False
    port.port = args.port
    try:
        port.open()
        deadline = time.monotonic() + args.seconds
        output = bytearray()
        sent = 0
        next_send = time.monotonic() + 1
        while time.monotonic() < deadline and len(output) < MAX_BYTES:
            if sent < len(COMMANDS) and time.monotonic() >= next_send:
                port.write((COMMANDS[sent] + "\n").encode("ascii"))
                sent += 1
                next_send = time.monotonic() + 2
            output.extend(port.read(min(512, MAX_BYTES - len(output))))
        print(redact(output.decode("utf-8", errors="replace")))
        print(f"Captured {len(output)} bytes; sent {sent} allowlisted information commands.")
    finally:
        port.close()


if __name__ == "__main__":
    main()
