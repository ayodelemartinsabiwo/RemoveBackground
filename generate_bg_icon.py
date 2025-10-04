#!/usr/bin/env python3
"""
Generate BG Icon Script
Creates a new icon.ico file matching the programmatic BG icon design.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QPen, QFont, QColor
from PyQt6.QtCore import Qt
from PIL import Image
import sys
import os

def create_bg_icon_pixmap(size=256):
    """Create a BG icon pixmap at the specified size matching the reference design"""
    # Use 4x supersampling for ultra-smooth anti-aliasing
    scale = 4
    high_res_size = size * scale

    pixmap = QPixmap(high_res_size, high_res_size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    # Enable all quality rendering hints
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)

    # Minimal padding to maximize icon size while preventing edge clipping
    padding = int(high_res_size * 0.015)  # 1.5% padding for smoother edges
    circle_size = high_res_size - (padding * 2)

    # Draw orange circle with a subtle darker border for smooth edges
    orange_color = QColor('#FF6B35')  # PRIMARY_ORANGE matching reference

    # First, draw a slightly darker outer circle for smooth anti-aliasing
    darker_orange = QColor('#E55A2A')  # Slightly darker for border
    border_width = max(int(high_res_size * 0.005), 1)  # 0.5% border
    painter.setBrush(QBrush(darker_orange))
    painter.setPen(QPen(Qt.GlobalColor.transparent))
    painter.drawEllipse(padding - border_width, padding - border_width,
                       circle_size + (border_width * 2), circle_size + (border_width * 2))

    # Draw main orange circle
    painter.setBrush(QBrush(orange_color))
    painter.setPen(QPen(Qt.GlobalColor.transparent))
    painter.drawEllipse(padding, padding, circle_size, circle_size)

    # Draw "BG" text with perfect centering and anti-aliasing
    painter.setPen(QPen(Qt.GlobalColor.white))

    # Increase font size to be more visible (40% of circle diameter)
    font_size = max(int(circle_size * 0.40), 10)
    font = QFont("Arial Black", font_size, QFont.Weight.ExtraBold)
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)  # Better quality
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)  # Force anti-aliasing
    painter.setFont(font)

    # Get text metrics for perfect centering
    from PyQt6.QtCore import QRect
    text_rect = QRect(0, 0, high_res_size, high_res_size)
    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "BG")

    painter.end()

    # Scale down to target size with Lanczos-like smooth transformation
    final_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)

    return final_pixmap

def create_ico_file(output_path):
    """Create an ICO file with multiple sizes"""
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Standard ICO sizes
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        # Create pixmap
        pixmap = create_bg_icon_pixmap(size)

        # Convert to PIL Image
        # Save QPixmap to temporary file and load with PIL
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_path = temp_file.name

        pixmap.save(temp_path, 'PNG')
        pil_image = Image.open(temp_path).convert('RGBA')

        # Clean up temp file
        os.unlink(temp_path)
        images.append(pil_image)

        print(f"✅ Created {size}x{size} icon")

    # Save as ICO file
    images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    print(f"🎉 Icon saved to: {output_path}")

def main():
    print("BG Icon Generator")
    print("=" * 40)

    # Output path
    output_path = os.path.join("assets", "icon.ico")

    # Backup existing icon if it exists
    if os.path.exists(output_path):
        backup_path = os.path.join("assets", "icon_backup.ico")
        import shutil
        shutil.copy2(output_path, backup_path)
        print(f"📁 Backed up existing icon to: {backup_path}")

    # Create new icon
    try:
        create_ico_file(output_path)
        print("\n🎉 SUCCESS!")
        print(f"   New BG icon created: {output_path}")
        print("   This icon will now be used for:")
        print("   • Context menu")
        print("   • Desktop shortcut")
        print("   • Installed app icon")
        print("   • Windows 'Installed Apps' section")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
