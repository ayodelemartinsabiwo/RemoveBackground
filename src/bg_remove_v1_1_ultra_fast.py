"""
Background Remover V1.1 Ultra Fast - Speed-Optimized Version
Targets: <30s processing, file size optimization, minimal hair artifacts

This version strips down to essential optimizations to meet the 30-second target
while still providing better hair processing than V12.
"""

import os
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter
import time
import gc
from scipy import ndimage

class BackgroundRemoverV11UltraFast:
    def __init__(self):
        self.session = None
        self.start_time = None

    def _log_progress(self, message):
        """Quick progress logging"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"   {message} (t+{elapsed:.1f}s)")

    def _initialize_session(self):
        """Initialize BiRefNet session with minimal overhead"""
        if not self.session:
            self._log_progress("Loading ultra-fast AI model... 🚀")
            # Use BiRefNet with fastest settings
            self.session = new_session('birefnet-portrait')

    def _ultra_fast_hair_fix(self, mask, original_image):
        """
        Ultra-fast hair enhancement targeting only major artifacts
        Uses single-pass morphological operations
        """
        # Convert to binary for fastest processing
        binary_mask = (mask > 128).astype(np.uint8) * 255

        # Single morphological operation to clean hair artifacts
        # Use small kernel for speed
        kernel = np.ones((3,3), np.uint8)

        # Single erosion-dilation cycle to remove small artifacts
        cleaned = ndimage.binary_erosion(binary_mask > 0, structure=kernel)
        cleaned = ndimage.binary_dilation(cleaned, structure=kernel)

        return (cleaned * 255).astype(np.uint8)

    def _lightning_file_optimization(self, image_array, alpha_array):
        """
        Lightning-fast file size optimization
        Quantizes alpha channel aggressively for smaller files
        """
        # Quantize alpha to 16 levels instead of 256
        alpha_quantized = (alpha_array // 16) * 16

        # Ensure full transparency/opacity at extremes
        alpha_quantized[alpha_quantized < 32] = 0
        alpha_quantized[alpha_quantized > 224] = 255

        return alpha_quantized

    def remove_background(self, input_path, output_path=None, max_size=1600):
        """
        Ultra-fast background removal optimized for <30 second processing

        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            max_size: Max dimension for speed optimization
        """
        self.start_time = time.time()

        try:
            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_no_bg_v11_ultra{ext}"

            self._log_progress("Loading image for ultra-fast processing... ⚡")

            # Load and resize for speed
            with Image.open(input_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Aggressive resize for speed - prioritize <30s target
                original_size = img.size
                if max(original_size) > max_size:
                    ratio = max_size / max(original_size)
                    new_width = int(original_size[0] * ratio)
                    new_height = int(original_size[1] * ratio)
                    new_size = (new_width, new_height)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    self._log_progress(f"Resized to {new_size} for speed")

                img_array = np.array(img)

            self._log_progress("Initializing ultra-fast AI... 🎯")
            self._initialize_session()

            self._log_progress("AI magic in ultra-fast mode... ✨")

            # Use rembg with minimal post-processing for speed
            with Image.fromarray(img_array) as pil_img:
                # Direct rembg processing - no custom post-processing
                result = remove(pil_img, session=self.session)

            self._log_progress("Applying lightning-fast hair optimization... 🧹")

            # Convert result to arrays
            result_array = np.array(result)
            rgb_array = result_array[:, :, :3]
            alpha_array = result_array[:, :, 3]

            # Ultra-fast hair fix - single operation only
            enhanced_alpha = self._ultra_fast_hair_fix(alpha_array, rgb_array)

            # Lightning file optimization
            optimized_alpha = self._lightning_file_optimization(rgb_array, enhanced_alpha)

            # Combine and save
            final_array = np.dstack([rgb_array, optimized_alpha])
            final_image = Image.fromarray(final_array, 'RGBA')

            # Resize back to original if we resized
            if final_image.size != original_size:
                final_image = final_image.resize(original_size, Image.Resampling.LANCZOS)

            self._log_progress("Saving with ultra compression... 💾")

            # Save with maximum compression for file size
            final_image.save(output_path, 'PNG', optimize=True, compress_level=9)

            elapsed = time.time() - self.start_time

            # Quick memory cleanup
            del img_array, result_array, rgb_array, alpha_array, enhanced_alpha, optimized_alpha
            gc.collect()

            self._log_progress(f"✅ ULTRA FAST processing complete in {elapsed:.1f}s!")

            # Check if we met the 30-second target
            if elapsed <= 30:
                print(f"   🎯 SUCCESS: Met <30s target! ({elapsed:.1f}s)")
            else:
                print(f"   ⚠️ TIMEOUT: {elapsed:.1f}s exceeds 30s target")

            return output_path, elapsed

        except Exception as e:
            print(f"   ❌ Ultra-fast processing failed: {str(e)}")
            return None, -1

def remove_background_ultra_fast(input_path, output_path=None, max_size=1600):
    """
    Convenience function for ultra-fast background removal
    Optimized specifically for the <30 second target
    """
    print("🚀 BACKGROUND REMOVER V1.1 ULTRA FAST")
    print("    Targeting: <30 seconds, optimized hair processing")
    print("=" * 60)

    remover = BackgroundRemoverV11UltraFast()
    result_path, processing_time = remover.remove_background(
        input_path, output_path, max_size
    )

    if result_path:
        # Calculate file sizes
        input_size = os.path.getsize(input_path) / (1024 * 1024)
        output_size = os.path.getsize(result_path) / (1024 * 1024)

        print("=" * 60)
        print("📊 ULTRA FAST RESULTS:")
        print(f"   ⏱️ Processing Time: {processing_time:.1f}s")
        print(f"   🎯 Target Met: {'✅ YES' if processing_time <= 30 else '❌ NO'}")
        print(f"   📁 Input Size: {input_size:.2f} MB")
        print(f"   📁 Output Size: {output_size:.2f} MB")
        print(f"   📏 Size Ratio: {output_size/input_size:.1f}x")
        print(f"   💾 Output: {result_path}")

        return result_path
    else:
        print("❌ Ultra-fast processing failed!")
        return None

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bg_remove_v1_1_ultra_fast.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)

    result = remove_background_ultra_fast(input_file)

    if result:
        print(f"\n🎉 Success! Output saved to: {result}")
    else:
        print("\n💥 Failed to process image!")
        sys.exit(1)
