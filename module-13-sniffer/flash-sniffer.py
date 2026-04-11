#!/usr/bin/env python3
"""
Flash nRF Sniffer firmware onto a Raytac/Nordic nRF52840 dongle via USB DFU.

This script automates the three-step process:
  1. Generate a DFU package from the included hex file
  2. Detect the dongle in DFU/bootloader mode
  3. Flash the firmware

Prerequisites:
  - nrfutil installed: https://www.nordicsemi.com/Products/Development-tools/nRF-Util
  - nrfutil device subcommand: nrfutil install device
  - nrfutil nrf5sdk-tools subcommand: nrfutil install nrf5sdk-tools

Before running this script, put the dongle into DFU/bootloader mode:
  1. Plug in the dongle
  2. Press the RESET button while holding the user button (SW1),
     or double-press the RESET button quickly
  3. The LED should start pulsing red/amber (indicating bootloader mode)
  4. A new serial port will appear (different from the normal one)

Usage:
  python3 flash-sniffer.py
  python3 flash-sniffer.py --check   # just verify if the dongle is in DFU mode
"""

import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_HEX = os.path.join(SCRIPT_DIR, 'hex',
                            'sniffer_nrf52840dongle_nrf52840_4.1.1.hex')


def find_nrfutil():
    """Find the nrfutil executable."""
    path = shutil.which('nrfutil')
    if path:
        return path
    # Common install locations
    candidates = []
    if platform.system() == 'Windows':
        candidates.append(os.path.expandvars(r'%USERPROFILE%\nrfutil\nrfutil.exe'))
    else:
        candidates.append(os.path.expanduser('~/nrfutil/nrfutil'))
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def run_cmd(args, capture=True):
    """Run a command and return stdout. Exits on failure."""
    try:
        result = subprocess.run(args, capture_output=capture, text=True,
                                timeout=120)
        if result.returncode != 0:
            print(f"ERROR: Command failed: {' '.join(args)}")
            if result.stderr:
                print(result.stderr.strip())
            sys.exit(1)
        return result.stdout if capture else ''
    except FileNotFoundError:
        print(f"ERROR: Command not found: {args[0]}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"ERROR: Command timed out: {' '.join(args)}")
        sys.exit(1)


def find_dfu_port(nrfutil):
    """Detect the dongle's serial port in DFU mode."""
    output = run_cmd([nrfutil, 'device', 'list'])

    # nrfutil device list shows ports for each device
    # Look for serial port lines
    ports = []
    for line in output.splitlines():
        # Match port paths: /dev/cu.*, /dev/ttyACM*, COM*
        match = re.search(r'(/dev/\S+|COM\d+)', line)
        if match:
            port = match.group(1)
            # On macOS, prefer cu. over tty.
            if platform.system() == 'Darwin' and '/dev/tty.' in port:
                port = port.replace('/dev/tty.', '/dev/cu.')
            ports.append(port)

    if not ports:
        return None
    return ports[0]


def main():
    check_only = '--check' in sys.argv

    print('=== nRF Sniffer Firmware Flasher ===')
    print()

    # Find nrfutil
    nrfutil = find_nrfutil()
    if not nrfutil:
        print('ERROR: nrfutil not found.')
        print()
        print('Install it from:')
        print('  https://www.nordicsemi.com/Products/Development-tools/nRF-Util')
        print()
        print('Then install the required subcommands:')
        print('  nrfutil install device')
        print('  nrfutil install nrf5sdk-tools')
        sys.exit(1)

    version_output = run_cmd([nrfutil, '--version'])
    print(f'nrfutil: {version_output.strip()}')
    print()

    # Check firmware hex exists
    if not os.path.isfile(FIRMWARE_HEX):
        print(f'ERROR: Firmware hex file not found at:')
        print(f'  {FIRMWARE_HEX}')
        sys.exit(1)

    print(f'Firmware: {os.path.basename(FIRMWARE_HEX)}')
    print()

    # Find DFU device
    print('Looking for dongle in DFU mode...')
    dfu_port = find_dfu_port(nrfutil)

    if not dfu_port:
        print()
        print('No device found in DFU mode.')
        print()
        print('To enter DFU mode:')
        print('  1. Plug in the Raytac dongle')
        print('  2. Press RESET while holding the user button (SW1),')
        print('     or double-press RESET quickly')
        print('  3. The LED should start pulsing red/amber')
        print('  4. Then run this script again')
        sys.exit(1)

    print(f'Found DFU device at: {dfu_port}')
    print()

    if check_only:
        print('Dongle is in DFU mode and ready to flash.')
        return

    # Step 1: Generate DFU package
    dfu_package = os.path.join(tempfile.gettempdir(), 'sniffer_dfu_package.zip')
    print('Step 1/2: Generating DFU package...')
    run_cmd([nrfutil, 'nrf5sdk-tools', 'pkg', 'generate',
             '--hw-version', '52',
             '--sd-req', '0x00',
             '--application', FIRMWARE_HEX,
             '--application-version', '1',
             dfu_package])
    print(f'  Package created: {dfu_package}')
    print()

    # Step 2: Flash
    print('Step 2/2: Flashing firmware (this takes about 10 seconds)...')
    run_cmd([nrfutil, 'nrf5sdk-tools', 'dfu', 'usb-serial',
             '-pkg', dfu_package, '-p', dfu_port], capture=False)

    print()
    print('=== Flash complete! ===')
    print()
    print('Next steps:')
    print('  1. Unplug and replug the dongle')
    print('  2. Open Wireshark')
    print('  3. Look for "nRF Sniffer for Bluetooth LE" in the interface list')
    print('  4. If it appears, the flash was successful!')


if __name__ == '__main__':
    main()
