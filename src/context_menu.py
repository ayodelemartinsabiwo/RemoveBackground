import winreg
import os
import sys
from pathlib import Path

class ContextMenuManager:
    def __init__(self):
        self.app_name = "Background Remover"
        self.registry_key = r"*\shell\RemoveBackground"
        self.command_key = r"*\shell\RemoveBackground\command"

    def install_context_menu(self, exe_path):
        """
        Install context menu entry for all file types

        Args:
            exe_path (str): Path to the main executable
        """
        try:
            # Use icon.ico for context menu icon instead of executable
            icon_path = os.path.join(os.path.dirname(exe_path), "icon.ico")
            if not os.path.exists(icon_path):
                # Fallback to exe if icon missing
                icon_path = exe_path

            # Create main registry key
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, self.registry_key) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "Remove Background")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)

            # Create command registry key
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, self.command_key) as key:
                command = f'"{exe_path}" "%1"'
                winreg.SetValue(key, "", winreg.REG_SZ, command)

            return True, "Context menu installed successfully"

        except Exception as e:
            return False, f"Failed to install context menu: {str(e)}"

    def uninstall_context_menu(self):
        """
        Remove context menu entry from registry
        """
        try:
            # Remove command key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, self.command_key)
            except FileNotFoundError:
                pass

            # Remove main key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, self.registry_key)
            except FileNotFoundError:
                pass

            return True, "Context menu uninstalled successfully"

        except Exception as e:
            return False, f"Failed to uninstall context menu: {str(e)}"

    def is_installed(self):
        """
        Check if context menu is currently installed
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, self.registry_key):
                return True
        except FileNotFoundError:
            return False

# Command line interface for installer
if __name__ == "__main__":
    manager = ContextMenuManager()

    if len(sys.argv) < 2:
        print("Usage: context_menu.py [install|uninstall] [exe_path]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "install":
        if len(sys.argv) < 3:
            print("Error: exe_path required for install")
            sys.exit(1)

        exe_path = sys.argv[2]
        success, message = manager.install_context_menu(exe_path)
        print(message)
        sys.exit(0 if success else 1)

    elif action == "uninstall":
        success, message = manager.uninstall_context_menu()
        print(message)
        sys.exit(0 if success else 1)

    else:
        print(f"Error: Unknown action '{action}'")
        sys.exit(1)
