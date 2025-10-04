@echo off
REM Icon Cache Rebuilder for Windows
REM This forces Windows to reload icons after updating the executable

echo ================================================
echo  Windows Icon Cache Rebuild Tool
echo ================================================
echo.

echo Step 1: Stopping Explorer to clear icon cache...
taskkill /f /im explorer.exe >nul 2>&1

echo Step 2: Deleting icon cache files...
cd /d "%userprofile%\AppData\Local"

REM Windows 10/11 IconCache location
if exist IconCache.db (
    del /f /q IconCache.db >nul 2>&1
    echo    - Deleted IconCache.db
)

REM Windows 10/11 additional caches
if exist Microsoft\Windows\Explorer (
    del /f /q "Microsoft\Windows\Explorer\iconcache*.db" >nul 2>&1
    echo    - Deleted Explorer icon caches
)

REM Windows 11 specific
if exist Microsoft\Windows\Explorer\thumbcache*.db (
    del /f /q "Microsoft\Windows\Explorer\thumbcache*.db" >nul 2>&1
    echo    - Deleted thumbnail caches
)

echo.
echo Step 3: Restarting Windows Explorer...
start explorer.exe

echo.
echo ================================================
echo  Icon cache cleared successfully!
echo ================================================
echo.
echo Please wait a few seconds for Explorer to restart,
echo then check your desktop shortcut and taskbar icons.
echo.
echo If icons still appear old:
echo 1. Delete the desktop shortcut
echo 2. Run this script again
echo 3. Create a new shortcut
echo.
pause
