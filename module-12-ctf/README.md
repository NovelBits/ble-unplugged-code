# Module 12: Capture the Flag (CTF) Challenges

This directory contains the setup script for the Bluetooth LE CTF challenges in Module 12.

## What This Script Does

The `ctf-challenge-setup.py` script configures a BleuIO dongle as the CTF challenge server. It programs AUTOEXEC commands onto the dongle so it boots up ready to serve a specific challenge. The script hides the flag values from your screen so you do not accidentally see them before solving the challenge.

## Usage

```bash
python3 ctf-challenge-setup.py <challenge_number> [--port PORT]
```

### Examples

```bash
# Set up Challenge 2 (auto-detects the dongle port)
python3 ctf-challenge-setup.py 2

# Set up Challenge 3 with an explicit port
python3 ctf-challenge-setup.py 3 --port /dev/cu.usbmodem4048FDEAED1A1   # macOS
python3 ctf-challenge-setup.py 3 --port /dev/ttyACM0                    # Linux
python3 ctf-challenge-setup.py 3 --port COM4                            # Windows
```

### Available Challenges

| Number | Title |
|--------|-------|
| 2 | Hidden Device |
| 3 | GATT Treasure Hunt |
| 4 | Crack the Code |
| 5 | Speed Run |
| 6 | The Impostor |

## After Running the Script

1. Unplug and replug the dongle (or send `ATR`) so the AUTOEXEC commands run on boot
2. Do **not** open a serial terminal on the challenge server dongle after rebooting
3. Use your second dongle (the "attacker") to solve the challenge

## Requirements

- Python 3.6 or later
- `pyserial` installed (`pip install pyserial`)
- One BleuIO dongle designated as the challenge server
