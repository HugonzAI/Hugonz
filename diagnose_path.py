#!/usr/bin/env python3
"""Diagnose file path and working directory issues"""
import os
import sys

print("=" * 70)
print("File Path Diagnosis Tool")
print("=" * 70)

# 1. Current working directory
print("\n1. Current Working Directory:")
cwd = os.getcwd()
print(f"   {cwd}")

# 2. Script location
print("\n2. Script Location:")
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"   {script_dir}")

if cwd != script_dir:
    print(f"\n   ⚠️  WARNING: Working directory is DIFFERENT from script location!")
    print(f"   This is why the program can't find template files!")

# 3. Check for template files in BOTH locations
print("\n3. Checking for files:")

files_to_check = [
    'example_Good.xlsx',
    'EST Tester.xlsx',
    'EST_Tester.xlsx',  # Check both with space and underscore
    'EST_Limits_Summary.xlsx'
]

print(f"\n   In Working Directory ({cwd}):")
for f in files_to_check:
    exists = os.path.exists(os.path.join(cwd, f))
    status = "✅" if exists else "❌"
    print(f"      {status} {f}")

print(f"\n   In Script Directory ({script_dir}):")
for f in files_to_check:
    exists = os.path.exists(os.path.join(script_dir, f))
    status = "✅" if exists else "❌"
    print(f"      {status} {f}")
    if exists:
        full_path = os.path.join(script_dir, f)
        size = os.path.getsize(full_path)
        print(f"         Path: {full_path}")
        print(f"         Size: {size:,} bytes")

# 4. List all files in current directory
print(f"\n4. All files in current directory:")
try:
    files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
    xlsx_files = [f for f in files if f.endswith('.xlsx')]
    py_files = [f for f in files if f.endswith('.py')]
    
    print(f"\n   Excel files (.xlsx):")
    if xlsx_files:
        for f in xlsx_files:
            print(f"      - {f}")
    else:
        print(f"      (none found)")
    
    print(f"\n   Python files (.py):")
    if py_files:
        for f in py_files[:5]:  # Show first 5
            print(f"      - {f}")
        if len(py_files) > 5:
            print(f"      ... and {len(py_files)-5} more")
    else:
        print(f"      (none found)")
        
except Exception as e:
    print(f"   Error listing files: {e}")

# 5. Check how est_converter.py looks for the template
print("\n5. Checking est_converter.py template path:")
try:
    with open(os.path.join(script_dir, 'est_converter.py'), 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Look for template path references
    if 'template_path = "example_Good.xlsx"' in content:
        print("   ✅ Code uses: template_path = \"example_Good.xlsx\"")
        print("   This is a relative path (looks in working directory)")
    else:
        print("   ⚠️  Template path definition not found in expected format")
        
except Exception as e:
    print(f"   Error reading est_converter.py: {e}")

# 6. Solution
print("\n" + "=" * 70)
print("DIAGNOSIS & SOLUTION:")
print("=" * 70)

if cwd != script_dir:
    print("""
🔴 PROBLEM FOUND: Working Directory Mismatch

When you run 'python est_converter.py', Python's working directory is:
  {cwd}

But the script and template files are located in:
  {script_dir}

SOLUTION 1 - Change to the correct directory before running:
  cd "{script_dir}"
  python est_converter.py

SOLUTION 2 - Run using full path:
  python "{script_dir}\\est_converter.py"
  
SOLUTION 3 - Use Python launcher with -X flag:
  py -X cd_to_script_dir est_converter.py
""".format(cwd=cwd, script_dir=script_dir))
else:
    print("""
✅ Working directory is correct.

Checking for other issues:
""")
    
    # Check file name variations
    if not os.path.exists('example_Good.xlsx'):
        print("\n❌ example_Good.xlsx not found in current directory")
        print("\nPossible issues:")
        print("  1. File is named differently (check spelling/capitalization)")
        print("  2. File is in a subdirectory")
        print("  3. File was not downloaded from repository")
        print("\nRun this to list all .xlsx files:")
        print("  dir *.xlsx      (Command Prompt)")
        print("  ls *.xlsx       (PowerShell/Git Bash)")
    else:
        print("\n✅ example_Good.xlsx found!")
        print("\nIf the program still can't find it, try:")
        print("  1. Close the program completely")
        print("  2. Open a NEW command prompt/PowerShell")
        print("  3. cd to the program directory")
        print("  4. Run: python est_converter.py")

print("=" * 70)
