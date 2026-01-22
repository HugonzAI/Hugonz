#!/usr/bin/env python3
"""Quick fix to make template paths work from script directory"""
import os
import shutil

print("=" * 70)
print("Template Path Quick Fix")
print("=" * 70)

# Read est_converter.py
print("\nReading est_converter.py...")
try:
    with open('est_converter.py', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
except Exception as e:
    print(f"❌ Error: {e}")
    input("Press Enter to exit...")
    exit(1)

# Backup original
print("Creating backup: est_converter.py.backup")
shutil.copy('est_converter.py', 'est_converter.py.backup')

# Find and modify the template path section
modified = False
new_lines = []

for i, line in enumerate(lines):
    # Look for the template path initialization
    if 'self.template_path = "example_Good.xlsx"' in line and not modified:
        indent = len(line) - len(line.lstrip())
        new_lines.append(line)
        # Add code to use script directory
        new_lines.append(' ' * indent + '# Auto-fix: Use script directory for template files\n')
        new_lines.append(' ' * indent + 'script_dir = os.path.dirname(os.path.abspath(__file__))\n')
        new_lines.append(' ' * indent + 'self.template_path = os.path.join(script_dir, "example_Good.xlsx")\n')
        modified = True
        print(f"✅ Modified line {i+1}: Added script directory path resolution")
        # Skip the original line we just replaced
        continue
    else:
        new_lines.append(line)

if modified:
    # Write modified file
    print("\nWriting modified est_converter.py...")
    with open('est_converter.py', 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(new_lines)
    
    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print("""
✅ Template path has been fixed!

The program will now look for template files in the same directory
as the script, regardless of where you run it from.

Changes made:
  - Backup created: est_converter.py.backup
  - Template path now uses script directory

To undo this fix:
  - Delete est_converter.py
  - Rename est_converter.py.backup to est_converter.py

Now try running: python est_converter.py
""")
else:
    print("\n⚠️  Could not find the template path line to modify.")
    print("The code structure may be different than expected.")
    print("\nNo changes were made.")

print("=" * 70)
input("\nPress Enter to exit...")
