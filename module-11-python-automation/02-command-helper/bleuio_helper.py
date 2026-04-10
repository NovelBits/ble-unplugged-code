#!/usr/bin/env python3
"""bleuio_helper.py - Reusable helper for BleuIO serial communication.

Provides send_command(), port auto-detection, and a convenience function
to open a BleuIO dongle with echo disabled. Import this module in your
scripts:

    from bleuio_helper import open_bleuio, send_command, is_error

Lesson 11.2: Building a Command Helper
"""

import serial
import serial.tools.list_ports
import time


def find_bleuio_port():
    """Find the first serial port that looks like a BleuIO dongle.

    Checks for common BleuIO port naming patterns:
      - macOS: /dev/cu.usbmodem*
      - Linux: /dev/ttyACM*
      - Windows: USB Serial in description

    Returns:
        The port device path (str), or None if not found.
    """
    for port in serial.tools.list_ports.comports():
        if 'usbmodem' in port.device.lower() or 'ttyacm' in port.device.lower():
            return port.device
        if 'usb serial' in port.description.lower():
            return port.device
    return None


def open_bleuio(port_name=None, baud=57600):
    """Open a serial connection to a BleuIO dongle.

    Args:
        port_name: Serial port path, or None to auto-detect.
                   macOS example: '/dev/cu.usbmodem4048FDE834D21'
                   Linux example: '/dev/ttyACM0'
                   Windows example: 'COM4'
        baud: Baud rate (default 57600, required for BleuIO)

    Returns:
        An open serial.Serial connection with echo disabled.

    Raises:
        RuntimeError: If no BleuIO dongle is found during auto-detection.
    """
    if port_name is None:
        port_name = find_bleuio_port()
        if port_name is None:
            raise RuntimeError("No BleuIO dongle found. Is it plugged in?")

    port = serial.Serial(port_name, baud, timeout=1)
    time.sleep(0.5)
    send_command(port, 'ATE0')  # Disable echo
    return port


def send_command(port, command, timeout=2):
    """Send an AT command and return the response lines.

    Handles buffer clearing, command sending, echo stripping,
    timeout detection, and multi-line response collection.

    Args:
        port: An open serial.Serial connection
        command: The AT command string (without \\r)
        timeout: Maximum seconds to wait for a complete response

    Returns:
        A list of response lines (echo and terminators stripped)
    """
    port.reset_input_buffer()
    port.write(f'{command}\r'.encode('utf-8'))

    response_lines = []
    start = time.time()

    while time.time() - start < timeout:
        if port.in_waiting:
            line = port.readline().decode('utf-8', errors='replace').strip()
            if line and line != command:
                response_lines.append(line)
            if line in ('OK', 'ERROR'):
                break
        else:
            time.sleep(0.05)

    return response_lines


def is_error(response):
    """Check if a response indicates an error.

    Args:
        response: A list of response lines from send_command()

    Returns:
        True if 'ERROR' is in the response list.
    """
    return 'ERROR' in response
