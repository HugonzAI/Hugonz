#!/usr/bin/env python3
"""Check if required template files are present"""
import os
import sys

print("=" * 70)
print("EST Converter Template File Checker")
print("=" * 70)

# Required template files
required_files = {
    'example_Good.xlsx': 'Output template (CRITICAL - conversion will fail without this)',
    'EST Tester.xlsx': 'Tester S/N to Asset mapping',
    'EST_Limits_Summary.xlsx': 'Fixed limits for all test types'
}

print(f"\nCurrent directory: {os.getcwd()}\n")

missing_files = []
found_files = []

for filename, description in required_files.items():
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✅ {filename}")
        print(f"   {description}")
        print(f"   Size: {size:,} bytes")
        print()
        found_files.append(filename)
    else:
        print(f"❌ {filename} - MISSING!")
        print(f"   {description}")
        print()
        missing_files.append(filename)

print("=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"Found: {len(found_files)}/{len(required_files)} files")

if missing_files:
    print(f"\n🔴 MISSING FILES ({len(missing_files)}):")
    for f in missing_files:
        print(f"   - {f}")
    
    print("\n" + "=" * 70)
    print("SOLUTION:")
    print("=" * 70)
    print("""
These template files should be included in the repository.

Option 1 - Re-download from GitHub:
  1. Go to your repository on GitHub
  2. Select branch: claude/est-converter-baseline-sbRr5
  3. Download as ZIP
  4. Extract to a new folder
  5. Files should be included

Option 2 - Check if files are in a different location:
  Run this to search for the files:
    dir example_Good.xlsx /s     (Windows Command Prompt)
    Get-ChildItem -Recurse -Filter "example_Good.xlsx"  (PowerShell)

Option 3 - Files may be in parent/subdirectory:
  Check if you're running from the correct directory.
  Template files MUST be in the same folder as est_converter.py
    """)
else:
    print("\n✅ All required template files are present!")
    print("\nYou can now run: python est_converter.py")

print("=" * 70)

# Additional check - look for files in nearby directories
if missing_files:
    print("\nSearching nearby directories...")
    for root, dirs, files in os.walk('..', topdown=True):
        # Limit search depth
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
        if root.count(os.sep) - '..'.count(os.sep) > 2:
            continue
            
        for missing in missing_files:
            if missing in files:
                full_path = os.path.join(root, missing)
                print(f"   Found: {full_path}")
                print(f"   → Copy this file to: {os.getcwd()}")
