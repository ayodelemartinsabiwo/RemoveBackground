@echo off
echo Background Remover - Executable Test
echo =====================================
echo.

echo Testing the built executable...
echo.

echo Method 1: GUI Mode (File Dialog)
echo ---------------------------------
echo Running: dist\BackgroundRemover.exe
echo This should open a file selection dialog.
echo.
start "" "dist\BackgroundRemover.exe"

echo.
echo Method 2: Command Line Mode
echo ---------------------------
if exist "2F3A0942-1.jpg" (
    echo Running: dist\BackgroundRemover.exe "2F3A0942-1.jpg"
    echo This should process the image directly.
    echo.
    start "" "dist\BackgroundRemover.exe" "2F3A0942-1.jpg"
) else (
    echo No test image found. Place an image file in this directory to test command-line mode.
)

echo.
echo Both methods should show:
echo 1. Orange progress window
echo 2. Success dialog with "Open Folder" button
echo 3. Background-removed PNG file created
echo.

pause
