@echo off
echo Building Background Remover Application...
echo.

echo Step 1: Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Step 2: Building executable with PyInstaller...
pyinstaller build.spec --clean --noconfirm

echo.
echo Step 3: Build complete!
echo Executable created at: dist/BackgroundRemover.exe
echo.

echo To create installer:
echo 1. Install Inno Setup from https://jrsoftware.org/isdl.php
echo 2. Open installer_config.iss in Inno Setup
echo 3. Click Build to create the installer
echo.

pause
