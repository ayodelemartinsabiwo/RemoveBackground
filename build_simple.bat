@echo off
echo Background Remover - Simple Build Script
echo =====================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then: .venv\Scripts\pip install -r src\requirements.txt
    pause
    exit /b 1
)

echo ✅ Using virtual environment: .venv
echo.

echo 🔨 Building executable with simple configuration...
REM Kill any existing processes
taskkill /F /IM BackgroundRemover.exe /T 2>nul

REM Activate virtual environment and build
call .venv\Scripts\activate.bat
python -m PyInstaller build_simple.spec --clean --noconfirm

if %errorlevel% equ 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📦 Executable: dist\BackgroundRemover.exe
    echo.
    echo Testing executable...
    echo.

    REM Check if executable exists
    if exist "dist\BackgroundRemover.exe" (
        echo ✅ Executable file exists
        echo 📏 Size:
        dir "dist\BackgroundRemover.exe" | findstr "BackgroundRemover.exe"
        echo.
        echo ✅ Ready to use!
        echo.
        echo Next steps:
        echo 1. Test the executable: dist\BackgroundRemover.exe
        echo 2. If it works, create installer: installer_config.iss
    ) else (
        echo ❌ Executable not found in dist folder!
    )
) else (
    echo.
    echo ❌ Build failed!
    echo Check the error messages above.
)

echo.
pause
