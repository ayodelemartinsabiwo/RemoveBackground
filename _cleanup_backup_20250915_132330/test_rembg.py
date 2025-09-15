#!/usr/bin/env python3
"""
Test script to diagnose rembg import issues in the executable
"""
import sys
import os

print("Python executable:", sys.executable)
print("Python path:", sys.path[:3])
print("Current working directory:", os.getcwd())

try:
    print("Attempting to import rembg...")
    import rembg
    print(f"✓ rembg imported successfully")
    print(f"  rembg location: {rembg.__file__}")
    print(f"  rembg version: {getattr(rembg, '__version__', 'unknown')}")

    try:
        from rembg import remove
        print("✓ rembg.remove imported successfully")

        try:
            from PIL import Image
            print("✓ PIL imported successfully")

            # Try to create a simple test
            print("Testing basic rembg functionality...")
            # This would require an actual image, but we're just testing import
            print("✓ All imports successful - rembg should work")

        except ImportError as e:
            print(f"✗ PIL import failed: {e}")

    except ImportError as e:
        print(f"✗ rembg.remove import failed: {e}")

except ImportError as e:
    print(f"✗ rembg import failed: {e}")
    print("Available modules:")
    for module_name in sorted(sys.modules.keys()):
        if 'rembg' in module_name.lower():
            print(f"  {module_name}: {sys.modules[module_name]}")

print("\nTest completed.")
