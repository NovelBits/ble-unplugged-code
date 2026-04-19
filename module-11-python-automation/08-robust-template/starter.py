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

    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)(?:\s+\(([^)]*)\))?'
    )

    for attempt in range(MAX_RETRIES):
        print(f"Scan attempt {attempt + 1} of {MAX_RETRIES}...")
        raw = send_command(port, f'AT+GAPSCAN={scan_duration}', timeout=scan_duration + 3)

        for line in raw:
            match = pattern.match(line)
            if match and match.group(4).strip().upper() == target_name.upper():
                addr = f"[{match.group(1)}]{match.group(2)}"
                print(f"Found '{target_name}' at {addr}")
                return addr

        if attempt < MAX_RETRIES - 1:
            print(f"Not found. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    return None


def connect_with_retry(port, address):
    """Connect with exponential backoff.

    Retries up to MAX_RETRIES times, doubling the wait between attempts.
    """
    for attempt in range(MAX_RETRIES):
        print(f"Connection attempt {attempt + 1} of {MAX_RETRIES}...")
        # TODO: Send AT+GAPCONNECT with the address and a 10-second timeout

        # TODO: Check response for 'CONNECTED' and return True if found
        #       (remember to wait 3 seconds for service discovery)

        if attempt < MAX_RETRIES - 1:
            # TODO: Calculate exponential backoff delay: RETRY_DELAY * (2 ** attempt)
            # TODO: Sleep for the calculated delay
            pass

    return False


def safe_read(port, handle):
    """Read a characteristic with error checking."""
    # TODO: Send AT+GATTCREAD with the handle

    # TODO: Check for errors with is_error()

    # TODO: Find and return the value from the 'Value read:' line

    return None


def safe_disconnect(port):
    """Disconnect gracefully, ignoring errors."""
    # TODO: Wrap the disconnect in a try/except that catches all exceptions
    #       Send AT+GAPDISCONNECT and sleep briefly
    pass


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

    # TODO: Add except block for serial.SerialException with a helpful message

    except Exception as e:
        print(f"\nUnexpected error: {e}")

    finally:
        # TODO: Check if port exists and is open, then disconnect and close
        pass


if __name__ == '__main__':
    import serial  # Import here so SerialException is available for catching
    main()
