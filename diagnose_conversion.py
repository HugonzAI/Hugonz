#!/usr/bin/env python3
"""Diagnose why conversion produces NA values"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from est_converter import parse_fluke_file, build_interface_row

def diagnose_csv(csv_path):
    """Detailed diagnosis of CSV parsing and conversion"""
    print("=" * 80)
    print("CSV Conversion Diagnosis")
    print("=" * 80)
    print(f"\nFile: {csv_path}\n")
    
    # Step 1: Parse the CSV
    print("Step 1: Parsing CSV file...")
    parsed, error = parse_fluke_file(csv_path)
    
    if error:
        print(f"❌ PARSING FAILED: {error}")
        return False
    
    print("✅ Parsing successful!")
    print(f"\nExtracted Metadata:")
    print(f"  Operator: {parsed.operator}")
    print(f"  Equipment: {parsed.equipment}")
    print(f"  Tester S/N: {parsed.tester_sn}")
    print(f"  Template: {parsed.template}")
    print(f"  Date/Time: {parsed.dt}")
    print(f"  Measurements: {len(parsed.measurements)} found")
    
    if len(parsed.measurements) == 0:
        print("\n❌ PROBLEM: No measurements extracted!")
        print("   This is why all fields show NA")
        print("\n   Possible reasons:")
        print("   1. Results header not found in CSV")
        print("   2. Test names don't match expected format")
        print("   3. Column mapping incorrect")
        return False
    
    # Step 2: Show measurements details
    print(f"\n{'='*80}")
    print("Step 2: Measurements Details")
    print(f"{'='*80}")
    
    # Group by canonical group
    from collections import defaultdict
    by_group = defaultdict(list)
    for m in parsed.measurements:
        by_group[m.group].append(m)
    
    print(f"\nMeasurements grouped by test type:")
    for group, measurements in by_group.items():
        print(f"\n  {group}: {len(measurements)} measurements")
        for m in measurements[:3]:  # Show first 3
            print(f"    - Cond: {m.cond}, Subtest: {m.subtest[:40]}, Value: {m.value}, P/F: {m.pf}")
        if len(measurements) > 3:
            print(f"    ... and {len(measurements)-3} more")
    
    # Step 3: Test build_interface_row
    print(f"\n{'='*80}")
    print("Step 3: Testing Interface Row Mapping")
    print(f"{'='*80}")
    
    try:
        interface_row = build_interface_row(parsed)
        print("✅ Interface row built successfully!")
        
        # Count how many fields are populated
        fields_with_data = 0
        fields_with_na = 0
        
        print(f"\nInterface Row Fields:")
        for field_name, value in vars(interface_row).items():
            if value and value != "NA":
                fields_with_data += 1
                status = "✅"
            else:
                fields_with_na += 1
                status = "❌"
            
            # Show first 20 chars of value
            value_str = str(value)[:40] if value else "NA"
            print(f"  {status} {field_name}: {value_str}")
        
        print(f"\n{'='*80}")
        print("SUMMARY:")
        print(f"{'='*80}")
        print(f"  Fields with data: {fields_with_data}")
        print(f"  Fields with NA: {fields_with_na}")
        
        if fields_with_na > fields_with_data:
            print(f"\n❌ PROBLEM: Most fields are NA!")
            print(f"\n   Common causes:")
            print(f"   1. Field name mapping doesn't match measurement groups")
            print(f"   2. Condition codes don't match expected values")
            print(f"   3. Standard/ClassType inference failed")
            
    except Exception as e:
        print(f"❌ ERROR building interface row: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n{'='*80}")
    print("NEXT STEPS:")
    print(f"{'='*80}")
    
    if len(parsed.measurements) == 0:
        print("""
To fix 'No measurements' issue:
  1. Open the CSV file and check the format
  2. Look for 'TEST NAME' header row
  3. Ensure test results follow this header
  4. Send me a sample of your CSV file structure
""")
    elif fields_with_na > fields_with_data:
        print("""
To fix 'Too many NA' issue:
  1. Check if Standard was correctly inferred
  2. Check if ClassType was correctly inferred  
  3. Verify canonical group names match your test names
  4. Send me the 'Measurements Details' output above
""")
    else:
        print("""
✅ Conversion looks good!
   If you still see NA in output, it might be:
   1. Template file structure issue
   2. Column ordering in template
""")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        if os.path.exists(csv_file):
            diagnose_csv(csv_file)
        else:
            print(f"❌ File not found: {csv_file}")
    else:
        print("Usage: python diagnose_conversion.py <csv_file>")
        print("\nExample:")
        print("  python diagnose_conversion.py WHA252760-30_07_2024-13_06.csv")
