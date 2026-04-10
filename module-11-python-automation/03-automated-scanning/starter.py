#!/usr/bin/env python3
"""Automated Bluetooth LE device scanner.

Sets the dongle to Central role, runs a timed scan, parses results
into structured data, deduplicates by address, and displays a sorted table.

Lesson 11.3: Automated Scanning

Requires: bleuio_helper.py (copy from 02-command-helper/ or add to PYTHONPATH)
"""

from bleuio_helper import open_bleuio, send_command, is_error
import re

SCAN_DURATION = 5  # seconds


def setup_scanner(port):
    """Configure the dongle for scanning."""
    response = send_command(port, 'AT+CENTRAL')
    if is_error(response):
        print("Warning: Could not set Central role.")

    response = send_command(port, 'ATASSN1')
    if is_error(response):
        print("Warning: Could not enable device names.")

    print("Scanner configured.")


def run_scan(port, duration=5):
    """Run a Bluetooth LE scan and return the raw output lines."""
    print(f"Scanning for {duration} seconds...")
    response = send_command(port, f'AT+GAPSCAN={duration}', timeout=duration + 3)
    return response


def parse_scan_results(raw_lines):
    """Parse raw scan output into structured device records.

    Each scan result line looks like:
        [01] Device: [0]50:65:83:C9:A3:71 RSSI: -42 Name: PERIPHERAL

    Returns:
        A list of dictionaries, each with keys:
        address, address_type, rssi, name
    """
    devices = []

    # TODO: Create a regex pattern that captures:
    #   - group(1): address type (single digit, 0=public, 1=random)
    #   - group(2): MAC address (17 chars, hex digits and colons)
    #   - group(3): RSSI value (negative integer)
    #   - group(4): device name (may be empty)
    pattern = re.compile(
        r''  # TODO: Write the regex pattern
    )

    for line in raw_lines:
        match = pattern.match(line)
        if match:
            # TODO: Build a device dictionary from the captured groups
            # Keys: 'address_type', 'address', 'rssi', 'name'
            pass

    return devices


def deduplicate_devices(devices):
    """Remove duplicates, keeping the strongest RSSI per address.

    RSSI is negative, so a stronger signal is closer to 0.
    For example, -40 is stronger than -80.
    """
    best = {}

    # TODO: Loop through devices. For each address, keep the entry
    #       with the highest (closest to zero) RSSI value.

    # TODO: Return the values sorted by RSSI (strongest first)
    return sorted(best.values(), key=lambda d: d['rssi'], reverse=True)


def display_devices(devices):
    """Print a formatted table of discovered devices."""
    if not devices:
        print("No devices found.")
        return

    print(f"\n{'Address':<20} {'Type':<8} {'RSSI':<7} {'Name'}")
    print("-" * 60)
    for d in devices:
        print(f"{d['address']:<20} {d['address_type']:<8} {d['rssi']:<7} {d['name']}")
    print(f"\nTotal unique devices: {len(devices)}")


# === Main ===
if __name__ == '__main__':
    port = open_bleuio()

    setup_scanner(port)
    raw = run_scan(port, SCAN_DURATION)

    all_devices = parse_scan_results(raw)
    unique_devices = deduplicate_devices(all_devices)

    display_devices(unique_devices)

    port.close()
