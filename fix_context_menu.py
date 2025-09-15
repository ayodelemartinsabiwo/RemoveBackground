#!/usr/bin/env python3
"""
Context Menu Cleanup and Reinstall Script
Removes old/broken context menu entries and installs the correct one.
"""

import winreg
import os
import sys
import subprocess
from pathlib import Path

def remove_all_background_removal_entries():
    """Remove all possible background removal context menu entries."""
    print("🧹 Cleaning up old context menu entries...")

    # Common registry paths that might have old entries
    possible_keys = [
        r"*\shell\RemoveBackground",
        r"*\shell\Remove Background",
        r"*\shell\BackgroundRemover",
        r"*\shell\Background Remover",
        r"SystemFileAssociations\image\shell\RemoveBackground",
        r"SystemFileAssociations\image\shell\Remove Background",
        r"SystemFileAssociations\image\shell\BackgroundRemover",
        r"Directory\Background\shell\RemoveBackground",
        r"Directory\shell\RemoveBackground",
    ]

    removed_count = 0

    for key_path in possible_keys:
        try:
            # Try to delete command subkey first
            command_key = key_path + r"\command"
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, command_key)
                print(f"  ✅ Removed: {command_key}")
                removed_count += 1
            except FileNotFoundError:
                pass

            # Then delete main key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
                print(f"  ✅ Removed: {key_path}")
                removed_count += 1
            except FileNotFoundError:
                pass

        except Exception as e:
            print(f"  ⚠️  Could not remove {key_path}: {e}")

    print(f"  🗑️  Removed {removed_count} old registry entries")
    return removed_count > 0

def install_correct_context_menu():
    """Install the correct context menu pointing to our working executable."""
    print("\n🔧 Installing correct context menu...")

    # Path to our working executable
    exe_path = os.path.abspath("dist/BackgroundRemover.exe")

    if not os.path.exists(exe_path):
        print(f"  ❌ Executable not found: {exe_path}")
        return False

    print(f"  📍 Target executable: {exe_path}")

    try:
        # Registry key for image files context menu
        registry_key = r"*\shell\RemoveBackground"
        command_key = r"*\shell\RemoveBackground\command"

        # Create main registry key
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, registry_key) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Remove Background")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)
            print(f"  ✅ Created registry key: {registry_key}")

        # Create command registry key
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key) as key:
            command = f'"{exe_path}" "%1"'
            winreg.SetValue(key, "", winreg.REG_SZ, command)
            print(f"  ✅ Set command: {command}")

        # Also create specific image file associations for better integration
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']

        for ext in image_extensions:
            try:
                ext_key = f"SystemFileAssociations\\{ext}\\shell\\RemoveBackground"
                ext_command_key = f"SystemFileAssociations\\{ext}\\shell\\RemoveBackground\\command"

                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext_key) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, "Remove Background")
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)

                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext_command_key) as key:
                    command = f'"{exe_path}" "%1"'
                    winreg.SetValue(key, "", winreg.REG_SZ, command)

            except Exception as e:
                print(f"  ⚠️  Could not set association for {ext}: {e}")

        print("  ✅ Context menu installed successfully!")
        return True

    except Exception as e:
        print(f"  ❌ Failed to install context menu: {e}")
        return False

def test_context_menu():
    """Test if the context menu is properly installed."""
    print("\n🧪 Testing context menu installation...")

    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\RemoveBackground\command") as key:
            command_value = winreg.QueryValue(key, "")
            print(f"  📋 Command found: {command_value}")

            # Check if the executable exists
            if "BackgroundRemover.exe" in command_value:
                exe_path = command_value.split('"')[1]  # Extract path from quoted command
                if os.path.exists(exe_path):
                    print(f"  ✅ Executable exists: {exe_path}")
                    return True
                else:
                    print(f"  ❌ Executable missing: {exe_path}")
                    return False
            else:
                print("  ❌ Command does not point to BackgroundRemover.exe")
                return False

    except FileNotFoundError:
        print("  ❌ Context menu not found in registry")
        return False
    except Exception as e:
        print(f"  ❌ Error testing context menu: {e}")
        return False

def main():
    print("Background Remover - Context Menu Fix")
    print("=" * 40)

    # Check if running as administrator
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("⚠️  WARNING: Not running as Administrator!")
            print("   Registry changes may fail. Consider running as Admin.")
    except:
        pass

    # Step 1: Clean up old entries
    cleaned = remove_all_background_removal_entries()

    # Step 2: Install correct context menu
    installed = install_correct_context_menu()

    # Step 3: Test installation
    if installed:
        working = test_context_menu()

        if working:
            print("\n🎉 SUCCESS!")
            print("   Context menu is now properly configured.")
            print("   Right-click any file to see 'Remove Background' option.")
        else:
            print("\n❌ FAILED!")
            print("   Context menu was installed but is not working correctly.")
    else:
        print("\n❌ INSTALLATION FAILED!")
        print("   Could not install context menu.")

    print("\n💡 Next steps:")
    print("   1. Try right-clicking on an image file")
    print("   2. Look for 'Remove Background' in the context menu")
    print("   3. If it doesn't work, try running this script as Administrator")

if __name__ == "__main__":
    main()
