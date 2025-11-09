@echo off
REM Context Menu Test Script
echo ============================================
echo Context Menu Test Script
echo ============================================
echo.

echo 1. Checking context menu installation...
reg query "HKCU\Software\Classes\*\shell\RemoveBackground" >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] Context menu registry entry found

    REM Check command path
    reg query "HKCU\Software\Classes\*\shell\RemoveBackground\command" >nul 2>&1
    if %errorlevel% equ 0 (
        echo   [OK] Command entry found
        for /f "tokens=2*" %%a in ('reg query "HKCU\Software\Classes\*\shell\RemoveBackground\command" /ve 2^>nul ^| find "REG_SZ"') do (
            echo   Command: %%b
        )
    ) else (
        echo   [ERROR] Command entry missing
    )
) else (
    echo   [ERROR] Context menu NOT installed
    echo.
    echo   To install manually:
    echo   1. Go to Start Menu -^> Background Remover
    echo   2. Click "Install Context Menu"
    goto :end
)

echo.
echo 2. Creating test image...
set "TEST_IMAGE=%USERPROFILE%\Desktop\test_bg_removal.png"
echo This is a test image for context menu testing > "%TEST_IMAGE%"
echo   [OK] Created: %TEST_IMAGE%

echo.
echo 3. Testing Instructions:
echo ============================================
echo   1. Go to your Desktop
echo   2. Find: test_bg_removal.png
echo   3. RIGHT-CLICK on the file
echo   4. Look for: "Remove Background"
echo   5. If you see it: SUCCESS!
echo   6. If not: PROBLEM - try solutions below
echo.
echo If context menu doesn't appear:
echo   - Press F5 to refresh the folder
echo   - Close/reopen File Explorer
echo   - Restart your computer
echo   - Run "Install Context Menu" as Administrator

echo.
echo Opening Desktop folder for testing...
explorer "%USERPROFILE%\Desktop"

echo.
:end
echo ============================================
echo Press any key when done testing...
pause
if exist "%TEST_IMAGE%" del "%TEST_IMAGE%" 2>nul
echo Test complete!
