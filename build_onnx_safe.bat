@echo off
echo ============================================
echo Building Background Remover (ONNX-Safe)
echo ============================================

REM Ensure we're in the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Verify environment
echo.
echo Verifying environment:
python -c "import sys; print(f'Python: {sys.executable}')"
python -c "import onnxruntime; print(f'ONNX Runtime: {onnxruntime.__version__}')"
python -c "import rembg; print('Rembg: OK')"

REM Test that the main application works in this environment
echo.
echo Testing application in virtual environment...
python -c "from src.bg_remove_v1_2_bulletproof import BackgroundRemoverV12Bulletproof; print('Bulletproof version: OK')"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Application test failed in virtual environment!
    echo Please check the environment setup.
    pause
    exit /b 1
)

echo.
echo Environment test passed! Proceeding with build...
echo.

REM Clean previous build
echo Cleaning previous build...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build with PyInstaller using the updated spec
echo.
echo Building with PyInstaller (ONNX-safe configuration)...
python -m PyInstaller build_optimized.spec --clean --noconfirm

if %ERRORLEVEL% neq 0 (
    echo.
    echo ====================================
    echo BUILD FAILED!
    echo ====================================
    pause
    exit /b 1
)

echo.
echo ====================================
echo BUILD SUCCESSFUL!
echo ====================================

echo.
echo Executable created:
if exist "dist\BackgroundRemover\BackgroundRemover.exe" (
    echo   File: dist\BackgroundRemover\BackgroundRemover.exe
    for %%I in (dist\BackgroundRemover\BackgroundRemover.exe) do echo   Size: %%~zI bytes
    echo.
    echo Testing executable for DLL errors...
    echo.

    REM Test the executable briefly (just to see if it starts without DLL errors)
    timeout /t 2 /nobreak >nul
    echo If no DLL errors appeared above, the build is successful!
) else (
    echo [ERROR] Executable not found!
    exit /b 1
)

echo.
echo Ready to create installer? Run: build_installer.bat
echo.
pause
