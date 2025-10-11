@echo off
echo ========================================
echo Background Remover - Direct Run Script
echo ========================================
echo.
echo Running from Python directly (no build needed)
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the application
python src\main_optimized.py

pause
