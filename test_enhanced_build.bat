@echo off
echo ============================================
echo Testing Enhanced Background Remover Build
echo ============================================
echo.

echo [1/4] Testing UI Border Radius Fix...
echo Starting application to check loader window appearance...
echo Look for rounded corners on all edges (no black sharp corners)
echo.

echo [2/4] Building optimized installer with size reduction...
call build_onnx_safe.bat
echo.

if exist "dist\BackgroundRemover\BackgroundRemover.exe" (
    echo [3/4] Build successful! Testing executable...
    echo Starting Background Remover to test functionality...
    start "" "dist\BackgroundRemover\BackgroundRemover.exe"
    echo.
    echo Check for:
    echo - Rounded window corners (no black edges)
    echo - Proper model loading (with decompression if needed)
    echo - Working background removal functionality
    echo.

    echo [4/4] Testing installer with dynamic button positioning...
    if exist "output\BackgroundRemover_Setup.exe" (
        echo Installer created successfully!
        echo.
        echo You can now test:
        echo - Dynamic button positioning in installer
        echo - Reduced installer size
        echo - All functionality preserved
        echo.
        echo Next steps:
        echo 1. Run the installer to test button positioning
        echo 2. Check installer size (should be significantly reduced)
        echo 3. Verify all features work correctly
    ) else (
        echo ERROR: Installer was not created. Check build process.
    )
) else (
    echo ERROR: Build failed. Check build_onnx_safe.bat for errors.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Test complete! Review the above results.
echo ============================================
pause
