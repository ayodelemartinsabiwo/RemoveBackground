# Testing Checklist for Background Remover

## Pre-Build Testing (Development Environment)

### ✅ Test 1: Environment Setup
- [ ] Virtual environment activated
- [ ] All dependencies installed: `pip list | findstr rembg`
- [ ] Python version 3.8+: `python --version`

**Run:**
```powershell
python -c "import rembg, PIL, cv2, numpy; print('All imports OK')"
```

### ✅ Test 2: Download AI Models
- [ ] Run: `python download_models.py`
- [ ] Models downloaded to `/models` directory
- [ ] Check file size: `dir models` (should see ~170-973MB .onnx file)
- [ ] Model verified by download script

**Expected files:**
- `models/birefnet-portrait.onnx` (~973MB) OR
- `models/u2net.onnx` (~176MB)

### ✅ Test 3: Quick Functionality Test
- [ ] Run: `python test_quick.py`
- [ ] All 5 tests pass
- [ ] Test image processed successfully
- [ ] Output image created with transparency

**Expected output:**
```
✅ ALL TESTS PASSED!
The background remover is working correctly!
```

### ✅ Test 4: Direct Script Test
- [ ] Run: `python src/bg_remove_v1_2_bulletproof.py blackhairtest.jpg`
- [ ] Background removed successfully
- [ ] Output file created with `_no_bg_YYYYMMDD.png` suffix
- [ ] Processing time reasonable (< 30 seconds)

### ✅ Test 5: Main Application Test
- [ ] Run: `python src/main_optimized.py blackhairtest.jpg`
- [ ] Loader window appears
- [ ] Progress messages display
- [ ] Background removed successfully
- [ ] Success message shown

---

## Build Testing

### ✅ Test 6: Build Executable
- [ ] Run: `python -m PyInstaller build_optimized.spec --clean --noconfirm`
- [ ] Build completes without errors
- [ ] Executable created: `dist/BackgroundRemover.exe`
- [ ] Check size: Should be ~400-500MB (with bundled models)

**Check bundled models:**
```powershell
# Models should be in the executable directory
dir dist\models
```

### ✅ Test 7: Test Executable ONLINE
- [ ] Run: `dist\BackgroundRemover.exe blackhairtest.jpg`
- [ ] Shows: "✓ Using bundled models (no internet required)"
- [ ] Processes image successfully
- [ ] No download attempts
- [ ] Output file created

### ✅ Test 8: Test Executable OFFLINE (Critical!)
- [ ] Disconnect from internet OR disable network adapter
- [ ] Run: `dist\BackgroundRemover.exe Fripikbigtest.jpg`
- [ ] Should work WITHOUT internet
- [ ] No error about downloading models
- [ ] Image processed successfully

**If this fails:**
- Models weren't bundled correctly
- Check if `/models` directory exists with .onnx files
- Rebuild with: `python download_models.py` then rebuild

---

## Installer Testing

### ✅ Test 9: Create Installer
- [ ] Run: `iscc installer_config.iss` OR `build_offline_version.bat`
- [ ] Installer created: `output/BackgroundRemover_Setup.exe`
- [ ] Check size: Should be ~150-200MB (compressed)

### ✅ Test 10: Test Installer on Same Machine
- [ ] Run installer: `output/BackgroundRemover_Setup.exe`
- [ ] Installation completes successfully
- [ ] Desktop shortcut created
- [ ] Start menu entry created
- [ ] Context menu registered

### ✅ Test 11: Test Installed Application ONLINE
- [ ] Right-click a test image → "Remove Background"
- [ ] Or run from Start Menu
- [ ] Processes image successfully
- [ ] Output created in same folder

### ✅ Test 12: Test Installed Application OFFLINE
- [ ] Disconnect from internet
- [ ] Process another image
- [ ] Should work without internet!
- [ ] Verify no "Failed to initialize AI model" error

---

## Clean Machine Testing (Most Important!)

### ✅ Test 13: Fresh Windows Machine (Virtual Machine or Different PC)
**Requirements:**
- Clean Windows 10 or 11 installation
- NO Python installed
- NO previous Background Remover installation
- **INTERNET DISCONNECTED** (to verify offline functionality)

**Steps:**
1. [ ] Copy `output/BackgroundRemover_Setup.exe` to test machine
2. [ ] Disconnect internet on test machine
3. [ ] Run installer
4. [ ] Installation completes
5. [ ] Right-click a test image → "Remove Background"
6. [ ] Image processes successfully WITHOUT internet
7. [ ] Output file created with transparency

