@echo off
REM Context Menu Installation Script for Background Remover
REM This script installs the right-click context menu

echo Installing Background Remover context menu...

REM Try to run the Python script for context menu installation
python "%~dp0context_menu.py" install "%~dp0BackgroundRemover.exe" >nul 2>&1

REM If Python is not available system-wide, try to register directly via registry commands
if errorlevel 1 (
    echo Python not found, attempting direct registry modification...

    REM Create registry entries for context menu (using icon.ico for icon)
    reg add "HKCR\*\shell\RemoveBackground" /ve /d "Remove Background" /f >nul 2>&1
    reg add "HKCR\*\shell\RemoveBackground" /v "Icon" /d "\"%~dp0icon.ico\"" /f >nul 2>&1
    reg add "HKCR\*\shell\RemoveBackground\command" /ve /d "\"%~dp0BackgroundRemover.exe\" \"%%1\"" /f >nul 2>&1

    if errorlevel 1 (
        echo Failed to install context menu - may require administrator privileges
        exit /b 1
    ) else (
        echo Context menu installed successfully via registry
    )
) else (
    echo Context menu installed successfully via Python script
)

exit /b 0
