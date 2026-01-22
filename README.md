# EST Converter Baseline (V3.3)

## Overview

EST Converter is a desktop application that converts Fluke ESA615 electrical safety test results (CSV format) into standardized Interface Transactions XLSX format for upload and compliance tracking.

**Version:** 3.3 Baseline
**Purpose:** Fixed baseline behavior ensuring consistent output for AS/NZS 3551 and AS/NZS 3760 standards.

## Key Features

- **Input:** Fluke ESA615 exported CSV files
- **Output:** Single consolidated XLSX file (EST_UPLOAD_YYYYMMDD_HHMMSS.xlsx)
- **Standards Support:** AS/NZS 3551 and AS/NZS 3760
- **Fixed Limits:** Uses predefined limits from EST_Limits_Summary.xlsx (ignores Fluke CSV limits)
- **Asset Mapping:** Maps Tester S/N to Asset Number via EST Tester.xlsx
- **Error Tracking:** Generates error CSV for failed conversions

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Required packages:
- PySide6 (UI framework)
- openpyxl (Excel file handling)
- python-dateutil (Date parsing)

### Required Files (Same Directory as Script)

The following files must be present in the same directory as `est_converter.py`:

1. **example_Good.xlsx** - Output template file
2. **EST Tester.xlsx** - Tester S/N to Asset Number mapping
3. **EST_Limits_Summary.xlsx** - Fixed limits data source

### Optional UI Resources

- **hnz_logo.png** - Company logo (displayed in UI)
- **est_icon.ico** - Application icon

## Usage

### Running the Application

```bash
python est_converter.py
```

### Workflow

1. **Add CSV Files:**
   - Click "Add Files" or drag-and-drop CSV files into the list
   - Hover over filenames to see full paths

2. **Select Output Folder:**
   - Click "Browse" to choose where output files will be saved

3. **Convert:**
   - Click "Convert" to process all files
   - Progress is shown in real-time
   - Success/error summary displayed on completion

### Output Files

**Success:**
- `EST_UPLOAD_YYYYMMDD_HHMMSS.xlsx` - Converted data

**Errors (if any):**
- `EST_ERRORS_YYYYMMDD_HHMMSS.csv` - List of files that failed conversion with error messages

## Core Promises (Baseline Contract)

The following behaviors are **guaranteed** and must not be broken in future versions:

### 1. Output File Format
- **Filename:** EST_UPLOAD_YYYYMMDD_HHMMSS.xlsx
- **Structure:** Copy of example_Good.xlsx template with data rows appended at bottom

### 2. Output Field Format

Each measurement field uses this format (as string):

```
<value>,<Pass/Failed>,<limit>,<unit>
```

- **value:** Numeric value from Fluke measurement
- **Pass/Failed:** P or F based on test result
- **limit:** Fixed limit from EST_Limits_Summary.xlsx or defaults
- **unit:** Ohms / MOhms / uA (with voltage label for insulation)

### 3. Standard Inference Rules

Standard is inferred from Template Name:
1. Contains "3760" → AS/NZS 3760
2. Contains "3551" → AS/NZS 3551
3. "NO EARTH" + "DOMESTIC" → 3760
4. "NO EARTH" (non-domestic) → 3551
5. Token "1D/2D/5D" → 3760
6. Token "5B/5BF/5CF/5C" or "TYPE BF/CF/B" → 3551
7. **Inference fails → File fails (no output row)**

### 4. ClassType Inference Rules

Derived from Template Name + Standard:
- NO EARTH DOMESTIC → 5D
- NO EARTH + (5CF & (5BF or BF)) → 5CF&5BF
- NO EARTH + NO AP → 5
- NO EARTH + TYPE CF → 5CF
- NO EARTH + TYPE BF → 5BF
- NO EARTH + TYPE B → 5B
- Non-NO EARTH:
  - 3760 → `<base>D` (e.g., 1D, 2D)
  - 3551 → `<base>BF/CF/B` based on template keywords

### 5. Fixed Limits (Never Trust Fluke Limits)

**AS/NZS 3551 (Earthed Classes):**
- Earth Bond: 0.2 Ohms
- Insulation: 1.0 MOhms (with voltage label: MOhms [250V] or MOhms [500V])
- Leakage limits from EST_Limits_Summary.xlsx or defaults

**AS/NZS 3760:**
- Earth Bond (earthed): 1 Ohms
- Insulation: 1.0 MOhms
- Earth Leakage NC: 5000 uA
- Enclosure Leakage Class 2 NC: 1000 uA
- Patient Leakage / Mains on Applied Parts: **NA** (baseline simplification)

### 6. Legitimate NA Values

The following NA outputs are **correct** baseline behavior:
- 3760 tests with no patient leakage / mains on applied parts (simplified)
- Missing measurement groups (not in Fluke template)
- No earth class earth bond (class_is_earthed=False)

## Code Structure

### Layered Architecture (Single File)

**1. Pure Rules Layer** (No UI mixing)
- Template Name → Standard / ClassType inference
- Limits reading and field limit decisions
- Condition normalization (NC/NO/EO)
- Measurement group canonicalization

