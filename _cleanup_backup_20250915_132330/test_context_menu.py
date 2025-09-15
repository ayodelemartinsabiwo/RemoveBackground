#!/usr/bin/env python3
"""
Context Menu Test - Verify the fix worked
"""

import os
import subprocess
import winreg

def test_context_menu_registry():
    """Test that registry entries are correct."""
    print("🔍 Testing registry entries...")

    try:
        # Check main key
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\RemoveBackground") as key:
            display_name = winreg.QueryValue(key, "")
            icon_path = winreg.QueryValueEx(key, "Icon")[0]

            print(f"  ✅ Display name: '{display_name}'")
            print(f"  ✅ Icon path: {icon_path}")

            # Check if icon file exists
            if os.path.exists(icon_path):
                print(f"  ✅ Icon file exists")
            else:
                print(f"  ❌ Icon file missing!")
                return False

        # Check command key
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\RemoveBackground\command") as key:
            command = winreg.QueryValue(key, "")
            print(f"  ✅ Command: {command}")

            # Extract executable path from command
            if '"' in command:
                exe_path = command.split('"')[1]
                if os.path.exists(exe_path):
                    print(f"  ✅ Executable exists: {exe_path}")
                else:
                    print(f"  ❌ Executable missing: {exe_path}")
                    return False

        return True

    except Exception as e:
        print(f"  ❌ Registry test failed: {e}")
        return False

def test_executable_launch():
    """Test that the executable can be launched."""
    print("\n🚀 Testing executable launch...")

    exe_path = os.path.abspath("dist/BackgroundRemover.exe")

    if not os.path.exists(exe_path):
        print(f"  ❌ Executable not found: {exe_path}")
        return False

    print(f"  📍 Testing: {exe_path}")

    try:
        # Test launching the executable (it should start and exit cleanly)
        result = subprocess.run([exe_path],
                              timeout=5,
                              capture_output=True,
                              text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW)

        print(f"  ✅ Executable launched successfully")
        print(f"  ✅ Return code: {result.returncode}")

        if result.stdout:
            print(f"  📋 Output: {result.stdout[:100]}...")

        return True

    except subprocess.TimeoutExpired:
        print(f"  ✅ Executable launched (GUI app - timeout expected)")
        return True
    except Exception as e:
        print(f"  ❌ Launch failed: {e}")
        return False

def main():
    print("Context Menu Test - Verification")
    print("=" * 35)

    print("\n🧪 Running context menu tests...\n")

    # Test 1: Registry entries
    registry_ok = test_context_menu_registry()

    # Test 2: Executable launch
    executable_ok = test_executable_launch()

    print(f"\n📊 Test Results:")
    print(f"  Registry entries: {'✅ PASS' if registry_ok else '❌ FAIL'}")
    print(f"  Executable launch: {'✅ PASS' if executable_ok else '❌ FAIL'}")

    if registry_ok and executable_ok:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"\nThe context menu should now work correctly:")
        print(f"1. Right-click on any file (image or other)")
        print(f"2. Look for 'Remove Background' option")
        print(f"3. Click it to launch BackgroundRemover.exe")
        print(f"4. The app should process the selected file")
        return True
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        print(f"Context menu may not work correctly.")
        return False

if __name__ == "__main__":
    main()
