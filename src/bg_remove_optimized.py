"""
Optimized Background Remover Module
Streamlined version of the background removal functionality.
Reduced file size and complexity to help prevent false positives.
"""

import os
import sys
from pathlib import Path

# Import rembg with proper error handling for PyInstaller
try:
    import rembg
    from rembg import remove as rembg_remove
    from PIL import Image
    REMBG_AVAILABLE = True
except ImportError as e:
    rembg_remove = None
    REMBG_AVAILABLE = False

class OptimizedBackgroundRemover:
    """Optimized background removal class with reduced complexity"""

    def __init__(self):
        if not REMBG_AVAILABLE:
            raise ImportError("rembg library not available. Please install: pip install rembg")

    def remove_background(self, input_path):
        """
        Remove background from image

        Args:
            input_path (str): Path to input image

        Returns:
            tuple: (success: bool, output_path: str)
        """
        try:
            # Validate input
            if not os.path.exists(input_path):
                return False, f"Input file not found: {input_path}"

            # Generate output path
            output_path = self._generate_output_path(input_path)

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

            # Remove background
            if rembg_remove:
                output_data = rembg_remove(input_data)
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
