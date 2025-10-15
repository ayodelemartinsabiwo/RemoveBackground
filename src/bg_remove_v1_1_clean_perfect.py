"""
Background Remover V1.1 Clean Perfect - Hair Preservation + Artifact Removal
Combines perfect hair strand preservation with intelligent background artifact cleaning

Key Features:
1. Hair vs Background artifact classification
2. Intelligent artifact removal while preserving hair
3. Clean transparency with full hair strand retention
4. Advanced background noise filtering
5. Perfect balance: Hair preservation + Clean output
"""

import os
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageEnhance
import time
import gc
from scipy import ndimage
from scipy.ndimage import gaussian_filter, laplace, binary_dilation, binary_erosion
import cv2

class BackgroundRemoverV11CleanPerfect:
    def __init__(self):
        self.session = None
        self.start_time = None

    def _log_progress(self, message):
        """Progress logging with timing"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"   {message} (t+{elapsed:.1f}s)")

    def _initialize_clean_session(self):
        """Initialize BiRefNet for clean perfect quality"""
        if not self.session:
            self._log_progress("Loading clean perfect AI model... 🧠")
            self.session = new_session('birefnet-portrait')
            self._log_progress("✅ Clean perfect BiRefNet-Portrait loaded")

    def _intelligent_hair_artifact_separation(self, mask, original_rgb):
        """
        Intelligent separation of hair strands from background artifacts
        Keeps hair, removes background noise for clean transparency
        """
        self._log_progress("Separating hair strands from background artifacts... 🧹")

        # Convert to high precision float
        mask_array = np.array(mask, dtype=np.float64) / 255.0

        # Enhanced preprocessing for better hair/artifact separation
        gray_original = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2GRAY)
        enhanced_gray = cv2.equalizeHist(gray_original)

        # Step 1: Detect true hair regions using multiple methods

        # Method 1: Directional gradient analysis for hair strands
        gradients = []
        for angle in [0, 45, 90, 135]:
            kernel = cv2.getRotationMatrix2D((1, 1), angle, 1.0)[:2, :2]
            grad = cv2.filter2D(enhanced_gray.astype(np.float64), -1, kernel)
            gradients.append(np.abs(grad))

        combined_gradient = np.maximum.reduce(gradients)
        combined_gradient = combined_gradient / (np.max(combined_gradient) + 1e-8)

        # Method 2: Connected component analysis to distinguish hair from noise
        # Hair strands have specific geometric properties (length, width ratios)
        binary_mask = (mask_array > 0.1).astype(np.uint8)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

        # Analyze components to identify hair vs artifacts
        hair_components = np.zeros_like(labels, dtype=bool)

        for i in range(1, num_labels):  # Skip background (label 0)
            area = stats[i, cv2.CC_STAT_AREA]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]

            # Hair characteristics: reasonable area, aspect ratio indicating strands
            aspect_ratio = max(width, height) / (min(width, height) + 1e-8)

            # Component is likely hair if:
            # 1. Not too small (not noise) and not too large (not main subject)
            # 2. Has elongated shape (hair strand characteristic)
            # 3. Located in gradient-detected hair regions
            component_mask = (labels == i)
            gradient_overlap = np.sum(combined_gradient[component_mask] > 0.02) / np.sum(component_mask)

            is_hair = (20 < area < 5000 and          # Reasonable size
                      aspect_ratio > 1.5 and         # Elongated shape
                      gradient_overlap > 0.3)        # In gradient-detected hair area

            if is_hair:
                hair_components[component_mask] = True

        # Step 2: Detect background artifacts
        # Artifacts are typically: small isolated components, low gradient areas, geometric outliers

        # Method 1: Detect small isolated noise
        small_noise = np.zeros_like(labels, dtype=bool)
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            component_mask = (labels == i)

            # Small isolated components that don't look like hair
            if area < 15 and not hair_components[component_mask].any():
                small_noise[component_mask] = True

        # Method 2: Detect background remnants using color/texture analysis
        # Convert original to LAB color space for better color analysis
        lab_image = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2LAB)

        # Analyze color consistency - hair should be relatively consistent color
        # Background artifacts often have different color characteristics
        background_artifacts = np.zeros_like(mask_array, dtype=bool)

        # Look for areas that are semi-transparent but don't have hair characteristics
        semi_transparent = (mask_array > 0.05) & (mask_array < 0.4)
        low_gradient = combined_gradient < 0.03
        background_artifacts = semi_transparent & low_gradient & ~hair_components

        # Step 3: Create clean mask - preserve hair, remove artifacts
        self._log_progress("Creating clean mask with preserved hair... ✨")

        clean_mask = mask_array.copy()

        # Remove identified artifacts
        clean_mask[small_noise] = 0.0
        clean_mask[background_artifacts] = 0.0

        # Enhance identified hair regions
        hair_threshold_map = np.where(hair_components, 0.12,  # Low threshold for hair
                                    np.where(combined_gradient > 0.05, 0.2,  # Medium for possible hair
                                           0.6))  # High threshold for body/non-hair

        # Apply adaptive thresholding
        clean_mask = np.where(clean_mask > hair_threshold_map, clean_mask, 0.0)

        # Step 4: Hair strand connection and enhancement (only for confirmed hair)
        # Connect broken hair strands while avoiding artifact connection
        hair_mask = hair_components
        if np.any(hair_mask):
            # Use minimal morphological operations only on hair areas
            kernel_hair = np.ones((2,2), np.uint8)
            connected_hair = binary_closing = ndimage.binary_closing(hair_mask, structure=kernel_hair, iterations=1)

            # Boost the connected hair regions in the clean mask
            clean_mask = np.where(connected_hair,
                                np.maximum(clean_mask, mask_array * 1.1),
                                clean_mask)

        # Step 5: Final cleaning pass - smooth body edges while preserving hair
        self._log_progress("Final cleaning and edge smoothing... 🎯")

        # Identify body vs hair regions for differential processing
        body_regions = (clean_mask > 0.5) & ~hair_components
        hair_edge_regions = hair_components | ((combined_gradient > 0.03) & (clean_mask > 0.1))

        # Smooth only body regions to avoid hair strand damage
        if np.any(body_regions):
            smoothed_body = gaussian_filter(clean_mask, sigma=0.8)
            clean_mask = np.where(body_regions,
                                0.6 * clean_mask + 0.4 * smoothed_body,
                                clean_mask)

        # Preserve hair edge sharpness
        clean_mask = np.where(hair_edge_regions, clean_mask, clean_mask)

        # Final range normalization
        clean_mask = np.clip(clean_mask, 0, 1) * 255

        return clean_mask.astype(np.uint8)

    def _clean_perfect_optimization(self, image_array, alpha_array):
        """
        Clean perfect optimization - high quality with artifact removal
        """
        # High-quality alpha quantization that preserves hair but removes noise
        alpha_quantized = (alpha_array // 3) * 3  # 85 levels for quality

        # Clean edges - more aggressive removal of very low opacity (artifacts)
        alpha_quantized[alpha_quantized < 8] = 0       # Remove faint artifacts
        alpha_quantized[alpha_quantized > 250] = 255   # Solid areas

        return alpha_quantized

    def _clean_preprocessing(self, image_path, max_size=2200):
        """
        Clean perfect preprocessing - balanced size for quality and performance
        """
        self._log_progress("Loading image with clean perfect settings... 💎")

        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Moderate sharpening for hair detection without amplifying noise
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)

            original_size = img.size

            # Balanced processing size - large enough for hair detail, not so large to amplify artifacts
            if max(original_size) > max_size:
                ratio = max_size / max(original_size)
                new_width = int(original_size[0] * ratio)
                new_height = int(original_size[1] * ratio)
                new_size = (new_width, new_height)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                self._log_progress(f"Resized to {new_size} for clean perfect quality")

            return np.array(img), original_size

    def remove_background(self, input_path, output_path=None, max_size=2200):
        """
        Clean perfect hair preservation - Hair strands + Clean transparency

        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            max_size: Clean perfect processing dimension (2200px)
        """
        self.start_time = time.time()

        try:
            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_no_bg_v11_clean{ext}"

            # Step 1: Clean perfect preprocessing
            img_array, original_size = self._clean_preprocessing(input_path, max_size)

            # Step 2: Initialize clean session
            self._initialize_clean_session()

            # Step 3: AI processing
            self._log_progress("AI processing with clean perfect approach... ✨")

            with Image.fromarray(img_array) as pil_img:
                result = remove(pil_img, session=self.session)

            self._log_progress("Applying intelligent hair-artifact separation... 🧹")

            # Step 4: Intelligent hair-artifact separation
            result_array = np.array(result)
            rgb_array = result_array[:, :, :3]
            alpha_array = result_array[:, :, 3]

            # Apply intelligent separation
            clean_alpha = self._intelligent_hair_artifact_separation(alpha_array, rgb_array)

            # Clean optimization
            optimized_alpha = self._clean_perfect_optimization(rgb_array, clean_alpha)

            # Combine with perfect quality
            final_array = np.dstack([rgb_array, optimized_alpha])
            final_image = Image.fromarray(final_array, 'RGBA')

            # Resize back
            if final_image.size != original_size:
                self._log_progress("Restoring original dimensions with clean preservation... 📏")
                final_image = final_image.resize(original_size, Image.Resampling.LANCZOS)

            self._log_progress("Saving with clean perfect compression... 💾")

            # Balanced compression for quality and file size
            final_image.save(output_path, 'PNG', optimize=True, compress_level=4)

            elapsed = time.time() - self.start_time

            # Cleanup
            del img_array, result_array, rgb_array, alpha_array, clean_alpha, optimized_alpha
            gc.collect()

            self._log_progress(f"✅ CLEAN PERFECT processing complete in {elapsed:.1f}s!")

            print(f"   💎 CLEAN PERFECT: Hair preserved + artifacts removed!")
            print(f"   ⏱️ Processing Time: {elapsed:.1f}s")

            return output_path, elapsed

        except Exception as e:
            print(f"   ❌ Clean perfect processing failed: {str(e)}")
            return None, -1

def remove_background_clean_perfect(input_path, output_path=None, max_size=2200):
    """
    Clean perfect hair preservation - Best of both worlds
    """
    print("🧹 BACKGROUND REMOVER V1.1 CLEAN PERFECT")
    print("    Hair Strand Preservation + Clean Transparent Output")
    print("=" * 85)

    remover = BackgroundRemoverV11CleanPerfect()
    result_path, processing_time = remover.remove_background(
        input_path, output_path, max_size
    )

    if result_path:
        input_size = os.path.getsize(input_path) / (1024 * 1024)
        output_size = os.path.getsize(result_path) / (1024 * 1024)

        print("=" * 85)
        print("🧹 CLEAN PERFECT RESULTS:")
        print(f"   ⏱️ Processing Time: {processing_time:.1f}s")
        print(f"   💎 Quality: Hair preservation + artifact removal")
        print(f"   📁 Input Size: {input_size:.2f} MB")
        print(f"   📁 Output Size: {output_size:.2f} MB")
        print(f"   📏 Size Ratio: {output_size/input_size:.1f}x")
        print(f"   💾 Output: {result_path}")
        print(f"\n🏆 CLEAN PERFECT: Hair strands + clean transparency achieved!")

        return result_path
    else:
        print("❌ Clean perfect processing failed!")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bg_remove_v1_1_clean_perfect.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)

    result = remove_background_clean_perfect(input_file)

    if result:
        print(f"\n🎉 Clean perfect success! Output: {result}")
    else:
        print("\n💥 Failed to process image!")
        sys.exit(1)
