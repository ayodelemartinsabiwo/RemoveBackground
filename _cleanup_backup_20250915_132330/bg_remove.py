import os
from pathlib import Path
from typing import Union, Tuple
import io

# Import these at module level to avoid repeated imports
try:
    from rembg import remove
    from PIL import Image
except ImportError as e:
    print(f"Required libraries not found: {e}")
    raise

class BackgroundRemover:
    def __init__(self):
        pass

    def remove_background(self, input_path: Union[str, Path]) -> Tuple[bool, str]:
        """
        Remove background from image and save as transparent PNG

        Args:
            input_path (str): Path to input image

        Returns:
            tuple: (success: bool, output_path: str or error_message: str)
        """
        try:
            input_path = Path(input_path)

            # Validate input file
            if not input_path.exists():
                return False, f"Input file does not exist: {input_path}"

            # Generate output filename
            output_path = input_path.parent / f"{input_path.stem}_bg_removed.png"

            # Read input image
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()

            # Remove background - this returns bytes
            output_data = remove(input_data)

            # Write the output - rembg actually returns bytes, so this should work
            with open(output_path, 'wb') as output_file:
                if isinstance(output_data, bytes):
                    output_file.write(output_data)
                else:
                    # Handle edge case where it's not bytes
                    output_file.write(output_data)  # type: ignore

            return True, str(output_path)

        except Exception as e:
            return False, str(e)

    def remove_background_with_white_bg(self, input_path: Union[str, Path]) -> Tuple[bool, str]:
        """
        Remove background and replace with white background for JPG output

        Args:
            input_path (str): Path to input image

        Returns:
            tuple: (success: bool, output_path: str or error_message: str)
        """
        try:
            input_path = Path(input_path)

            # First remove background to get transparent image
            success, temp_output = self.remove_background(input_path)
            if not success:
                return False, temp_output

            # Load the transparent image
            transparent_img = Image.open(temp_output)

            # Create white background
            white_bg = Image.new('RGB', transparent_img.size, (255, 255, 255))

            # Paste transparent image onto white background
            if transparent_img.mode == 'RGBA':
                white_bg.paste(transparent_img, mask=transparent_img.split()[-1])
            else:
                white_bg.paste(transparent_img)

            # Save as JPG with white background
            output_path = input_path.parent / f"{input_path.stem}_bg_removed_white.jpg"
            white_bg.save(output_path, 'JPEG', quality=95)

            # Clean up temporary transparent PNG
            os.remove(temp_output)

            return True, str(output_path)

        except Exception as e:
            return False, str(e)
