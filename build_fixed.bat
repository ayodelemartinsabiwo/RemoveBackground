@echo off
echo Background Remover - Build Script
echo ==================================
echo.

:: Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then activate and install requirements
    pause
    exit /b 1
)

echo ✅ Using virtual environment: .venv
echo.

:: Build using virtual environment Python
echo 🔨 Building executable with PyInstaller...
echo.
.\.venv\Scripts\python.exe -m PyInstaller build_optimized.spec --clean --noconfirm

if %errorlevel% == 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📦 Executable: dist\BackgroundRemover.exe
    echo.
    echo Testing executable...
    echo.

    :: Test the executable
    if exist "dist\BackgroundRemover.exe" (
        echo ✅ Executable file exists
        echo 💾 Size:
        dir "dist\BackgroundRemover.exe" | findstr BackgroundRemover.exe
        echo.
        echo 🎉 Ready to use!
        echo.
        echo Next steps:
        echo 1. Test the executable: dist\BackgroundRemover.exe
        echo 2. If it works, create installer: installer_config.iss
    ) else (
        echo ❌ Executable not found!
    )
) else (
    echo.
    echo ❌ Build failed!
    echo Check the error messages above.
)

echo.
pause
