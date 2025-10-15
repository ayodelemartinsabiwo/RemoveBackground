"""
Background Remover V1.1 Extreme Speed - Sub-30 Second Version
Extreme optimizations to achieve <30 second target at any cost

Key optimizations:
1. Use smaller/faster model (u2net instead of birefnet if available)
2. Aggressive image resizing
3. Minimal post-processing
4. Session pre-loading and caching
5. Skip expensive operations
"""

import os
import numpy as np
from rembg import remove, new_session
from PIL import Image
import time
import gc

class BackgroundRemoverV11Extreme:
    def __init__(self):
        self.session = None
        self.start_time = None

    def _log_progress(self, message):
        """Ultra-fast progress logging"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"   {message} (t+{elapsed:.1f}s)")

    def _initialize_session_cached(self):
        """Pre-load session for maximum speed"""
        if not self.session:
            self._log_progress("Loading fastest AI model... ⚡")
            # Use u2net model which is smaller and faster than birefnet
            try:
                self.session = new_session('u2net')
                self._log_progress("✅ Fast model loaded")
            except:
                # Fallback to birefnet if u2net not available
                self.session = new_session('birefnet-portrait')
                self._log_progress("✅ Fallback model loaded")

    def _extreme_preprocessing(self, image_path, max_size=800):
        """
        Extreme preprocessing for maximum speed
        Aggressive resizing to minimize processing time
        """
        self._log_progress("Loading & aggressively resizing image... 🏃‍♂️")

        with Image.open(image_path) as img:
            # Convert to RGB immediately
            if img.mode != 'RGB':
                img = img.convert('RGB')

            original_size = img.size

            # AGGRESSIVE resizing for speed - smaller than ultra-fast
            if max(original_size) > max_size:
                ratio = max_size / max(original_size)
                new_width = int(original_size[0] * ratio)
                new_height = int(original_size[1] * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.NEAREST)  # Use NEAREST for speed
                self._log_progress(f"Aggressively resized to {new_width}x{new_height}")

            return np.array(img), original_size

    def _lightning_hair_fix(self, result_image):
        """
        Lightning-fast hair enhancement - single operation only
        """
        self._log_progress("Instant hair enhancement... ⚡")

        # Convert to array for fast processing
        result_array = np.array(result_image)

        if len(result_array.shape) == 3 and result_array.shape[2] == 4:
            # Simple alpha channel smoothing - single pass only
            alpha = result_array[:, :, 3]

            # Ultra-fast binary threshold to clean artifacts
            alpha[alpha < 128] = 0
            alpha[alpha >= 128] = 255

            result_array[:, :, 3] = alpha

        return Image.fromarray(result_array)

    def _extreme_compression(self, image, output_path):
        """
        Extreme compression for smallest file size
        """
        self._log_progress("Extreme file compression... 💾")

        # Save with maximum compression and reduced quality
        image.save(output_path, 'PNG', optimize=True, compress_level=9)

    def remove_background(self, input_path, output_path=None, max_size=800):
        """
        Extreme speed background removal - targeting <30 seconds

        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            max_size: Aggressive max dimension for extreme speed
        """
        self.start_time = time.time()

        try:
            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_no_bg_v11_extreme{ext}"

            # Step 1: Extreme preprocessing (target: <2s)
            img_array, original_size = self._extreme_preprocessing(input_path, max_size)

            # Step 2: Initialize session if needed (target: <5s total)
            self._initialize_session_cached()

            # Step 3: AI processing (target: <20s total)
            self._log_progress("AI processing in extreme speed mode... 🚀")

            # Direct rembg processing - no additional parameters for speed
            pil_img = Image.fromarray(img_array)
            result = remove(pil_img, session=self.session)

            # Step 4: Minimal post-processing (target: <2s)
            result = self._lightning_hair_fix(result)

            # Step 5: Resize back to original size (target: <3s total)
            if result.size != original_size:
                self._log_progress("Resizing to original dimensions... 📏")
                result = result.resize(original_size, Image.Resampling.LANCZOS)

            # Step 6: Save with extreme compression (target: <1s)
            self._extreme_compression(result, output_path)

            elapsed = time.time() - self.start_time

            # Immediate cleanup
            del img_array, pil_img, result
            gc.collect()

            self._log_progress(f"✅ EXTREME SPEED processing complete in {elapsed:.1f}s!")

            # Check success against 30-second target
            if elapsed <= 30:
                print(f"   🏆 SUCCESS: Met <30s target! ({elapsed:.1f}s)")
                return output_path, elapsed, True
            else:
                print(f"   ⚠️ CLOSE: {elapsed:.1f}s (target: 30s, over by {elapsed-30:.1f}s)")
                return output_path, elapsed, False

        except Exception as e:
            print(f"   ❌ Extreme processing failed: {str(e)}")
            return None, -1, False

def remove_background_extreme_speed(input_path, output_path=None, max_size=800):
    """
    Convenience function for extreme-speed background removal
    Targeting <30 seconds at any cost
    """
    print("⚡ BACKGROUND REMOVER V1.1 EXTREME SPEED")
    print("    Targeting: <30 seconds, minimal quality compromise")
    print("=" * 70)

    remover = BackgroundRemoverV11Extreme()
    result_path, processing_time, success = remover.remove_background(
        input_path, output_path, max_size
    )

    if result_path:
        # Calculate file sizes
        input_size = os.path.getsize(input_path) / (1024 * 1024)
        output_size = os.path.getsize(result_path) / (1024 * 1024)

        print("=" * 70)
        print("⚡ EXTREME SPEED RESULTS:")
        print(f"   ⏱️ Processing Time: {processing_time:.1f}s")
        print(f"   🎯 30s Target: {'🏆 MET!' if success else '⚠️ MISSED'}")
        print(f"   📁 Input Size: {input_size:.2f} MB")
        print(f"   📁 Output Size: {output_size:.2f} MB")
        print(f"   📏 Size Ratio: {output_size/input_size:.1f}x")
        print(f"   💾 Output: {result_path}")

        if success:
            print(f"\n🎉 EXTREME SUCCESS: Sub-30 second processing achieved!")
        else:
            print(f"\n🔧 OPTIMIZATION NEEDED: {processing_time-30:.1f}s over target")

        return result_path
    else:
        print("❌ Extreme processing failed!")
        return None

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bg_remove_v1_1_extreme.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)

    result = remove_background_extreme_speed(input_file)

    if result:
        print(f"\n🎉 Success! Output saved to: {result}")
    else:
        print("\n💥 Failed to process image!")
        sys.exit(1)
