"""
V1.1 SPEED OPTIMIZED: SMART & FAST
Based on benchmark results - V1.1 was too slow due to over-processing
New approach: Strategic optimizations that improve speed AND quality

Key Changes:
1. Reduce expensive operations (fewer gaussian filters)
2. Smart algorithm selection (fast paths for simple cases)
3. Optimized file compression only
4. Memory management without performance penalty
5. Focus on user's main concerns: speed + file size + hair quality
"""

import os
import sys
import gc
import time
from pathlib import Path

_LIBRARY_CACHE = {
    'rembg_remove': None,
    'PIL_Image': None,
    'numpy': None,
    'scipy_ndimage': None,
    'loaded': False,
    'session': None
}

class OptimizedBackgroundRemoverV11Fast:
    """
    V1.1 SPEED OPTIMIZED: Focus on user priorities

    TARGETS:
    - Speed: <30 seconds (vs current 67s)
    - File Size: <2MB (vs current 0.89MB - maintain)
    - Hair Quality: Enhanced artifact removal
    - Memory: Efficient management
    - No PC lag: Smart resource usage
    """

    def __init__(self):
        self._rembg_loaded = _LIBRARY_CACHE['loaded']
        self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
        self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
        self._numpy = _LIBRARY_CACHE['numpy']
        self._scipy_ndimage = _LIBRARY_CACHE['scipy_ndimage']
        self._session = None

    def _load_rembg_libraries(self, progress_callback=None):
        """Load libraries efficiently"""
        global _LIBRARY_CACHE

        if _LIBRARY_CACHE['loaded']:
            self._rembg_loaded = True
            self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
            self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
            self._numpy = _LIBRARY_CACHE['numpy']
            self._scipy_ndimage = _LIBRARY_CACHE['scipy_ndimage']
            self._session = _LIBRARY_CACHE.get('session')
            if progress_callback:
                progress_callback("AI libraries ready!")
            return True

        try:
            if progress_callback:
                progress_callback("Summoning the AI wizards... 🧙‍♂️")

            # Optimize threading - use fewer threads to prevent lag
            os.environ['OMP_NUM_THREADS'] = '3'  # Reduced from 4
            os.environ['MKL_NUM_THREADS'] = '3'
            os.environ['OPENBLAS_NUM_THREADS'] = '3'

            from rembg import remove, new_session
            from PIL import Image
            import numpy as np
            from scipy import ndimage

            if progress_callback:
                progress_callback("Waking up the pixel wizards... 🎯")

            session = new_session("birefnet-portrait")

            if progress_callback:
                progress_callback("AI wizards are ready! ✨")

            _LIBRARY_CACHE['rembg_remove'] = remove
            _LIBRARY_CACHE['PIL_Image'] = Image
            _LIBRARY_CACHE['numpy'] = np
            _LIBRARY_CACHE['scipy_ndimage'] = ndimage
            _LIBRARY_CACHE['session'] = session
            _LIBRARY_CACHE['loaded'] = True

            self._rembg_remove = remove
            self._PIL_Image = Image
            self._numpy = np
            self._scipy_ndimage = ndimage
            self._session = session
            self._rembg_loaded = True

            return True

        except ImportError as e:
            if progress_callback:
                progress_callback(f"Oops! AI magic failed to load: {str(e)}")
            return False

    def preload_model(self, progress_callback=None):
        """Preload model"""
        try:
            success = self._load_rembg_libraries(progress_callback)
            if success and progress_callback:
                progress_callback("AI magic is ready!")
            return success
        except Exception:
            return False

    def _smart_hair_enhancement(self, img_array, progress_callback=None):
        """
        SMART HAIR ENHANCEMENT - Fast but effective
        Focus on user's main concern: hair artifacts like Freepik
        """
        if progress_callback:
            progress_callback("Enhancing hair with smart algorithms... ✨")

        np = self._numpy
        ndimage = self._scipy_ndimage

        # Extract alpha channel
        alpha = img_array[:, :, 3].astype(np.float32) / 255.0

        # FAST hair artifact detection
        # Use edge detection to find hair regions
        grad_x = ndimage.sobel(alpha, axis=1)
        grad_y = ndimage.sobel(alpha, axis=0)
        gradient_mag = np.sqrt(grad_x**2 + grad_y**2)

        # Identify hair vs non-hair areas quickly
        hair_threshold = np.percentile(gradient_mag[gradient_mag > 0], 70)
        hair_mask = gradient_mag > hair_threshold

        # SMART cleanup - only process hair areas
        # Binary operations for speed
        alpha_binary = alpha > 0.1

        # Small morphological operations (fast)
        kernel = np.ones((3, 3))
        cleaned_binary = ndimage.binary_opening(alpha_binary, kernel)
        cleaned_binary = ndimage.binary_closing(cleaned_binary, kernel)

        # Apply enhanced cleanup only to hair areas
        enhanced_alpha = np.where(hair_mask,
                                 np.where(cleaned_binary, alpha, alpha * 0.2),
                                 np.where(cleaned_binary, alpha, 0))

        # Single light smoothing pass (fast)
        enhanced_alpha = ndimage.gaussian_filter(enhanced_alpha, sigma=0.4)

        # Apply back to image
        img_array[:, :, 3] = (enhanced_alpha * 255).astype(np.uint8)

        return img_array

    def _fast_file_optimization(self, img, progress_callback=None):
        """
        FAST FILE SIZE OPTIMIZATION
        Target: Reduce 10MB→2MB inflation without quality loss
        """
        if progress_callback:
            progress_callback("Optimizing file size... ⚡")

        # Simple but effective alpha optimization
        img_array = self._numpy.array(img)
        alpha = img_array[:, :, 3]

        # Quick alpha cleanup (removes file size bloat)
        # Convert low values to 0, high values to 255
        alpha_clean = self._numpy.where(alpha < 8, 0, alpha)
        alpha_clean = self._numpy.where(alpha_clean > 247, 255, alpha_clean)

        # Quantize mid-range values (reduces precision = smaller file)
        mid_mask = (alpha_clean >= 8) & (alpha_clean <= 247)
        alpha_clean[mid_mask] = (alpha_clean[mid_mask] // 16) * 16

        img_array[:, :, 3] = alpha_clean

        return self._PIL_Image.fromarray(img_array, 'RGBA')

    def _memory_cleanup_light(self):
        """Light memory cleanup that doesn't slow down processing"""
        gc.collect()

    def remove_background(self, input_path, progress_callback=None):
        """Remove background with V1.1 speed-optimized processing"""
        start_time = time.time()

        try:
            if not self._load_rembg_libraries(progress_callback):
                return False, "Failed to load AI libraries"

            if not os.path.exists(input_path):
                return False, f"Input file not found: {input_path}"

            if progress_callback:
                progress_callback("Getting ready for the magic show... 🎪")

            output_path = self._generate_output_path(input_path)

            if progress_callback:
                progress_callback("Sprinkling AI pixie dust... ✨")

            success = self._process_image_v11_fast(input_path, output_path, progress_callback)

            if success:
                elapsed_time = time.time() - start_time
                if progress_callback:
                    progress_callback(f"✅ V1.1 SPEED processing complete in {elapsed_time:.1f}s!")
                return True, output_path
            else:
                return False, "Background removal failed"

        except Exception as e:
            return False, f"Error during processing: {str(e)}"
        finally:
            # Light cleanup only
            self._memory_cleanup_light()

    def _generate_output_path(self, input_path):
        """Generate output path with V1.1 suffix"""
        path = Path(input_path)
        return str(path.parent / f"{path.stem}_no_bg_v11_fast{path.suffix}")

    def _process_image_v11_fast(self, input_path, output_path, progress_callback):
        """Process image with speed-optimized V1.1"""
        try:
            # Load image
            img = self._PIL_Image.open(input_path)

            if progress_callback:
                progress_callback("Teaching pixels to let go of the background... 🎨")

            # BiRefNet processing with optimized settings
            if not self._session:
                raise ValueError("Model not initialized")

            # Use slightly faster BiRefNet settings
            output_img = self._rembg_remove(
                img,
                session=self._session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=248,  # Slightly faster
                alpha_matting_background_threshold=6,
                alpha_matting_erode_size=8,              # Reduced for speed
                post_process_mask=False                   # Disable for speed
            )

            if output_img is None:
                raise ValueError("Background removal returned None")

            if progress_callback:
                progress_callback("Finding the fuzzy edges... 🔍")

            # Convert to numpy for processing
            img_array = self._numpy.array(output_img)

            if progress_callback:
                progress_callback("Applying smart hair enhancement... 🧹")

            # Smart hair enhancement (fast but effective)
            img_array = self._smart_hair_enhancement(img_array, progress_callback)

            if progress_callback:
                progress_callback("Hugging the edges for that perfect look... 🤗")

            # Light edge smoothing (much faster than V12)
            alpha = img_array[:, :, 3].astype(self._numpy.float32) / 255.0

            # Single quick smoothing pass
            alpha_smooth = self._scipy_ndimage.gaussian_filter(alpha, sigma=0.3)

            # Conservative blend (faster than multiple passes)
            alpha_final = 0.8 * alpha + 0.2 * alpha_smooth

            img_array[:, :, 3] = (alpha_final * 255).astype(self._numpy.uint8)

            # Convert back to PIL
            final_img = self._PIL_Image.fromarray(img_array, 'RGBA')

            if progress_callback:
                progress_callback("Optimizing file size for lightning save... ⚡")

            # Fast file optimization
            optimized_img = self._fast_file_optimization(final_img, progress_callback)

            # Save with good compression settings
            optimized_img.save(output_path, 'PNG', optimize=True, compress_level=6)

            return True

        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return False


# For compatibility and easy switching
OptimizedBackgroundRemoverV11 = OptimizedBackgroundRemoverV11Fast
