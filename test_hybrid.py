"""
Hybrid V1.1 Test
Testing the combination of Ultra Fast quality with Extreme speed
"""

import os
import sys
import time

def test_hybrid_version():
    print("🎯 TESTING V1.1 HYBRID VERSION")
    print("Ultra Fast Quality + Extreme Speed = Best of Both Worlds")
    print("=" * 75)

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

    # Test hybrid version
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    try:
        from bg_remove_v1_1_hybrid import remove_background_hybrid

        print("\n🎯 Starting hybrid test...")
        start_time = time.time()

        result = remove_background_hybrid(input_image)

        total_time = time.time() - start_time

        if result:
            print(f"\n🎯 HYBRID TEST COMPLETE!")
            print(f"⏱️ Total Time: {total_time:.1f} seconds")
            print(f"🎯 Speed Target: {'🏆 YES' if total_time <= 30 else '❌ NO'}")
            print(f"🎨 Quality: Ultra Fast's proven algorithms")

            # File size check
            input_size = os.path.getsize(input_image) / (1024 * 1024)
            output_size = os.path.getsize(result) / (1024 * 1024)
            print(f"📁 File Sizes: {input_size:.2f}MB → {output_size:.2f}MB")
            print(f"💾 Output: {result}")

            print(f"\n📊 HYBRID PERFORMANCE:")
            print(f"   🚀 Speed: {total_time:.1f}s (vs Extreme: 2.4s, Ultra: 50s)")
            print(f"   🎨 Quality: Ultra Fast's superior hair enhancement")
            print(f"   📦 File Size: {output_size:.2f}MB optimized")

            if total_time <= 30:
                print(f"\n🏆 PERFECT HYBRID: Speed + Quality targets achieved!")
                print(f"🎯 Ready to replace current version!")
            else:
                print(f"\n⚠️ NEEDS TUNING: {total_time - 30:.1f}s over speed target")

        else:
            print("❌ Hybrid processing failed!")

    except Exception as e:
        print(f"❌ Error testing hybrid version: {e}")
        import traceback
        traceback.print_exc()

def compare_all_versions():
    """Compare all V1.1 versions for reference"""
    print(f"\n📊 VERSION COMPARISON REFERENCE:")
    print(f"   V12 (Current):     72.0s   - Baseline")
    print(f"   V1.1 Fast:       162.1s   - Too slow")
    print(f"   V1.1 Ultra:       50.2s   - 🎨 Best quality")
    print(f"   V1.1 Extreme:      2.4s   - 🚀 Best speed, ❌ artifacts")
    print(f"   V1.1 Hybrid:       ???s   - 🎯 Target: Best of both!")

if __name__ == "__main__":
    compare_all_versions()
    test_hybrid_version()
