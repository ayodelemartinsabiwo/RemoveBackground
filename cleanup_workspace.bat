@echo off
echo ====================================
echo  Workspace Cleanup Script
echo ====================================
echo.

echo Cleaning up redundant files...
echo.

REM Delete test/temporary files
if exist "test_ico.py" (
    echo [X] Deleting test_ico.py
    del /f /q "test_ico.py"
)

if exist "test_import_speed.py" (
    echo [X] Deleting test_import_speed.py
    del /f /q "test_import_speed.py"
)

if exist "test_multi.ico" (
    echo [X] Deleting test_multi.ico
    del /f /q "test_multi.ico"
)

if exist "test_single.ico" (
    echo [X] Deleting test_single.ico
    del /f /q "test_single.ico"
)

REM Delete old/backup icon conversion scripts
if exist "convert_svg_to_ico.py" (
    echo [X] Deleting convert_svg_to_ico.py (replaced by create_proper_ico.py)
    del /f /q "convert_svg_to_ico.py"
)

if exist "generate_bg_icon.py" (
    echo [X] Deleting generate_bg_icon.py (no longer needed)
    del /f /q "generate_bg_icon.py"
)

REM Delete old build spec (keeping optimized version)
if exist "build.spec" (
    echo [X] Deleting build.spec (using build_optimized.spec)
    del /f /q "build.spec"
)

REM Delete backup icon file
if exist "assets\icon_backup.ico" (
    echo [X] Deleting assets\icon_backup.ico
    del /f /q "assets\icon_backup.ico"
)

REM Delete uncorrected icon PNGs folder (keeping corrected version)
if exist "assets\Icon PNGs" (
    echo [X] Deleting assets\Icon PNGs folder (using corrected version)
    rmdir /s /q "assets\Icon PNGs"
)

REM Delete documentation files now that issues are resolved
if exist "DESKTOP_TASKBAR_ICON_FIX.md" (
    echo [X] Deleting DESKTOP_TASKBAR_ICON_FIX.md (issue resolved)
    del /f /q "DESKTOP_TASKBAR_ICON_FIX.md"
)

if exist "ICON_QUALITY_SOLUTION.md" (
    echo [X] Deleting ICON_QUALITY_SOLUTION.md (issue resolved)
    del /f /q "ICON_QUALITY_SOLUTION.md"
)

REM Delete utility scripts no longer needed
if exist "verify_icons.py" (
    echo [X] Deleting verify_icons.py (diagnostic tool, no longer needed)
    del /f /q "verify_icons.py"
)

if exist "fix_icon_sizes.py" (
    echo [X] Deleting fix_icon_sizes.py (one-time fix completed)
    del /f /q "fix_icon_sizes.py"
)

if exist "fix_context_menu.py" (
    echo [X] Deleting fix_context_menu.py (issue resolved)
    del /f /q "fix_context_menu.py"
)

if exist "rebuild_icon_cache.bat" (
    echo [X] Deleting rebuild_icon_cache.bat (utility completed)
    del /f /q "rebuild_icon_cache.bat"
)

REM Delete BGoutput.zip if it exists
if exist "BGoutput.zip" (
    echo [X] Deleting BGoutput.zip
    del /f /q "BGoutput.zip"
)

REM Clean up __pycache__ in root
if exist "__pycache__" (
    echo [X] Deleting root __pycache__ folder
    rmdir /s /q "__pycache__"
)

REM Clean up build artifacts (keeping dist folder with final executable)
if exist "build" (
    echo [X] Deleting build folder (temporary build files)
    rmdir /s /q "build"
)

echo.
echo ====================================
echo  Cleanup Complete!
echo ====================================
echo.
echo Kept important files:
echo   - build_optimized.spec (PyInstaller config)
echo   - build_fixed.bat (build script)
echo   - create_proper_ico.py (icon creation tool)
echo   - install-context-menu.bat
echo   - uninstall-context-menu.bat
echo   - installer_config.iss (Inno Setup config)
echo   - assets\Icon PNGs Corrected (corrected icons)
echo   - assets\icon.ico (final icon file)
echo   - dist\ (final executable)
echo   - src\ (source code)
echo.
pause
