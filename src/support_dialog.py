"""
Support Dialog Module
Contains the ThemedSupportDialog class for the "Buy us a Red Bull" functionality.
Separated from main GUI for better organization and smaller file sizes.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from gui_styles import COLORS, DIMENSIONS, get_support_dialog_style, get_support_dialog_main_frame_style

class ThemedSupportDialog(QDialog):
    """Support dialog with consistent theme for Palmer Enterprises"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialize the support dialog UI"""
        self.setWindowTitle("Support Palmer Enterprises")
        self.setFixedSize(450, 480)
        # Remove FramelessWindowHint to make dialog movable and use standard window controls
        self.setWindowFlags(Qt.WindowType.Dialog)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create main frame with proper rounded corners (no custom header)
        main_frame = self._create_main_frame()
        layout.addWidget(main_frame)
        self.setLayout(layout)

        # Apply background styling
        self.setStyleSheet(get_support_dialog_style())

    def _create_main_frame(self):
        """Create and return the main frame with all content"""
        main_frame = QFrame()
        main_frame.setStyleSheet(get_support_dialog_main_frame_style())

        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Add content directly (no custom header)
        content_frame = self._create_content()
        frame_layout.addWidget(content_frame)

        return main_frame

    def _create_content(self):
        """Create and return the content frame"""
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
                border-bottom-left-radius: {DIMENSIONS['BORDER_RADIUS']}px;
                border-bottom-right-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            }}
        """)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(18)
        content_layout.setContentsMargins(30, 25, 30, 25)

        # Add title
        title = self._create_title()
        content_layout.addWidget(title)

        # Add message
        message = self._create_message()
        content_layout.addWidget(message)

        # Add bank details
        bank_details = self._create_bank_details()
        content_layout.addWidget(bank_details)

        # Add close button
        button_layout = self._create_button_layout()
        content_layout.addLayout(button_layout)

        return content_frame

    def _create_title(self):
        """Create and return the title label"""
        title = QLabel("🍺 Buy us a Red Bull!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['PRIMARY_ORANGE']}; margin: 10px 0;")
        return title

    def _create_message(self):
        """Create and return the message label"""
        message = QLabel("Thank you for using Background Remover!")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setFont(QFont("Segoe UI", 12, QFont.Weight.Normal))
        message.setStyleSheet(f"color: {COLORS['TEXT_DARK']}; margin: 10px 0;")
        return message

    def _create_bank_details(self):
        """Create and return the bank details label"""
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
        bank_details.setStyleSheet(f"color: {COLORS['TEXT_BLACK']}; line-height: 1.6; padding: 15px; background-color: transparent;")
        bank_details.setWordWrap(True)
        return bank_details

    def _create_button_layout(self):
        """Create and return the button layout with close button"""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 15, 20, 10)
        button_layout.addStretch()

        # Close button
        close_main_btn = QPushButton("Close")
        close_main_btn.setFixedHeight(DIMENSIONS['BUTTON_HEIGHT'])
        close_main_btn.setMinimumWidth(DIMENSIONS['BUTTON_MIN_WIDTH'])
        close_main_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['PRIMARY_ORANGE']};
                color: {COLORS['WHITE']};
                font-weight: bold;
                border: none;
                border-radius: {DIMENSIONS['SMALL_RADIUS']}px;
                padding: 10px 20px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['SECONDARY_ORANGE']};
            }}
        """)
        close_main_btn.clicked.connect(self.close)

        button_layout.addWidget(close_main_btn)
        button_layout.addStretch()

        return button_layout
