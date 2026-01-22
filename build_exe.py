#!/usr/bin/env python3
"""
EST Converter - PyInstaller Build Script
Creates a standalone Windows executable with all dependencies.

Usage:
    python build_exe.py

Output:
    dist/EST_Converter.exe (standalone executable)
"""

import PyInstaller.__main__
import os
import sys

# Configuration
APP_NAME = "EST_Converter"
MAIN_SCRIPT = "est_converter.py"
ICON_FILE = "est_icon.ico" if os.path.exists("est_icon.ico") else None

# Build arguments
pyinstaller_args = [
    MAIN_SCRIPT,
    f'--name={APP_NAME}',
    '--onefile',              # Single executable
    '--windowed',             # No console window (GUI only)
    '--clean',                # Clean cache before build

    # Icon
    f'--icon={ICON_FILE}' if ICON_FILE else '',

    # Add data files (templates, logo)
    '--add-data=example_Good.xlsx;.',
    '--add-data=EST_Tester.xlsx;.',
    '--add-data=EST_Limits_Summary.xlsx;.',

    # Optional: Add logo and icon if they exist
    *(['--add-data=hnz_logo.png;.'] if os.path.exists('hnz_logo.png') else []),
    *(['--add-data=est_icon.ico;.'] if os.path.exists('est_icon.ico') else []),

    # Hidden imports (explicit dependencies)
    '--hidden-import=openpyxl',
    '--hidden-import=openpyxl.cell',
    '--hidden-import=openpyxl.styles',
    '--hidden-import=dateutil',
    '--hidden-import=serial',

    # Exclude unnecessary modules (reduce size)
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',

    # Version info
    '--version-file=version_info.txt' if os.path.exists('version_info.txt') else '',
]

# Remove empty strings
pyinstaller_args = [arg for arg in pyinstaller_args if arg]

print("=" * 70)
print("EST Converter - Building Windows Executable")
print("=" * 70)
print(f"\nConfiguration:")
print(f"  App Name: {APP_NAME}")
print(f"  Main Script: {MAIN_SCRIPT}")
print(f"  Icon: {ICON_FILE if ICON_FILE else 'None'}")
print(f"  Include Templates: Yes")
print(f"  Include Logo: {'Yes' if os.path.exists('hnz_logo.png') else 'No'}")
print(f"\nBuilding...")
print("-" * 70)

try:
    PyInstaller.__main__.run(pyinstaller_args)

    print("\n" + "=" * 70)
    print("✓ Build Complete!")
    print("=" * 70)
    print(f"\nExecutable location:")
    print(f"  dist/{APP_NAME}.exe")
    print(f"\nDistribution package:")
    print(f"  1. Copy dist/{APP_NAME}.exe to target system")
    print(f"  2. Ensure template files are in the same directory:")
    print(f"     - example_Good.xlsx")
    print(f"     - EST_Tester.xlsx")
    print(f"     - EST_Limits_Summary.xlsx")
    print(f"     - hnz_logo.png (optional)")
    print(f"     - est_icon.ico (optional)")
    print(f"\nNote: Template files are embedded in the EXE, but can be")
    print(f"      extracted/modified by placing them alongside the EXE.")
    print("=" * 70)

except Exception as e:
    print(f"\n✗ Build failed: {e}")
    sys.exit(1)
