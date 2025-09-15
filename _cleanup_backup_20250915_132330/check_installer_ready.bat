@echo off
echo Installer Readiness Check
echo =========================
echo.

echo Checking required files...
echo.

if exist "assets\splash.bmp" (
    echo ✅ splash.bmp found
    for %%A in ("assets\splash.bmp") do echo    Size: %%~zA bytes
) else (
    echo ❌ splash.bmp missing
)

if exist "assets\icon.ico" (
    echo ✅ icon.ico found
) else (
    echo ❌ icon.ico missing
)

if exist "dist\BackgroundRemover.exe" (
    echo ✅ BackgroundRemover.exe found
) else (
    echo ❌ BackgroundRemover.exe missing - run build.bat first
)

if exist "installer_config.iss" (
    echo ✅ installer_config.iss found
) else (
    echo ❌ installer_config.iss missing
)

echo.
echo Checking Inno Setup configuration...
findstr /i "Palmar Tech" installer_config.iss >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Publisher set to "Palmar Tech"
) else (
    echo ❌ Publisher not configured
)

echo.
echo =========================
echo Ready for Inno Setup compilation!
echo.
echo Next steps:
echo 1. Open Inno Setup
echo 2. Open installer_config.iss
echo 3. Build ^> Compile
echo 4. Test output\BackgroundRemover_Setup.exe
echo.

pause
