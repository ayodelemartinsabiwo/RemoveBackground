@echo off@echo off@echo off

cd /d "%~dp0"

echo =========================================echo Testing Background Remover executable...echo ============================================

echo Testing Background Remover Executable

echo =========================================echo.echo Testing Background Remover Executable

echo.

echo Current directory: %CD%echo Current directory: %CD%echo ============================================

echo Executable: dist\BackgroundRemover\BackgroundRemover.exe

echo Test image: Fripikbigtest.jpgecho Executable path: %~dp0dist\BackgroundRemover\BackgroundRemover.exeecho.

echo.

echo Test image: Fripikbigtest.jpgecho Test 1: Checking executable exists...

if not exist "dist\BackgroundRemover\BackgroundRemover.exe" (

    echo ERROR: Executable not found!echo.if exist "dist\BackgroundRemover.exe" (

    pause

    exit /b 1echo Starting test...    echo [OK] Executable found

)

"%~dp0dist\BackgroundRemover\BackgroundRemover.exe" "%~dp0Fripikbigtest.jpg"    for %%I in (dist\BackgroundRemover.exe) do echo     Size: %%~zI bytes (~1.8GB)

if not exist "Fripikbigtest.jpg" (

    echo ERROR: Test image not found!echo.) else (

    pause

    exit /b 1echo Test completed. Check for output files:    echo [ERROR] Executable not found!

)

dir /b *no_bg*.png 2>nul    pause

echo Starting test...

echo =========================================if errorlevel 1 (    exit /b 1

echo.

    echo No output files found - there may be an error)

REM Run the executable and capture any errors

dist\BackgroundRemover\BackgroundRemover.exe Fripikbigtest.jpg 2>&1) else (



echo.    echo Output files found - test successfulecho.

echo =========================================

echo Test completed. Checking results...)echo Test 2: Checking test image exists...

echo.

pauseif exist "blackhairtest.jpg" (

REM Check for output files    echo [OK] Test image found

if exist "*no_bg*.png" () else (

    echo SUCCESS: Output files found:    echo [WARNING] Test image not found, will use Fripikbigtest.jpg

    dir /b *no_bg*.png)

) else (

    echo ERROR: No output files foundecho.

)echo Test 3: Running executable on test image...

echo This will open the GUI window...

echo.echo.

echo Check if models were created:echo Running: dist\BackgroundRemover.exe blackhairtest.jpg

if exist "dist\BackgroundRemover\models" (echo.

    echo Models directory exists:

    dir /b "dist\BackgroundRemover\models\*.onnx" 2>nuldist\BackgroundRemover.exe blackhairtest.jpg

    if errorlevel 1 (

        echo   No ONNX files in models directoryecho.

    )echo Test 4: Checking for output file...

) else (timeout /t 2 /nobreak >nul

    echo   No models directory found

)for %%F in (*no_bg*.png) do (

    echo [OK] Output file found: %%F

echo.    for %%I in (%%F) do echo     Size: %%~zI bytes

echo Press any key to exit...    echo     This means the executable works!

pause >nul    goto :success
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
