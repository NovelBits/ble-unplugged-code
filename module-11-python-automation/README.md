# Module 11: Python Automation Foundations

Hands-on exercises for automating Bluetooth LE operations with Python and the BleuIO dongle.

## Prerequisites

- Python 3.6 or later
- One or two BleuIO USB dongles
- `pyserial` installed (`pip install pyserial`)
- `bleuio` installed for exercise 04 (`pip install bleuio`)
- No serial terminal connected to the dongle (only one program can use a serial port at a time)

## How to Use

Each exercise directory contains two files:

- **`starter.py`** contains the full script structure with `TODO` comments where the key learning code goes. Try filling these in yourself first.
- **`solution.py`** is the complete, runnable reference implementation. Use it to check your work or if you get stuck.

## Exercise Directory

| Directory | Lesson | Description |
|-----------|--------|-------------|
| `01-first-serial/` | 11.1 | Open a serial port, send AT, read the response |
| `02-command-helper/` | 11.2 | Build a reusable `send_command()` helper function |
| `03-automated-scanning/` | 11.3 | Scan for devices, parse results, deduplicate |
| `04-bleuio-library/` | 11.4 | Use the official `bleuio` Python library |
| `05-connect-read-disconnect/` | 11.5 | Full workflow: scan, connect, read, disconnect |
| `06-data-logging/` | 11.6 | Periodic reads with CSV export |
| `08-robust-template/` | 11.8 | Error handling, retries, graceful shutdown |

## The Helper Module

The `02-command-helper/bleuio_helper.py` file is a reusable module used by exercises 03 through 08. To use it from other exercise directories, either:

1. Copy `bleuio_helper.py` into each exercise directory, or
2. Add the `02-command-helper/` directory to your Python path:
   ```python
   import sys
   sys.path.insert(0, '../02-command-helper')
   ```
3. Or run scripts from the `02-command-helper/` directory.

## Important Notes

- **Baud rate:** Always use 57600 for BleuIO dongles. Using the wrong baud rate produces garbled output or no response.
- **Port names:** Update the `PORT` variable in each script to match your system. See the comments in each file for macOS, Linux, and Windows examples.
- **Close your serial terminal** before running any Python script. Two programs cannot share the same serial port.
- **bleuio library bug:** The `port='auto'` mode in `BleuIO()` is broken in version 1.7.5. Always pass an explicit port name.
