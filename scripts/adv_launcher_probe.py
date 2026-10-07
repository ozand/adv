"""Bounded Launcher queries that emit only validated diagnostic fields."""
import argparse
import re
import time

COMMANDS = ("help", "version", "whoami", "partitions")
MAX_SECONDS = 12
MAX_BYTES = 16384
PARTITION_LINE = re.compile(
    r"^(?P<label>[A-Za-z0-9_-]{1,16})\s+type=(?P<type>app|data)\s+"
    r"subtype=(?P<subtype>[A-Za-z0-9_x-]{1,12})\s+"
    r"offset=(?P<offset>0x[0-9A-Fa-f]{1,8})\s+"
    r"size=(?P<size>0x[0-9A-Fa-f]{1,8})\s+"
    r"\((?P<human>[0-9]{1,8}(?:KB|MB|B))\)(?P<boot>\s+<-- BOOT)?$"
)
VERSION_LINE = re.compile(r"^Launcher\s+([A-Za-z0-9._+-]{1,32})$")
ALLOWED_DEVICE_NAMES = {"M5Stack Cardputer & ADV"}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument(
        "--seconds", type=int, default=12, choices=range(1, MAX_SECONDS + 1)
    )
    return parser.parse_args()


def parse_response(raw):
    """Extract only known, tightly validated Launcher information fields."""
    text = raw.decode("utf-8", errors="replace")
    result = {"version": None, "device": None, "flash": None, "free": None, "partitions": []}
    for line in text.splitlines():
        line = line.strip()
        version = VERSION_LINE.fullmatch(line)
        if version:
            result["version"] = version.group(1)
            continue
        if line in ALLOWED_DEVICE_NAMES:
            result["device"] = line
            continue
        if line.startswith("Flash size: "):
            match = re.fullmatch(r"Flash size: ([0-9]{1,3}MB)", line)
            if match:
                result["flash"] = match.group(1)
            continue
        if line.startswith("<free> "):
            match = re.fullmatch(
                r"<free> offset=0x[0-9A-Fa-f]{1,8} size=0x[0-9A-Fa-f]{1,8} "
                r"\(([0-9]{1,8}(?:KB|MB|B))\)", line
            )
            if match:
                result["free"] = match.group(1)
            continue
        match = PARTITION_LINE.fullmatch(line)
        if match:
            fields = match.groupdict()
            result["partitions"].append(
                {
                    "label": fields["label"],
                    "type": fields["type"],
                    "subtype": fields["subtype"],
                    "offset": fields["offset"],
                    "size": fields["size"],
                    "human_size": fields["human"],
                    "boot_selected": bool(fields["boot"]),
                }
            )
    return result


def format_report(parsed, captured, sent):
    lines = ["Sanitized Launcher probe result"]
    if parsed["version"]:
        lines.append(f"version: {parsed['version']}")
    if parsed["device"]:
        lines.append(f"device: {parsed['device']}")
    if parsed["flash"]:
        lines.append(f"flash: {parsed['flash']}")
    if parsed["free"]:
        lines.append(f"free: {parsed['free']}")
    for item in parsed["partitions"]:
        boot = " (boot selected)" if item["boot_selected"] else ""
        lines.append(
            "partition: {label} type={type} subtype={subtype} offset={offset} "
            "size={size} ({human_size}){boot}".format(**item, boot=boot)
        )
    lines.append(f"captured_bytes: {captured}; allowlisted_commands_sent: {sent}")
    lines.append("unrecognized serial content was suppressed")
    return "\n".join(lines)


def run_probe(serial_port, seconds, clock=time.monotonic, sleeper=time.sleep):
    """Run the finite probe against a serial-like object; caller owns its lifecycle."""
    deadline = clock() + seconds
    output = bytearray()
    sent = 0
    next_send = clock() + 1
    while clock() < deadline and len(output) < MAX_BYTES:
        if sent < len(COMMANDS) and clock() >= next_send:
            serial_port.write((COMMANDS[sent] + "\n").encode("ascii"))
            sent += 1
            next_send = clock() + 2
        chunk = serial_port.read(min(512, MAX_BYTES - len(output)))
        if chunk:
            output.extend(chunk[: MAX_BYTES - len(output)])
        else:
            sleeper(0.01)
    return parse_response(bytes(output)), len(output), sent


def main():
    import serial

    args = parse_args()
    port = serial.Serial(port=None, baudrate=115200, timeout=0.2, write_timeout=1)
    port.dtr = False
    port.rts = False
    port.port = args.port
    try:
        port.open()
        parsed, captured, sent = run_probe(port, args.seconds)
        print(format_report(parsed, captured, sent))
    finally:
        port.close()


if __name__ == "__main__":
    main()
