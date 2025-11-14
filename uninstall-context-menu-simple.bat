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

REM Refresh File Explorer safely without killing it
REM Using SHChangeNotify to refresh shell instead of dangerous explorer restart
powershell -Command "$null = [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.SendKeys]::SendWait('{F5}')" >nul 2>&1

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
