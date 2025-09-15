@echo off
echo.
echo ========================================
echo  Windows Defender - Add Exclusions
echo  Background Remover False Positive Fix
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges...
    echo.
) else (
    echo [ERROR] This script requires administrator privileges!
    echo [FIX] Right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [STEP 1] Adding Windows Defender exclusions...
echo.

REM Add folder exclusions
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Program Files\BackgroundRemover'" 2>nul
if %errorLevel% == 0 (
    echo ✅ Added installation folder exclusion
) else (
    echo ❌ Failed to add installation folder exclusion
)

powershell -Command "Add-MpPreference -ExclusionPath 'C:\RemoveBackground\dist'" 2>nul
if %errorLevel% == 0 (
    echo ✅ Added development folder exclusion
) else (
    echo ⚠️  Development folder exclusion may have failed (this is normal if folder doesn't exist)
)

REM Add process exclusion
powershell -Command "Add-MpPreference -ExclusionProcess 'BackgroundRemover.exe'" 2>nul
if %errorLevel% == 0 (
    echo ✅ Added process exclusion for BackgroundRemover.exe
) else (
    echo ❌ Failed to add process exclusion
)

echo.
echo [STEP 2] Restarting Windows Defender service...
powershell -Command "Restart-Service -Name 'WinDefend' -Force" 2>nul
if %errorLevel% == 0 (
    echo ✅ Windows Defender service restarted
) else (
    echo ⚠️  Service restart may have failed (this is sometimes normal)
)

echo.
echo ========================================
echo                 COMPLETE
echo ========================================
echo.
echo ✅ Background Remover should now work without false positive warnings!
echo.
echo 📋 Next steps:
echo    1. Right-click on any image file
echo    2. Select "Remove Background" from context menu
echo    3. If still issues, restart your computer
echo.
echo 📧 Support: palmarenterprise@gmail.com
echo.
pause
