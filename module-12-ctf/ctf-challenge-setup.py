#!/usr/bin/env python3
"""
CTF Challenge Setup Script

Configures a BleuIO dongle as the challenge server for CTF lessons 12.2 through
12.6. Students run this script instead of pasting raw AT commands so that hex
encoded flag values never appear on their screen, which would spoil the
challenge for hex literate students.

Usage:
    python3 scripts/ctf-challenge-setup.py <challenge_number> [--port PORT]

Examples:
    python3 scripts/ctf-challenge-setup.py 2
    python3 scripts/ctf-challenge-setup.py 3 --port /dev/cu.usbmodem4048FDEAED1A1

After the script finishes, unplug and replug the dongle (or send ATR) so the
AUTOEXEC commands run on boot. Do not open a serial terminal on the challenge
server dongle after rebooting.
"""

import argparse
import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("ERROR: pyserial is not installed. Install it with: pip install pyserial")
    sys.exit(1)


BAUD = 57600
TIMEOUT = 2


# Challenge titles (safe to display).
CHALLENGE_TITLES = {
    2: "Hidden Device",
    3: "GATT Treasure Hunt",
    4: "Crack the Code",
    5: "The Whisper",
    6: "The Impostor",
}


# AUTOEXEC command lists pulled directly from docs/ctf-challenge-design.md.
# These are intentionally kept inside function scope so the hex bytes are not
# printed or dumped in help output.

def _commands_challenge_2():
    # AT+ADVDATA requires colon-separated hex; bare hex returns ERROR.
    return [
        "AT+AUTOEXEC=AT+PERIPHERAL",
        "AT+AUTOEXEC=AT+ADVDATA=07:09:53:68:61:64:6F:77:12:FF:00:59:46:4C:41:47:7B:52:46:5F:48:55:4E:54:45:52:7D",
        "AT+AUTOEXEC=AT+ADVSTART=0;500;600;0;",
    ]


def _commands_challenge_3():
    # Each char needs LEN before VALUE — without LEN, max-size defaults
    # to 0 and the VALUE is silently stored as size 0.
    # AT+ADVDATA needs colon-separated hex.
    return [
        "AT+AUTOEXEC=AT+PERIPHERAL",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=0=UUID=12345678-1234-1234-1234-123456789abc",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=UUID=0001",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PERM=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=LEN=20",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=VALUE=FLAG{GA",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=UUID=0002",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=PERM=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=LEN=20",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=VALUE=TT_MAST",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=3=UUID=0003",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=3=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=3=PERM=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=3=LEN=20",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=3=VALUE=ER}",
        "AT+AUTOEXEC=AT+CUSTOMSERVICESTART",
        "AT+AUTOEXEC=AT+ADVDATA=0E:09:54:72:65:61:73:75:72:65:56:61:75:6C:74",
        "AT+AUTOEXEC=AT+ADVSTART",
    ]


def _commands_challenge_4():
    # Each char needs LEN before VALUE; AT+ADVDATA needs colon-separated hex.
    return [
        "AT+AUTOEXEC=AT+PERIPHERAL",
        "AT+AUTOEXEC=AT+GAPIOCAP=3",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=0=UUID=aabbccdd-1122-3344-5566-778899aabbcc",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=UUID=0010",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PERM=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=LEN=50",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=VALUE=Pair with me to unlock the secret",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=UUID=0020",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=PERM=E",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=LEN=20",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=2=VALUE=FLAG{PAIRED_UP}",
        "AT+AUTOEXEC=AT+CUSTOMSERVICESTART",
        "AT+AUTOEXEC=AT+ADVDATA=0A:09:56:61:75:6C:74:4C:6F:63:6B",
        "AT+AUTOEXEC=AT+ADVSTART",
    ]


def _commands_challenge_5():
    # The Whisper: split flag between AT+ADVDATA and AT+ADVRESP — only
    # ACTIVE scanners retrieve the scan response, so a passive scan only
    # gets half the flag. The whole point is to teach the distinction
    # between the advertising packet and the scan response packet.
    #
    # ADVDATA bytes: name "Whisper" (08:09:57:68:69:73:70:65:72) +
    #                manufacturer-specific (length 0D, type FF, company
    #                0059, payload "FLAG{ACTIV").
    # ADVRESP bytes: manufacturer-specific (length 0A, type FF, company
    #                0059, payload "E_EYES}").
    #
    # Combining the two payloads in order yields FLAG{ACTIVE_EYES}.
    return [
        "AT+AUTOEXEC=AT+PERIPHERAL",
        "AT+AUTOEXEC=AT+ADVDATA=08:09:57:68:69:73:70:65:72:0D:FF:00:59:46:4C:41:47:7B:41:43:54:49:56",
        "AT+AUTOEXEC=AT+ADVRESP=0A:FF:00:59:45:5F:45:59:45:53:7D",
        "AT+AUTOEXEC=AT+ADVSTART",
    ]


