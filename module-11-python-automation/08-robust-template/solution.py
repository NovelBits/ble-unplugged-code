#!/usr/bin/env python3
"""Production-ready Bluetooth LE automation template.

Combines all robustness patterns: try/finally for port cleanup,
Ctrl+C handling, retry logic with exponential backoff, connection
drop detection, and ATE0 at script start.

Lesson 11.8: Error Handling and Robustness

Requires: bleuio_helper.py (copy from 02-command-helper/ or add to PYTHONPATH)
"""

from bleuio_helper import open_bleuio, send_command, is_error
import time
import re
import sys


# === Configuration ===
TARGET_NAME = 'PERIPHERAL'
CHAR_HANDLE = '0033'
MAX_RETRIES = 3
RETRY_DELAY = 2


def find_target(port, target_name, scan_duration=5):
    """Scan for a target device with retry."""
    send_command(port, 'AT+CENTRAL')
    send_command(port, 'ATASSN1')

    # BleuIO puts device names in parentheses after RSSI (with ATASSN=1).
    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)'
        r'(?:\s+\(([^)]*)\))?'
    )

    for attempt in range(MAX_RETRIES):
        print(f"Scan attempt {attempt + 1} of {MAX_RETRIES}...")
        raw = send_command(port, f'AT+GAPSCAN={scan_duration}', timeout=scan_duration + 3)

        for line in raw:
            match = pattern.match(line)
            name = match.group(4) if match else None
            if match and name and name.strip().upper() == target_name.upper():
                addr = f"[{match.group(1)}]{match.group(2)}"
                print(f"Found '{target_name}' at {addr}")
                return addr

        if attempt < MAX_RETRIES - 1:
            print(f"Not found. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    return None


def connect_with_retry(port, address):
    """Connect with exponential backoff.

    A failed AT+GAPCONNECT (no CONNECTED. event before timeout) leaves the
    dongle in "Busy trying to connect" state. Without AT+CANCELCONNECT to
    abort the in-flight attempt, every subsequent connect command fails
    with "Busy" and the retry loop achieves nothing. We send CANCELCONNECT
    after each failed attempt so the next iteration starts from a clean
    state.
    """
    for attempt in range(MAX_RETRIES):
        print(f"Connection attempt {attempt + 1} of {MAX_RETRIES}...")
        response = send_command(port, f'AT+GAPCONNECT={address}', timeout=10)

        for line in response:
            if 'CONNECTED' in line.upper():
                print("Connected. Waiting for service discovery...")
                time.sleep(3)
                return True

        # Failed attempt: clear the in-flight connect so the next retry can fire.
        send_command(port, 'AT+CANCELCONNECT', timeout=2)

        if attempt < MAX_RETRIES - 1:
            delay = RETRY_DELAY * (2 ** attempt)
            print(f"Failed. Retrying in {delay} seconds...")
            time.sleep(delay)

    return False


def safe_read(port, handle):
    """Read a characteristic with error checking."""
    response = send_command(port, f'AT+GATTCREAD={handle}', timeout=3)

    if is_error(response):
        return None

    for line in response:
        if line.startswith('Value read:'):
            return line.split(':', 1)[1].strip()

    return None


def safe_disconnect(port):
    """Disconnect gracefully, ignoring errors."""
    try:
        send_command(port, 'AT+GAPDISCONNECT', timeout=3)
        time.sleep(0.5)
    except Exception:
        pass  # Best effort


# === Main ===
def main():
    port = None

    try:
        # Open connection
        print("Opening serial connection...")
        port = open_bleuio()

        # Find target
        address = find_target(port, TARGET_NAME)
        if not address:
            print(f"Could not find '{TARGET_NAME}' after {MAX_RETRIES} scan attempts.")
            sys.exit(1)

        # Connect
        if not connect_with_retry(port, address):
            print(f"Could not connect after {MAX_RETRIES} attempts.")
            sys.exit(1)

        # Read
        value = safe_read(port, CHAR_HANDLE)
        if value:
            print(f"\n>>> Value: {value}\n")
        else:
            print("Read failed or returned no data.")

        # Disconnect
        safe_disconnect(port)
        print("Done.")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")

    except serial.SerialException as e:
        print(f"\nSerial error: {e}")
        print("Check that the dongle is plugged in and no other program is using the port.")

    except Exception as e:
        print(f"\nUnexpected error: {e}")

    finally:
        if port and port.is_open:
            safe_disconnect(port)
            port.close()
            print("Port closed.")


if __name__ == '__main__':
    import serial  # Import here so SerialException is available for catching
    main()
