"""
Loader Window Module
Contains the main LoaderWindow class for the background removal interface.
Refactored from gui_loader.py for better organization and smaller file sizes.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame, QPushButton, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QCloseEvent
from gui_styles import (COLORS, DIMENSIONS, get_main_frame_style, get_header_frame_style,
                        get_close_button_style, get_title_style, get_status_label_style,
                        get_progress_bar_style, get_success_frame_style, get_primary_button_style)
from support_dialog import ThemedSupportDialog
from window_utils import center_window_on_screen, load_application_icon

class LoaderWindow(QWidget):
    """Main loader window for background removal process"""

    finished = pyqtSignal(bool, str)  # Signal for completion

    def __init__(self):
        super().__init__()
        self.is_success_state = False
        self.auto_close_timer = None
        self.progress_timer = None
        self.progress_value = 0

        self.init_ui()
        self.setup_progress_animation()

    def init_ui(self):
        """Initialize the user interface - optimized for instant display"""
        self.setWindowTitle("Background Remover")
        self.setFixedSize(DIMENSIONS['LOADER_WIDTH'], DIMENSIONS['LOADER_HEIGHT'])
        # Remove FramelessWindowHint to make window movable, keep WindowStaysOnTopHint
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # Quick icon setup - use built-in if custom fails
        try:
            icon_pixmap = load_application_icon(size=64, use_svg=False)  # Smaller for speed
            if icon_pixmap:
                from PyQt6.QtGui import QIcon
                self.setWindowIcon(QIcon(icon_pixmap))
        except Exception:
            pass  # Continue without icon if it fails

        # Make window background transparent to fix black corners with rounded border
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Main layout with no margins for clean look
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create main frame
        self.main_frame = self._create_main_frame()
        layout.addWidget(self.main_frame)
        self.setLayout(layout)

        # Show immediately FIRST for instant response
        self.show()

        # Center window AFTER showing for faster display
        center_window_on_screen(self)

        # Force immediate update
        QApplication.processEvents()
        self.raise_()  # Bring to front immediately
        QApplication.processEvents()  # Force immediate display

    def _create_main_frame(self):
        """Create and return the main frame with all content"""
        main_frame = QFrame()
        main_frame.setStyleSheet(get_main_frame_style())

        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Remove header frame - using standard window controls instead
        # Add content directly
        content_frame = self._create_content()
        frame_layout.addWidget(content_frame)

        return main_frame

    def _create_content(self):
        """Create and return the content frame"""
        content_frame = QFrame()
        content_frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")

        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(8)  # Increased spacing for better visual separation
        content_layout.setContentsMargins(30, 30, 30, 30)  # Increased margins for better balance

        # Add stretch at the top to center content vertically
        content_layout.addStretch(1)

        # Title with icon
        self.title_frame = self._create_title_frame()
        content_layout.addWidget(self.title_frame)

        # Status label - make it larger and more prominent
        self.status_label = QLabel("🤗 Hugging the edges...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: normal;
            color: {COLORS['TEXT_DARK']};
            padding: 10px 15px;
            background-color: transparent;
            border: none;
            text-align: center;
            line-height: 1.3;
        """)
        self.status_label.setWordWrap(True)
        content_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(DIMENSIONS['PROGRESS_BAR_HEIGHT'])
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setStyleSheet(get_progress_bar_style())
        content_layout.addWidget(self.progress_bar)

        # Success frame (initially hidden)
        self.success_frame = self._create_success_frame()
        self.success_frame.hide()
        content_layout.addWidget(self.success_frame)

        # Add stretch at the bottom to center content vertically
        content_layout.addStretch(1)
        return content_frame

    def _create_title_frame(self):
        """Create and return the title frame with icon and text"""
        title_frame = QFrame()
        title_frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon - use PNG for custom design quality
        icon_label = QLabel()
        icon_pixmap = load_application_icon(size=36, use_svg=False)
        if icon_pixmap:
            icon_label.setPixmap(icon_pixmap)
        else:
            # Fallback to BG text if icon loading fails
            icon_label.setText("BG")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet(f"""
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['WHITE']};
                background-color: {COLORS['PRIMARY_ORANGE']};
                border-radius: 18px;
                padding: 4px;
            """)
        icon_label.setFixedSize(36, 36)
        title_layout.addWidget(icon_label)

        # Title text
        title_label = QLabel("Background Remover")
        title_label.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {COLORS['PRIMARY_ORANGE']};
            padding: 0px;
            margin: 0px;
        """)
        title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title_layout.addWidget(title_label)

        return title_frame

    def _create_bg_icon(self):
        """Create a custom BG icon programmatically matching the reference design"""
        try:
            from PyQt6.QtGui import QPixmap, QPainter, QBrush, QPen, QFont, QColor, QFontMetrics

            # Create a 36x36 pixmap
            size = 36
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

            # Minimal padding to maximize icon size while preventing edge clipping
            padding = int(size * 0.01)  # 1% padding
            circle_size = size - (padding * 2)

            # Draw orange circle background with padding
            orange_color = QColor(COLORS['PRIMARY_ORANGE'])
            painter.setBrush(QBrush(orange_color))
            painter.setPen(QPen(Qt.GlobalColor.transparent))
            painter.drawEllipse(padding, padding, circle_size, circle_size)

            # Draw "BG" text with perfect centering
            painter.setPen(QPen(Qt.GlobalColor.white))

            # Increase font size to be more visible (40% of circle diameter)
            font_size = max(int(circle_size * 0.40), 10)
            font = QFont("Arial Black", font_size, QFont.Weight.ExtraBold)
            painter.setFont(font)

            # Use drawText with rect for perfect centering
            from PyQt6.QtCore import QRect
            text_rect = QRect(0, 0, size, size)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "BG")

            painter.end()
            return pixmap

        except Exception as e:
            print(f"Could not create BG icon: {e}")
            return None

    def _create_success_frame(self):
        """Create and return the success frame"""
        success_frame = QFrame()
        success_frame.setStyleSheet(get_success_frame_style())

        success_layout = QVBoxLayout(success_frame)
        success_layout.setSpacing(0)  # No spacing between elements
        success_layout.setContentsMargins(15, 0, 15, 0)  # Remove bottom margin completely

        # Success message removed - will be shown in status label instead

        # File path label with enhanced visibility and minimal padding
        self.file_path_label = QLabel()
        self.file_path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_path_label.setStyleSheet(f"""
            color: {COLORS['TEXT_DARK']};
            font-size: 12px;
            font-weight: bold;
            padding: 5px 10px;
            background-color: {COLORS['WHITE']};
            border: 1px solid {COLORS['WHITE']};
            border-radius: 6px;
            margin: 0px 5px;
            line-height: 1.2;
        """)
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setMinimumHeight(45)  # Reduced height
        self.file_path_label.setMaximumHeight(55)  # Reduced max height
        success_layout.addWidget(self.file_path_label)

        # Remove spacing before button to eliminate all gaps
        # success_layout.addSpacing(2) - REMOVED

        # Buttons frame with support buttons only
        button_frame = QFrame()
        button_frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)  # Spacing between two buttons

        # Red Bull button
        support_btn = QPushButton("🍺 Buy us a Red Bull!")
        support_btn.setFixedHeight(DIMENSIONS['BUTTON_HEIGHT'])
        support_btn.setMaximumWidth(160)  # Slightly wider with more space
        support_btn.setStyleSheet(get_primary_button_style())
        support_btn.clicked.connect(self.show_support_dialog)

        # Contact Us button with proper email icon and same orange color
        contact_btn = QPushButton("📧 Contact Us")
        contact_btn.setFixedHeight(DIMENSIONS['BUTTON_HEIGHT'])
        contact_btn.setMaximumWidth(120)  # Adjusted width
        contact_btn.setStyleSheet(get_primary_button_style())  # Use same orange styling
        contact_btn.clicked.connect(self.show_contact_dialog)

        # Center both buttons
        button_layout.addStretch(1)
        button_layout.addWidget(support_btn)
        button_layout.addWidget(contact_btn)
        button_layout.addStretch(1)

        success_layout.addWidget(button_frame)

        return success_frame

    def setup_progress_animation(self):
        """Setup animated progress bar"""
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.animate_progress)
        self.progress_timer.start(100)  # Update every 100ms

    def animate_progress(self):
        """Animate the progress bar"""
        if not self.is_success_state:
            self.progress_value = (self.progress_value + 2) % 100
            if self.progress_bar.maximum() != 100:
                self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(self.progress_value)

    def update_status(self, message):
        """Update the status message"""
        self.status_label.setText(message)

    def show_success(self, output_path):
        """Transform the loader into success state"""
        self.is_success_state = True

        # Stop progress animation and completely remove progress bar
        if self.progress_timer:
            self.progress_timer.stop()

        # Remove progress bar from layout completely to free up space
        self.progress_bar.setParent(None)  # Remove from layout

        # Update status to show success message in green
        self.status_label.setText("✅ Background removed successfully!")
        self.status_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: #28a745;
            padding: 5px 10px;
            background-color: transparent;
            border: none;
            text-align: center;
        """)

        # Show success frame with enhanced file path display
        import os
        filename = os.path.basename(output_path)
        folder_path = os.path.dirname(output_path)
        self.file_path_label.setText(f"📁 Saved to: {folder_path}\n File: {filename}")
        self.success_frame.show()

    def show_support_dialog(self):
        """Show the support dialog"""
        dialog = ThemedSupportDialog(self)
        dialog.exec()

    def show_contact_dialog(self):
        """Open email client for contact"""
        # Compose default email with professional body
        subject = "Background Remover - Contact Request"
        body = """Hi Palmer Enterprises team!

I'm reaching out regarding your Background Remover application.

Please let me know how I can:
• Get support with the application
• Provide feedback or suggestions
• Report any issues I'm experiencing
• Ask questions about features

Looking forward to hearing from you!

Best regards,
[Your Name]"""

        # URL encode the subject and body for proper email formatting
        import urllib.parse
        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)

        # Create mailto URL
        email_url = f"mailto:palmarenterprise@gmail.com?subject={encoded_subject}&body={encoded_body}"

        # Open user's default email client using subprocess (safer for distribution)
        try:
            import subprocess
            import os
            if os.name == 'nt':  # Windows
                subprocess.run(['cmd', '/c', 'start', '', email_url], shell=True)
            else:  # macOS/Linux
                subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', email_url])
        except Exception as e:
            print(f"Could not open email client: {e}")
            # Fallback: Copy email to clipboard
            try:
                from PyQt6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                if clipboard:
                    clipboard.setText(f"Email: palmarenterprise@gmail.com\nSubject: {subject}\n\n{body}")
            except:
                pass

    def open_installation_folder(self):
        """Open the installation folder where the application is located"""
        import os
        import sys

        # Get the application's executable path
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_path = sys.executable
        else:
            # Running as script
            app_path = os.path.abspath(__file__)

        # Get the directory containing the executable
        install_dir = os.path.dirname(app_path)

        # Open the installation directory using subprocess (safer for distribution)
        if os.path.exists(install_dir):
            try:
                import subprocess
                if os.name == 'nt':  # Windows
                    subprocess.run(['explorer', install_dir])
                else:  # macOS/Linux
                    subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', install_dir])
            except Exception as e:
                print(f"Could not open installation directory: {e}")

    def closeEvent(self, a0):
        """Handle window close event with cleanup"""
        if self.auto_close_timer:
            self.auto_close_timer.stop()
        if self.progress_timer:
            self.progress_timer.stop()
        if a0:
            a0.accept()
