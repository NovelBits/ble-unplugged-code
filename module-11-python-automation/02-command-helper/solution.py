#!/usr/bin/env python3
"""Command helper demonstration.

Tests the send_command() helper function with several AT commands,
showing how to send commands and get clean responses.

Lesson 11.2: Building a Command Helper
"""

import serial
import time


def send_command(port, command, timeout=2, quiet_period=0.3):
    """Send an AT command and return the response lines.

    Termination logic:
      - If we see 'OK' or 'ERROR', wait quiet_period to capture trailing
        data (AT+GETMAC emits OK BEFORE the MAC line, so we can't bail
        out the moment OK arrives).
      - If no clear terminator arrives (e.g. AT+GAPCONNECT prints
        'Trying to connect...' then has a multi-second silent gap before
        'CONNECTED.'), wait the full timeout instead of bailing out on
        quiet periods.

    Args:
        port: An open serial.Serial connection
        command: The AT command string (without \\r)
        timeout: Maximum seconds to wait for a complete response
        quiet_period: Quiet seconds after an OK/ERROR before exit

    Returns:
        A list of response lines (echo and terminators stripped)
    """
    port.reset_input_buffer()
    port.write(f'{command}\r'.encode('utf-8'))

    response_lines = []
    start = time.time()
    last_data_time = start
    saw_terminator = False

    while time.time() - start < timeout:
        if port.in_waiting:
            line = port.readline().decode('utf-8', errors='replace').strip()
            if line and line != command:  # Skip echo
                response_lines.append(line)
                last_data_time = time.time()
                if line in ('OK', 'ERROR'):
                    saw_terminator = True
        else:
            if saw_terminator and (time.time() - last_data_time) >= quiet_period:
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
