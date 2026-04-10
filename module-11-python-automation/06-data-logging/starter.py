#!/usr/bin/env python3
"""Periodic characteristic reader with CSV export.

Connects to a peripheral, reads a characteristic at regular intervals,
timestamps each reading, and writes everything to a CSV file.
Handles Ctrl+C gracefully so the CSV is always saved properly.

Lesson 11.6: Data Logging and CSV Export

Requires: bleuio_helper.py (copy from 02-command-helper/ or add to PYTHONPATH)
"""

from bleuio_helper import open_bleuio, send_command, is_error
import csv
import time
import re
from datetime import datetime

# === Configuration ===
TARGET_NAME = 'PERIPHERAL'
SCAN_DURATION = 5
CHAR_HANDLE = '0033'           # Handle to read
READ_INTERVAL = 5              # Seconds between reads
NUM_READINGS = 10              # Number of readings (0 = unlimited)
OUTPUT_FILE = 'ble_readings.csv'


def find_and_connect(port, target_name, scan_duration=5):
    """Scan for a target device and connect to it.

    Returns:
        The target's MAC address string, or None if connection failed.
    """
    send_command(port, 'AT+CENTRAL')
    send_command(port, 'ATASSN1')

    print(f"Scanning for '{target_name}'...")
    raw = send_command(port, f'AT+GAPSCAN={scan_duration}', timeout=scan_duration + 3)

    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)\s+Name:\s*(.*)'
    )

    address = None
    for line in raw:
        match = pattern.match(line)
        if match and match.group(4).strip().upper() == target_name.upper():
            addr_type = match.group(1)
            addr = match.group(2)
            address = f"[{addr_type}]{addr}"
            break

    if not address:
        return None

    print(f"Connecting to {address}...")
    response = send_command(port, f'AT+GAPCONNECT={address}', timeout=10)

    for line in response:
        if 'CONNECTED' in line.upper():
            time.sleep(3)
            mac = address.split(']')[1] if ']' in address else address
            return mac

    return None


def read_characteristic_full(port, handle):
    """Read a characteristic and return (ascii_value, hex_value).

    Returns:
        A tuple of (ascii_value, hex_value), or (None, None) on failure.
    """
    response = send_command(port, f'AT+GATTCREAD={handle}', timeout=3)

    ascii_val = None
    hex_val = None

    # TODO: Loop through response lines:
    #   - If a line starts with 'Value read:', extract the value after the colon
    #   - If a line starts with 'Hex:', extract the hex string after the colon

    return ascii_val, hex_val


def run_data_logger(port, address, handle, output_file, interval=5, max_readings=0):
    """Read a characteristic periodically and log to CSV.

    Args:
        port: Open serial connection
        address: Device MAC address (for CSV records)
        handle: GATT characteristic handle to read
        output_file: Path to the output CSV file
        interval: Seconds between readings
        max_readings: Maximum readings to take (0 = unlimited)
    """
    print(f"\nLogging to {output_file}")
    print(f"Reading handle {handle} every {interval} seconds")
    if max_readings > 0:
        print(f"Will take {max_readings} readings")
    else:
        print("Running until Ctrl+C is pressed")
    print()

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'address', 'handle', 'raw_value', 'ascii_value'])

        reading_count = 0

        try:
            while max_readings == 0 or reading_count < max_readings:
                # TODO: Call read_characteristic_full() to get (ascii_val, hex_val)

                # TODO: Get a timestamp using datetime.now().isoformat(timespec='seconds')

                # TODO: If ascii_val is not None:
                #   - Write a row to the CSV: [timestamp, address, handle, hex_val, ascii_val]
                #   - Call f.flush() to write to disk immediately
                #   - Increment reading_count
                #   - Print the reading

                # TODO: Sleep for the configured interval before the next read
                pass

        except KeyboardInterrupt:
            print(f"\n\nStopped by user after {reading_count} readings.")

    print(f"Data saved to {output_file}")


# === Main ===
if __name__ == '__main__':
    port = open_bleuio()

    address = find_and_connect(port, TARGET_NAME, SCAN_DURATION)
    if not address:
        print(f"Could not find or connect to '{TARGET_NAME}'.")
        port.close()
        exit(1)

    print(f"Connected to {address}")

    try:
        run_data_logger(port, address, CHAR_HANDLE, OUTPUT_FILE, READ_INTERVAL, NUM_READINGS)
    finally:
        # Always disconnect and close
        send_command(port, 'AT+GAPDISCONNECT', timeout=3)
        time.sleep(0.5)
        port.close()
        print("Disconnected and port closed.")
