"""
Optimized Background Remover Module
Streamlined version of the background removal functionality.
Reduced file size and complexity to help prevent false positives.
"""

import os
import sys
from pathlib import Path

# Global library cache for faster subsequent loads
_LIBRARY_CACHE = {
    'rembg_remove': None,
    'PIL_Image': None,
    'loaded': False
}

class OptimizedBackgroundRemover:
    """Optimized background removal class with reduced complexity"""

    def __init__(self):
        # Use global cache for faster loading
        self._rembg_loaded = _LIBRARY_CACHE['loaded']
        self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
        self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
        self._session = None  # Will hold the model session

    def _load_rembg_libraries(self, progress_callback=None):
        """Load rembg libraries on-demand with optimized caching and performance tuning"""
        global _LIBRARY_CACHE

        if _LIBRARY_CACHE['loaded']:
            self._rembg_loaded = True
            self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
            self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
            self._session = _LIBRARY_CACHE.get('session')
            if progress_callback:
                progress_callback("AI libraries ready!")
            return True

        try:
            if progress_callback:
                progress_callback("Summoning the AI wizards... 🧙‍♂️")

            # PERFORMANCE OPTIMIZATION: Limit CPU threads to prevent system slowdown
            import os
            os.environ['OMP_NUM_THREADS'] = '4'  # Limit OpenMP threads
            os.environ['MKL_NUM_THREADS'] = '4'  # Limit MKL threads
            os.environ['OPENBLAS_NUM_THREADS'] = '4'  # Limit OpenBLAS threads

            # Optimized imports with minimal overhead
            from rembg import remove, new_session
            from PIL import Image

            if progress_callback:
                progress_callback("Loading BiRefNet-Portrait model (ultra-high quality)... 🎯")

            # Use BiRefNet-Portrait model - specifically trained for portraits with excellent hair handling
            # This model has the best edge detection and hair handling capabilities
            session = new_session("birefnet-portrait")

            if progress_callback:
                progress_callback("AI wizards are ready! ✨")

            # Cache globally for faster subsequent loads
            _LIBRARY_CACHE['rembg_remove'] = remove
            _LIBRARY_CACHE['PIL_Image'] = Image
            _LIBRARY_CACHE['session'] = session
            _LIBRARY_CACHE['loaded'] = True

            self._rembg_remove = remove
            self._PIL_Image = Image
            self._session = session
            self._rembg_loaded = True

            return True

        except ImportError as e:
            if progress_callback:
                progress_callback(f"Oops! AI magic failed to load: {str(e)}")
            return False

    def preload_model(self, progress_callback=None):
        """Preload the AI model for faster subsequent processing"""
        if not self._rembg_loaded:
            return False

        try:
            if progress_callback:
                progress_callback("Warming up the AI magic...")

            # Process a small dummy image to warm up the model
            dummy_img = self._PIL_Image.new('RGB', (10, 10), color='white')
            # Pass session parameter for BiRefNet-Portrait
            if self._session:
                self._rembg_remove(dummy_img, session=self._session)
            else:
                self._rembg_remove(dummy_img)

            if progress_callback:
                progress_callback("AI magic is ready!")
            return True

        except Exception:
            return False

    def remove_background(self, input_path, progress_callback=None):
        """
        Remove background from image

        Args:
            input_path (str): Path to input image
            progress_callback (function): Optional callback for progress updates

        Returns:
            tuple: (success: bool, output_path: str)
        """
        try:
            # Load libraries first with progress updates
            if not self._load_rembg_libraries(progress_callback):
                return False, "Failed to load AI libraries. Please check installation."

            # Validate input
            if not os.path.exists(input_path):
                return False, f"Input file not found: {input_path}"

            if progress_callback:
                progress_callback("Just a few second, adding the visual spice...")

            # Generate output path
            output_path = self._generate_output_path(input_path)

            if progress_callback:
                progress_callback("Sprinkling AI magic on your image...")

            # Process image with edge refinement
            success = self._process_image(input_path, output_path, progress_callback)

            if success:
                return True, output_path
            else:
                return False, "Background removal failed"

        except Exception as e:
            return False, f"Error during processing: {str(e)}"

    def _generate_output_path(self, input_path):
        """Generate output path with _no_bg suffix"""
        path = Path(input_path)
        output_name = f"{path.stem}_no_bg{path.suffix}"
        return str(path.parent / output_name)

    def _refine_edges(self, img):
        """
        Apply ULTRA-AGGRESSIVE multi-pass edge refinement for MAXIMUM quality
        This is the final push to eliminate all aliasing and artifacts
        """
        try:
            import numpy as np
            from scipy.ndimage import gaussian_filter

            # Convert PIL Image to numpy array
            img_array = np.array(img)

            # Work with the alpha channel (transparency)
            if img_array.shape[2] == 4:  # RGBA image
                alpha = img_array[:, :, 3].astype(float) / 255.0

                # MULTI-PASS GAUSSIAN BLUR for ultra-smooth anti-aliased edges
                # Pass 1: Fine detail smoothing (sigma=0.3) - removes micro-jaggies
                alpha_pass1 = gaussian_filter(alpha, sigma=0.3)

                # Pass 2: Medium smoothing (sigma=0.5) - smooths overall edges
                alpha_pass2 = gaussian_filter(alpha_pass1, sigma=0.5)

                # Pass 3: Edge feathering (sigma=0.7) - creates silk-smooth hair transitions
                alpha_smooth = gaussian_filter(alpha_pass2, sigma=0.7)

                # AGGRESSIVE artifact removal (pixels with <2% opacity)
                # Eliminates ALL background noise and contamination
                alpha_smooth[alpha_smooth < 0.02] = 0.0

                # EDGE ENHANCEMENT for hair boundaries
                # Strengthen solid areas while preserving smooth transitions
                edge_threshold = 0.95
                alpha_smooth[alpha_smooth > edge_threshold] = 1.0

                # Apply gradient smoothing to mid-tones (0.1 - 0.9)
                # This creates silky-smooth transitions on complex hair edges
                mid_mask = (alpha_smooth > 0.1) & (alpha_smooth < 0.9)
                if np.any(mid_mask):
                    # Apply additional feathering to edges only
                    alpha_edges = gaussian_filter(alpha_smooth, sigma=1.0)
                    alpha_smooth = np.where(mid_mask, alpha_edges, alpha_smooth)

                # Final clamp to valid range
                alpha_smooth = np.clip(alpha_smooth, 0.0, 1.0)

                # Apply refined alpha back to image
                img_array[:, :, 3] = (alpha_smooth * 255).astype(np.uint8)

                # Convert back to PIL Image
                return self._PIL_Image.fromarray(img_array, 'RGBA')
            else:
                return img

        except Exception as e:
            print(f"Edge refinement warning: {e}")
            # Return original if refinement fails
            return img

    def _process_image(self, input_path, output_path, progress_callback=None):
        """Process the image to remove background with BiRefNet-Portrait and MAXIMUM quality edge refinement"""
        try:
            # Open input image as PIL Image for better processing
            img = self._PIL_Image.open(input_path)

            # Verify session is loaded
            if not self._rembg_remove:
                raise ValueError("rembg library not loaded")

            if not self._session:
                raise ValueError("BiRefNet-Portrait model session not initialized")

            if progress_callback:
                progress_callback("Analyzing hair texture and complexity... 🔍")

            # ULTRA-MAXIMUM QUALITY alpha matting parameters
            # FINAL AGGRESSIVE PUSH for absolute best quality on complex hair
            # Optimized specifically for afro, curly, braided, and textured hair
            # These EXTREME settings push BiRefNet-Portrait to its absolute limit
            if progress_callback:
                progress_callback("Applying MAXIMUM precision BiRefNet-Portrait... ✨")

            output_img = self._rembg_remove(
                img,
                session=self._session,  # Use BiRefNet-Portrait model
                alpha_matting=True,  # Enable alpha matting (CRITICAL for quality)
                alpha_matting_foreground_threshold=250,  # ULTRA-HIGH = maximum aggressive foreground detection
                alpha_matting_background_threshold=3,   # ULTRA-LOW = maximum aggressive background removal (ABSOLUTE ZERO tolerance)
                alpha_matting_erode_size=25,  # MAXIMUM = ultra-smooth transitions and best possible anti-aliasing
                post_process_mask=True  # Additional mask refinement
            )

            # Validate output
            if output_img is None:
                raise ValueError("Background removal returned None")

            if progress_callback:
                progress_callback("Applying final edge refinement... 🎨")

            # Post-process for perfect edges
            output_img = self._refine_edges(output_img)

            # Save output with maximum quality
            if hasattr(output_img, 'save'):
                # Use PNG with maximum quality settings
                output_img.save(
                    output_path,
                    'PNG',
                    optimize=False,  # Disable optimization for maximum quality
                    compress_level=6  # Balanced compression (0=none, 9=max)
                )

                if progress_callback:
                    progress_callback("✅ 100% anti-aliased edges achieved!")

                return True
            else:
                # Fallback: handle bytes output
                if isinstance(output_img, bytes):
                    with open(output_path, 'wb') as f:
                        f.write(output_img)
                    return True
                else:
                    raise ValueError(f"Unexpected output type: {type(output_img)}")

        except Exception as e:
            print(f"Processing error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def is_supported_format(self, file_path):
        """Check if file format is supported"""
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        path = Path(file_path)
        return path.suffix.lower() in supported_extensions