**If this test fails:**
- Models weren't bundled in installer
- Go back to Test 6 and verify models are in `dist/models/`

### ✅ Test 14: Context Menu Integration
- [ ] Context menu appears for .jpg files
- [ ] Context menu appears for .png files
- [ ] "Remove Background" option visible
- [ ] Clicking it processes the image
- [ ] Can process multiple images in sequence

### ✅ Test 15: Various Image Types
Test with different image formats:
- [ ] JPG/JPEG images
- [ ] PNG images (with transparency)
- [ ] PNG images (without transparency)
- [ ] BMP images
- [ ] WEBP images (if supported)

### ✅ Test 16: Various Image Sizes
- [ ] Small images (< 1MB)
- [ ] Medium images (1-5MB)
- [ ] Large images (5-20MB)
- [ ] Very large images (> 20MB)

### ✅ Test 17: Edge Cases
- [ ] Image with complex hair
- [ ] Image with transparent background (input)
- [ ] Image with very dark background
- [ ] Image with very light background
- [ ] Portrait photos
- [ ] Object photos (non-human)

---

## Performance Testing

### ✅ Test 18: Processing Speed
- [ ] Small image (< 1MB): Should be < 10 seconds
- [ ] Medium image (1-5MB): Should be < 20 seconds
- [ ] Large image (> 5MB): Should be < 30 seconds

### ✅ Test 19: Memory Usage
- [ ] Monitor RAM during processing
- [ ] Should use < 2GB RAM for typical images
- [ ] No memory leaks (test multiple images in sequence)

### ✅ Test 20: Multiple Processes
- [ ] Process 5 images in quick succession
- [ ] All complete successfully
- [ ] No conflicts or errors
- [ ] Output quality consistent

---

## Error Handling Testing

### ✅ Test 21: Invalid Input
- [ ] Non-image file: Should show error
- [ ] Corrupted image: Should handle gracefully
- [ ] Non-existent file: Should show error

### ✅ Test 22: Permission Issues
- [ ] Read-only input file: Should still work
- [ ] Write-protected output folder: Should show error
- [ ] Network drive: Should work if accessible

### ✅ Test 23: Uninstall
- [ ] Run uninstaller from Start Menu
- [ ] Or use Windows Settings → Uninstall
- [ ] Context menu removed
- [ ] Desktop shortcut removed
- [ ] Program Files folder removed
- [ ] Registry entries cleaned up

---

## Final Checklist Before Release

- [ ] All 23 tests passed
- [ ] Tested on at least 2 different Windows machines
- [ ] Tested offline functionality confirmed
- [ ] No "Failed to initialize AI model" errors
- [ ] Models are bundled (file size ~150-200MB installer)
- [ ] Documentation updated (README, USER_GUIDE)
- [ ] Version number updated
- [ ] Release notes prepared

---

## Quick Test Commands

```powershell
# Complete test sequence
python download_models.py                    # Download models
python test_quick.py                         # Quick test
python -m PyInstaller build_optimized.spec --clean  # Build
dist\BackgroundRemover.exe blackhairtest.jpg # Test exe
# Disconnect internet
dist\BackgroundRemover.exe Fripikbigtest.jpg # Test offline
iscc installer_config.iss                    # Create installer
```

---

## Test Results Log

| Test | Status | Notes | Date |
|------|--------|-------|------|
| 1. Environment Setup | ⬜ | | |
| 2. Download Models | ⬜ | | |
| 3. Quick Test | ⬜ | | |
| 4. Direct Script | ⬜ | | |
| 5. Main App | ⬜ | | |
| 6. Build Exe | ⬜ | | |
| 7. Exe Online | ⬜ | | |
| 8. Exe Offline | ⬜ | | |
| 9. Create Installer | ⬜ | | |
| 10. Install Same PC | ⬜ | | |
| 11. Installed Online | ⬜ | | |
| 12. Installed Offline | ⬜ | | |
| 13. Clean Machine | ⬜ | | |
| 14. Context Menu | ⬜ | | |
| 15. Image Types | ⬜ | | |
| 16. Image Sizes | ⬜ | | |
| 17. Edge Cases | ⬜ | | |
| 18. Speed | ⬜ | | |
| 19. Memory | ⬜ | | |
| 20. Multiple | ⬜ | | |
| 21. Invalid Input | ⬜ | | |
| 22. Permissions | ⬜ | | |
| 23. Uninstall | ⬜ | | |

**Legend:** ⬜ Not tested | ✅ Passed | ❌ Failed | ⚠️ Partial

---

**Remember: Test 13 (Clean Machine Offline) is THE most important test!**
