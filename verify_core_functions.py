#!/usr/bin/env python3
"""Verify core functions are intact and not corrupted"""
import sys
import os

print("=" * 80)
print("Core Functions Integrity Check")
print("=" * 80)

# Check if file exists
if not os.path.exists('est_converter.py'):
    print("❌ est_converter.py not found!")
    sys.exit(1)

# Read the file
with open('est_converter.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("\n1. Checking protected core functions...")

# Core functions that must exist
required_functions = {
    'parse_fluke_file': 'Parse Fluke CSV files',
    'build_interface_row': 'Build interface row from parsed data',
    'load_fixed_limits_from_summary': 'Load limits from summary file',
    'append_rows_to_template': 'Append rows to template XLSX',
    'canonical_group': 'Canonical group mapping',
    'normalize_condition': 'Normalize condition codes',
}

all_good = True
for func_name, description in required_functions.items():
    if f'def {func_name}(' in content:
        print(f"  ✅ {func_name}: Found")
    else:
        print(f"  ❌ {func_name}: MISSING! ({description})")
        all_good = False

print("\n2. Checking critical code patterns...")

# Critical patterns that must exist
critical_patterns = {
    'Try multiple encodings': 'Multi-encoding CSV support',
    'canonical_group': 'Group canonicalization',
    'G_PROT_EARTH_RES': 'Canonical group constants',
    'FlukeParsed': 'Data model',
    'InterfaceRow': 'Output data model',
    'PySide6': 'GUI framework',
}

for pattern, description in critical_patterns.items():
    if pattern in content:
        print(f"  ✅ {pattern}: Found ({description})")
    else:
        print(f"  ❌ {pattern}: MISSING! ({description})")
        all_good = False

print("\n3. Checking for suspicious modifications...")

# Patterns that suggest AI "optimization"
suspicious_patterns = [
    ('TODO:', 'AI-generated TODOs'),
    ('# pylint:', 'AI linter suggestions'),
    ('# type: ignore', 'Excessive type ignores'),
    ('# noqa', 'Excessive noqa comments'),
]

found_suspicious = []
for pattern, desc in suspicious_patterns:
    count = content.count(pattern)
    if count > 5:  # More than 5 is suspicious
        found_suspicious.append(f"{desc}: {count} occurrences")
        print(f"  ⚠️  {pattern}: {count} occurrences ({desc})")

print("\n4. Code statistics...")
lines = content.split('\n')
print(f"  Total lines: {len(lines)}")
print(f"  Function definitions: {content.count('def ')}")
print(f"  Class definitions: {content.count('class ')}")

print("\n" + "=" * 80)
print("RESULT:")
print("=" * 80)

if all_good and not found_suspicious:
    print("✅ ALL CHECKS PASSED - Core functions are intact!")
    print("\nIf you're still seeing issues (NA values in output),")
    print("it's likely a data mapping problem, not code corruption.")
    print("\nRun this to diagnose:")
    print("  python diagnose_conversion.py your_file.csv")
elif all_good and found_suspicious:
    print("⚠️  CORE FUNCTIONS OK, but suspicious patterns found")
    print("\nSuspicious items:")
    for item in found_suspicious:
        print(f"  - {item}")
    print("\nThese might be AI-added comments/annotations.")
    print("They probably don't affect functionality.")
else:
    print("❌ CRITICAL: Core functions are MISSING or CORRUPTED!")
    print("\nYou need to restore from a clean backup:")
    print("  git reset --hard 5a1a921")
    print("  git push --force origin claude/est-converter-baseline-sbRr5")

print("=" * 80)
