#!/usr/bin/env python3
"""
Test script to verify that the Background Remover app is working correctly.
Tests the rembg import and basic functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing module imports...")

    try:
        import rembg
        print("✅ rembg imported successfully")

        # Test rembg functionality
        from rembg import new_session
        session = new_session('u2net')
        print("✅ rembg session created successfully")

        # Test PIL
        from PIL import Image
        print("✅ PIL imported successfully")

        # Test numpy
        import numpy as np
        print("✅ numpy imported successfully")

        # Test PyQt6
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6 imported successfully")

        # Test our modules
        import bg_remove
        print("✅ bg_remove module imported successfully")

        import gui_loader
        print("✅ gui_loader module imported successfully")

        import context_menu
        print("✅ context_menu module imported successfully")

        print("\n🎉 All imports successful! The app should work correctly.")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Background Remover - Testing Application Components")
    print("=" * 50)

    success = test_imports()

    if success:
        print("\n✅ ALL TESTS PASSED - The application should work!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED - Check the errors above")
        sys.exit(1)
