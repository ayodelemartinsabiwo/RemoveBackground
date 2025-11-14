@echo off
REM Simple Context Menu Uninstaller for Background Remover
echo ================================================
echo Background Remover Context Menu Uninstaller
echo ================================================
echo.

echo Removing context menu entry...

REM Remove the context menu entry and all subkeys
reg delete "HKCU\Software\Classes\*\shell\RemoveBackground" /f >nul 2>&1

REM Also try to remove from HKLM in case it was installed there
reg delete "HKLM\SOFTWARE\Classes\*\shell\RemoveBackground" /f >nul 2>&1

REM Force refresh of File Explorer
taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe >nul 2>&1

REM Wait a moment for explorer to restart
timeout /t 2 >nul 2>&1

REM Check if removal was successful
reg query "HKCU\Software\Classes\*\shell\RemoveBackground" >nul 2>&1
if %errorlevel% neq 0 (
    echo [SUCCESS] Context menu removed successfully!
) else (
    echo [WARNING] Context menu may still be present
    echo Try rebooting your computer for complete removal
)

echo.
echo ================================================
if "%1" neq "silent" pause
