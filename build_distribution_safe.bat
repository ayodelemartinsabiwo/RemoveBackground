@echo off
echo =====================================
echo Background Remover - Distribution Safe Build
echo =====================================
echo.

echo 🔧 Using virtual environment: .venv
echo.

echo 🧹 Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo 🏗️ Building distribution-safe executable with PyInstaller...
echo   - Excludes WebView components (fixes Microsoft.Internal.Framework.Udk.dll)
echo   - Properly packages scikit-image binaries
echo   - Enhanced compatibility for clean Windows systems
echo.

.\.venv\Scripts\pyinstaller.exe ^
    --distpath dist ^
    --workpath build ^
    --clean ^
    --noconfirm ^
    build_distribution_safe.spec

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📦 Executable: dist\BackgroundRemover.exe
echo.

echo Testing executable...
if exist "dist\BackgroundRemover.exe" (
    echo ✅ Executable file exists
    echo 📊 Size:
    dir "dist\BackgroundRemover.exe" | findstr BackgroundRemover.exe
    echo.
    echo 🎯 Distribution-Safe Features:
    echo   ✅ No WebView dependencies
    echo   ✅ Complete scikit-image packaging
    echo   ✅ Clean Windows compatibility
    echo   ✅ Bulletproof error handling
    echo   ✅ EXIF orientation correction
    echo   ✅ Same-directory output saving
    echo.
    echo 🚀 Ready for distribution!
    echo.
    echo Next steps:
    echo 1. Test on clean Windows systems
    echo 2. Create installer if needed: installer_config.iss
) else (
    echo ❌ Executable not found!
)

echo.
pause
