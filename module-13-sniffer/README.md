# Module 13: Sniffer Firmware Flasher

This directory contains everything you need to flash the nRF Sniffer for Bluetooth LE firmware onto your Raytac MDBT50Q-RX dongle.

## What's Here

| File | Purpose |
|------|---------|
| `flash-sniffer.py` | Cross-platform Python script that flashes the sniffer firmware |
| `hex/sniffer_nrf52840dongle_nrf52840_4.1.1.hex` | Nordic nRF Sniffer firmware v4.1.1 |

## Prerequisites

- **Python 3.6+** (already installed if you completed Module 11)
- **nrfutil** with the `device` and `nrf5sdk-tools` subcommands

### Installing nrfutil

Download from [Nordic's developer tools page](https://www.nordicsemi.com/Products/Development-tools/nRF-Util), then install the required subcommands:

```
nrfutil install device
nrfutil install nrf5sdk-tools
```

## Usage

### 1. Check if flashing is needed

If your dongle already shows up as a serial device when plugged in (e.g., `/dev/cu.usbmodem*` on macOS, `/dev/ttyACM*` on Linux, or a new COM port on Windows), the firmware is already installed and you can skip flashing.

### 2. Enter DFU mode

1. Plug in the Raytac dongle
2. Press **RESET** while holding the **user button (SW1)**, or double-press RESET quickly
3. The LED should start pulsing red/amber (bootloader mode)

### 3. Flash

```
python3 flash-sniffer.py
```

The script detects the dongle, generates a DFU package, and flashes the firmware. Takes about 10 seconds. Unplug and replug when done.

### Verify

You can check that the dongle is in DFU mode without flashing:

```
python3 flash-sniffer.py --check
```

## Notes

- You only need to flash once. The firmware persists across power cycles.
- The Wireshark extcap plugin (needed to capture packets) is installed separately. See Lesson 13.2 in the course for instructions.
