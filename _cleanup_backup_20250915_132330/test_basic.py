import sys
import os

print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())

try:
    print("Testing PyQt6 import...")
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 imported successfully")

    print("Testing rembg import...")
    import rembg
    print("✓ rembg imported successfully")

    print("Testing PIL import...")
    from PIL import Image
    print("✓ PIL imported successfully")

    print("All basic imports successful!")

except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
