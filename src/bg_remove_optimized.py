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

    def _load_rembg_libraries(self, progress_callback=None):
        """Load rembg libraries on-demand with optimized caching"""
        global _LIBRARY_CACHE

        if _LIBRARY_CACHE['loaded']:
            self._rembg_loaded = True
            self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
            self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
            if progress_callback:
                progress_callback("AI libraries ready!")
            return True

        try:
            if progress_callback:
                progress_callback("Summoning the AI wizards... 🧙‍♂️")

            # Optimized imports with minimal overhead
            from rembg import remove
            from PIL import Image

            if progress_callback:
                progress_callback("AI wizards are ready! ✨")

            # Cache globally for faster subsequent loads
            _LIBRARY_CACHE['rembg_remove'] = remove
            _LIBRARY_CACHE['PIL_Image'] = Image
            _LIBRARY_CACHE['loaded'] = True

            self._rembg_remove = remove
            self._PIL_Image = Image
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

            # Process image
            success = self._process_image(input_path, output_path)

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

    def _process_image(self, input_path, output_path):
        """Process the image to remove background"""
        try:
            # Open input image
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()

            # Remove background using loaded library
            if self._rembg_remove:
                output_data = self._rembg_remove(input_data)
            else:
                return False

            # Save output
            if isinstance(output_data, bytes):
                with open(output_path, 'wb') as output_file:
                    output_file.write(output_data)
            else:
                return False

            return True

        except Exception as e:
            print(f"Processing error: {e}")
            return False

    def is_supported_format(self, file_path):
        """Check if file format is supported"""
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        path = Path(file_path)
        return path.suffix.lower() in supported_extensions
