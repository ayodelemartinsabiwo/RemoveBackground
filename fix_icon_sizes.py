"""
Resize the PNG icons to exact Windows sizes and regenerate ICO
"""
from PIL import Image
import os

# Target sizes for Windows
sizes = [16, 24, 32, 48, 64, 128, 256]

print("Resizing PNG icons to exact Windows sizes...")
print("="*60)

png_folder = "assets/Icon PNGs"
corrected_folder = "assets/Icon PNGs Corrected"

# Create corrected folder
os.makedirs(corrected_folder, exist_ok=True)

for size in sizes:
    # Find the source PNG (might be 2x size)
    source_path = os.path.join(png_folder, f"icon_{size}x{size}.png")

    if os.path.exists(source_path):
        img = Image.open(source_path)
        current_size = img.size[0]

        print(f"Processing {size}×{size}:")
        print(f"  Current size: {current_size}×{current_size}")

        # Resize to exact target size with high-quality downsampling
        if current_size != size:
            img_resized = img.resize(
                (size, size),
                Image.Resampling.LANCZOS  # Highest quality downsampling
            )
            print(f"  Resized to: {size}×{size}")
        else:
            img_resized = img
            print(f"  Already correct size")

        # Save corrected PNG
        output_path = os.path.join(corrected_folder, f"icon_{size}x{size}.png")
        img_resized.save(output_path, 'PNG', optimize=True)
        print(f"  Saved: {output_path}")
        print()
    else:
        print(f"✗ Missing: {source_path}\n")

print("="*60)
print("✓ All PNGs resized to exact Windows sizes!")
print(f"✓ Saved in: {corrected_folder}")
print("\nNow regenerating ICO file...")

# Import the proper ICO creator
import sys
sys.path.insert(0, '.')
from create_proper_ico import create_ico_from_pngs

# Create ICO from corrected PNGs
output_ico = "assets/icon.ico"
success = create_ico_from_pngs(corrected_folder, output_ico)

if success:
    print("\n" + "="*60)
    print("SUCCESS! Icon files are now correctly sized!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: .\\build_fixed.bat")
    print("2. After build, reinstall the application")
    print("3. Run: rebuild_icon_cache.bat (as Administrator)")
