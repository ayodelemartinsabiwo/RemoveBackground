from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QProgressBar, QFrame, QPushButton, QMenu, QDialog)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QCloseEvent
import os

class LoaderWindow(QWidget):
    finished = pyqtSignal(bool, str)  # Signal for completion

    def __init__(self):
        super().__init__()
        self.is_success_state = False
        self.auto_close_timer = None
        self.init_ui()
        self.setup_progress_animation()

    def init_ui(self):
        self.setWindowTitle("Background Remover")
        self.setFixedSize(480, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                           Qt.WindowType.WindowStaysOnTopHint)

        # Center window on screen
        self.center_window()

        # Main layout with no margins for clean look
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create main frame with clean modern styling
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Window header with light grey border
        header_frame = QFrame()
        header_frame.setFixedHeight(40)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F8F8;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 5, 10, 5)
        header_layout.addStretch()

        # Close button (X) in top right
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #999;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                color: #666;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)
        frame_layout.addWidget(header_frame)

        # Content area with proper padding
        content_frame = QFrame()
        content_frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(35, 30, 35, 30)

        # Title with icon
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load and display icon
        self.icon_label = QLabel()
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.icon_label.setPixmap(scaled_pixmap)
        else:
            self.icon_label.setText("🖼️")
            self.icon_label.setFont(QFont("Segoe UI", 20))

        self.title = QLabel("Background Remover")
        self.title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #FF6B35;")

        title_layout.addWidget(self.icon_label)
        title_layout.addWidget(self.title)
        content_layout.addLayout(title_layout)

        # Status label
        self.status_label = QLabel("Initializing AI model...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setStyleSheet("color: #666; padding: 10px;")
        content_layout.addWidget(self.status_label)

        # Progress bar (initially visible)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #F0F0F0;
                margin: 10px 0;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B35, stop:1 #FF8C42);
                border-radius: 4px;
            }
        """)
        content_layout.addWidget(self.progress_bar)

        # Success content (initially hidden)
        self.success_frame = QFrame()
        self.success_frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        success_layout = QVBoxLayout(self.success_frame)
        success_layout.setSpacing(20)
        success_layout.setContentsMargins(0, 15, 0, 15)

        # Success icon and message
        self.success_label = QLabel("✅ Background removed successfully!")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.success_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        success_layout.addWidget(self.success_label)

        # File path label
        self.path_label = QLabel("")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_label.setFont(QFont("Segoe UI", 10))
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("color: #888; padding: 5px 20px;")
        success_layout.addWidget(self.path_label)

        # Action button (centered)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(40, 15, 40, 15)
        button_layout.addStretch()

        # Red Bull button (centered)
        self.red_bull_btn = QPushButton("🍺 Buy us a Red Bull")
        self.red_bull_btn.setFixedHeight(50)
        self.red_bull_btn.setMinimumWidth(220)
        self.red_bull_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 15px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E55A2E;
            }
        """)
        self.red_bull_btn.clicked.connect(self.show_support_dialog)

        button_layout.addWidget(self.red_bull_btn)
        button_layout.addStretch()
        success_layout.addLayout(button_layout)

        # Initially hide success content
        self.success_frame.hide()
        content_layout.addWidget(self.success_frame)

        frame_layout.addWidget(content_frame)
        layout.addWidget(self.main_frame)
        self.setLayout(layout)

        # Apply clean window styling
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 80);
            }
        """)

    def center_window(self):
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

    def setup_progress_animation(self):
        # Show immediately without delay
        self.show()
        self.raise_()
        self.activateWindow()

    def update_status(self, message):
        """Update status message during processing"""
        if not self.is_success_state:
            self.status_label.setText(message)

    def show_success(self, file_path):
        """Transform loader into success state"""
        self.is_success_state = True

        # Hide progress elements only (keep title and icon visible)
        self.progress_bar.hide()
        self.status_label.hide()

        # Update path label
        self.path_label.setText(f"📁 Saved to: {file_path}")

        # Make sure all success elements are visible
        self.success_label.show()
        self.path_label.show()
        self.red_bull_btn.show()

        # Show success content
        self.success_frame.show()

        # Note: Removed auto-close timer - let user close manually

    def show_support_dialog(self):
        """Show themed support dialog"""
        dialog = ThemedSupportDialog(self)
        dialog.exec()

    def closeEvent(self, a0):
        """Clean up when closing"""
        if self.auto_close_timer:
            self.auto_close_timer.stop()
        if a0:
            a0.accept()

class ThemedSupportDialog(QDialog):
    """Support dialog with consistent theme"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Support Palmer Enterprises")
        self.setFixedSize(450, 480)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create main frame with proper rounded corners
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Window header with light grey border (same as main window)
        header_frame = QFrame()
        header_frame.setFixedHeight(40)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F8F8;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 5, 10, 5)
        header_layout.addStretch()

        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #999;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                color: #666;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        frame_layout.addWidget(header_frame)

        # Content area with proper padding and bottom radius
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(18)
        content_layout.setContentsMargins(30, 25, 30, 25)        # Title
        title = QLabel("🍺 Buy us a Red Bull!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF6B35; margin: 10px 0;")
        content_layout.addWidget(title)

        # Message
        message = QLabel("Thank you for using Background Remover!")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setFont(QFont("Segoe UI", 12, QFont.Weight.Normal))
        message.setStyleSheet("color: #333; margin: 10px 0;")
        content_layout.addWidget(message)

        # Bank details with all information
        bank_details = QLabel(
            "If this free software saved you time,\n"
            "consider buying us a Red Bull!\n\n"
            "💰 Bank Details:\n"
            "Account Name: PALMER ENTERPRISES\n"
            "Bank: Zenith Bank\n"
            "Account Number: 1017441664\n\n"
            "Your support helps keep this software free for everyone! 🙏"
        )
        bank_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bank_details.setFont(QFont("Segoe UI", 11, QFont.Weight.Normal))
        bank_details.setStyleSheet("color: #000; line-height: 1.6; padding: 15px; background-color: transparent;")
        bank_details.setWordWrap(True)
        content_layout.addWidget(bank_details)        # Single Close button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 15, 20, 10)
        button_layout.addStretch()

        # Close button
        close_main_btn = QPushButton("Close")
        close_main_btn.setFixedHeight(42)
        close_main_btn.setMinimumWidth(120)
        close_main_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E55A2E;
            }
        """)
        close_main_btn.clicked.connect(self.close)

        button_layout.addWidget(close_main_btn)
        button_layout.addStretch()
        content_layout.addLayout(button_layout)

        frame_layout.addWidget(content_frame)
        layout.addWidget(main_frame)
        self.setLayout(layout)

        # Apply transparent background without interfering with rounded corners
        self.setStyleSheet("""
            ThemedSupportDialog {
                background-color: rgba(50, 50, 50, 180);
                border-radius: 12px;
            }
        """)

        # Ensure the dialog itself respects the rounded corners
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
