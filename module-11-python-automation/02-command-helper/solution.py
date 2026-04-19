#!/usr/bin/env python3
"""Command helper demonstration.

Tests the send_command() helper function with several AT commands,
showing how to send commands and get clean responses.

Lesson 11.2: Building a Command Helper
"""

import serial
import time


def send_command(port, command, timeout=2, quiet_period=0.2):
    """Send an AT command and return the response lines.

    Reads until either the timeout elapses OR a quiet period passes
    with no new data. We can't break early on 'OK' because some AT
    commands (notably AT+GETMAC) emit 'OK' *before* the actual data,
    so an early break would lose the trailing data line.

    Args:
        port: An open serial.Serial connection
        command: The AT command string (without \\r)
        timeout: Maximum seconds to wait for a complete response
        quiet_period: Seconds of no-new-data that means "response done"

    Returns:
        A list of response lines (echo and terminators stripped)
    """
    port.reset_input_buffer()
    port.write(f'{command}\r'.encode('utf-8'))

    response_lines = []
    start = time.time()
    last_data_time = start

    while time.time() - start < timeout:
        if port.in_waiting:
            line = port.readline().decode('utf-8', errors='replace').strip()
            if line and line != command:  # Skip echo
                response_lines.append(line)
                last_data_time = time.time()
        else:
            if response_lines and (time.time() - last_data_time) >= quiet_period:
                break
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

    # Test: GAP status
    response = send_command(port, 'AT+GAPSTATUS')
    print(f"GAP status: {response}")

    # Test: MAC address
    response = send_command(port, 'AT+GETMAC')
    print(f"MAC address: {response}")

    port.close()
