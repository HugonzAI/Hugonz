# Changelog

All notable changes to EST Converter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2026-01-22

### Added
- Initial baseline implementation of EST Converter V3.3
- Fluke ESA615 CSV parsing with flexible header detection
- Standard inference from Template Name (AS/NZS 3551 and AS/NZS 3760)
- ClassType inference with comprehensive rules
- Fixed limits loading from EST_Limits_Summary.xlsx with fallback defaults
- Tester S/N to Asset Number mapping from EST Tester.xlsx
- InterfaceTransactions XLSX output generation
- PySide6 GUI with drag-and-drop file support
- Error tracking and error CSV generation
- Group canonicalization (8 measurement groups)
- Condition normalization (NC/NO/EO)
- Comprehensive field mapping for all output columns
- Line Load calculation from mains voltage measurements
- Voltage label preservation in insulation results
- Overall Pass/Fail determination
- Background conversion thread for responsive UI
- Progress tracking during conversion

### Core Promises (Protected Functions)
- `parse_fluke_file()` - CSV parsing
- `build_interface_row()` - Field mapping logic
- `load_fixed_limits_from_summary()` / `get_fixed_limit_for_field()` - Limits handling
- `append_rows_to_template()` - Output generation

### Documentation
- README.md with comprehensive usage guide
- TEMPLATE_FILES.md documenting required Excel file structures
- Inline code documentation following V3.3 specification
- Clear layer separation in code architecture

### Standards Compliance
- AS/NZS 3551 full support (Classes 1-5, BF/CF/B types)
- AS/NZS 3760 support (Classes 1D/2D/5D)
- Baseline simplification: 3760 patient leakage/mains contact → NA

### Dependencies
- PySide6 >= 6.5.0
- openpyxl >= 3.1.0
- python-dateutil >= 2.8.0

## [Unreleased]

### Planned
- ESA612 support
- Direct tester connection (serial/USB)
- DTA mode integration
- EAM system upload integration
- Batch processing improvements
- Enhanced error diagnostics
- Regression test suite
- Unit tests for core functions

---

## Version History Notes

### Version 3.3 Baseline
This is the first stable baseline release. All future changes must maintain backward compatibility with the core promises and output format defined in this version.

### Breaking Changes Policy
Any modifications to the four protected core functions require:
1. Full regression testing with minimum 6-file test set
2. Verification that output format remains identical
3. Documentation of any intentional behavior changes
4. Approval from project maintainer

### Extension Guidelines
- UI changes: Free to modify
- New input sources: Must convert to FlukeParsed equivalent
- New features: Must not alter existing output behavior
- Limits/rules: Must preserve baseline defaults
