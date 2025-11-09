@echo off
REM Simple Context Menu Installer for Background Remover
echo ================================================
echo Background Remover Context Menu Installer
echo ================================================
echo.

REM Get the executable path
set "EXE_PATH=%~dp0BackgroundRemover.exe"

REM Check if executable exists
if not exist "%EXE_PATH%" (
    echo ERROR: BackgroundRemover.exe not found in current directory!
    echo Please run this script from the installation folder.
    pause
    exit /b 1
)

echo Installing context menu for image files...
echo Executable: %EXE_PATH%
echo.

REM Install context menu (HKCU - no admin required)
reg add "HKCU\Software\Classes\*\shell\RemoveBackground" /ve /d "Remove Background" /f >nul 2>&1
reg add "HKCU\Software\Classes\*\shell\RemoveBackground" /v "Icon" /d "\"%EXE_PATH%\",0" /f >nul 2>&1
reg add "HKCU\Software\Classes\*\shell\RemoveBackground\command" /ve /d "\"%EXE_PATH%\" \"%%1\"" /f >nul 2>&1

REM Apply to image files only
reg add "HKCU\Software\Classes\*\shell\RemoveBackground" /v "AppliesTo" /d "System.FileName:\"*.jpg\" OR System.FileName:\"*.jpeg\" OR System.FileName:\"*.png\" OR System.FileName:\"*.bmp\" OR System.FileName:\"*.tiff\" OR System.FileName:\"*.webp\"" /f >nul 2>&1

REM Check if installation was successful
reg query "HKCU\Software\Classes\*\shell\RemoveBackground" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Context menu installed successfully!
    echo.
    echo How to use:
    echo    1. Right-click any image file (.jpg, .png, etc.)
    echo    2. Select "Remove Background"
    echo    3. Wait for processing to complete
    echo.
    echo Output files will be saved with "_no_bg" suffix
    echo    Example: photo.jpg -^> photo_no_bg.jpg
) else (
    echo [FAILED] Context menu installation unsuccessful
    echo.
    echo Try these solutions:
    echo    1. Run as Administrator (right-click -^> Run as administrator)
    echo    2. Check Windows security settings
    echo    3. Restart File Explorer
    echo    4. Reboot your computer
)

echo.
echo ================================================
if "%1" neq "silent" pause
