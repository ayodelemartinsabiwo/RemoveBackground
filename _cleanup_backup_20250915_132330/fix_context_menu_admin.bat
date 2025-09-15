@echo off
echo Background Remover - Context Menu Fix (Administrator Mode)
echo =========================================================
echo.
echo This script will fix the context menu by:
echo 1. Removing old/broken "Remove Background" entries
echo 2. Installing the correct context menu pointing to BackgroundRemover.exe
echo.
echo Requesting Administrator privileges...
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - OK
    echo.
) else (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %CD% && python fix_context_menu.py && pause' -Verb RunAs"
    exit /b
)

:: Run the Python script
python fix_context_menu.py

echo.
echo Context menu fix completed!
echo You can now test by right-clicking on any image file.
echo.
pause
