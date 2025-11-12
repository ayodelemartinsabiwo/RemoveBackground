#!/usr/bin/env python3
"""
Test script to verify performance optimizations
"""

import os
import sys
import time
from PIL import Image

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_image():
    """Create a simple test image"""
    test_image = Image.new('RGB', (500, 500), color='red')
    test_path = 'test_image.jpg'
    test_image.save(test_path, 'JPEG')
    return test_path

def test_performance():
    """Test the optimized background remover"""
    print("🚀 Testing Performance Optimizations...")

    # Create test image
    test_path = create_test_image()
    print(f"✅ Created test image: {test_path}")

    try:
        # Import the optimized remover
        from bg_remove_v1_2_bulletproof import BackgroundRemoverV12Bulletproof

        def progress_print(message):
            print(f"Status: {message}")

        # Test processing
        start_time = time.time()
        remover = BackgroundRemoverV12Bulletproof()
        success, result = remover.remove_background(test_path, progress_callback=progress_print)
        end_time = time.time()

        processing_time = end_time - start_time

        if success:
            print(f"\n🏆 SUCCESS!")
            print(f"⏱️ Processing Time: {processing_time:.2f} seconds")
            print(f"📁 Output: {result}")

            if processing_time < 30:  # Should be much faster than 7 minutes
                print("✅ Performance optimization SUCCESSFUL!")
            else:
                print("⚠️ Still slow, need more optimization")
        else:
            print(f"❌ FAILED: {result}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        try:
            os.remove(test_path)
            print(f"🧹 Cleaned up test image")
        except:
            pass

if __name__ == "__main__":
    test_performance()
