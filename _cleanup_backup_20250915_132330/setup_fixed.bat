@echo off
echo Background Remover - Advanced Setup
echo ====================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing compatible dependencies...
echo This may take a few minutes...

rem Install packages with specific versions for compatibility
pip install "rembg>=2.0.60"
pip install "PyQt6>=6.6.0"
pip install "Pillow>=10.0.0"
pip install "onnxruntime==1.17.0"
pip install "numpy<2"
pip install "opencv-python-headless<4.10"
pip install "pyinstaller>=6.0.0"

echo.
echo Testing installation...
python -c "import rembg; import PyQt6; import PIL; import onnxruntime; print('All imports successful!')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Setup completed successfully!
    echo.
    echo You can now:
    echo 1. Test with: python src\main.py "path\to\image.jpg"
    echo 2. Build with: build.bat
    echo.
) else (
    echo.
    echo ❌ Setup failed. Check error messages above.
    echo.
)

pause
