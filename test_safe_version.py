"""
Quick test for the SAFE speed-optimized version
This ensures the functionality works before rebuilding
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PIL import Image
import numpy as np

def create_simple_test_image():
    """Create a simple test image"""
    # Create a simple 800x600 test image
    image = Image.new('RGB', (800, 600), color=(100, 150, 200))

    # Add some content
    pixels = np.array(image)

    # Add a simple gradient
    for y in range(600):
        for x in range(800):
            pixels[y, x] = [x % 256, y % 256, (x + y) % 256]

    # Convert back to PIL Image
    result = Image.fromarray(pixels)

    # Save test image
    test_path = "quick_test_image.jpg"
    result.save(test_path, 'JPEG', quality=85)
    print(f"Created test image: {test_path}")

    return test_path

def test_safe_version():
    """Test the safe speed-optimized version"""
    print("🧪 TESTING SAFE SPEED-OPTIMIZED VERSION")
    print("=" * 50)

    # Create test image
    test_image = create_simple_test_image()

    try:
        from bg_remove_v1_3_speed_safe import BackgroundRemoverV13SpeedOptimized

        def progress_callback(msg):
            print(f"  {msg}")

        print("⚡ Testing Safe Speed Optimized version...")
        import time
        start_time = time.time()

        remover = BackgroundRemoverV13SpeedOptimized()
        success, result = remover.remove_background(
            test_image,
            progress_callback=progress_callback
        )

        processing_time = time.time() - start_time

        if success:
            print(f"✅ SUCCESS: {processing_time:.1f}s")
            print(f"Result: {result}")

            # Check if output file exists
            if "Saved to:" in result:
                output_path = result.split("Saved to: ")[-1].split("\n")[0]
                if os.path.exists(output_path):
                    print(f"✅ Output file confirmed: {output_path}")
                else:
                    print(f"⚠️ Output file not found: {output_path}")
        else:
            print(f"❌ FAILED: {result}")

    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup
    try:
        if os.path.exists(test_image):
            os.remove(test_image)
            print(f"Cleaned up: {test_image}")
    except:
        pass

    # Cleanup any output files
    for pattern in ['*_no_bg_*.png', 'output_no_bg_speed.png']:
        import glob
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"Cleaned up: {file}")
            except:
                pass

if __name__ == "__main__":
    test_safe_version()
