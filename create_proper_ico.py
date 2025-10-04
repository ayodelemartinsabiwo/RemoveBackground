#!/usr/bin/env python3
"""
Create a proper multi-resolution ICO file from PNG files
Works around Pillow's broken append_images for ICO format
"""

from PIL import Image
import struct
import os

def create_ico_from_pngs(png_folder, output_ico):
    """
    Create a proper multi-resolution ICO file manually
    This bypasses Pillow's broken append_images for ICO
    """

    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    print("Creating Windows ICO file from PNG sources...")
    print("=" * 50)

    # Load all PNG files
    for size in sizes:
        png_path = os.path.join(png_folder, f"icon_{size}x{size}.png")
        if os.path.exists(png_path):
            img = Image.open(png_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            images.append((size, img))
            print(f"✅ Loaded: icon_{size}x{size}.png")
        else:
            print(f"⚠️  Missing: icon_{size}x{size}.png")

    if not images:
        print("\n❌ Error: No PNG files found!")
        return False

    # Backup existing ICO
    if os.path.exists(output_ico):
        backup_path = output_ico.replace('.ico', '_backup.ico')
        try:
            os.replace(output_ico, backup_path)
            print(f"\n📁 Backed up existing: {backup_path}")
        except:
            pass

    print(f"\n💾 Creating ICO file: {output_ico}")

    # Write ICO file manually
    with open(output_ico, 'wb') as f:
        # ICO Header
        f.write(struct.pack('<HHH', 0, 1, len(images)))  # Reserved, Type (1=ICO), Count

        # Directory entries
        offset = 6 + (16 * len(images))  # Header + all directory entries

        entries_data = []
        for size, img in images:
            # Convert image to PNG in memory
            from io import BytesIO
            png_data = BytesIO()
            img.save(png_data, format='PNG')
            png_bytes = png_data.getvalue()

            # ICO Directory Entry
            width = size if size < 256 else 0  # 0 means 256
            height = size if size < 256 else 0

            entry = struct.pack('<BBBBHHII',
                width,           # Width (0 = 256)
                height,          # Height (0 = 256)
                0,               # Color palette (0 = no palette)
                0,               # Reserved
                1,               # Color planes
                32,              # Bits per pixel
                len(png_bytes),  # Size of image data
                offset           # Offset to image data
            )

            entries_data.append((entry, png_bytes))
            offset += len(png_bytes)

        # Write all directory entries
        for entry, _ in entries_data:
            f.write(entry)

        # Write all image data
        for _, png_bytes in entries_data:
            f.write(png_bytes)

    file_size = os.path.getsize(output_ico)
    print(f"\n🎉 SUCCESS!")
    print(f"   Created: {output_ico}")
    print(f"   File size: {file_size:,} bytes")
    print(f"   Resolutions: {', '.join([f'{size}x{size}' for size, _ in images])}")
    print(f"\n   This ICO contains PNG-compressed data for maximum quality!")
    print(f"   Ready for:")
    print(f"   • Desktop shortcuts")
    print(f"   • Context menu")
    print(f"   • Windows Explorer")
    print(f"   • Installer")

    return True

if __name__ == "__main__":
    png_folder = os.path.join("assets", "Icon PNGs")
    output_ico = os.path.join("assets", "icon.ico")

    success = create_ico_from_pngs(png_folder, output_ico)

    if not success:
        exit(1)
