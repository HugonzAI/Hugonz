# EST Converter Required Template Files

This document describes the structure and requirements for the three Excel template files needed by EST Converter.

## Overview

EST Converter requires three Excel files to be present in the same directory as the application:

1. **example_Good.xlsx** - Output template
2. **EST Tester.xlsx** - Tester S/N to Asset Number mapping
3. **EST_Limits_Summary.xlsx** - Fixed limits reference

## 1. example_Good.xlsx (Output Template)

### Purpose
This file serves as the template for the output XLSX file. The converter copies this template and appends new data rows at the bottom.

### Structure

**Sheet:** Any name (uses active sheet)

**Columns (22 total):**

| Column | Field Name | Description |
|--------|------------|-------------|
| A | Operator | Person who performed the test |
| B | Equipment Number | Asset/equipment identifier |
| C | Asset Number | Tester asset number (mapped from S/N) |
| D | Standard | AS/NZS 3551 or AS/NZS 3760 |
| E | Test Type | Usually "Routine" |
| F | Class Type | 1D, 2D, 5BF, 5CF, etc. |
| G | Test Seq | Template name (cleaned) |
| H | Test Date | DD/MM/YYYY format |
| I | Visual Pass/Fail | P or F |
| J | Line Load | `<LN>V [L-N=<NE>V][Load=0.0kVA]` |
| K | Earth Bond | `<value>,<Pass/Failed>,<limit>,Ohms` |
| L | Insulation | `<value>,<Pass/Failed>,<limit>,MOhms [voltage]` |
| M | Earth Leakage NC | `<value>,<Pass/Failed>,<limit>,uA` |
| N | Earth Leakage NO | `<value>,<Pass/Failed>,<limit>,uA` |
| O | Enclosure Leakage NC | `<value>,<Pass/Failed>,<limit>,uA` |
| P | Enclosure Leakage NO | `<value>,<Pass/Failed>,<limit>,uA` |
| Q | Enclosure Leakage EO | `<value>,<Pass/Failed>,<limit>,uA` |
| R | Applied Part Leakage NC | `<value>,<Pass/Failed>,<limit>,uA` |
| S | Applied Part Leakage NO | `<value>,<Pass/Failed>,<limit>,uA` |
| T | Applied Part Leakage EO | `<value>,<Pass/Failed>,<limit>,uA` |
| U | Mains Contact | `<value>,<Pass/Failed>,<limit>,uA` |
| V | Overall Pass/Fail | P or F |

### Example Row

```
John Doe | EQ12345 | A-0123 | AS/NZS 3551 | Routine | 1BF | Class 1 BF Test | 22/01/2026 | P | 240V [L-N=0.5V][Load=0.0kVA] | 0.15,Pass,0.2,Ohms | 120,Pass,1.0,MOhms [250V] | 450,Pass,5000,uA | NA | 320,Pass,500,uA | NA | NA | 180,Pass,500,uA | NA | NA | 15000,Pass,25000,uA | P
```

### Notes
- The template can contain header rows and existing data rows
- EST Converter appends new rows starting at `max_row + 1`
- No existing rows are modified or deleted
- If template has formatting/styles, they are preserved (though new rows use default formatting)

---

## 2. EST Tester.xlsx (Tester Mapping)

### Purpose
Maps Fluke tester serial numbers to asset numbers for tracking and inventory management.

### Structure

**Sheet:** Any name (uses active sheet)

