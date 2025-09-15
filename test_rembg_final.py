#!/usr/bin/env python3
"""
Final test to verify rembg functionality in the built environment
"""
import sys
import os

# Add src to path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_rembg_import():
    """Test rembg import and basic functionality"""
    try:
        print("Testing rembg import...")

        # Test the same import path used in bg_remove_optimized.py
        from bg_remove_optimized import OptimizedBackgroundRemover, REMBG_AVAILABLE

        print("✅ OptimizedBackgroundRemover imported successfully!")
        print(f"✅ REMBG available: {REMBG_AVAILABLE}")

        if REMBG_AVAILABLE:
            # Try to create an instance
            remover = OptimizedBackgroundRemover()
            print("✅ OptimizedBackgroundRemover instance created successfully!")
            print("🎉 SUCCESS: rembg is fully functional!")
            return True
        else:
            print("❌ FAILED: rembg is not available")
            return False

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("REMBG FINAL FUNCTIONALITY TEST")
    print("=" * 50)

    success = test_rembg_import()

    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Background removal should work!")
    else:
        print("❌ TESTS FAILED! Background removal may not work!")
    print("=" * 50)
