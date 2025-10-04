"""
Window Utilities Module
Contains utility functions for window management and common operations.
Helps reduce code duplication and file sizes.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
import os

def center_window_on_screen(window):
    """Center a window on the screen"""
    screen = QApplication.primaryScreen()
    if screen:
        screen_geometry = screen.geometry()
        window_geometry = window.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        window.move(window_geometry.topLeft())

def load_application_icon(size=256, use_svg=True):
    """Load the application icon - preferably from SVG for best quality"""
    import sys

    try:
        # Check if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_dir = sys._MEIPASS  # type: ignore[attr-defined]
        else:
            # Running as script
            base_dir = os.path.dirname(os.path.dirname(__file__))

        # Try to load from custom PNG files first (best quality from design software)
        if not use_svg:
            # Try to find exact size match first
            png_path = os.path.join(base_dir, "assets", "Icon PNGs", f"icon_{size}x{size}.png")

            if not os.path.exists(png_path):
                # Fall back to 256x256 and scale
                png_path = os.path.join(base_dir, "assets", "Icon PNGs", "icon_256x256.png")

            if os.path.exists(png_path):
                pixmap = QPixmap(png_path)
                if not pixmap.isNull():
                    # Scale to requested size with smooth transformation if needed
                    if pixmap.width() != size:
                        pixmap = pixmap.scaled(
                            size, size,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                    return pixmap

        # Try to load SVG for best quality (if requested)
        if use_svg:
            from PyQt6.QtSvg import QSvgRenderer
            from PyQt6.QtGui import QPainter, QImage

            svg_path = os.path.join(base_dir, "assets", "bg icon_256 x 256.svg")

            if os.path.exists(svg_path):
                # Render SVG at requested size with anti-aliasing
                renderer = QSvgRenderer(svg_path)
                if renderer.isValid():
                    # Use 2x rendering for better quality
                    render_size = size * 2
                    image = QImage(render_size, render_size, QImage.Format.Format_ARGB32_Premultiplied)
                    image.fill(0)  # Transparent

                    painter = QPainter(image)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
                    renderer.render(painter)
                    painter.end()

                    # Scale down for final size
                    final_image = image.scaled(
                        size, size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    pixmap = QPixmap.fromImage(final_image)
                    if not pixmap.isNull():
                        return pixmap

        # Final fallback to ICO
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                return pixmap

        print(f"Warning: Icon file not found")
    except Exception as e:
        print(f"Warning: Could not load icon: {e}")

    return None

def setup_auto_close_timer(window, delay_ms=5000):
    """Setup an auto-close timer for a window"""
    timer = QTimer(window)
    timer.setSingleShot(True)
    timer.timeout.connect(window.close)
    timer.start(delay_ms)
    return timer

def apply_window_flags(window, frameless=True, stay_on_top=True):
    """Apply common window flags for modern UI"""
    from PyQt6.QtCore import Qt

    flags = Qt.WindowType.Widget

    if frameless:
        flags |= Qt.WindowType.FramelessWindowHint

    if stay_on_top:
        flags |= Qt.WindowType.WindowStaysOnTopHint

    window.setWindowFlags(flags)

def create_progress_animation_timer(progress_bar, callback_func):
    """Create a timer for progress bar animation"""
    timer = QTimer()
    timer.timeout.connect(lambda: callback_func(progress_bar))
    return timer

def get_screen_dimensions():
    """Get the current screen dimensions"""
    screen = QApplication.primaryScreen()
    if screen:
        screen_geometry = screen.geometry()
        return screen_geometry.width(), screen_geometry.height()
    return 1920, 1080  # Default fallback

def calculate_window_position(window_width, window_height, offset_x=0, offset_y=0):
    """Calculate centered window position with optional offset"""
    screen_width, screen_height = get_screen_dimensions()

    x = (screen_width - window_width) // 2 + offset_x
    y = (screen_height - window_height) // 2 + offset_y

    return x, y

def safe_close_window(window):
    """Safely close a window with proper cleanup"""
    try:
        if hasattr(window, 'auto_close_timer') and window.auto_close_timer:
            window.auto_close_timer.stop()

        if hasattr(window, 'progress_timer') and window.progress_timer:
            window.progress_timer.stop()

        window.close()
    except Exception as e:
        print(f"Warning: Error during window cleanup: {e}")
        window.close()

def create_window_with_settings(window_class, width, height, title="", **kwargs):
    """Factory function to create a window with common settings"""
    window = window_class(**kwargs)
    window.setWindowTitle(title)
    window.setFixedSize(width, height)

    apply_window_flags(window)
    center_window_on_screen(window)

    return window
