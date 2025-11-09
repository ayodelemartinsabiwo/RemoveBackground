@echo off
REM Simple Context Menu Uninstaller for Background Remover
echo ================================================
echo Background Remover Context Menu Uninstaller
echo ================================================
echo.

echo Removing context menu entry...

REM Remove the context menu entry
reg delete "HKCU\Software\Classes\*\shell\RemoveBackground" /f >nul 2>&1

REM Check if removal was successful
reg query "HKCU\Software\Classes\*\shell\RemoveBackground" >nul 2>&1
if %errorlevel% neq 0 (
    echo [SUCCESS] Context menu removed successfully!
) else (
    echo [WARNING] Context menu may still be present
    echo Try restarting File Explorer or rebooting
)

echo.
echo ================================================
if "%1" neq "silent" pause
