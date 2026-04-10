# Bluetooth LE Unplugged: Student Code Repository

Exercise files for the [Bluetooth LE Unplugged](https://academy.novelbits.io) course by Novel Bits.

## Requirements

- **Python 3.6+**
- **Two BleuIO USB dongles** (included with your course bundle)
- **pyserial** for serial communication (`pip install pyserial`)
- **bleuio** library for Module 11 exercise 04 (`pip install bleuio`)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/novelbits/ble-unplugged-code.git
   cd ble-unplugged-code
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Plug in your BleuIO dongle and verify it is detected:
   ```
   python3 -c "import serial; print('pyserial ready')"
   ```

4. Find your serial port name:
   - **macOS:** `ls /dev/cu.usbmodem*`
   - **Linux:** `ls /dev/ttyACM*`
   - **Windows:** Check Device Manager under Ports (COM & LPT)

## Structure

Each exercise directory contains:

- **`starter.py`** is your starting point. The script structure, imports, and comments are all in place. Fill in the `TODO` sections yourself.
- **`solution.py`** is the complete, runnable reference. Try the starter first, then check your work against the solution.

## Module Listing

| Directory | Module | Description |
|-----------|--------|-------------|
| `module-11-python-automation/` | Python Automation Foundations | Serial communication, scanning, connecting, data logging, error handling |
| `module-12-ctf/` | Capture the Flag | CTF challenge setup script for the Bluetooth LE security challenges |

## Important Notes

### Baud Rate

The BleuIO dongle communicates at **57600 baud**. This is not the typical 115200 used by many other serial devices. If you get garbled output or no response, check the baud rate first.

### Serial Port Conflicts

Only one program can use a serial port at a time. **Close your serial terminal** (the one you use for the course lessons) before running any Python script. If you get a "port in use" error, check for other programs that might have the port open.

### bleuio Library: Use Explicit Ports

The `bleuio` Python library's `port='auto'` mode is broken in version 1.7.5 (it crashes with `'BleuIO' object has no attribute 'port'`). Always pass an explicit port name when creating a `BleuIO()` instance:

```python
from bleuio_lib.bleuio_funcs import BleuIO

# Always specify the port explicitly
dongle = BleuIO(port='/dev/cu.usbmodem4048FDE834D21')
```

### The Helper Module

The file `module-11-python-automation/02-command-helper/bleuio_helper.py` is a reusable module imported by exercises 03 through 08. See the Module 11 README for instructions on making it available to other exercises.

## License

These exercise files accompany the Bluetooth LE Unplugged course. They are provided for personal educational use by enrolled students.
