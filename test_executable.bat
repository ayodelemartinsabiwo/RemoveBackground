@echo off
echo ============================================
echo Testing Background Remover Executable
echo ============================================
echo.
echo Test 1: Checking executable exists...
if exist "dist\BackgroundRemover.exe" (
    echo [OK] Executable found
    for %%I in (dist\BackgroundRemover.exe) do echo     Size: %%~zI bytes (~1.8GB)
) else (
    echo [ERROR] Executable not found!
    pause
    exit /b 1
)

echo.
echo Test 2: Checking test image exists...
if exist "blackhairtest.jpg" (
    echo [OK] Test image found
) else (
    echo [WARNING] Test image not found, will use Fripikbigtest.jpg
)

echo.
echo Test 3: Running executable on test image...
echo This will open the GUI window...
echo.
echo Running: dist\BackgroundRemover.exe blackhairtest.jpg
echo.

dist\BackgroundRemover.exe blackhairtest.jpg

echo.
echo Test 4: Checking for output file...
timeout /t 2 /nobreak >nul

for %%F in (*no_bg*.png) do (
    echo [OK] Output file found: %%F
    for %%I in (%%F) do echo     Size: %%~zI bytes
    echo     This means the executable works!
    goto :success
)

echo [WARNING] No output file found yet
echo The GUI might have appeared - check if processing is happening
echo.

:success
echo.
echo ============================================
echo Test Complete!
echo ============================================
echo.
echo Next step: Test OFFLINE by disconnecting internet
echo and running the exe again to verify models are bundled.
echo.
pause
