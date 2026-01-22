#!/usr/bin/env python3
"""Quick test to verify encoding fix"""
import sys
sys.path.insert(0, '.')

from est_converter import parse_fluke_file

def test_file(csv_path):
    print(f"Testing: {csv_path}")
    print("-" * 60)
    
    parsed, error = parse_fluke_file(csv_path)
    
    if error:
        print(f"❌ ERROR: {error}")
        return False
    else:
        print(f"✅ SUCCESS!")
        print(f"Equipment: {parsed.equipment}")
        print(f"Tester S/N: {parsed.tester_sn}")
        print(f"Template: {parsed.template}")
        print(f"Measurements: {len(parsed.measurements)}")
        return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_file(sys.argv[1])
    else:
        print("Usage: python quick_test.py <csv_file>")
