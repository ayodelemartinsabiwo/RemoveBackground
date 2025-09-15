#!/usr/bin/env python3
"""
Registry Inspector - Check current context menu entries
"""

import winreg
import os

def check_registry_key(key_path):
    """Check if a registry key exists and what it contains."""
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            try:
                value = winreg.QueryValue(key, "")
                print(f"  ✅ {key_path} = '{value}'")

                # Try to get icon value if it exists
                try:
                    icon = winreg.QueryValueEx(key, "Icon")[0]
                    print(f"      Icon: {icon}")
                except FileNotFoundError:
                    pass

                return True, value
            except:
                print(f"  ✅ {key_path} (exists but no default value)")
                return True, ""
    except FileNotFoundError:
        print(f"  ❌ {key_path} (not found)")
        return False, ""
    except Exception as e:
        print(f"  ⚠️  {key_path} (error: {e})")
        return False, ""

def main():
    print("Registry Inspector - Context Menu Entries")
    print("=" * 45)

    # Check common context menu locations
    keys_to_check = [
        r"*\shell\RemoveBackground",
        r"*\shell\RemoveBackground\command",
        r"*\shell\Remove Background",
        r"*\shell\Remove Background\command",
        r"*\shell\BackgroundRemover",
        r"*\shell\BackgroundRemover\command",
        r"SystemFileAssociations\image\shell\RemoveBackground",
        r"SystemFileAssociations\image\shell\RemoveBackground\command",
        r"SystemFileAssociations\.jpg\shell\RemoveBackground",
        r"SystemFileAssociations\.png\shell\RemoveBackground",
    ]

    print("\n🔍 Checking registry entries...")
    found_entries = []

    for key_path in keys_to_check:
        exists, value = check_registry_key(key_path)
        if exists:
            found_entries.append((key_path, value))

    if found_entries:
        print(f"\n📋 Found {len(found_entries)} registry entries:")
        for key_path, value in found_entries:
            print(f"   {key_path} = '{value}'")
    else:
        print("\n❌ No context menu entries found in registry")

    print(f"\n💡 Our target executable: {os.path.abspath('dist/BackgroundRemover.exe')}")
    print(f"   Exists: {'✅' if os.path.exists('dist/BackgroundRemover.exe') else '❌'}")

if __name__ == "__main__":
    main()
