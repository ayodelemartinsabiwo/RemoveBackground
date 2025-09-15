"""
Optimized Main Module for Background Remover
Refactored for smaller file sizes and better maintainability.
Uses modular components to reduce false positives.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from loader_window import LoaderWindow
from bg_remove_optimized import OptimizedBackgroundRemover
from context_menu import ContextMenuManager

class BackgroundRemovalThread(QThread):
    """Thread for background removal processing"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_path):
        super().__init__()
        self.input_path = input_path

    def run(self):
        """Execute background removal in separate thread"""
        try:
            self.progress.emit("Initializing background removal...")
            remover = OptimizedBackgroundRemover()

            self.progress.emit("Hugging the edges nice and tight....")
            success, output_path = remover.remove_background(self.input_path)

            if success:
                self.progress.emit("Background removed successfully!")
                self.finished.emit(True, output_path)
            else:
                self.finished.emit(False, "Failed to remove background")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.finished.emit(False, error_msg)

def handle_context_menu_args():
    """Handle context menu installation/uninstallation"""
    if len(sys.argv) >= 2:
        if sys.argv[1] == "install_context_menu" and len(sys.argv) >= 3:
            manager = ContextMenuManager()
            exe_path = sys.argv[2]
            success, message = manager.install_context_menu(exe_path)
            print(message)
            return True
        elif sys.argv[1] == "uninstall_context_menu":
            manager = ContextMenuManager()
            success, message = manager.uninstall_context_menu()
            print(message)
            return True
    return False

def get_image_path_from_user():
    """Get image path from user via file dialog"""
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Image Files (*.jpg *.jpeg *.png *.bmp *.tiff *.webp)")
    file_dialog.setWindowTitle("Select Image for Background Removal")
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

    if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
    return None

def show_error_dialog(message):
    """Show error dialog to user"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec()

def setup_background_removal(loader, image_path):
    """Setup and start background removal process"""
    thread = BackgroundRemovalThread(image_path)

    def on_progress(message):
        loader.update_status(message)

    def on_finished(success, message):
        if success:
            loader.show_success(message)
        else:
            loader.update_status(f"Error: {message}")
            # Auto-close on error after 3 seconds
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(3000, loader.close)

    thread.progress.connect(on_progress)
    thread.finished.connect(on_finished)
    thread.start()

    return thread

def main():
    """Main application entry point"""
    # Handle context menu commands first
    if handle_context_menu_args():
        return

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Get image path from command line or file dialog
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
    else:
        image_path = get_image_path_from_user()
        if not image_path:
            return  # User cancelled

    # Validate image path
    if not os.path.exists(image_path):
        show_error_dialog(f"File not found: {image_path}")
        return

    # Create and show loader window
    loader = LoaderWindow()

    # Start background removal process
    thread = setup_background_removal(loader, image_path)

    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
