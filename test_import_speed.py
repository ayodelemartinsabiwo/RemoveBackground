#!/usr/bin/env python3
"""
Test script to measure import and window creation times
"""

import time
import sys

def time_import(module_name):
    """Time how long it takes to import a module"""
    start = time.time()
    try:
        if module_name == "PyQt6.QtWidgets":
            from PyQt6.QtWidgets import QApplication
            app = QApplication([])
        elif module_name == "loader_window":
            from loader_window import LoaderWindow
        elif module_name == "bg_remove_optimized":
            from bg_remove_optimized import OptimizedBackgroundRemover
        elif module_name == "rembg":
            from rembg import remove
        elif module_name == "PIL":
            from PIL import Image

        end = time.time()
        return end - start
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Import Speed Test")
    print("=" * 40)

    modules = [
        "PyQt6.QtWidgets",
        "loader_window",
        "bg_remove_optimized",
        "rembg",
        "PIL"
    ]

    for module in modules:
        duration = time_import(module)
        if isinstance(duration, str):
            print(f"{module:20}: {duration}")
        else:
            print(f"{module:20}: {duration:.3f}s")

    # Test window creation
    print("\nWindow Creation Test")
    print("=" * 40)

    start = time.time()
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    from loader_window import LoaderWindow
    loader = LoaderWindow()
    end = time.time()

    print(f"Window created in: {end - start:.3f}s")
    loader.close()

if __name__ == "__main__":
    main()
