import os
import sys
from pathlib import Path

def test_basic_functionality():
    """Test basic import functionality"""
    print("Testing basic imports...")

    try:
        from src.context_menu import ContextMenuManager
        print("✅ Context menu module imported successfully")
    except Exception as e:
        print(f"❌ Context menu import failed: {e}")
        return False

    try:
        from src.bg_remove import BackgroundRemover
        print("✅ Background remover module imported successfully")
    except Exception as e:
        print(f"❌ Background remover import failed: {e}")
        return False

    try:
        from src.gui_loader import LoaderWindow
        print("✅ GUI loader module imported successfully")
    except Exception as e:
        print(f"❌ GUI loader import failed: {e}")
        return False

    return True

def test_context_menu():
    """Test context menu functionality"""
    print("\nTesting context menu functionality...")

    try:
        from src.context_menu import ContextMenuManager
        manager = ContextMenuManager()

        # Test if context menu is already installed
        is_installed = manager.is_installed()
        print(f"Context menu currently installed: {is_installed}")

        return True
    except Exception as e:
        print(f"❌ Context menu test failed: {e}")
        return False

def main():
    print("🧪 Testing Background Remover Application...")
    print("=" * 50)

    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality test failed")
        return False

    # Test context menu
    if not test_context_menu():
        print("\n❌ Context menu test failed")
        return False

    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("\nYour application is ready!")
    print("\nNext steps:")
    print("1. Find a test image (JPG/PNG)")
    print("2. Run: python src/main.py <path_to_image>")
    print("3. Build executable: pyinstaller build.spec --clean --noconfirm")

    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
