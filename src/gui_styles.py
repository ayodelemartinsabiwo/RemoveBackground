"""
GUI Styles Module
Contains all styling constants and functions for the Background Remover application.
Separated for better maintainability and reduced file sizes.
"""

# Color constants
COLORS = {
    'PRIMARY_ORANGE': '#FF6B35',
    'SECONDARY_ORANGE': '#E55A2E',
    'SECONDARY_GRAY': '#6C757D',
    'WHITE': '#FFFFFF',
    'LIGHT_GREY': '#F8F8F8',
    'BORDER_GREY': '#E0E0E0',
    'TEXT_DARK': '#333333',
    'TEXT_BLACK': '#000000',
    'TEXT_MEDIUM': '#222222',
    'TEXT_LIGHT': '#999999',
    'BACKGROUND_OVERLAY': 'rgba(50, 50, 50, 180)',
    'SUCCESS_GREEN': '#28A745',
    'HOVER_GREY': '#E0E0E0',
    'PRESSED_GREY': '#D0D0D0'
}

# Common dimensions
DIMENSIONS = {
    'LOADER_WIDTH': 460,  # Reduced from 480
    'LOADER_HEIGHT': 300,  # Reverted back to 300 as requested
    'HEADER_HEIGHT': 35,   # Reduced from 40
    'CLOSE_BUTTON_SIZE': 28, # Reduced from 30
    'PROGRESS_BAR_HEIGHT': 6,
    'BUTTON_HEIGHT': 40,   # Reduced from 42
    'BUTTON_MIN_WIDTH': 120,
    'BORDER_RADIUS': 12,
    'SMALL_RADIUS': 8
}

def get_main_frame_style():
    """Returns the main frame stylesheet"""
    return f"""
        QFrame {{
            background-color: {COLORS['WHITE']};
            border-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            border: none;
        }}
    """

def get_header_frame_style():
    """Returns the header frame stylesheet"""
    return f"""
        QFrame {{
            background-color: {COLORS['LIGHT_GREY']};
            border: none;
            border-bottom: 1px solid {COLORS['BORDER_GREY']};
            border-top-left-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            border-top-right-radius: {DIMENSIONS['BORDER_RADIUS']}px;
        }}
    """

def get_close_button_style():
    """Returns the close button stylesheet"""
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {COLORS['TEXT_LIGHT']};
            border: none;
            border-radius: {DIMENSIONS['CLOSE_BUTTON_SIZE']//2}px;
            font-size: 18px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['HOVER_GREY']};
            color: #666;
        }}
        QPushButton:pressed {{
            background-color: {COLORS['PRESSED_GREY']};
        }}
    """

def get_title_style():
    """Returns the title label stylesheet"""
    return f"""
        QLabel {{
            color: {COLORS['PRIMARY_ORANGE']};
            font-size: 16px;
            font-weight: bold;
            padding: 8px;
            background-color: transparent;
            margin: 0px;
        }}
    """

def get_status_label_style():
    """Returns the status label stylesheet"""
    return f"""
        QLabel {{
            color: {COLORS['TEXT_DARK']};
            font-size: 12px;
            padding: 8px 15px;
            background-color: transparent;
            margin: 0px;
        }}
    """

def get_progress_bar_style():
    """Returns the progress bar stylesheet"""
    return f"""
        QProgressBar {{
            border: none;
            background-color: #F0F0F0;
            border-radius: {DIMENSIONS['PROGRESS_BAR_HEIGHT']//2}px;
            text-align: center;
            font-size: 0px;
            color: transparent;
            padding: 1px;
            margin: 5px 0px;
        }}
        QProgressBar::chunk {{
            background-color: {COLORS['PRIMARY_ORANGE']};
            border-radius: {DIMENSIONS['PROGRESS_BAR_HEIGHT']//2}px;
        }}
    """

def get_success_frame_style():
    """Returns the success frame stylesheet"""
    return f"""
        QFrame {{
            background-color: {COLORS['WHITE']};
            border: none;
            border-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            padding: 20px;
        }}
    """

def get_primary_button_style():
    """Returns the primary button stylesheet (Orange)"""
    return f"""
        QPushButton {{
            background-color: {COLORS['PRIMARY_ORANGE']};
            color: {COLORS['WHITE']};
            font-weight: bold;
            border: none;
            border-radius: {DIMENSIONS['SMALL_RADIUS']}px;
            padding: 12px 20px;
            font-size: 12px;
            outline: none;
        }}
        QPushButton:hover {{
            background-color: {COLORS['SECONDARY_ORANGE']};
        }}
        QPushButton:pressed {{
            background-color: #D4501F;
        }}
        QPushButton:focus {{
            outline: none;
            border: none;
        }}
    """

def get_content_frame_style():
    """Returns the content frame stylesheet"""
    return f"""
        QFrame {{
            background-color: transparent;
            border: none;
            border-bottom-left-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            border-bottom-right-radius: {DIMENSIONS['BORDER_RADIUS']}px;
        }}
    """

def get_support_dialog_style():
    """Returns the support dialog stylesheet"""
    return f"""
        ThemedSupportDialog {{
            background-color: {COLORS['BACKGROUND_OVERLAY']};
            border-radius: {DIMENSIONS['BORDER_RADIUS']}px;
        }}
    """

def get_support_dialog_main_frame_style():
    """Returns the support dialog main frame stylesheet"""
    return f"""
        QFrame {{
            background-color: {COLORS['WHITE']};
            border-radius: {DIMENSIONS['BORDER_RADIUS']}px;
            border: 1px solid {COLORS['BORDER_GREY']};
        }}
    """
