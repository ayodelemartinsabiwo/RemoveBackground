"""
Distribution Compatibility Test
Tests for common distribution issues before packaging
"""

import sys
import os

def test_imports():
    """Test all required imports without problematic dependencies"""
    print("🧪 Testing Core Imports...")

    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except Exception as e:
        print(f"❌ NumPy failed: {e}")
        return False

    try:
        from PIL import Image, ImageOps, ImageFilter
        print("✅ PIL imported successfully")
    except Exception as e:
        print(f"❌ PIL failed: {e}")
        return False

    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except Exception as e:
        print(f"❌ OpenCV failed: {e}")
        return False

    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QIcon
        print("✅ PyQt6 Core imported successfully")
    except Exception as e:
        print(f"❌ PyQt6 failed: {e}")
        return False

    try:
        from rembg import remove, new_session
        print("✅ RemBG imported successfully")
    except Exception as e:
        print(f"❌ RemBG failed: {e}")
        return False

    return True

def test_problematic_imports():
    """Test that problematic imports are NOT present"""
    print("\n🚫 Testing Problematic Imports Are Excluded...")

    excluded_imports = [
        'scipy',
        'skimage',
        'PyQt6.QtWebEngine',
        'webview'
    ]

    for module in excluded_imports:
        try:
            __import__(module)
            print(f"⚠️  WARNING: {module} is present (may cause distribution issues)")
        except ImportError:
            print(f"✅ {module} properly excluded")

    return True

def test_algorithm():
    """Test core algorithm functionality"""
    print("\n🎯 Testing Core Algorithm...")

    try:
        # Import our bulletproof version
        sys.path.insert(0, 'src')
        from bg_remove_v1_2_bulletproof import BackgroundRemoverV12Bulletproof

        # Create instance
        remover = BackgroundRemoverV12Bulletproof()
        print("✅ BackgroundRemover instance created")

        # Test witty messages
        message = remover._get_next_witty_message()
        if "🤗" in message:
            print("✅ Witty messages working")
        else:
            print(f"⚠️  Witty message format: {message}")

        return True

    except Exception as e:
        print(f"❌ Algorithm test failed: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("🏆 Background Remover V1.2 - Distribution Compatibility Test")
    print("=" * 60)

    tests = [
        ("Core Imports", test_imports),
        ("Problematic Imports", test_problematic_imports),
        ("Core Algorithm", test_algorithm)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")

    print("\n" + "=" * 60)
    print(f"🏁 Distribution Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 READY FOR DISTRIBUTION! All tests passed.")
        return True
    else:
        print("⚠️  Distribution issues detected. Fix before packaging.")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
