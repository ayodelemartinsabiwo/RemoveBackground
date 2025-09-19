@echo off
echo.
echo =====================================================
echo    Background Remover - Open Installation Folder
echo    Palmer Enterprises
echo =====================================================
echo.
echo This utility will open the installation folder where
echo Background Remover is installed.
echo.
echo Opening installation folder...
echo.

REM Open the current directory (where this batch file is located)
explorer.exe "%~dp0"

echo Installation folder opened successfully!
echo.
echo You can find the uninstaller (unins000.exe) in this folder
echo if you need to uninstall Background Remover.
echo.
timeout /t 3 /nobreak >nul
