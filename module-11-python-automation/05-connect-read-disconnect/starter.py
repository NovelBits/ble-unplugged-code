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

    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)\s+Name:\s*(.*)'
    )

    for line in raw:
        match = pattern.match(line)
        if match and match.group(4).strip().upper() == target_name.upper():
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
    # TODO: Send AT+GAPCONNECT with the address and a 10-second timeout

    # TODO: Check the response lines for 'CONNECTED'
    # If found, wait 3 seconds for service discovery and return True

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
    # TODO: Send AT+GETSERVICES with a 5-second timeout

    # TODO: Search response lines for the target UUID
    # Lines with characteristics look like: "0033 ---- 12345678-1234-..."
    # Return the handle (first field) if the UUID is found

    return None


def read_characteristic(port, handle):
    """Read a characteristic value by handle.

    Returns:
        The value string, or None if the read failed.
    """
    print(f"Reading handle {handle}...")
    # TODO: Send AT+GATTCREAD with the handle

    # TODO: Find the line starting with 'Value read:' and return
    #       the value after the colon

    return None


def disconnect(port):
    """Disconnect from the remote device."""
    print("Disconnecting...")
    # TODO: Send AT+GAPDISCONNECT
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
