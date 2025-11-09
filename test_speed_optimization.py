"""
Quick test script for speed optimization
Tests both versions and compares performance
"""

import os
import sys
import time
import shutil
from PIL import Image
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_image(width=1920, height=1080, complexity='medium'):
    """Create a test image with specified complexity"""
    print(f"Creating test image: {width}x{height}, complexity: {complexity}")

    # Create base image
    image = Image.new('RGB', (width, height), color=(120, 150, 200))
    pixels = np.array(image)

    if complexity == 'simple':
        # Simple gradient
        for y in range(height):
            for x in range(width):
                pixels[y, x] = [x % 256, y % 256, (x + y) % 256]

    elif complexity == 'medium':
        # Medium complexity with shapes
        center_x, center_y = width // 2, height // 2
        for y in range(height):
            for x in range(width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                color_val = int(128 + 127 * np.sin(dist / 50))
                pixels[y, x] = [color_val, (x * y) % 256, (x + y) % 256]

    elif complexity == 'complex':
        # Complex with many edges and textures
        for y in range(height):
            for x in range(width):
                # Multiple sine waves for complexity
                val1 = int(128 + 127 * np.sin(x / 20) * np.cos(y / 30))
                val2 = int(128 + 127 * np.sin(x / 15) * np.cos(y / 25))
                val3 = int(128 + 127 * np.sin(x / 10) * np.cos(y / 20))
                pixels[y, x] = [val1, val2, val3]

    # Convert back to PIL Image
    result = Image.fromarray(pixels)

    # Save test image
    test_path = f"test_image_{complexity}_{width}x{height}.jpg"
    result.save(test_path, 'JPEG', quality=85)
    print(f"Saved test image: {test_path}")

    return test_path

def test_processing_speed():
    """Test processing speed of both versions"""
    print("🚀 BACKGROUND REMOVER SPEED TEST")
    print("=" * 50)

    # Create test images
    test_images = []

    # Small simple image
    test_images.append(create_test_image(800, 600, 'simple'))

    # Medium complexity image
    test_images.append(create_test_image(1920, 1080, 'medium'))

    # Large complex image
    test_images.append(create_test_image(2400, 1600, 'complex'))

    results = []

    for test_image in test_images:
        print(f"\n📸 Testing: {test_image}")
        print("-" * 30)

        image_results = {'image': test_image}

        # Test V1.3 Speed Optimized
        try:
            from bg_remove_v1_3_speed import BackgroundRemoverV13SpeedOptimized

            def progress_callback(msg):
                print(f"  {msg}")

            print("⚡ Testing V1.3 Speed Optimized...")
            start_time = time.time()

            remover_v13 = BackgroundRemoverV13SpeedOptimized()
            success, result = remover_v13.remove_background(
                test_image,
                progress_callback=progress_callback
            )

            v13_time = time.time() - start_time
            image_results['v1.3_speed'] = v13_time
            image_results['v1.3_success'] = success

            print(f"  ✅ V1.3 Speed: {v13_time:.1f}s {'(SUCCESS)' if success else '(FAILED)'}")

            if success and os.path.exists(result.split('Saved to: ')[-1].split('\n')[0]):
                output_path = result.split('Saved to: ')[-1].split('\n')[0]
                print(f"  📁 Output: {output_path}")

        except Exception as e:
            print(f"  ❌ V1.3 Speed failed: {e}")
            image_results['v1.3_speed'] = None
            image_results['v1.3_success'] = False

        # Test V1.2 Bulletproof (for comparison)
        try:
            from bg_remove_v1_2_bulletproof import BackgroundRemoverV12Bulletproof

            def progress_callback_v12(msg):
                print(f"  {msg}")

            print("🛡️ Testing V1.2 Bulletproof...")
            start_time = time.time()

            remover_v12 = BackgroundRemoverV12Bulletproof()
            success, result = remover_v12.remove_background(
                test_image,
                progress_callback=progress_callback_v12
            )

            v12_time = time.time() - start_time
            image_results['v1.2_bulletproof'] = v12_time
            image_results['v1.2_success'] = success

            print(f"  ✅ V1.2 Bulletproof: {v12_time:.1f}s {'(SUCCESS)' if success else '(FAILED)'}")

        except Exception as e:
            print(f"  ❌ V1.2 Bulletproof failed: {e}")
            image_results['v1.2_bulletproof'] = None
            image_results['v1.2_success'] = False

        # Calculate improvement
        v13_time = image_results.get('v1.3_speed')
        v12_time = image_results.get('v1.2_bulletproof')

        if v13_time is not None and v12_time is not None and v12_time > 0:
            improvement = ((v12_time - v13_time) / v12_time) * 100
            image_results['improvement'] = improvement
            print(f"  🏆 Speed improvement: {improvement:.1f}%")

        # Check 40-second target
        if v13_time is not None:
            target_met = v13_time <= 40
            print(f"  🎯 40s target: {'✅ MET' if target_met else '⚠️ EXCEEDED'}")

        results.append(image_results)

    # Summary
    print("\n" + "=" * 50)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 50)

    for result in results:
        print(f"\n📸 {result['image']}:")
        if result.get('v1.3_speed'):
            target_status = '✅ MET' if result['v1.3_speed'] <= 40 else '⚠️ EXCEEDED'
            print(f"  ⚡ V1.3 Speed: {result['v1.3_speed']:.1f}s ({target_status} 40s target)")
        if result.get('v1.2_bulletproof'):
            print(f"  🛡️ V1.2 Bulletproof: {result['v1.2_bulletproof']:.1f}s")
        if result.get('improvement'):
            print(f"  🏆 Improvement: {result['improvement']:.1f}%")

    # Overall assessment
    v13_times = [r['v1.3_speed'] for r in results if r.get('v1.3_speed')]
    if v13_times:
        avg_time = sum(v13_times) / len(v13_times)
        max_time = max(v13_times)
        target_met = all(t <= 40 for t in v13_times)

        print(f"\n🎯 OPTIMIZATION ASSESSMENT:")
        print(f"  Average processing time: {avg_time:.1f}s")
        print(f"  Maximum processing time: {max_time:.1f}s")
        print(f"  40-second target: {'✅ ACHIEVED' if target_met else '⚠️ NOT MET'}")

        if target_met:
            print("  🏆 SUCCESS! All images processed within 40 seconds!")
        else:
            print("  ⚠️ Some images exceeded 40-second target. Further optimization needed.")

    # Cleanup test files
    print(f"\n🧹 Cleaning up test files...")
    for test_image in test_images:
        try:
            if os.path.exists(test_image):
                os.remove(test_image)
                print(f"  Removed: {test_image}")
        except:
            pass

    # Cleanup output files
    for pattern in ['*_no_bg_*.png', 'output_no_bg_speed.png']:
        import glob
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"  Removed: {file}")
            except:
                pass

if __name__ == "__main__":
    test_processing_speed()
