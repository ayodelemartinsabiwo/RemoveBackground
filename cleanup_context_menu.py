#!/usr/bin/env python3
"""
Context Menu Cleanup Utility
Removes the "Remove Background" context menu entry
"""

import winreg
import sys

def check_and_remove_context_menu():
    registry_key = r"*\shell\RemoveBackground"
    command_key = r"*\shell\RemoveBackground\command"

    print("Checking for 'Remove Background' context menu entry...")

    # Check if installed
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, registry_key):
            print("✓ Context menu entry found")
            installed = True
    except FileNotFoundError:
        print("✗ Context menu entry not found")
        installed = False
        return True, "Context menu entry was not installed"

    if installed:
        print("Attempting to remove context menu entry...")
        try:
            # Remove command key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, command_key)
                print("✓ Removed command registry key")
            except FileNotFoundError:
                print("- Command key already removed")

            # Remove main key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, registry_key)
                print("✓ Removed main registry key")
            except FileNotFoundError:
                print("- Main key already removed")

            print("✅ Context menu entry removed successfully!")
            return True, "Context menu uninstalled successfully"

        except PermissionError:
            print("❌ Permission denied - Please run as Administrator")
            return False, "Permission denied - run as Administrator"
        except Exception as e:
            print(f"❌ Failed to remove: {str(e)}")
            return False, f"Failed to uninstall: {str(e)}"

    return True, "No action needed"

if __name__ == "__main__":
    print("Background Remover - Context Menu Cleanup")
    print("=" * 45)

    success, message = check_and_remove_context_menu()
    print(f"\nResult: {message}")

    if not success:
        print("\nTo run with administrator privileges:")
        print("Right-click Command Prompt → 'Run as administrator'")
        print("Then run: python cleanup_context_menu.py")

    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)