**Required Columns (order doesn't matter):**

| Column Header | Description | Example |
|---------------|-------------|---------|
| Serial Number (or S/N) | Fluke tester serial number | 4212345 |
| Asset Number | Organization's asset tracking number | A-0123 |

### Example

| Serial Number | Asset Number | Location | Notes |
|---------------|--------------|----------|-------|
| 4212345 | A-0123 | Building A | ESA615 Unit 1 |
| 4212346 | A-0124 | Building B | ESA615 Unit 2 |
| 4212347 | A-0125 | Mobile Lab | ESA615 Unit 3 |

### Header Detection
- The converter searches the first 10 rows for headers
- Matches columns containing:
  - "SERIAL" or "S/N" (case-insensitive)
  - "ASSET" (case-insensitive)
- Data is read from the row immediately after the header

### Fallback Behavior
If a tester S/N is not found in this file, the converter uses the S/N itself as the Asset Number.

### Notes
- Only the first sheet is read
- Extra columns (Location, Notes, etc.) are ignored
- Blank rows are skipped
- Case-insensitive matching for headers

---

## 3. EST_Limits_Summary.xlsx (Fixed Limits)

### Purpose
Defines fixed test limits for different standards, class types, and measurement fields. These limits override any limits present in the Fluke CSV files.

### Structure

**Sheet:** "Summary" (preferred) or active sheet

**Required Columns (order doesn't matter):**

| Column Header | Description | Example |
|---------------|-------------|---------|
| Standard | AS/NZS 3551 or AS/NZS 3760 | AS/NZS 3551 |
| ClassType | Class type identifier | 1BF |
| Field | Field name (lowercase) | earth_bond |
| Limit | Numeric limit value (as text) | 0.2 |

### Valid Field Names

| Field Name | Description | Unit |
|------------|-------------|------|
| earth_bond | Protective earth resistance | Ohms |
| insulation | Insulation resistance | MOhms |
| earth_leakage_nc | Earth leakage (normal condition) | uA |
| earth_leakage_no | Earth leakage (open neutral) | uA |
| enclosure_leakage_nc | Enclosure leakage (normal) | uA |
| enclosure_leakage_no | Enclosure leakage (open neutral) | uA |
| enclosure_leakage_eo | Enclosure leakage (open earth) | uA |
| patient_leakage_nc | Patient leakage (normal) | uA |
| patient_leakage_no | Patient leakage (open neutral) | uA |
| patient_leakage_eo | Patient leakage (open earth) | uA |
| mains_contact | Mains on applied parts | uA |

### Example

| Standard | ClassType | Field | Limit | Notes |
|----------|-----------|-------|-------|-------|
| AS/NZS 3551 | | earth_bond | 0.2 | All earthed 3551 |
| AS/NZS 3551 | | insulation | 1.0 | All 3551 |
| AS/NZS 3551 | 1BF | patient_leakage_nc | 500 | Class 1 BF NC |
| AS/NZS 3551 | 1BF | patient_leakage_no | 500 | Class 1 BF NO |
| AS/NZS 3551 | 1CF | patient_leakage_nc | 100 | Class 1 CF NC |
| AS/NZS 3760 | | earth_bond | 1 | All earthed 3760 |
| AS/NZS 3760 | | insulation | 1.0 | All 3760 |
| AS/NZS 3760 | | earth_leakage_nc | 5000 | 3760 earth leak NC |
| AS/NZS 3760 | 2D | enclosure_leakage_nc | 1000 | Class 2 enclosure NC |

### Lookup Logic

When determining a limit, the converter uses this priority:

1. **Exact match:** `Standard|ClassType|Field`
   - Example: `AS/NZS 3551|1BF|patient_leakage_nc`

2. **Generic match:** `Standard||Field` (empty ClassType)
   - Example: `AS/NZS 3551||earth_bond`

3. **Default hardcoded values** (if file missing or no match)

### Default Hardcoded Limits

**AS/NZS 3551:**
- earth_bond: 0.2 Ohms
- insulation: 1.0 MOhms
- earth_leakage_nc/no: 5000 uA
- enclosure_leakage_nc/no/eo: 500 uA
- patient_leakage_nc/no/eo: 500 uA
- mains_contact: 25000 uA

**AS/NZS 3760:**
- earth_bond: 1 Ohms
- insulation: 1.0 MOhms
- earth_leakage_nc/no: 5000 uA
- enclosure_leakage_nc/no/eo: 1000 uA (Class 2)
- patient_leakage: NA (not applicable - baseline simplification)
- mains_contact: NA (not applicable - baseline simplification)

### Header Detection
- Searches first 10 rows for "Standard" and "Field" keywords
- Case-insensitive matching
- Data read from row immediately after header

### Notes
- ClassType can be blank (empty string) for generic standard-wide limits
- Extra columns are ignored
- Blank rows are skipped
- If file is missing, converter falls back to hardcoded defaults
- Limits are stored as strings (not converted to numbers)

---

## Creating Template Files

### Quick Start Templates

If you don't have existing template files, you can create minimal versions:

#### example_Good.xlsx
1. Create new Excel workbook
2. Add header row with 22 column names (see structure above)
3. Optionally add example data rows
4. Save as `example_Good.xlsx`

#### EST Tester.xlsx
1. Create new Excel workbook
2. Add headers: "Serial Number" and "Asset Number"
3. Add rows with your tester S/N and asset numbers
4. Save as `EST Tester.xlsx`

#### EST_Limits_Summary.xlsx
1. Create new Excel workbook
2. Rename first sheet to "Summary" (optional)
3. Add headers: "Standard", "ClassType", "Field", "Limit"
4. Add rows for limits you want to customize
5. Save as `EST_Limits_Summary.xlsx`

**Note:** If you only create example_Good.xlsx, the converter will still work using:
- Tester S/N as Asset Number
- Hardcoded default limits

---

## File Location Requirements

All three template files MUST be in the same directory as:
- `est_converter.py` (if running script)
- `est_converter.exe` (if using packaged executable)

### Example Directory Structure

```
/path/to/converter/
├── est_converter.py          (or .exe)
├── example_Good.xlsx          ← Required
├── EST Tester.xlsx           ← Required
├── EST_Limits_Summary.xlsx   ← Required
├── hnz_logo.png              (optional)
├── est_icon.ico              (optional)
└── requirements.txt          (for Python script)
```

---

## Troubleshooting

### "Template file not found"
- Ensure `example_Good.xlsx` exists in the same directory as the converter
- Check file name spelling (case-sensitive on some systems)

### "Tester mapping not loaded"
- Check `EST Tester.xlsx` exists
- Verify headers contain "Serial" or "S/N" and "Asset"
- If missing, converter will use S/N as Asset Number (non-fatal)

### "Limits not loaded"
- Check `EST_Limits_Summary.xlsx` exists
- Verify sheet named "Summary" exists (or uses first sheet)
- Verify headers contain "Standard" and "Field"
- If missing, converter uses hardcoded defaults (non-fatal)

### Incorrect limits in output
- Check Field names in limits file match exactly (lowercase)
- Verify Standard names: "AS/NZS 3551" or "AS/NZS 3760" (exact match)
- Check ClassType matches your test templates (or leave blank for generic)

---

## Validation Checklist

Before running EST Converter, verify:

- [ ] `example_Good.xlsx` exists and has 22 columns
- [ ] `EST Tester.xlsx` exists with Serial Number and Asset Number columns
- [ ] `EST_Limits_Summary.xlsx` exists with Standard, ClassType, Field, Limit columns
- [ ] All three files are in the same directory as `est_converter.py` (or .exe)
- [ ] Files are not open in Excel (prevents write access)
- [ ] Files are not read-only

---

## Advanced: Programmatic Generation

For large deployments, you can generate these files programmatically:

```python
from openpyxl import Workbook

# Generate example_Good.xlsx
wb = Workbook()
ws = wb.active
ws.append(['Operator', 'Equipment Number', 'Asset Number', 'Standard',
           'Test Type', 'Class Type', 'Test Seq', 'Test Date',
           'Visual Pass/Fail', 'Line Load', 'Earth Bond', 'Insulation',
           'Earth Leakage NC', 'Earth Leakage NO', 'Enclosure Leakage NC',
           'Enclosure Leakage NO', 'Enclosure Leakage EO',
           'Applied Part Leakage NC', 'Applied Part Leakage NO',
           'Applied Part Leakage EO', 'Mains Contact', 'Overall Pass/Fail'])
wb.save('example_Good.xlsx')

# Generate EST Tester.xlsx
wb = Workbook()
ws = wb.active
ws.append(['Serial Number', 'Asset Number'])
ws.append(['4212345', 'A-0123'])
wb.save('EST Tester.xlsx')

# Generate EST_Limits_Summary.xlsx
wb = Workbook()
ws = wb.active
ws.title = 'Summary'
ws.append(['Standard', 'ClassType', 'Field', 'Limit'])
ws.append(['AS/NZS 3551', '', 'earth_bond', '0.2'])
ws.append(['AS/NZS 3551', '', 'insulation', '1.0'])
ws.append(['AS/NZS 3760', '', 'earth_bond', '1'])
ws.append(['AS/NZS 3760', '', 'insulation', '1.0'])
wb.save('EST_Limits_Summary.xlsx')
```

---

## Contact

For questions about template file structure or issues with file loading, contact the development team or refer to README.md.
