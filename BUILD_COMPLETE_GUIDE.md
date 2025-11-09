# Complete Build Guide - Offline-Ready Application

## Overview
This guide shows how to build the Background Remover app with **bundled AI models** so users don't need internet connection.

## Prerequisites
- Python 3.8+
- Virtual environment activated
- All dependencies installed: `pip install -r src/requirements.txt`
- Inno Setup 6 (for installer creation)
- ~500MB free disk space (for models)

## Step-by-Step Build Process

### Step 1: Download AI Models
**This is crucial - skip this and users will need internet!**

```powershell
# Download models (~200MB, takes 1-2 minutes)
python download_models.py
```

**What this does:**
- Downloads BiRefNet-Portrait model (~170MB) to `/models` directory
- Falls back to U2Net if BiRefNet fails
- Verifies models work correctly
- These models will be bundled with your executable

**Expected output:**
```
📥 Downloading BiRefNet-Portrait model...
   ✓ Testing model...
   ✅ BiRefNet-Portrait model downloaded and verified!

Downloaded Models:
  ✓ birefnet-portrait.onnx (169.8 MB)

✅ SUCCESS! Models ready for bundling
```

### Step 2: Verify Models Downloaded
```powershell
# Check models directory exists
dir models

# Should see .onnx files (~170MB each)
```

### Step 3: Build Executable
```powershell
# Clean build (recommended)
python -m PyInstaller build_optimized.spec --clean --noconfirm

# Models are automatically bundled!
```

**What gets bundled:**
- Your Python code
- PyQt6 GUI framework
- rembg AI library
- onnxruntime
- **AI models from /models directory** ← This is the key!
- All assets (icons, etc.)

**Build time:** 2-5 minutes depending on your machine

**Output:** `dist/BackgroundRemover.exe` (~350-400MB with bundled models)

### Step 4: Test the Executable OFFLINE
**Critical test - disconnect from internet!**

```powershell
# Disconnect from internet or disable network adapter
# Then run:
.\dist\BackgroundRemover.exe "test_image.jpg"
```

**Expected behavior:**
- ✅ Shows: "✓ Using bundled models (no internet required)"
- ✅ Processes image successfully
- ✅ No download attempts
- ✅ Fast processing (~5-15 seconds)

**If it tries to download:**
- ❌ Models weren't bundled correctly
- Check `/models` directory exists and has .onnx files
- Rebuild with `--clean` flag

### Step 5: Create Installer
```powershell
# Create Windows installer (Inno Setup required)
iscc installer_config.iss
```

**Output:** `output/BackgroundRemover_Setup.exe` (~150-180MB compressed)

**What the installer includes:**
- BackgroundRemover.exe (with bundled models)
- Uninstaller
- Start menu shortcuts
- Desktop shortcut
- Context menu integration

### Step 6: Test Installation on Clean Machine
**This is the ultimate test!**

1. Copy `output/BackgroundRemover_Setup.exe` to a test machine
2. **Disconnect internet** on test machine
3. Run installer
4. Use the app on a test image
5. Should work perfectly offline!

## File Size Reference

| Component | Size | Notes |
|-----------|------|-------|
| AI Models (uncompressed) | ~170MB | BiRefNet-Portrait |
| BackgroundRemover.exe | ~350MB | With bundled models |
| Installer (compressed) | ~150MB | Compressed with Inno Setup |
| After installation | ~350MB | On user's machine |

## Verification Checklist

Before distributing to users:

- [ ] Downloaded models with `download_models.py`
- [ ] Models directory exists with .onnx files
- [ ] Built exe with: `python -m PyInstaller build_optimized.spec --clean`
- [ ] Tested exe **offline** - no internet needed
- [ ] Created installer with Inno Setup
- [ ] Tested installer on clean Windows machine **offline**
- [ ] Verified no "Failed to initialize AI model" errors
- [ ] Confirmed fast processing (no download delays)

## Troubleshooting

### "Failed to initialize AI model" (even after bundling)
```powershell
# Check if models are in the exe directory
dir dist\models

# Should show .onnx files
# If missing, rebuild after running download_models.py
```

### Models not bundling
```powershell
# Verify models directory exists
dir models

# Check build_optimized.spec includes:
# ('models', 'models'),  # in datas section

# Clean rebuild
Remove-Item -Recurse -Force build, dist
python -m PyInstaller build_optimized.spec --clean --noconfirm
```

### Exe is too large
**This is normal!** AI models are ~170MB. Options:
1. Accept the size (users get offline functionality)
2. Don't bundle models (users need internet once)
3. Use smaller model like U2Net-lite (lower quality)

**Recommended:** Keep bundled models for best user experience

### Download script fails
```powershell
# Check internet connection
ping google.com

# Check dependencies
pip install -r src/requirements.txt

# Try manual download
python -c "from rembg import new_session; new_session('birefnet-portrait')"
```

## Build Script (Automated)

Create `build_all.bat`:
```batch
@echo off
echo ================================================
echo Building Background Remover (Offline Version)
echo ================================================

echo.
echo Step 1: Downloading AI models...
python download_models.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Model download failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Building executable...
python -m PyInstaller build_optimized.spec --clean --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Creating installer...
iscc installer_config.iss
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Installer creation failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo ✅ BUILD COMPLETE!
echo ================================================
echo.
echo Executable: dist\BackgroundRemover.exe
echo Installer:  output\BackgroundRemover_Setup.exe
echo.
echo Test offline before distributing!
pause
```

## Testing Script

Create `test_offline.bat`:
```batch
@echo off
echo Testing Background Remover OFFLINE...
echo.
echo Please disconnect from internet, then press any key...
pause

dist\BackgroundRemover.exe test_image.jpg

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! App works offline!
) else (
    echo.
    echo ❌ FAILED! Check for errors above.
)
pause
```

## Distribution

### For End Users:
1. Provide `BackgroundRemover_Setup.exe`
2. Tell them: "No internet required - all AI models included!"
3. File size: ~150MB (compressed installer)

### For Updates:
1. Rebuild following this guide
2. Increment version number
3. Test offline functionality
4. Distribute new installer

---

## Summary

✅ **Download models first:** `python download_models.py`
✅ **Build with bundling:** `python -m PyInstaller build_optimized.spec --clean`
✅ **Test offline:** Disconnect internet and test
✅ **Create installer:** `iscc installer_config.iss`
✅ **Distribute:** Users get 100% offline app!

**Result:** Users can use Background Remover anywhere, anytime, without internet! 🎉
