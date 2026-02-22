# Bluetooth LE Unplugged — Course Exercises

Student exercise files for the [Bluetooth LE Unplugged](https://learn.novelbits.io/courses/ble-unplugged) course.

## Requirements

- Python 3.6+
- Two BleuIO USB dongles (included with your course bundle)
- `bleuio` Python package: `pip install bleuio`

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/novelbits/ble-unplugged-code.git
   cd ble-unplugged-code
   ```

2. Install the BleuIO Python library:
   ```
   pip install bleuio
   ```

3. Plug in your BleuIO dongle and verify it's detected:
   ```
   python -c "import bleuio; print('BleuIO library ready')"
   ```

## Structure

Each module directory contains exercises with:
- `starter.py` — Your starting point (fill in the blanks)
- `solution.py` — Reference solution (try on your own first!)
- `README.md` — Exercise instructions

## Course Modules with Exercises

| Directory | Module | Tier |
|-----------|--------|------|
| `module-07-python-foundations/` | Python Automation Foundations | Professional |
| `module-08-security-pairing-bonding/` | Security — Pairing & Bonding | Professional |
| `module-09-advanced-connections/` | Advanced Connection Management | Professional |
| `module-10-packet-analysis/` | Packet Analysis with Sniffer | Expert |
| `module-11-multi-device-orchestration/` | Multi-Device Orchestration | Expert |
| `module-12-debugging/` | Debugging Real-World Issues | Expert |
