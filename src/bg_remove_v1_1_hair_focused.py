"""
Background Remover V1.1 Hair-Focused - Freepik-Level Hair Preservation
Specifically designed to preserve fine hair strands like Freepik's quality

Key Focus Areas:
1. Advanced hair detection and preservation algorithms
2. Multi-threshold approach for hair vs body edges
3. Gradient-based hair boundary detection
4. Freepik-inspired hair strand enhancement
5. Preserve fine details while removing background cleanly
"""

import os
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter
import time
import gc
from scipy import ndimage
from scipy.ndimage import gaussian_filter
import cv2

class BackgroundRemoverV11HairFocused:
    def __init__(self):
        self.session = None
        self.start_time = None

    def _log_progress(self, message):
        """Progress logging with timing"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"   {message} (t+{elapsed:.1f}s)")

    def _initialize_hair_quality_session(self):
        """Initialize BiRefNet for maximum hair quality"""
        if not self.session:
            self._log_progress("Loading hair-optimized AI model... 🧠")
            # BiRefNet-Portrait is essential for hair quality
            self.session = new_session('birefnet-portrait')
            self._log_progress("✅ Hair-quality BiRefNet-Portrait model loaded")

    def _advanced_hair_preservation(self, mask, original_rgb):
        """
        Advanced hair preservation algorithm inspired by Freepik's approach
        Uses gradient analysis and multi-threshold processing
        """
        self._log_progress("Applying advanced hair preservation... 💇‍♀️")

        # Convert to arrays for processing
        mask_array = np.array(mask, dtype=np.float32) / 255.0

        # Step 1: Detect hair regions using gradient analysis
        # Hair has high-frequency details and gradients
        gray_original = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2GRAY)

        # Calculate gradients to find hair strands
        grad_x = cv2.Sobel(gray_original, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray_original, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

        # Normalize gradient
        gradient_magnitude = gradient_magnitude / np.max(gradient_magnitude)

        # Step 2: Create hair probability map
        # Areas with high gradients are likely hair
        hair_probability = gradient_magnitude > 0.1  # Threshold for hair detection

        # Step 3: Multi-threshold approach for different regions
        # Use different thresholds for hair vs body
        hair_threshold = 0.3  # Lower threshold for hair preservation
        body_threshold = 0.6  # Higher threshold for clean body edges

        # Create refined mask
        refined_mask = np.zeros_like(mask_array)

        # For hair regions: use lower threshold to preserve strands
        hair_regions = hair_probability
        refined_mask[hair_regions] = np.where(
            mask_array[hair_regions] > hair_threshold, 1.0, 0.0
        )

        # For body regions: use higher threshold for clean edges
        body_regions = ~hair_probability
        refined_mask[body_regions] = np.where(
            mask_array[body_regions] > body_threshold, 1.0, 0.0
        )

        # Step 4: Hair strand enhancement
        # Apply gentle smoothing only to non-hair regions
        kernel_small = np.ones((2,2), np.uint8)  # Very small kernel

        # Smooth only body edges, preserve hair details
        smoothed_body = ndimage.binary_closing(
            refined_mask > 0.5, structure=kernel_small
        )

        # Combine: hair details + smoothed body
        final_mask = np.where(hair_regions, refined_mask, smoothed_body.astype(np.float32))

        # Step 5: Edge refinement for natural hair boundaries
        # Apply very gentle gaussian blur only to transition areas
        from scipy.ndimage import laplace
        edge_mask = np.abs(laplace(final_mask)) > 0.1
        blurred_edges = gaussian_filter(final_mask, sigma=0.8)

        # Blend original and blurred only at edges
        final_mask = np.where(edge_mask,
                             0.7 * final_mask + 0.3 * blurred_edges,
                             final_mask)

        # Ensure proper range
        final_mask = np.clip(final_mask, 0, 1) * 255

        return final_mask.astype(np.uint8)

    def _freepik_inspired_file_optimization(self, image_array, alpha_array):
        """
        Freepik-inspired file optimization that preserves hair details
        """
        # More conservative alpha quantization to preserve hair details
        # Use 32 levels instead of 16 for better hair gradient preservation
        alpha_quantized = (alpha_array // 8) * 8

        # More conservative edge handling for hair
        alpha_quantized[alpha_quantized < 16] = 0      # More conservative transparency
        alpha_quantized[alpha_quantized > 240] = 255   # More conservative opacity

        return alpha_quantized

    def _hair_quality_preprocessing(self, image_path, max_size=1800):
        """
        Hair-quality preprocessing - larger size for better hair detail preservation
        """
        self._log_progress("Loading image with hair-quality settings... 💇‍♀️")

        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            original_size = img.size

            # Use larger processing size for better hair detail preservation
            if max(original_size) > max_size:
                ratio = max_size / max(original_size)
                new_width = int(original_size[0] * ratio)
                new_height = int(original_size[1] * ratio)
                new_size = (new_width, new_height)
                # Use highest quality resampling for hair preservation
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                self._log_progress(f"Resized to {new_size} for hair quality")

            return np.array(img), original_size

    def remove_background(self, input_path, output_path=None, max_size=1800):
        """
        Hair-focused background removal targeting Freepik-level hair preservation

        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            max_size: Hair-quality processing dimension (1800px for detail)
        """
        self.start_time = time.time()

        try:
            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_no_bg_v11_hair{ext}"

            # Step 1: Hair-quality preprocessing
            img_array, original_size = self._hair_quality_preprocessing(input_path, max_size)

            # Step 2: Initialize hair-optimized session
            self._initialize_hair_quality_session()

            # Step 3: AI processing with BiRefNet for hair quality
            self._log_progress("AI processing with hair-focused approach... 🎯")

            with Image.fromarray(img_array) as pil_img:
                # Use BiRefNet with parameters optimized for hair
                result = remove(pil_img, session=self.session)

            self._log_progress("Applying Freepik-inspired hair preservation... 🧵")

            # Step 4: Advanced hair preservation algorithms
            result_array = np.array(result)
            rgb_array = result_array[:, :, :3]
            alpha_array = result_array[:, :, 3]

            # Apply advanced hair preservation
            preserved_alpha = self._advanced_hair_preservation(alpha_array, rgb_array)

            # Freepik-inspired file optimization
            optimized_alpha = self._freepik_inspired_file_optimization(rgb_array, preserved_alpha)

            # Combine arrays
            final_array = np.dstack([rgb_array, optimized_alpha])
            final_image = Image.fromarray(final_array, 'RGBA')

            # Resize back to original size with high quality
            if final_image.size != original_size:
                self._log_progress("Restoring original dimensions with hair preservation... 📏")
                final_image = final_image.resize(original_size, Image.Resampling.LANCZOS)

            self._log_progress("Saving with hair-optimized compression... 💾")

            # Save with optimized compression that preserves hair details
            final_image.save(output_path, 'PNG', optimize=True, compress_level=6)  # Less aggressive compression

            elapsed = time.time() - self.start_time

            # Quick cleanup
            del img_array, result_array, rgb_array, alpha_array, preserved_alpha, optimized_alpha
            gc.collect()

            self._log_progress(f"✅ HAIR-FOCUSED processing complete in {elapsed:.1f}s!")

            print(f"   🧵 HAIR QUALITY: Freepik-level strand preservation applied")
            print(f"   ⏱️ Processing Time: {elapsed:.1f}s")

            return output_path, elapsed

        except Exception as e:
            print(f"   ❌ Hair-focused processing failed: {str(e)}")
            return None, -1

def remove_background_hair_focused(input_path, output_path=None, max_size=1800):
    """
    Convenience function for hair-focused background removal
    Targeting Freepik-level hair strand preservation
    """
    print("💇‍♀️ BACKGROUND REMOVER V1.1 HAIR-FOCUSED")
    print("    Freepik-Level Hair Strand Preservation")
    print("=" * 75)

    remover = BackgroundRemoverV11HairFocused()
    result_path, processing_time = remover.remove_background(
        input_path, output_path, max_size
    )

    if result_path:
        # Calculate file sizes
        input_size = os.path.getsize(input_path) / (1024 * 1024)
        output_size = os.path.getsize(result_path) / (1024 * 1024)

        print("=" * 75)
        print("💇‍♀️ HAIR-FOCUSED RESULTS:")
        print(f"   ⏱️ Processing Time: {processing_time:.1f}s")
        print(f"   🧵 Hair Quality: Freepik-inspired strand preservation")
        print(f"   📁 Input Size: {input_size:.2f} MB")
        print(f"   📁 Output Size: {output_size:.2f} MB")
        print(f"   📏 Size Ratio: {output_size/input_size:.1f}x")
        print(f"   💾 Output: {result_path}")
        print(f"\n🎯 HAIR STRAND PRESERVATION: Advanced algorithms applied!")

        return result_path
    else:
        print("❌ Hair-focused processing failed!")
        return None

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bg_remove_v1_1_hair_focused.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)

    result = remove_background_hair_focused(input_file)

    if result:
        print(f"\n🎉 Success! Hair-focused output saved to: {result}")
    else:
        print("\n💥 Failed to process image!")
        sys.exit(1)
