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

    Returns:
        A list of dictionaries, each with keys:
        address, address_type, rssi, name
    """
    devices = []
    # BleuIO scan lines look like:
    #   [01] Device: [0]10:CA:BF:0F:81:71  RSSI: -68
    #   [02] Device: [0]40:48:FD:EA:ED:1A  RSSI: -13 (PERIPHERAL)
    # The name (when ATASSN=1) appears in parentheses after RSSI.
    pattern = re.compile(
        r'\[\d+\]\s+Device:\s+\[(\d)\]([0-9A-Fa-f:]{17})\s+RSSI:\s+(-?\d+)'
        r'(?:\s+\(([^)]*)\))?'
    )

    for line in raw_lines:
        match = pattern.match(line)
        if match:
            name = match.group(4)
            device = {
                'address_type': 'public' if match.group(1) == '0' else 'random',
                'address': match.group(2).upper(),
                'rssi': int(match.group(3)),
                'name': name.strip() if name else '(unknown)',
            }
            devices.append(device)

    return devices


def deduplicate_devices(devices):
    """Remove duplicates, keeping the strongest RSSI per address."""
    best = {}
    for device in devices:
        addr = device['address']
        if addr not in best or device['rssi'] > best[addr]['rssi']:
            best[addr] = device
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
