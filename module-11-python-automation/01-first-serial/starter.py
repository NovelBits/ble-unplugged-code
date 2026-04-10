#!/usr/bin/env python3
"""First serial communication with a BleuIO dongle.

Opens a serial connection at 57600 baud, sends the AT command,
reads and prints the response, then closes the port.

Lesson 11.1: Python Serial Communication
"""

import serial
import time

# === Configuration ===
# Replace with YOUR port name (see lesson for how to find it)
PORT = '/dev/cu.usbmodem4048FDE834D21'  # macOS example
# PORT = '/dev/ttyACM0'                 # Linux example
# PORT = 'COM4'                         # Windows example
BAUD_RATE = 57600
TIMEOUT = 1  # seconds

# === Open the serial port ===
# TODO: Create a serial.Serial connection using PORT, BAUD_RATE, and TIMEOUT

time.sleep(0.5)  # Give the dongle a moment to initialize

# === Clear any leftover data in the buffer ===
# TODO: Call reset_input_buffer() on the port to clear stale data

# === Send the AT command ===
# TODO: Send the string 'AT\r' encoded as UTF-8 bytes using port.write()
print(f"Sent: AT")

# === Read the response ===
time.sleep(0.3)  # Brief pause to let the dongle respond
# TODO: Loop while port.in_waiting is true, read lines with port.readline(),
#       decode them as UTF-8, strip whitespace, and print non-empty lines

# === Close the port ===
# TODO: Close the serial port
print("Port closed.")
