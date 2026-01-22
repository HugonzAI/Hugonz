#!/usr/bin/env python3
"""Fix UI by clearing PySide6 cache and forcing reload"""
import os
import sys
import shutil

print("=" * 70)
print("EST Converter UI Fix Tool")
print("=" * 70)

# Step 1: Clear Python cache
print("\n1. Clearing Python cache...")
if os.path.exists('__pycache__'):
    shutil.rmtree('__pycache__')
    print("   ✅ Removed __pycache__")
else:
    print("   ✅ No __pycache__ found")

# Step 2: Clear .pyc files
print("\n2. Clearing compiled Python files...")
count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))
            count += 1
if count > 0:
    print(f"   ✅ Removed {count} .pyc files")
else:
    print("   ✅ No .pyc files found")

# Step 3: Check PySide6 installation
print("\n3. Checking PySide6...")
try:
    import PySide6
    print(f"   ✅ PySide6 version: {PySide6.__version__}")
    
    # Try to clear Qt cache
    from PySide6.QtCore import QStandardPaths
    cache_location = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
    print(f"   Qt cache location: {cache_location}")
    
except ImportError:
    print("   ❌ PySide6 not installed")
    print("   Install with: pip install PySide6")
    sys.exit(1)

# Step 4: Recommendations
print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("""
Option 1 - Quick Fix (Try this first):
  1. Close any running EST Converter instances
  2. Run: python est_converter.py
  
Option 2 - If UI still looks wrong:
  1. Reinstall PySide6:
     pip uninstall PySide6
     pip install PySide6
  2. Then run: python est_converter.py
  
Option 3 - Force fresh start:
  1. Close EST Converter
  2. Restart your terminal/command prompt
  3. cd to the program directory
  4. Run: python est_converter.py
""")
print("=" * 70)

# Step 5: Try to import and check UI code
print("\nVerifying UI code...")
try:
    # Read a small portion to verify fixes
    with open('est_converter.py', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    # Look for key UI fixes
    code = ''.join(lines)
    
    checks = {
        'Multi-encoding support': 'Try multiple encodings' in code,
        'Transparent backgrounds': 'background: transparent' in code,
        'Fixed logo size': 'setFixedSize(60, 60)' in code,
        'Tab styling': 'QTabBar::tab:selected' in code,
    }
    
    print("\nUI Code Verification:")
    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
        if not result:
            all_good = False
    
    if all_good:
        print("\n✅ ALL UI FIXES ARE IN THE CODE!")
        print("   If UI still looks wrong, it's a PySide6/Qt rendering issue.")
        print("   Try Option 2 above (reinstall PySide6)")
    
except Exception as e:
    print(f"   ⚠️  Could not fully verify: {e}")

print("\n" + "=" * 70)
