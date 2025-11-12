#!/usr/bin/env python3
"""
Test script to verify session caching performance improvements
"""

import os
import sys
import time
from PIL import Image

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_images():
    """Create multiple test images"""
    test_images = []
    colors = ['red', 'blue', 'green']

    for i, color in enumerate(colors):
        test_image = Image.new('RGB', (400, 400), color=color)
        test_path = f'test_image_{i}.jpg'
        test_image.save(test_path, 'JPEG')
        test_images.append(test_path)

    return test_images

def test_session_caching():
    """Test session caching performance"""
    print("🚀 Testing Session Caching Performance...")

    # Create test images
    test_images = create_test_images()
    print(f"✅ Created {len(test_images)} test images")

    try:
        # Import the optimized remover
        from bg_remove_v1_2_bulletproof import BackgroundRemoverV12Bulletproof

        def progress_print(message):
            print(f"Status: {message}")

        total_time = 0
        remover = BackgroundRemoverV12Bulletproof()

        for i, test_path in enumerate(test_images):
            print(f"\n🔄 Processing image {i+1}/{len(test_images)}: {test_path}")

            start_time = time.time()
            success, result = remover.remove_background(test_path, progress_callback=progress_print)
            end_time = time.time()

            processing_time = end_time - start_time
            total_time += processing_time

            if success:
                print(f"✅ Image {i+1} processed in {processing_time:.2f}s")
            else:
                print(f"❌ Image {i+1} failed: {result}")

        avg_time = total_time / len(test_images)
        print(f"\n🏆 RESULTS:")
        print(f"⏱️ Total Time: {total_time:.2f} seconds")
        print(f"📊 Average Time: {avg_time:.2f} seconds per image")

        if avg_time < 15:  # Should be much faster with caching
            print("✅ Session caching is working - good performance!")
        elif avg_time < 25:
            print("⚠️ Moderate performance - some optimization working")
        else:
            print("❌ Still slow - need more optimization")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        for test_path in test_images:
            try:
                os.remove(test_path)
                # Also remove output files
                output_path = test_path.replace('.jpg', '_no_bg_20251110.png')
                if os.path.exists(output_path):
                    os.remove(output_path)
            except:
                pass
        print(f"🧹 Cleaned up test files")

if __name__ == "__main__":
    test_session_caching()
