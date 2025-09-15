# Background Remover - Windows Desktop Application

A professional Windows desktop application that removes image backgrounds with smooth, refined edges using AI technology.

## Features

- **One-click background removal** via Windows right-click context menu
- **AI-powered processing** handles complex images (hair, models, objects, buildings)
- **Transparent PNG output** by default
- **Professional orange-themed installer**
- **Modern loader window** with progress indication
- **Self-contained** - no Python installation required

## Project Structure

```
/background_remover_app
    /src
        main.py                # Entry point and threading logic
        gui_loader.py          # Modern loader window with orange theme
        bg_remove.py           # Background removal using rembg
        context_menu.py        # Windows registry integration
        requirements.txt       # Python dependencies
    /assets
        icon.ico              # Application icon
        splash.bmp            # Installer splash image
    build.spec               # PyInstaller configuration
    installer_config.iss     # Inno Setup installer script
    build.bat               # Build automation script
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r src/requirements.txt
```

### 2. Test the Application

```bash
python src/main.py "path/to/test/image.jpg"
```

### 3. Build Executable

```bash
# Use the build script
build.bat

# Or manually:
pyinstaller build.spec --clean --noconfirm
```

### 4. Create Installer

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Open `installer_config.iss` in Inno Setup
3. Click **Build** > **Compile**
4. Installer will be created in `output/BackgroundRemover_Setup.exe`

## Usage

### For End Users

1. **Install**: Run `BackgroundRemover_Setup.exe`
2. **Use**: Right-click any image → "Remove Background"
3. **Output**: Transparent PNG saved in same folder with `_bg_removed` suffix

### For Developers

#### Testing Locally
```bash
# Test background removal
python src/main.py "sample_image.jpg"

# Test context menu installation (run as admin)
python src/context_menu.py install "C:/path/to/BackgroundRemover.exe"
```

#### Building Distribution
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
pyinstaller build.spec --clean --noconfirm

# Result: dist/BackgroundRemover.exe
```

## Technical Details

### Dependencies

- **rembg**: AI background removal engine
- **PyQt6**: Modern cross-platform GUI framework
- **Pillow**: Python Imaging Library for image processing
- **onnxruntime**: ONNX Runtime for AI model execution

### Architecture

- **Multi-threaded design**: GUI remains responsive during AI processing
- **Registry integration**: Clean Windows context menu integration
- **Error handling**: Comprehensive error reporting and recovery
- **Self-contained**: All dependencies bundled in single executable

### Supported Image Formats

- **Input**: JPG, JPEG, PNG, BMP, TIFF, WEBP
- **Output**: PNG with transparency (default) or JPG with white background

## Advanced Features

### Custom Background Colors

Extend the `BackgroundRemover` class to support different background colors:

```python
def remove_background_with_color(self, input_path, bg_color=(255, 255, 255)):
    # Implementation for custom background colors
    pass
```

### Batch Processing

Add support for processing multiple files:

```python
def process_multiple_images(self, image_paths):
    # Implementation for batch processing
    pass
```

## Troubleshooting

### Common Build Issues

**Missing dependencies:**
```bash
pip install --upgrade pip
pip install -r src/requirements.txt
```

**PyInstaller errors:**
```bash
pip install --upgrade pyinstaller
pyinstaller --clean build.spec
```

**Large executable size:**
- Normal behavior due to AI models (~200MB)
- Models are downloaded on first run

### Runtime Issues

**Context menu not appearing:**
- Run installer as Administrator
- Check Windows registry for entries

**Slow first-time processing:**
- AI models download automatically on first use
- Subsequent runs are much faster

**Memory errors with large images:**
- Ensure sufficient RAM (4GB+ recommended)
- Close other applications during processing

### Installation Issues

**Installer won't run:**
- Right-click installer → "Run as Administrator"
- Disable antivirus temporarily during installation

**Context menu missing after install:**
- Restart Windows Explorer: `taskkill /f /im explorer.exe && start explorer.exe`
- Or restart computer

## Development

### Project Setup

```bash
# Clone and setup
git clone <repository>
cd background_remover_app

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Document all public methods
- Add error handling for external dependencies

### Testing

```bash
# Test individual components
python src/bg_remove.py
python src/context_menu.py install "test_path"
python src/gui_loader.py

# Test full application
python src/main.py "test_image.jpg"
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with description

## License

This project is open source. Individual components may have their own licenses:
- rembg: Apache License 2.0
- PyQt6: GPL v3 / Commercial License
- Pillow: PIL Software License

## Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing GitHub issues
3. Create new issue with detailed description and error logs

---

**Happy background removing! 🎨**
