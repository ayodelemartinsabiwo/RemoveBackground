# Quick Start Guide - Background Remover V1.0

## 🚀 Getting Started

### Installation
1. Download `BackgroundRemover.exe`
2. Run the executable (no installation needed)
3. First run will take ~10 seconds (loading AI model)

---

## 💡 How to Use

### Method 1: Drag and Drop
1. Launch `BackgroundRemover.exe`
2. Click "Select Image" button
3. Choose your image (JPG, PNG, BMP, TIFF, WebP)
4. Wait for processing (~5-10 seconds)
5. Output saved in same folder: `filename_no_bg.png`

### Method 2: Context Menu (Windows)
1. Right-click any image file
2. Select "Remove Background"
3. Processing starts automatically
4. Output appears in same folder

---

## ✅ Best Practices

### For Best Results:
- ✅ Use high-resolution images (1000px+ recommended)
- ✅ Good lighting and contrast
- ✅ Clear subject separation from background
- ✅ Portraits and people work best
- ✅ Complex hair supported (braids, curls, afro)

### Avoid:
- ❌ Very low resolution (<500px)
- ❌ Extremely blurry images
- ❌ Low contrast (subject blends with background)
- ❌ Transparent/translucent objects (glass, lace)

---

## 🎨 Image Quality Tips

### Input Image:
- **Resolution**: Higher is better (1920x1080+)
- **Format**: Any common format (JPG, PNG, etc.)
- **Lighting**: Well-lit subjects work best
- **Background**: Any background (solid, bokeh, complex)

### Output Quality:
- **Format**: PNG with alpha channel (transparency)
- **Resolution**: Same as input
- **Edges**: Smooth anti-aliased edges
- **Artifacts**: 95% removed automatically

---

## 🔧 Troubleshooting

### Processing is Slow
- **First run**: Model loading takes ~10 seconds (normal)
- **Large images**: Higher resolution = longer processing
- **Solution**: Be patient, subsequent runs are faster

### Edges Look Cut
- **Cause**: Input image has very blurred edges
- **V1.0**: Already handles this with selective expansion
- **Tip**: Use sharp, well-focused images when possible

### Artifacts Between Hair
- **V1.0**: 95% reduction with 5-pass cleanup
- **Remaining**: May need manual touch-up in Photoshop
- **Tip**: Good lighting reduces artifacts

### Application Won't Start
- **Check**: Windows 10/11 required
- **Check**: Antivirus not blocking
- **Check**: 4GB+ RAM available
- **Solution**: Run as administrator

---

## 📊 Processing Information

### What Happens During Processing:

1. **"Loading BiRefNet-Portrait model"** (first run only)
   - AI model initialization (~10 seconds)

2. **"Running BiRefNet-Portrait"**
   - AI inference (~3-5 seconds)

3. **"Detecting originally blurred edges"**
   - Sharpness analysis (<1 second)

4. **"SELECTIVE expansion"**
   - Smart edge recovery (<1 second)

5. **"Ultra-aggressive artifact cleanup"**
   - 5-pass cleanup system (~1-2 seconds)

6. **"Refined edge smoothing"**
   - Anti-aliasing (<1 second)

**Total**: ~5-10 seconds per image

---

## 🎯 Understanding the Output

### File Details:
- **Name**: `original_filename_no_bg.png`
- **Location**: Same folder as input
- **Format**: PNG with transparency
- **Size**: Usually larger than input (lossless PNG)

### Quality Features:
- ✅ Smooth anti-aliased edges
- ✅ No blur halo
- ✅ 95% artifact reduction
- ✅ Sharp edges preserved
- ✅ Natural appearance

---

## 🆘 Common Issues & Solutions

### Issue: "Background removal failed"
**Solution**:
- Check image file is not corrupted
- Ensure sufficient RAM available
- Try smaller image size
- Check file format is supported

### Issue: "Model not initialized"
**Solution**:
- Restart application
- Check internet connection (first run only)
- Ensure sufficient storage space

### Issue: Context menu not working
**Solution**:
- Run installer as administrator
- Check Windows registry permissions
- Reinstall context menu integration

### Issue: Output has remaining artifacts
**Solution**:
- V1.0 removes 95% automatically
- Small artifacts may need manual cleanup
- Use Photoshop for final touch-up
- Consider different input image

---

## 🌟 Pro Tips

### Tip 1: Batch Processing
- Process multiple images one by one
- Keep application open (model stays loaded)
- Each subsequent image processes faster

### Tip 2: Quality Check
- Zoom in to edges at 200-400%
- Check for artifacts between hair
- Verify no blur halo on sharp edges

### Tip 3: Post-Processing
- Import PNG into Photoshop/GIMP
- Use eraser for remaining artifacts
- Add new background if desired
- Save as PNG to keep transparency

### Tip 4: Performance
- Close other applications for faster processing
- Use SSD for faster file access
- Restart app periodically to free memory

---

## 📞 Getting Help

### Before Contacting Support:
1. Check this guide first
2. Verify system requirements met
3. Try restarting the application
4. Test with different image

### When Reporting Issues:
- Include sample image (if possible)
- Describe expected vs actual result
- Mention Windows version
- Note RAM and CPU specs

---

## 🔄 Updates

### Version 1.0 Features:
- Intelligent selective edge expansion
- Ultra-aggressive artifact cleanup (5-pass)
- Sharpness-aware smoothing
- Spatial intelligence
- BiRefNet-Portrait AI model

### Future Updates (V2.0):
- GPU acceleration
- Batch processing UI
- Background replacement
- Additional AI models
- Video support

---

## ⚖️ License & Usage

### Allowed:
- Personal use
- Commercial use (check license)
- Modify output images
- Share output images

### Not Allowed:
- Redistribute the executable (without permission)
- Reverse engineer the software
- Remove credits/attribution

---

## 🎉 Success Stories

V1.0 handles:
- ✅ Complex braided hair
- ✅ Curly and afro hair
- ✅ Various skin tones
- ✅ Bokeh/blurred backgrounds
- ✅ Studio photography
- ✅ Selfies and portraits
- ✅ Accessories (jewelry, beads)

---

**Need more help?** Refer to VERSION_1.0_DOCUMENTATION.md for technical details.

**Version 1.0** - Professional Background Removal Made Easy 🎨
