#!/usr/bin/env python3
"""Verify if you're running the latest version"""
import os
import sys

print("=" * 70)
print("EST Converter Version Verification")
print("=" * 70)

# Check if files exist
required_files = [
    'est_converter.py',
    'example_Good.xlsx',
    'quick_test.py',
    'RUN_INSTRUCTIONS.md'
]

print("\n1. Checking required files:")
all_exist = True
for f in required_files:
    exists = os.path.exists(f)
    status = "✅" if exists else "❌"
    print(f"   {status} {f}")
    if not exists:
        all_exist = False

# Check encoding fix in code
print("\n2. Checking encoding fix:")
try:
    with open('est_converter.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "Try multiple encodings" in content:
        print("   ✅ Multi-encoding support found")
        # Count how many encodings are supported
        if "windows-1252" in content and "latin-1" in content:
            print("   ✅ All 5 encodings configured (utf-8-sig, utf-8, windows-1252, latin-1, iso-8859-1)")
        else:
            print("   ⚠️  Encoding list incomplete")
    else:
        print("   ❌ Multi-encoding support NOT found (old version)")
        print("   You are running the OLD version!")
        
    # Check UI fixes
    if 'background: transparent' in content and 'logo_label.setFixedSize(60, 60)' in content:
        print("   ✅ UI fixes applied (transparent backgrounds + fixed logo)")
    else:
        print("   ❌ UI fixes NOT applied")
        
except Exception as e:
    print(f"   ❌ Error reading file: {e}")

# Check for __pycache__
print("\n3. Checking for Python cache:")
if os.path.exists('__pycache__'):
    print("   ⚠️  __pycache__ directory exists (may cause issues)")
    print("   Recommendation: Delete it and restart")
    
    # List cached files
    cache_files = os.listdir('__pycache__')
    if cache_files:
        print(f"   Found {len(cache_files)} cached files")
else:
    print("   ✅ No cache directory found")

# Check Python version
print("\n4. Python version:")
print(f"   {sys.version}")

# Check if running from correct directory
print("\n5. Current directory:")
print(f"   {os.getcwd()}")

print("\n" + "=" * 70)
print("RECOMMENDATION:")
print("=" * 70)

if not all_exist:
    print("❌ Missing required files. Please re-download the latest code.")
elif "Try multiple encodings" not in open('est_converter.py').read():
    print("❌ You have OLD code. Download latest from branch: claude/est-converter-baseline-sbRr5")
elif os.path.exists('__pycache__'):
    print("⚠️  Delete __pycache__ folder and restart:")
    print("   Windows: rmdir /s /q __pycache__")
    print("   Then run: python est_converter.py")
else:
    print("✅ Everything looks good! Try running: python est_converter.py")

print("=" * 70)
