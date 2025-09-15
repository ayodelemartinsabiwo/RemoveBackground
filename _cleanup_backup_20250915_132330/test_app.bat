@echo off
echo Background Remover - Quick Test
echo ================================
echo.

if "%~1"=="" (
    echo Usage: test_app.bat "path\to\image.jpg"
    echo.
    echo Example: test_app.bat "C:\Users\YourName\Pictures\sample.jpg"
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Testing with image: %1
echo.

python src\main.py "%~1"

echo.
echo Test complete!
pause
