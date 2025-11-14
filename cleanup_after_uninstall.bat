@echo off
REM Final cleanup script that runs after main uninstaller
REM This script removes any stubborn leftover files and folders

echo Background Remover - Final Cleanup
echo ==================================

REM Wait for uninstaller to fully complete
timeout /t 3 >nul 2>&1

REM Get the installation directory from command line parameter
set "INSTALL_DIR=%~1"

if "%INSTALL_DIR%"=="" (
    echo No installation directory specified
    goto :end
)

echo Cleaning up remaining files in: %INSTALL_DIR%

REM Force remove models directory
if exist "%INSTALL_DIR%\models" (
    echo Removing models directory...
    rmdir /s /q "%INSTALL_DIR%\models" >nul 2>&1
)

REM Force remove _internal directory
if exist "%INSTALL_DIR%\_internal" (
    echo Removing _internal directory...
    rmdir /s /q "%INSTALL_DIR%\_internal" >nul 2>&1
)

REM Remove any log files
del /q "%INSTALL_DIR%\*.log" >nul 2>&1
del /q "%INSTALL_DIR%\*.tmp" >nul 2>&1

REM Try to remove the installation directory if empty
rmdir "%INSTALL_DIR%" >nul 2>&1

REM Clean up user data directory
if exist "%LOCALAPPDATA%\BackgroundRemover" (
    echo Removing user data...
    rmdir /s /q "%LOCALAPPDATA%\BackgroundRemover" >nul 2>&1
)

REM Final context menu cleanup with explorer restart
echo Performing final context menu cleanup...
reg delete "HKCU\Software\Classes\*\shell\RemoveBackground" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Classes\*\shell\RemoveBackground" /f >nul 2>&1

REM Restart explorer to refresh context menus
taskkill /f /im explorer.exe >nul 2>&1
start "" explorer.exe

echo.
echo Cleanup completed!
echo Background Remover has been completely removed.

:end
REM Self-destruct this cleanup script
del "%~f0" >nul 2>&1
