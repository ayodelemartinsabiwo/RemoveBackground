"""
Verify the icon files are correct and show their details
"""
import os
from PIL import Image

print("="*60)
print("Icon File Verification")
print("="*60)

# Check ICO file
ico_path = "assets/icon.ico"
if os.path.exists(ico_path):
    print(f"\n✓ ICO File: {ico_path}")
    print(f"  Size: {os.path.getsize(ico_path):,} bytes")

    try:
        ico = Image.open(ico_path)
        print(f"  Format: {ico.format}")
        print(f"  Main size: {ico.size}")
        print(f"  Mode: {ico.mode}")
    except Exception as e:
        print(f"  Error reading: {e}")
else:
    print(f"\n✗ ICO File NOT FOUND: {ico_path}")

# Check PNG files
print(f"\n✓ PNG Files in assets/Icon PNGs/:")
png_folder = "assets/Icon PNGs"
if os.path.exists(png_folder):
    for filename in sorted(os.listdir(png_folder)):
        if filename.endswith('.png'):
            png_path = os.path.join(png_folder, filename)
            size = os.path.getsize(png_path)
            try:
                img = Image.open(png_path)
                print(f"  {filename:25} - {size:,} bytes - {img.size[0]}x{img.size[1]} - {img.mode}")
            except Exception as e:
                print(f"  {filename:25} - ERROR: {e}")
else:
    print("  ✗ PNG folder NOT FOUND")

# Check EXE file
exe_path = "dist/BackgroundRemover.exe"
if os.path.exists(exe_path):
    print(f"\n✓ EXE File: {exe_path}")
    print(f"  Size: {os.path.getsize(exe_path):,} bytes")
    print(f"  Modified: {os.path.getmtime(exe_path)}")

    # Try to extract icon info from EXE
    print(f"\n  Note: EXE should contain embedded icon from {ico_path}")
    print(f"  Check build log for: 'INFO: Copying icon to EXE'")
else:
    print(f"\n✗ EXE File NOT FOUND: {exe_path}")

print("\n" + "="*60)
print("Verification complete!")
print("="*60)
print("\nIf desktop/taskbar icons are still old:")
print("1. Run: rebuild_icon_cache.bat (as Administrator)")
print("2. Delete old desktop shortcut")
print("3. Reinstall application")
print("4. Create new desktop shortcut")
