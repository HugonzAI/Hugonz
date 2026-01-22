# EST Converter - EXE Build Guide

Complete guide for packaging EST Converter as a standalone Windows executable.

## Prerequisites

1. **Python 3.8+** installed
2. **All dependencies** installed:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Required template files** in project directory:
   - `example_Good.xlsx`
   - `EST_Tester.xlsx`
   - `EST_Limits_Summary.xlsx`

4. **Optional UI resources**:
   - `hnz_logo.png` (logo image)
   - `est_icon.ico` (application icon)

## Quick Build (Recommended)

Use the automated build script:

```bash
python build_exe.py
```

This will:
- ✅ Create a single `EST_Converter.exe` file
- ✅ Embed all template files
- ✅ Include logo and icon (if present)
- ✅ Set up all dependencies
- ✅ Create a windowed (GUI) application

**Output:** `dist/EST_Converter.exe`

## Manual Build

If you prefer manual control:

### Basic Build

```bash
pyinstaller --onefile --windowed --name="EST_Converter" est_converter.py
```

### With Icon

```bash
pyinstaller --onefile --windowed --name="EST_Converter" --icon=est_icon.ico est_converter.py
```

### With Data Files

```bash
pyinstaller --onefile --windowed --name="EST_Converter" ^
    --icon=est_icon.ico ^
    --add-data="example_Good.xlsx;." ^
    --add-data="EST_Tester.xlsx;." ^
    --add-data="EST_Limits_Summary.xlsx;." ^
    --add-data="hnz_logo.png;." ^
    --add-data="est_icon.ico;." ^
    est_converter.py
```

**Note:** On Linux/Mac, use `:` instead of `;` in `--add-data` paths.

## Build Options Explained

| Option | Description |
|--------|-------------|
| `--onefile` | Creates a single EXE (vs multiple files) |
| `--windowed` | GUI mode (no console window) |
| `--noconsole` | Same as --windowed |
| `--icon=file.ico` | Sets application icon |
| `--name=Name` | Output executable name |
| `--clean` | Removes cache before build |
| `--add-data=src;dst` | Includes data files (templates, images) |

## Distribution Package

### Embedded Templates (Recommended)

When using `--add-data`, templates are embedded in the EXE:

**Distribution:**
```
EST_Converter.exe (standalone - all you need!)
```

Users can override templates by placing files alongside the EXE:
```
EST_Converter.exe
example_Good.xlsx     (optional - overrides embedded)
EST_Tester.xlsx       (optional - overrides embedded)
EST_Limits_Summary.xlsx (optional - overrides embedded)
```

### External Templates (Alternative)

Build without `--add-data` if you want to distribute templates separately:

**Distribution:**
```
EST_Converter.exe
example_Good.xlsx     (required)
EST_Tester.xlsx       (required)
EST_Limits_Summary.xlsx (required)
hnz_logo.png         (optional)
est_icon.ico         (optional)
```

## Size Optimization

### Reduce EXE Size

If the EXE is too large (>100MB), exclude unnecessary modules:

```bash
pyinstaller --onefile --windowed --name="EST_Converter" ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    --exclude-module=PIL ^
    est_converter.py
```

### Use UPX Compression

Install UPX and add `--upx-dir=<path>`:

```bash
pyinstaller --onefile --windowed --name="EST_Converter" --upx-dir="C:\upx" est_converter.py
```

**Download UPX:** https://upx.github.io/

## Troubleshooting

### "Module not found" errors

Add hidden imports:
```bash
pyinstaller ... --hidden-import=module_name ...
```

Common hidden imports:
- `openpyxl.cell`
- `openpyxl.styles`
- `dateutil.parser`
- `serial.tools`

### DLL not found errors

Copy missing DLLs to `dist/` folder alongside the EXE.

### Antivirus false positives

PyInstaller executables may trigger false positives. Solutions:
1. Sign the EXE with a code signing certificate
2. Submit to antivirus vendors as false positive
3. Use `--onedir` instead of `--onefile` (creates folder with DLLs)

### Large file size

Normal ranges:
- Basic build: 40-60 MB
- With PySide6: 80-120 MB
- With all dependencies: 100-150 MB

Use exclusions and UPX to reduce size.

## Advanced: Spec File Customization

Generate a spec file for advanced customization:

```bash
pyi-makespec --onefile --windowed --name="EST_Converter" est_converter.py
```

Edit `EST_Converter.spec` and build:

```bash
pyinstaller EST_Converter.spec
```

### Example Spec Modifications

**Add version info:**
```python
version_info = (
    '3.3.0',
    '3.3.0.0',
    'EST Converter',
    'Electrical Safety Testing Converter'
)
```

**Custom icon and resources:**
```python
exe = EXE(
    pyz,
    a.scripts,
    icon='est_icon.ico',
    name='EST_Converter',
    version='version_info.txt'
)
```

## Testing the EXE

1. **Basic functionality:**
   - Launch the EXE
   - UI should load correctly
   - Test file drag-and-drop
   - Test Add Files button
   - Test conversion

2. **With ESA615:**
   - Test serial port connection
   - Test file list retrieval
   - Test download and conversion

3. **On clean Windows VM:**
   - Test on a machine without Python installed
   - Verify no missing DLL errors
   - Confirm templates work (embedded or external)

## Deployment Checklist

- [ ] Build successful (no errors)
- [ ] EXE runs on development machine
- [ ] UI displays correctly
- [ ] All buttons functional
- [ ] File conversion works
- [ ] Template files load correctly
- [ ] Tested on clean Windows machine
- [ ] Icon displays correctly
- [ ] ESA615 features work (if applicable)
- [ ] File size acceptable (<150MB)
- [ ] Antivirus scan clean

## Distribution

### Internal Distribution

**Recommended structure:**
```
EST_Converter_v3.3/
├── EST_Converter.exe
├── README.txt (usage instructions)
├── example_Good.xlsx (if external)
├── EST_Tester.xlsx (if external)
└── EST_Limits_Summary.xlsx (if external)
```

Zip and distribute.

### Professional Distribution

For professional/commercial distribution:
1. Code sign the EXE
2. Create an installer (NSIS, Inno Setup, etc.)
3. Include uninstaller
4. Add to Windows Start Menu
5. Create desktop shortcut
6. Register file associations (.csv)

## Support

For build issues, check:
1. Python version compatibility (3.8+)
2. All dependencies installed
3. Template files present
4. PyInstaller version (latest recommended)

For runtime issues with EXE:
1. Test on development machine first
2. Check Windows Event Viewer for errors
3. Run from command line to see error messages
4. Verify template files are accessible

---

**Quick Reference:**

```bash
# Install PyInstaller
pip install pyinstaller

# Simple build
python build_exe.py

# Output
dist/EST_Converter.exe
```

Done! 🎉
