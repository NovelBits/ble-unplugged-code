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
port = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
time.sleep(0.5)  # Give the dongle a moment to initialize

# === Clear any leftover data in the buffer ===
port.reset_input_buffer()

# === Send the AT command ===
command = 'AT\r'
port.write(command.encode('utf-8'))
print(f"Sent: AT")

# === Read the response ===
time.sleep(0.3)  # Brief pause to let the dongle respond
while port.in_waiting:
    line = port.readline().decode('utf-8', errors='replace').strip()
    if line:
        print(f"Received: {line}")

# === Close the port ===
port.close()
print("Port closed.")