**2. Parsing Layer** (CSV → Parsed Model)
- CSV row reading
- Results header location
- Value/status column identification
- FlukeParsed + measurements generation

**3. Mapping Layer** (Parsed → InterfaceRow)
- Group/condition-based field writing
- InterfaceRow generation

**4. Output Layer** (Append to template XLSX)
- Template workbook loading
- Row appending
- New XLSX saving

**5. UI Layer**
- File list (drag-drop support, tooltips)
- Output directory selection
- Template selection
- Convert button trigger

### Key Data Models

```python
FlukeParsed:
  - operator
  - equipment
  - tester_sn
  - template
  - dt
  - measurements (list of Measurement)

Measurement:
  - group (canonical)
  - cond (normalized)
  - subtest
  - value (cleaned)
  - pf (Pass/Fail)

InterfaceRow:
  - 22 fixed output columns
```

## CSV Parsing Rules

### Header Identification
- Locate results area by finding row where first column = "Test Name" and contains "Value"
- Value/status columns identified via fuzzy matching
- Fallback: value=column 5, status=column 8

### Group Canonicalization

Raw Fluke group names are normalized to:
- `G_PROT_EARTH_RES` (Earth Bond)
- `G_MAINS_V_LN` (Mains Voltage L-N)
- `G_MAINS_V_NE` (Mains Voltage N-E)
- `G_INSULATION` (Insulation Resistance)
- `G_EARTH_LEAK` (Earth Leakage)
- `G_ENC_LEAK` (Enclosure Leakage)
- `G_PATIENT_LEAK` (Patient/Applied Part Leakage)
- `G_MAINS_ON_AP` (Mains on Applied Parts)

### Condition Normalization

Standardizes to:
- `NORMAL CONDITION`
- `OPEN NEUTRAL`
- `OPEN EARTH`

## Output Field Mapping

### Line Load
Requires both mains LN and mains NE values:
```
<LN>V [L-N=<NE>V][Load=0.0kVA]
```
If either missing → NA

### Field Sources
- **Earth Bond:** G_PROT_EARTH_RES
- **Insulation:** G_INSULATION
- **Earth Leakage:** G_EARTH_LEAK + condition (NC/NO)
- **Enclosure Leakage:** G_ENC_LEAK + condition (NC/NO/EO)
- **Applied Part Leakage:** G_PATIENT_LEAK + condition (NC/NO/EO)
- **Mains Contact:** G_MAINS_ON_AP
- **Pass/Fail:** Any measurement Fail → Row Fail, else Pass

## Error Handling

### Error File
`EST_ERRORS_YYYYMMDD_HHMMSS.csv`

Format: File, Error

### Failure Conditions

File will not produce output row if:
- Missing Equipment Number / Tester S/N / DateTime
- Cannot identify results header
- Template Name inference fails
- build_interface_row returns errors

## Extension Development Principles

**For AI/Developers working on future enhancements:**

### DO NOT MODIFY (Without Regression Proof)

The following four core functions are **protected**:
1. `parse_fluke_file()`
2. `build_interface_row()`
3. `load_fixed_limits_from_summary()` / `get_fixed_limit_for_field()`
4. `append_rows_to_template()`

**Allowed changes:**
- Refactoring with identical output behavior
- Adding unit tests
- Extracting string constants
- Modularization (separate files)

**Requires regression proof:**
- Any change affecting output format
- New field mapping logic
- Limit calculation changes

### UI Changes - Free to Modify

UI can be changed without restriction as long as:
- Conversion pipeline calls remain identical
- Default behaviors unchanged
- Template file paths still work

### New Input Sources (DTA/Serial)

Must follow the "equivalence principle":
- New sources should produce FlukeParsed equivalent to CSV parsing
- NO special cases in `build_interface_row()` for new sources
- All input types go through same mapping layer

## Regression Testing Recommendations

### Minimum Regression Set (6 CSV files)

Coverage:
- 3551 Class 1 BF / CF
- 3551 NO EARTH (5BF/5CF/5CF&5BF/5D)
- 3760 1D / 2D
- 250V insulation template
- Patient leakage structured rows (NC/EO/NO)

### Regression Assertions

Automated or manual checklist:
- ✓ Output column count/order unchanged
- ✓ TestSeq correctly strips `_#### - ` prefix
- ✓ Earth bond limit = 0.2 (3551 earthed) / 1 (3760 earthed)
- ✓ Insulation limit = 1.0
- ✓ Line Load not all NA (for templates with mains data)
- ✓ Patient leakage NC/EO/NO fields not mixed/misplaced

**Rollback trigger:** Output diff shows NA increase or field misalignment

## Deployment

### Standalone Executable (Optional)

Package as single EXE using PyInstaller:

```bash
pyinstaller --onefile --windowed --name="EST_Converter" est_converter.py
```

Include required files alongside EXE:
- example_Good.xlsx
- EST Tester.xlsx
- EST_Limits_Summary.xlsx
- hnz_logo.png (optional)
- est_icon.ico (optional)

## Support

For issues or questions, contact the development team or file an issue in the project repository.

## License

Internal tool for compliance testing. All rights reserved.
