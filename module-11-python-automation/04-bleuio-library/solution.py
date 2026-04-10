#!/usr/bin/env python3
"""Using the official bleuio Python library.

Demonstrates the BleuIO constructor (with EXPLICIT port), device info query,
scan callbacks, and status tracking.

Lesson 11.4: Using the bleuio Library

IMPORTANT: The library's port='auto' mode is broken in version 1.7.5.
It crashes with "'BleuIO' object has no attribute 'port'".
Always pass an explicit port name as shown below.
"""

from bleuio_lib.bleuio_funcs import BleuIO
import time

# === Configuration ===
# IMPORTANT: Always use an explicit port. port='auto' is broken.
# Replace with YOUR port name:
PORT = '/dev/cu.usbmodem4048FDE834D21'  # macOS example
# PORT = '/dev/ttyACM0'                 # Linux example
# PORT = 'COM4'                         # Windows example


# --- Example 1: Device Info ---
print("=== Device Info ===")
dongle = BleuIO(port=PORT)

resp = dongle.ati()
print(f"Command:  {resp.Cmd}")
print(f"Ack:      {resp.Ack}")
print(f"Response: {resp.Rsp}")
print(f"End:      {resp.End}")

# Extract firmware version
firmware = 'Unknown'
for item in resp.Rsp:
    if 'Firmware Version' in item:
        firmware = item['Firmware Version']
print(f"Firmware: {firmware}")


# --- Example 2: Status Tracking ---
print("\n=== Status ===")
print(f"Connected:   {dongle.status.isConnected}")
print(f"Scanning:    {dongle.status.isScanning}")
print(f"Advertising: {dongle.status.isAdvertising}")
print(f"Role:        {dongle.status.role}")


# --- Example 3: Scan with Callback ---
print("\n=== Scanning (5 seconds) ===")
scan_results = []


def on_scan(data):
    """Called for each scan result as it arrives."""
    scan_results.append(data)


dongle.register_scan_cb(on_scan)
dongle.at_central()
dongle.at_gapscan()

time.sleep(5)
dongle.stop_scan()
dongle.unregister_scan_cb()

print(f"Found {len(scan_results)} scan results:")
for result in scan_results:
    print(f"  {result}")