def _commands_challenge_6():
    # Char needs LEN before VALUE; AT+ADVDATA needs colon-separated hex.
    return [
        "AT+AUTOEXEC=AT+PERIPHERAL",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=0=UUID=deadbeef-cafe-face-babe-0123456789ab",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=UUID=0001",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PROP=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=PERM=R",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=LEN=20",
        "AT+AUTOEXEC=AT+CUSTOMSERVICE=1=VALUE=FLAG{TRUST_UUID}",
        "AT+AUTOEXEC=AT+CUSTOMSERVICESTART",
        "AT+AUTOEXEC=AT+ADVDATA=08:09:46:69:74:42:61:6E:64:11:07:AB:89:67:45:23:01:BE:BA:CE:FA:FE:CA:EF:BE:AD:DE",
        "AT+AUTOEXEC=AT+ADVSTART",
    ]


CHALLENGE_COMMANDS = {
    2: _commands_challenge_2,
    3: _commands_challenge_3,
    4: _commands_challenge_4,
    5: _commands_challenge_5,
    6: _commands_challenge_6,
}


def detect_port():
    """Auto-detect a connected BleuIO dongle by USB VID/PID or description."""
    candidates = []
    for p in list_ports.comports():
        desc = (p.description or "").lower()
        manuf = (p.manufacturer or "").lower()
        if "bleuio" in desc or "bleuio" in manuf or "smart sensor devices" in manuf:
            candidates.append(p.device)
        elif "usbmodem" in p.device.lower():
            candidates.append(p.device)

    if not candidates:
        return None
    return candidates[0]


def send_silent(ser, cmd):
    """Send an AT command and consume its response without printing it."""
    ser.reset_input_buffer()
    ser.write((cmd + "\r").encode())

    lines = []
    start = time.time()
    while time.time() - start < TIMEOUT:
        if ser.in_waiting:
            line = ser.readline().decode("utf-8", errors="replace").strip()
            if line:
                lines.append(line)
            if line in ("OK", "ERROR"):
                break
        else:
            time.sleep(0.05)

    return lines


def run_reset(ser):
    """Clear any existing AUTOEXEC and custom service configuration."""
    send_silent(ser, "AT+CLRAUTOEXEC")
    send_silent(ser, "AT+CUSTOMSERVICERESET")


def run_challenge(ser, number):
    """Send all AUTOEXEC commands for the given challenge number."""
    commands = CHALLENGE_COMMANDS[number]()
    ok = 0
    for cmd in commands:
        result = send_silent(ser, cmd)
        if any(line == "OK" for line in result):
            ok += 1
        elif any(line == "ERROR" for line in result):
            print(f"  Command failed. Aborting. ({ok}/{len(commands)} succeeded)")
            return False
    return ok == len(commands)


def _make_setup_func(number):
    def setup(ser):
        print(f"Loading Challenge {number}: {CHALLENGE_TITLES[number]}...", end=" ", flush=True)
        run_reset(ser)
        if run_challenge(ser, number):
            print("Done!")
            return True
        print("Failed.")
        return False
    setup.__name__ = f"setup_challenge_{number}"
    return setup


setup_challenge_2 = _make_setup_func(2)
setup_challenge_3 = _make_setup_func(3)
setup_challenge_4 = _make_setup_func(4)
setup_challenge_5 = _make_setup_func(5)
setup_challenge_6 = _make_setup_func(6)

SETUP_FUNCS = {
    2: setup_challenge_2,
    3: setup_challenge_3,
    4: setup_challenge_4,
    5: setup_challenge_5,
    6: setup_challenge_6,
}


def main():
    parser = argparse.ArgumentParser(
        description="Set up a BleuIO dongle as a CTF challenge server without spoiling flag values.",
    )
    parser.add_argument(
        "challenge",
        type=int,
        choices=sorted(CHALLENGE_COMMANDS.keys()),
        help="Challenge number (2 through 6).",
    )
    parser.add_argument(
        "--port",
        default=None,
        help="Serial port for the BleuIO dongle. If omitted, the script will try to auto-detect one.",
    )
    args = parser.parse_args()

    port = args.port or detect_port()
    if not port:
        print("ERROR: Could not auto-detect a BleuIO dongle.")
        print("Plug in the challenge server dongle and try again, or pass --port /dev/...")
        sys.exit(1)

    print(f"Using dongle on port: {port}")

    try:
        ser = serial.Serial(port, BAUD, timeout=TIMEOUT)
    except serial.SerialException as exc:
        print(f"ERROR: Could not open {port}: {exc}")
        sys.exit(1)

    time.sleep(0.3)

    try:
        # Wake the dongle.
        send_silent(ser, "AT")
        success = SETUP_FUNCS[args.challenge](ser)
    finally:
        ser.close()

    if not success:
        sys.exit(2)

    print()
    print("Challenge server is configured.")
    print("Next step: unplug and replug the dongle (or send ATR) so AUTOEXEC runs on boot.")
    print("Do NOT open a serial terminal on the challenge server dongle after rebooting.")


if __name__ == "__main__":
    main()
