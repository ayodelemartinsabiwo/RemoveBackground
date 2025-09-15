import os
import sys
import subprocess

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")

    # Install packages from requirements.txt
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'src/requirements.txt'
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_assets_folder():
    """Create assets folder and placeholder files"""
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"✅ Created {assets_dir} directory")

    # Create placeholder icon file
    icon_path = os.path.join(assets_dir, "icon.ico")
    if not os.path.exists(icon_path):
        # Create a simple text file as placeholder
        with open(icon_path + ".placeholder", "w") as f:
            f.write("Replace this with a real .ico file (32x32 or 48x48 pixels)")
        print(f"📝 Created icon placeholder: {icon_path}.placeholder")

    # Create placeholder splash file
    splash_path = os.path.join(assets_dir, "splash.bmp")
    if not os.path.exists(splash_path):
        with open(splash_path + ".placeholder", "w") as f:
            f.write("Replace this with a real .bmp file (164x314 pixels) for installer splash")
        print(f"📝 Created splash placeholder: {splash_path}.placeholder")

def test_imports():
    """Test if all required modules can be imported"""
    print("\nTesting imports...")

    try:
        import PyQt6
        print("✅ PyQt6 imported successfully")
    except ImportError:
        print("❌ PyQt6 import failed")
        return False

    try:
        import rembg
        print("✅ rembg imported successfully")
    except ImportError:
        print("❌ rembg import failed")
        return False

    try:
        import PIL
        print("✅ Pillow imported successfully")
    except ImportError:
        print("❌ Pillow import failed")
        return False

    try:
        import onnxruntime
        print("✅ onnxruntime imported successfully")
    except ImportError:
        print("❌ onnxruntime import failed")
        return False

    return True

def main():
    print("🚀 Setting up Background Remover Application...")
    print("=" * 50)

    # Create assets folder
    create_assets_folder()

    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        return False

    # Test imports
    if not test_imports():
        print("\n❌ Setup failed during import testing")
        return False

    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Replace asset placeholders with real files:")
    print("   - assets/icon.ico (32x32 Windows icon)")
    print("   - assets/splash.bmp (164x314 installer splash)")
    print("2. Test the application:")
    print("   python src/main.py <path_to_test_image>")
    print("3. Build executable:")
    print("   build.bat")
    print("4. Create installer with Inno Setup")

    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
