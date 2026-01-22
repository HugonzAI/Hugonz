@echo off
echo ========================================
echo EST Converter - Restore Clean Code
echo ========================================
echo.
echo This will restore all code files to the latest clean version.
echo Any local changes will be LOST!
echo.
pause

echo.
echo Checking git status...
git status

echo.
echo Restoring files...
git checkout -- est_converter.py
git checkout -- esa615_connector.py
git checkout -- dta_to_csv_converter.py
git checkout -- esa615_ui_addon.py

echo.
echo Pulling latest changes from remote...
git pull origin claude/est-converter-baseline-sbRr5

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo Files have been restored to clean version.
echo Please close any AI assistants (Copilot/Cursor) before editing!
echo.
pause
