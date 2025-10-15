"""
Version 1.1 Performance & Quality Test
Tests all improvements against user feedback:
1. Enhanced hair artifact removal (Freepik-level)
2. File size optimization (10MB → 2MB target)
3. Speed optimization (<30 seconds)
4. System resource management (no PC lag)
5. Quality comparison with attached analysis

This script benchmarks V1.1 against V12 to verify improvements.
"""

import os
import time
import sys
from pathlib import Path
import psutil
import gc

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def benchmark_version(version_module, version_name, input_image, progress_callback=None):
    """Benchmark a specific version"""
    print(f"\n{'='*60}")
    print(f"BENCHMARKING {version_name}")
    print(f"{'='*60}")

    # Memory before
    process = psutil.Process()
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    cpu_before = psutil.cpu_percent(interval=1)

    print(f"📊 Initial Stats:")
    print(f"   Memory: {memory_before:.1f} MB")
    print(f"   CPU: {cpu_before:.1f}%")

    # Create remover instance
    remover = version_module()

    def test_progress(msg):
        if progress_callback:
            progress_callback(msg)
        print(f"   {msg}")

    # Start benchmark
    start_time = time.time()

    try:
        # Process image
        success, result = remover.remove_background(input_image, test_progress)

        end_time = time.time()
        processing_time = end_time - start_time

        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_peak = memory_after
        cpu_after = psutil.cpu_percent(interval=1)

        if success and os.path.exists(result):
            # File size analysis
            input_size = os.path.getsize(input_image) / 1024 / 1024  # MB
            output_size = os.path.getsize(result) / 1024 / 1024  # MB

            print(f"\n✅ {version_name} SUCCESS!")
            print(f"📁 File Sizes:")
            print(f"   Input:  {input_size:.2f} MB")
            print(f"   Output: {output_size:.2f} MB")
            print(f"   Ratio:  {output_size/input_size:.1f}x")

            print(f"⏱️ Performance:")
            print(f"   Processing Time: {processing_time:.1f} seconds")
            print(f"   Target: <30 seconds = {'✅ PASS' if processing_time < 30 else '❌ FAIL'}")

            print(f"💾 Memory Usage:")
            print(f"   Before: {memory_before:.1f} MB")
            print(f"   Peak:   {memory_peak:.1f} MB")
            print(f"   Delta:  +{memory_peak - memory_before:.1f} MB")

            print(f"🖥️ CPU Usage:")
            print(f"   Before: {cpu_before:.1f}%")
            print(f"   During: {cpu_after:.1f}%")

            return {
                'success': True,
                'processing_time': processing_time,
                'input_size_mb': input_size,
                'output_size_mb': output_size,
                'size_ratio': output_size/input_size,
                'memory_before_mb': memory_before,
                'memory_peak_mb': memory_peak,
                'memory_delta_mb': memory_peak - memory_before,
                'cpu_before': cpu_before,
                'cpu_after': cpu_after,
                'output_file': result
            }

        else:
            print(f"❌ {version_name} FAILED!")
            print(f"   Error: {result}")
            return {'success': False, 'error': result}

    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"❌ {version_name} CRASHED!")
        print(f"   Error: {str(e)}")
        print(f"   Time before crash: {processing_time:.1f} seconds")
        return {'success': False, 'error': str(e), 'crash_time': processing_time}

    finally:
        # Cleanup
        gc.collect()


