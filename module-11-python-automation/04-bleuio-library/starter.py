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

# TODO: Call dongle.ati() and print the response fields:
#   resp.Cmd  - the command that was sent
#   resp.Ack  - acknowledgment with err (bool) and errMsg (str)
#   resp.Rsp  - response data list
#   resp.End  - end-of-response marker

# TODO: Extract the firmware version from resp.Rsp
# Each item in Rsp is a dict, e.g. {'Firmware Version': '2.7.9.70'}


# --- Example 2: Status Tracking ---
print("\n=== Status ===")
# TODO: Print the dongle's status properties:
#   dongle.status.isConnected
#   dongle.status.isScanning
#   dongle.status.isAdvertising
#   dongle.status.role


# --- Example 3: Scan with Callback ---
print("\n=== Scanning (5 seconds) ===")
scan_results = []

# TODO: Define a callback function that appends data to scan_results

# TODO: Register the callback with dongle.register_scan_cb()

# TODO: Set central role with dongle.at_central()

# TODO: Start scanning with dongle.at_gapscan()

time.sleep(5)

# TODO: Stop scanning and unregister the callback

print(f"Found {len(scan_results)} scan results:")
for result in scan_results:
    print(f"  {result}")
