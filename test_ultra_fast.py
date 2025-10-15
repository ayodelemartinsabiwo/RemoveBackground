"""
Ultra-Fast V1.1 Speed Test
Quick test to verify if V1.1 Ultra can achieve the <30 second target
"""

import os
import sys
import time

def test_ultra_fast():
    print("🚀 TESTING V1.1 ULTRA FAST VERSION")
    print("Target: <30 seconds processing time")
    print("=" * 60)

    # Find test image
    test_images = ["blackhair.jpg", "test_image.jpg", "sample.jpg"]
    input_image = None

    for img in test_images:
        if os.path.exists(img):
            input_image = img
            break

    if not input_image:
        print("❌ No test image found!")
        return

    print(f"📷 Testing with: {input_image}")

    # Test ultra-fast version
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    try:
        from bg_remove_v1_1_ultra_fast import remove_background_ultra_fast

        print("\n🎯 Starting ultra-fast test...")
        start_time = time.time()

        result = remove_background_ultra_fast(input_image)

        total_time = time.time() - start_time

        if result:
            print(f"\n🎉 ULTRA FAST TEST COMPLETE!")
            print(f"⏱️ Total Time: {total_time:.1f} seconds")
            print(f"🎯 Target Met: {'✅ YES' if total_time <= 30 else '❌ NO'}")

            # File size check
            input_size = os.path.getsize(input_image) / (1024 * 1024)
            output_size = os.path.getsize(result) / (1024 * 1024)
            print(f"📁 File Sizes: {input_size:.2f}MB → {output_size:.2f}MB")
            print(f"💾 Output: {result}")

            if total_time <= 30:
                print("\n🏆 SUCCESS: Ultra-fast version meets speed target!")
            else:
                print(f"\n⚠️ NEEDS MORE OPTIMIZATION: {total_time - 30:.1f}s over target")
        else:
            print("❌ Ultra-fast processing failed!")

    except Exception as e:
        print(f"❌ Error testing ultra-fast version: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ultra_fast()
