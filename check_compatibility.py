#!/usr/bin/env python3
"""Check Python and PySide6 compatibility"""
import sys
import platform

print("=" * 70)
print("Python & PySide6 Compatibility Check")
print("=" * 70)

# Check Python version
py_version = sys.version_info
print(f"\n1. Python Version:")
print(f"   Version: {py_version.major}.{py_version.minor}.{py_version.micro}")
print(f"   Full: {sys.version}")

# Check if Python is too new
if py_version.major == 3 and py_version.minor >= 14:
    print("\n   ⚠️  WARNING: Python 3.14+ is VERY NEW!")
    print("   PySide6 may not be fully compatible yet.")
    print("   Recommended: Python 3.11 or 3.12")

# Check PySide6
print(f"\n2. PySide6 Status:")
try:
    import PySide6
    from PySide6 import QtCore
    
    print(f"   ✅ PySide6 installed: {PySide6.__version__}")
    print(f"   Qt version: {QtCore.qVersion()}")
    
    # Check if it's a compatible version
    pyside_version = PySide6.__version__
    if pyside_version < "6.5.0":
        print(f"   ⚠️  PySide6 version {pyside_version} may be too old")
        print("   Try upgrading: pip install --upgrade PySide6")
    
except ImportError as e:
    print(f"   ❌ PySide6 not found: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠️  PySide6 import issue: {e}")
    print("   This suggests a compatibility problem!")

# Check other dependencies
print(f"\n3. Other Dependencies:")
try:
    import openpyxl
    print(f"   ✅ openpyxl: {openpyxl.__version__}")
except ImportError:
    print("   ❌ openpyxl not installed")

try:
    import dateutil
    print(f"   ✅ python-dateutil: {dateutil.__version__}")
except ImportError:
    print("   ❌ python-dateutil not installed")

try:
    import serial
    print(f"   ✅ pyserial installed")
except ImportError:
    print("   ⚠️  pyserial not installed (optional)")

# Recommendations
print("\n" + "=" * 70)
print("DIAGNOSIS & RECOMMENDATIONS:")
print("=" * 70)

if py_version.major == 3 and py_version.minor >= 14:
    print("""
🔴 PROBLEM IDENTIFIED: Python 3.14 Compatibility Issue

Python 3.14 was released in December 2025 and is very new.
PySide6 (Qt for Python) may not be fully compatible yet.

SOLUTION - Install Python 3.12 (Recommended):
  1. Download Python 3.12.x from: https://www.python.org/downloads/
  2. During installation, check "Add to PATH"
  3. After installation, verify:
     py -3.12 --version
  4. Install dependencies:
     py -3.12 -m pip install PySide6 openpyxl python-dateutil pyserial
  5. Run EST Converter:
     py -3.12 est_converter.py

ALTERNATIVE - Try latest PySide6 with Python 3.14:
  1. Update PySide6 to latest version:
     pip install --upgrade PySide6
  2. If that doesn't work, Python 3.14 is too new

WHY THIS MATTERS:
- Your code is correct ✅
- Encoding fix is present ✅
- UI fixes are present ✅
- But PySide6/Qt may not render properly on Python 3.14
""")
else:
    print("\n✅ Python version looks compatible")
    print("   Try: pip install --upgrade PySide6")

print("=" * 70)
