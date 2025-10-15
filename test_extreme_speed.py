"""
Extreme Speed V1.1 Test
Testing the most aggressive optimizations to hit <30 second target
"""

import os
import sys
import time

def test_extreme_speed():
    print("⚡ TESTING V1.1 EXTREME SPEED VERSION")
    print("Target: <30 seconds at any cost")
    print("=" * 70)

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

    # Test extreme version
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    try:
        from bg_remove_v1_1_extreme import remove_background_extreme_speed

        print("\n⚡ Starting extreme speed test...")
        start_time = time.time()

        result = remove_background_extreme_speed(input_image)

        total_time = time.time() - start_time

        if result:
            print(f"\n⚡ EXTREME SPEED TEST COMPLETE!")
            print(f"⏱️ Total Time: {total_time:.1f} seconds")
            print(f"🎯 Target Met: {'🏆 YES' if total_time <= 30 else '❌ NO'}")

            # File size check
            input_size = os.path.getsize(input_image) / (1024 * 1024)
            output_size = os.path.getsize(result) / (1024 * 1024)
            print(f"📁 File Sizes: {input_size:.2f}MB → {output_size:.2f}MB")
            print(f"💾 Output: {result}")

            if total_time <= 30:
                print("\n🏆 BREAKTHROUGH: Extreme version meets speed target!")
                print("🎯 Ready for integration into main application!")
            else:
                print(f"\n🔧 CLOSE CALL: {total_time - 30:.1f}s over target")
                print("💡 Consider further optimizations or accept near-target performance")

        else:
            print("❌ Extreme processing failed!")

    except Exception as e:
        print(f"❌ Error testing extreme version: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extreme_speed()
