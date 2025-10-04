import sys
import os
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from loader_window import LoaderWindow
from bg_remove_optimized import OptimizedBackgroundRemover
from context_menu import ContextMenuManager
import traceback

class BackgroundRemovalThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_path):
        super().__init__()
        self.input_path = input_path
        # Don't create remover instance here - do it in run() to avoid import delays

    def run(self):
        try:
            def progress_callback(message):
                self.progress.emit(message)

            # Create remover instance here to avoid blocking UI thread
            remover = OptimizedBackgroundRemover()
            success, output_path = remover.remove_background(
                self.input_path,
                progress_callback=progress_callback
            )

            if success:
                self.progress.emit("Background removed successfully!")
                self.finished.emit(True, output_path)
            else:
                self.finished.emit(False, "Failed to remove background")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.finished.emit(False, error_msg)

def show_support_dialog():
    """Show support dialog with bank details"""
    from PyQt6.QtWidgets import QMessageBox, QPushButton
    from PyQt6.QtCore import QUrl
    from PyQt6.QtGui import QDesktopServices

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Support the Developer 🍺")
    msg.setText("Thank you for using Background Remover!")
    msg.setInformativeText(
        "If this free software saved you time, consider buying me a Red Bull! ☕\n\n"
        "💰 Bank Details:\n"
        "Account Name: PALMER ENTERPRISES\n"
        "Bank: Zenith Bank\n"
        "Account Number: 1017441664\n\n"
        "Your support helps keep this software free for everyone! 🙏"
    )

    copy_btn = msg.addButton("📋 Copy Account Number", QMessageBox.ButtonRole.ActionRole)
    email_btn = msg.addButton("📧 Send Email", QMessageBox.ButtonRole.ActionRole)
    close_btn = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)

    result = msg.exec()

    if msg.clickedButton() == copy_btn:
        # Show account number for manual copying
        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Icon.Information)
        confirm_msg.setWindowTitle("Account Number")
        confirm_msg.setText("1017441664")
        confirm_msg.setInformativeText("Account Number ready to copy!\n\nAccount Name: PALMER ENTERPRISES\nBank: Zenith Bank")
        confirm_msg.exec()

    elif msg.clickedButton() == email_btn:
        # Open email client
        email_url = QUrl("mailto:palmarenterprise@gmail.com?subject=Background Remover Support&body=Hi! I'm using your Background Remover software and would like to show my support.")
        QDesktopServices.openUrl(email_url)

def show_contact_dialog():
    """Show contact dialog"""
    from PyQt6.QtWidgets import QMessageBox
    from PyQt6.QtCore import QUrl
    from PyQt6.QtGui import QDesktopServices

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Contact Palmer Enterprises")
    msg.setText("Get in touch with us!")
    msg.setInformativeText(
        "📧 Email: palmarenterprise@gmail.com\n\n"
        "We'd love to hear from you about:\n"
        "• Feature requests\n"
        "• Bug reports\n"
        "• General feedback\n"
        "• Business inquiries"
    )

    email_btn = msg.addButton("📧 Send Email", QMessageBox.ButtonRole.ActionRole)
    close_btn = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)

    result = msg.exec()

    if msg.clickedButton() == email_btn:
        # Open email client
        email_url = QUrl("mailto:palmarenterprise@gmail.com?subject=Background Remover Contact&body=Hi Palmer Enterprises team!")
        QDesktopServices.openUrl(email_url)

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

def main():
    # Handle context menu commands first
    if handle_context_menu_args():
        return

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Set application icon
    from window_utils import load_application_icon
    from PyQt6.QtGui import QIcon
    icon_pixmap = load_application_icon()
    if icon_pixmap:
        app.setWindowIcon(QIcon(icon_pixmap))

    # Get image path from command line or file dialog
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
    else:
        # No command line argument - show file dialog
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.jpg *.jpeg *.png *.bmp *.tiff *.webp)")
        file_dialog.setWindowTitle("Select Image for Background Removal")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
            else:
                return  # User cancelled
        else:
            return  # User cancelled

    if not os.path.exists(image_path):
        # Show error dialog instead of console message
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(f"File not found: {image_path}")
        msg.exec()
        return

    # Create and show loader window immediately
    loader = LoaderWindow()
    # Show immediately for fast response

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

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
