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

def load_application_icon(relative_path="assets/icon.ico"):
    """Load the application icon from assets folder"""
    try:
        # Get the icon path relative to the main directory
        base_dir = os.path.dirname(os.path.dirname(__file__))
        icon_path = os.path.join(base_dir, relative_path)

        # Also try the direct path in case we're running from dist
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), relative_path)

        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                # Return the original pixmap, let caller decide on scaling
                return pixmap
    except Exception as e:
        print(f"Warning: Could not load icon from {relative_path}: {e}")

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
