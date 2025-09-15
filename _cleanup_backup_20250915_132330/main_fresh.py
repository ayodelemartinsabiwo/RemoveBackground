import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from gui_loader import LoaderWindow
from bg_remove import BackgroundRemover
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
            remover = BackgroundRemover()

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
        if sys.argv[1] == "--install-context-menu":
            try:
                manager = ContextMenuManager()
                success, message = manager.install_context_menu(sys.argv[0])
                print(f"Context menu installation: {'Success' if success else 'Failed'}")
                print(message)
                return True
            except Exception as e:
                print(f"Failed to install context menu: {e}")
                return True

        elif sys.argv[1] == "--uninstall-context-menu":
            try:
                manager = ContextMenuManager()
                success, message = manager.uninstall_context_menu()
                print(f"Context menu removal: {'Success' if success else 'Failed'}")
                print(message)
                return True
            except Exception as e:
                print(f"Failed to uninstall context menu: {e}")
                return True

    return False

def get_image_path_from_user():
    """Get image path from user via file dialog"""
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()

    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(
        None,
        "Select Image to Remove Background",
        "",
        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
    )

    return file_path if file_path else None

def show_error_dialog(message):
    """Show error dialog to user"""
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Background Remover - Error")
    msg.setText("An error occurred:")
    msg.setInformativeText(message)
    msg.exec()

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

    # Start background removal in separate thread
    thread = BackgroundRemovalThread(image_path)

    def on_progress(message):
        loader.update_status(message)

    def on_finished(success, message):
        if success:
            # Transform loader into success state instead of showing separate dialog
            loader.show_success(message)
        else:
            loader.update_status(f"Error: {message}")
            # Auto-close on error after 3 seconds
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(3000, loader.close)

    thread.progress.connect(on_progress)
    thread.finished.connect(on_finished)
    thread.start()

    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
