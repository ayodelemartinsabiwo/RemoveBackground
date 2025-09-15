@echo off
title Background Remover - Context Menu Fix
echo.
echo ======================================================
echo Background Remover - Context Menu Fix
echo ======================================================
echo.
echo This will fix the context menu to point to the correct
echo BackgroundRemover.exe executable.
echo.
echo Current issue: Context menu points to old installation
echo Fix: Update registry to use current working executable
echo.
echo Target: C:\RemoveBackground\dist\BackgroundRemover.exe
echo.

:: Check if target executable exists
if not exist "C:\RemoveBackground\dist\BackgroundRemover.exe" (
    echo ❌ ERROR: BackgroundRemover.exe not found!
    echo    Make sure the executable is built in the dist folder.
    echo.
    pause
    exit /b 1
)

echo ✅ Target executable found
echo.
echo Importing registry fix...
echo.

:: Import the registry file
regedit /s "C:\RemoveBackground\fix_context_menu.reg"

if %errorlevel% == 0 (
    echo ✅ Registry updated successfully!
    echo.
    echo 🎉 Context menu fix completed!
    echo.
    echo Now try:
    echo 1. Right-click on any image file
    echo 2. Look for "Remove Background" option
    echo 3. It should now launch the correct BackgroundRemover.exe
) else (
    echo ❌ Failed to update registry
    echo    You may need to run as Administrator
)

echo.
pause