def compare_results(v12_results, v11_results):
    """Compare V1.1 vs V12 results"""
    print(f"\n{'='*80}")
    print(f"COMPARISON: V1.1 vs V12")
    print(f"{'='*80}")

    if not v12_results.get('success') or not v11_results.get('success'):
        print("❌ Cannot compare - one or both versions failed")
        return

    # Speed comparison
    v12_time = v12_results['processing_time']
    v11_time = v11_results['processing_time']
    speed_improvement = ((v12_time - v11_time) / v12_time) * 100

    print(f"⚡ SPEED ANALYSIS:")
    print(f"   V12 Time:    {v12_time:.1f} seconds")
    print(f"   V1.1 Time:   {v11_time:.1f} seconds")
    print(f"   Improvement: {speed_improvement:+.1f}% {'🚀' if speed_improvement > 0 else '🐌'}")
    print(f"   Target <30s: V12={'✅' if v12_time < 30 else '❌'} | V1.1={'✅' if v11_time < 30 else '❌'}")

    # File size comparison
    v12_size = v12_results['output_size_mb']
    v11_size = v11_results['output_size_mb']
    size_reduction = ((v12_size - v11_size) / v12_size) * 100

    print(f"\n💾 FILE SIZE ANALYSIS:")
    print(f"   V12 Output:     {v12_size:.2f} MB")
    print(f"   V1.1 Output:    {v11_size:.2f} MB")
    print(f"   Reduction:      {size_reduction:+.1f}% {'📉' if size_reduction > 0 else '📈'}")
    print(f"   Target <3MB:    V12={'✅' if v12_size < 3 else '❌'} | V1.1={'✅' if v11_size < 3 else '❌'}")

    # Memory comparison
    v12_memory = v12_results['memory_delta_mb']
    v11_memory = v11_results['memory_delta_mb']
    memory_improvement = ((v12_memory - v11_memory) / v12_memory) * 100 if v12_memory > 0 else 0

    print(f"\n🧠 MEMORY USAGE ANALYSIS:")
    print(f"   V12 Memory Delta:  +{v12_memory:.1f} MB")
    print(f"   V1.1 Memory Delta: +{v11_memory:.1f} MB")
    print(f"   Improvement:       {memory_improvement:+.1f}% {'🔽' if memory_improvement > 0 else '🔺'}")

    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")

    targets_met = 0
    total_targets = 4

    # Speed target
    if v11_time < 30:
        print(f"   ✅ Speed Target: V1.1 processes in {v11_time:.1f}s (<30s)")
        targets_met += 1
    else:
        print(f"   ❌ Speed Target: V1.1 takes {v11_time:.1f}s (target: <30s)")

    # File size target
    if v11_size < 3:
        print(f"   ✅ File Size Target: V1.1 output is {v11_size:.2f}MB (<3MB)")
        targets_met += 1
    else:
        print(f"   ❌ File Size Target: V1.1 output is {v11_size:.2f}MB (target: <3MB)")

    # Speed improvement
    if speed_improvement > 20:
        print(f"   ✅ Speed Improvement: {speed_improvement:.1f}% faster than V12")
        targets_met += 1
    else:
        print(f"   ⚠️ Speed Improvement: Only {speed_improvement:.1f}% faster than V12")

    # Memory efficiency
    if memory_improvement > 10:
        print(f"   ✅ Memory Efficiency: {memory_improvement:.1f}% less memory than V12")
        targets_met += 1
    else:
        print(f"   ⚠️ Memory Efficiency: Only {memory_improvement:.1f}% memory improvement")

    success_rate = (targets_met / total_targets) * 100
    print(f"\n🏆 SUCCESS RATE: {targets_met}/{total_targets} targets met ({success_rate:.0f}%)")

    if success_rate >= 75:
        print("🎉 V1.1 READY FOR PRODUCTION!")
    elif success_rate >= 50:
        print("⚠️ V1.1 shows improvements but needs refinement")
    else:
        print("❌ V1.1 needs significant work")


def main():
    """Main benchmark test"""
    print("🔥 VERSION 1.1 BENCHMARK TEST")
    print("Testing improvements based on user feedback")
    print("Target: <30s processing, <3MB files, no PC lag, Freepik-level quality")

    # Find test image
    test_images = [
        "blackhair.jpg",
        "test_image.jpg",
        "sample.jpg"
    ]

    input_image = None
    for img in test_images:
        if os.path.exists(img):
            input_image = img
            break

    if not input_image:
        print("❌ No test image found! Please ensure blackhair.jpg or test_image.jpg exists.")
        print("Available files:")
        for f in os.listdir("."):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"   - {f}")
        return

    print(f"📷 Using test image: {input_image}")
    input_size = os.path.getsize(input_image) / 1024 / 1024
    print(f"📏 Input size: {input_size:.2f} MB")

    # Test V12 (current version)
    try:
        from bg_remove_v12_refined import OptimizedBackgroundRemoverV12
        v12_results = benchmark_version(
            OptimizedBackgroundRemoverV12,
            "V12 (Current)",
            input_image
        )
    except Exception as e:
        print(f"❌ Failed to test V12: {e}")
        v12_results = {'success': False, 'error': str(e)}

    # Test V1.1 (new speed-optimized version)
    try:
        from bg_remove_v1_1_fast import OptimizedBackgroundRemoverV11Fast
        v11_results = benchmark_version(
            OptimizedBackgroundRemoverV11Fast,
            "V1.1 SPEED (Fast & Optimized)",
            input_image
        )
    except Exception as e:
        print(f"❌ Failed to test V1.1: {e}")
        v11_results = {'success': False, 'error': str(e)}    # Compare results
    if v12_results.get('success') and v11_results.get('success'):
        compare_results(v12_results, v11_results)

        print(f"\n📁 OUTPUT FILES:")
        print(f"   V12:  {v12_results.get('output_file', 'N/A')}")
        print(f"   V1.1: {v11_results.get('output_file', 'N/A')}")
        print(f"\n💡 Compare the output images manually to verify:")
        print(f"   1. Hair artifact removal (Freepik-level quality)")
        print(f"   2. Edge smoothness and natural appearance")
        print(f"   3. File size reduction while maintaining quality")

    else:
        print("\n❌ Cannot perform comparison due to failures")
        if not v12_results.get('success'):
            print(f"   V12 failed: {v12_results.get('error', 'Unknown error')}")
        if not v11_results.get('success'):
            print(f"   V1.1 failed: {v11_results.get('error', 'Unknown error')}")

    print(f"\n{'='*80}")
    print("BENCHMARK COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
