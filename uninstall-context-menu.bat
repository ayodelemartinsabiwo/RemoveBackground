@echo off
REM Context Menu Uninstallation Script for Background Remover
REM This script removes the right-click context menu

echo Uninstalling Background Remover context menu...

REM Try to run the Python script for context menu uninstallation
python "%~dp0context_menu.py" uninstall >nul 2>&1

REM If Python is not available system-wide, try to unregister directly via registry commands
if errorlevel 1 (
    echo Python not found, attempting direct registry modification...

    REM Remove registry entries for context menu
    reg delete "HKCR\*\shell\RemoveBackground" /f >nul 2>&1

    if errorlevel 1 (
        echo Context menu may already be uninstalled or requires administrator privileges
    ) else (
        echo Context menu uninstalled successfully via registry
    )
) else (
    echo Context menu uninstalled successfully via Python script
)

exit /b 0
