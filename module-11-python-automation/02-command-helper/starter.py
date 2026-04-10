#!/usr/bin/env python3
"""Command helper demonstration.

Tests the send_command() helper function with several AT commands,
showing how to send commands and get clean responses.

Lesson 11.2: Building a Command Helper
"""

import serial
import time


def send_command(port, command, timeout=2):
    """Send an AT command and return the response lines.

    Args:
        port: An open serial.Serial connection
        command: The AT command string (without \\r)
        timeout: Maximum seconds to wait for a complete response

    Returns:
        A list of response lines (echo and terminators stripped)
    """
    # TODO: Clear the input buffer to discard stale data

    # TODO: Send the command with '\r' appended, encoded as UTF-8 bytes

    response_lines = []
    start = time.time()

    while time.time() - start < timeout:
        if port.in_waiting:
            # TODO: Read a line, decode it as UTF-8 with errors='replace', and strip whitespace

            # TODO: If the line is not empty and not the echo of the command, append it

            # TODO: If the line is 'OK' or 'ERROR', break out of the loop
            pass
        else:
            time.sleep(0.05)

    return response_lines


def is_error(response):
    """Check if an AT command response indicates an error."""
    return 'ERROR' in response


# === Main script ===
if __name__ == '__main__':
    PORT = '/dev/cu.usbmodem4048FDE834D21'  # Replace with your port
    # PORT = '/dev/ttyACM0'                 # Linux example
    # PORT = 'COM4'                         # Windows example

    port = serial.Serial(PORT, 57600, timeout=1)
    time.sleep(0.5)

    # Disable echo first
    send_command(port, 'ATE0')

    # Test: basic connection check
    response = send_command(port, 'AT')
    print(f"AT response: {response}")

    # Test: device info
    response = send_command(port, 'ATI')
    print(f"ATI response: {response}")

    port.close()
