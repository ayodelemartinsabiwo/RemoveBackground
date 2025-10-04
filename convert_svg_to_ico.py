#!/usr/bin/env python3
"""
Convert SVG files to ICO format
Converts the custom SVG icons in assets/Icon SVGs/ to a multi-resolution .ico file
"""

from PIL import Image
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication
import os
import io
import sys

def svg_to_qimage(svg_path, size):
    """Convert SVG to QImage at specified size using PyQt6 with 8x supersampling for maximum quality"""
    try:
        # Create SVG renderer
        renderer = QSvgRenderer(svg_path)

        if not renderer.isValid():
            print(f"Error: Invalid SVG file: {svg_path}")
            return None

        # Use 8x supersampling for maximum anti-aliasing quality
        # This renders at 8x the target size, then scales down
        scale = 8
        high_res_size = size * scale

        # Create high-resolution QImage with premultiplied alpha for better quality
        image = QImage(high_res_size, high_res_size, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(0)  # Transparent background

        # Render SVG to high-res QImage with maximum quality settings
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)

        # Render SVG at high resolution
        renderer.render(painter)
        painter.end()

        # Scale down to target size with smooth transformation
        # This produces Lanczos-like quality
        final_image = image.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        return final_image
    except Exception as e:
        print(f"Error converting {svg_path}: {e}")
        return None

def qimage_to_pil(qimage):
    """Convert QImage to PIL Image with proper color profile"""
    # Convert QImage to bytes
    buffer = qimage.bits().asstring(qimage.sizeInBytes())
    # BGRA format from Qt needs to be converted to RGBA for PIL
    pil_image = Image.frombytes("RGBA", (qimage.width(), qimage.height()), buffer, "raw", "BGRA")
    return pil_image

def create_ico_from_svgs(svg_folder, output_path):
    """Create a multi-resolution ICO file from SVG files"""

    # Define the SVG files and their corresponding sizes
    svg_files = {
        16: "bg icon_16 x 16.svg",
        24: "bg icon_24 x 24.svg",
        32: "bg icon_32 x 32.svg",
        48: "bg icon_48 x 48.svg",
        64: "bg icon_64 x 64.svg",
        128: "bg icon_128 x 128.svg",
        256: "bg icon_256 x 256.svg"
    }

    images = []

    print("SVG to ICO Converter")
    print("=" * 50)

    for size, filename in svg_files.items():
        svg_path = os.path.join(svg_folder, filename)

        if not os.path.exists(svg_path):
            print(f"⚠️  Warning: {filename} not found, skipping...")
            continue

        print(f"Converting {filename} to {size}x{size} PNG...")

        # Convert SVG to QImage
        qimage = svg_to_qimage(svg_path, size)

        if qimage:
            # Convert QImage to PIL Image
            pil_image = qimage_to_pil(qimage)
            images.append(pil_image)
            print(f"✅ Converted {size}x{size}")
        else:
            print(f"❌ Failed to convert {size}x{size}")

    if not images:
        print("\n❌ Error: No images were converted!")
        return False

    # Backup existing icon if it exists
    if os.path.exists(output_path):
        backup_path = output_path.replace('.ico', '_backup.ico')
        try:
            os.replace(output_path, backup_path)
            print(f"\n📁 Backed up existing icon to: {backup_path}")
        except:
            pass

    # Save as ICO with all sizes and maximum quality
    print(f"\n💾 Saving multi-resolution ICO to: {output_path}")
    print(f"   Note: ICO format has quality limitations - use PNG files for best results")

    # Save ICO for Windows shell integration (shortcuts, context menu)
    # ICO format is required for these contexts but has inherent quality loss
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )

    print(f"\n🎉 SUCCESS!")
    print(f"   Created: {output_path}")
    print(f"   Resolutions: {', '.join([f'{img.width}x{img.height}' for img in images])}")

    # Also save individual PNG files for maximum quality (Adobe approach)
    # Windows can use these directly for better quality than ICO in some contexts
    print(f"\n💾 Also saving individual PNG files for maximum quality...")
    png_folder = os.path.join("assets", "Icon PNGs")
    os.makedirs(png_folder, exist_ok=True)

    for img in images:
        png_path = os.path.join(png_folder, f"icon_{img.width}x{img.height}.png")
        img.save(png_path, format='PNG', optimize=True)
        print(f"   ✅ Saved: icon_{img.width}x{img.height}.png")

    print(f"\n   This icon will now be used for:")
    print(f"   • Desktop shortcut")
    print(f"   • Context menu")
    print(f"   • Installed app icon")
    print(f"   • Windows 'Installed Apps' section")

    return True

if __name__ == "__main__":
    # Create QApplication (required for PyQt6)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Paths
    svg_folder = os.path.join("assets", "Icon SVGs")
    output_ico = os.path.join("assets", "icon.ico")

    # Convert SVGs to ICO
    success = create_ico_from_svgs(svg_folder, output_ico)

    if not success:
        exit(1)
