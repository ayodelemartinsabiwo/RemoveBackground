@echo off
REM Build Installer with Inno Setup
echo ====================================
echo Background Remover - Installer Build
echo ====================================
echo.

REM Check if executable exists
if not exist "dist\BackgroundRemover.exe" (
    echo ERROR: BackgroundRemover.exe not found in dist folder!
    echo Please build the executable first with: build_fixed.bat
    pause
    exit /b 1
)

echo Checking executable...
echo   File: dist\BackgroundRemover.exe
for %%F in ("dist\BackgroundRemover.exe") do echo   Size: %%~zF bytes
echo   Status: OK
echo.

REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo ERROR: Inno Setup 6 not found!
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

echo Checking Inno Setup...
echo   Path: C:\Program Files (x86)\Inno Setup 6\ISCC.exe
echo   Status: OK
echo.

REM Create output directory if it doesn't exist
if not exist "output" mkdir output

echo Building installer with Inno Setup...
echo.
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_config.iss

if %errorlevel% == 0 (
    echo.
    echo ====================================
    echo BUILD SUCCESSFUL!
    echo ====================================
    echo.
    echo Installer created:
    echo   File: output\BackgroundRemover_Setup.exe
    echo.
    for %%F in ("output\BackgroundRemover_Setup.exe") do echo   Size: %%~zF bytes
    echo.
    echo You can now distribute this installer!
    echo.
    echo What the installer does:
    echo   - Installs BackgroundRemover.exe to Program Files
    echo   - Creates Start Menu shortcuts
    echo   - Adds desktop icon (optional)
    echo   - Installs context menu integration
    echo   - Includes user guide and utilities
    echo.
    echo Ready to test? Run: output\BackgroundRemover_Setup.exe
    echo.
) else (
    echo.
    echo ====================================
    echo BUILD FAILED!
    echo ====================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
