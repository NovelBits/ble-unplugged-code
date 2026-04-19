#!/usr/bin/env python3
"""Automated connect-read-disconnect workflow.

Scans for a target device by name, connects, discovers services,
reads a characteristic value, prints it, and disconnects cleanly.

Lesson 11.5: Automated Connect-Read-Disconnect

Requires: bleuio_helper.py (copy from 02-command-helper/ or add to PYTHONPATH)
"""

from bleuio_helper import open_bleuio, send_command, is_error
import re
import time

# === Configuration ===
TARGET_NAME = 'PERIPHERAL'
SCAN_DURATION = 5
CHAR_UUID = '12340002-5678-9abc-def0-123456789abc'


def find_target(port, target_name, scan_duration=5):
    """Scan for a device by name and return its address.

    Returns:
        The address in AT+GAPCONNECT format (e.g., '[0]50:65:83:C9:A3:71'),
        or None if not found.
    """
    send_command(port, 'AT+CENTRAL')
    send_command(port, 'ATASSN1')

    print(f"Scanning for '{target_name}'...")
    raw = send_command(port, f'AT+GAPSCAN={scan_duration}', timeout=scan_duration + 3)

    # BleuIO puts device names in parentheses after RSSI (with ATASSN=1).
    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)'
        r'(?:\s+\(([^)]*)\))?'
    )

    for line in raw:
        match = pattern.match(line)
        name = match.group(4) if match else None
        if match and name and name.strip().upper() == target_name.upper():
            addr_type = match.group(1)
            address = match.group(2)
            print(f"Found '{target_name}' at [{addr_type}]{address}")
            return f"[{addr_type}]{address}"

    return None


def connect_to_device(port, address):
    """Connect to a device and wait for service discovery.

    Returns:
        True if connection succeeded, False otherwise.
    """
    print(f"Connecting to {address}...")
    response = send_command(port, f'AT+GAPCONNECT={address}', timeout=10)

    for line in response:
        if 'CONNECTED' in line.upper():
            print("Connected. Waiting for service discovery...")
            time.sleep(3)
            return True

    print("Connection failed.")
    return False


def find_characteristic_handle(port, target_uuid):
    """Find a characteristic handle by UUID in the GATT database.

    Args:
        port: Open serial connection
        target_uuid: The characteristic UUID to find (case-insensitive)

    Returns:
        The handle string (e.g., '0033') or None if not found.
    """
    response = send_command(port, 'AT+GETSERVICES', timeout=5)

    for line in response:
        if target_uuid.lower() in line.lower() and '----' in line:
            parts = line.strip().split()
            if len(parts) >= 1:
                return parts[0]

    return None


def read_characteristic(port, handle):
    """Read a characteristic value by handle.

    Returns:
        The value string, or None if the read failed.
    """
    print(f"Reading handle {handle}...")
    response = send_command(port, f'AT+GATTCREAD={handle}', timeout=3)

    for line in response:
        if line.startswith('Value read:'):
            return line.split(':', 1)[1].strip()

    return None


def disconnect(port):
    """Disconnect from the remote device."""
    print("Disconnecting...")
    send_command(port, 'AT+GAPDISCONNECT', timeout=3)
    time.sleep(0.5)
    print("Disconnected.")


# === Main workflow ===
if __name__ == '__main__':
    port = open_bleuio()

    # Step 1: Find the target device
    address = find_target(port, TARGET_NAME, SCAN_DURATION)
    if not address:
        print(f"Device '{TARGET_NAME}' not found. Is it advertising?")
        port.close()
        exit(1)

    # Step 2: Connect
    if not connect_to_device(port, address):
        print("Could not connect. Exiting.")
        port.close()
        exit(1)

    # Step 3: Find the characteristic handle
    handle = find_characteristic_handle(port, CHAR_UUID)
    if not handle:
        print(f"Characteristic {CHAR_UUID} not found. Using default handle.")
        handle = '0033'

    # Step 4: Read the value
    value = read_characteristic(port, handle)
    if value:
        print(f"\n>>> Characteristic value: {value}")
    else:
        print("Could not read characteristic value.")

    # Step 5: Disconnect
    disconnect(port)

    port.close()
    print("Done.")
