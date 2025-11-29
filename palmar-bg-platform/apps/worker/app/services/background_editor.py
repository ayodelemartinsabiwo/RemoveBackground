"""
Background Editor Service
Handles background customization: solid colors, gradients, and textures
"""
from PIL import Image, ImageDraw
from typing import Tuple, List, Optional
import io
import numpy as np


class BackgroundEditorService:
    """Service for adding custom backgrounds to transparent images"""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def add_solid_background(
        self,
        image_bytes: bytes,
        hex_color: str = "#FFFFFF"
    ) -> bytes:
        """
        Add solid color background to transparent image

        Args:
            image_bytes: Image with transparent background
            hex_color: Background color in hex format (e.g., "#FF5733")

        Returns:
            Image bytes with solid background
        """
        try:
            # Load transparent image
            foreground = Image.open(io.BytesIO(image_bytes)).convert('RGBA')

            # Create solid background
            rgb_color = self.hex_to_rgb(hex_color)
            background = Image.new('RGBA', foreground.size, rgb_color + (255,))

            # Composite images
            result = Image.alpha_composite(background, foreground)

            # Convert to RGB (remove alpha)
            final = Image.new('RGB', result.size, (255, 255, 255))
            final.paste(result, mask=result.split()[3] if result.mode == 'RGBA' else None)

            # Save to bytes
            output_buffer = io.BytesIO()
            final.save(output_buffer, 'PNG', optimize=True)
            output_buffer.seek(0)

            print(f"✓ Added solid background: {hex_color}")
            return output_buffer.read()

        except Exception as e:
            print(f"✗ Solid background failed: {e}")
            return image_bytes

    def add_gradient_background(
        self,
        image_bytes: bytes,
        colors: List[str],
        angle: int = 0
    ) -> bytes:
        """
        Add gradient background to transparent image

        Args:
            image_bytes: Image with transparent background
            colors: List of hex colors for gradient (2-3 colors)
            angle: Gradient angle in degrees (0-360)

        Returns:
            Image bytes with gradient background
        """
        try:
            # Load transparent image
            foreground = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
            width, height = foreground.size

            # Create gradient background
            gradient = self._create_gradient(width, height, colors, angle)

            # Composite images
            result = Image.alpha_composite(gradient, foreground)

            # Convert to RGB
            final = Image.new('RGB', result.size, (255, 255, 255))
            final.paste(result, mask=result.split()[3] if result.mode == 'RGBA' else None)

            # Save to bytes
            output_buffer = io.BytesIO()
            final.save(output_buffer, 'PNG', optimize=True)
            output_buffer.seek(0)

            print(f"✓ Added gradient background: {colors} at {angle}°")
            return output_buffer.read()

        except Exception as e:
            print(f"✗ Gradient background failed: {e}")
            return image_bytes

    def _create_gradient(
        self,
        width: int,
        height: int,
        colors: List[str],
        angle: int = 0
    ) -> Image.Image:
        """Create gradient image"""
        try:
            # Convert colors to RGB
            rgb_colors = [self.hex_to_rgb(color) for color in colors]

            # Create gradient array
            gradient_array = np.zeros((height, width, 3), dtype=np.uint8)

            # Calculate gradient direction based on angle
            angle_rad = np.radians(angle)
            cos_angle = np.cos(angle_rad)
            sin_angle = np.sin(angle_rad)

            # Create coordinate grid
            y, x = np.ogrid[:height, :width]

            # Calculate gradient position for each pixel
            if len(rgb_colors) == 2:
                # Two-color gradient
                # Rotate coordinates
                x_rot = x * cos_angle - y * sin_angle
                x_min, x_max = x_rot.min(), x_rot.max()

                # Normalize to 0-1
                if x_max != x_min:
                    t = (x_rot - x_min) / (x_max - x_min)
                else:
                    t = np.zeros_like(x_rot)

                # Interpolate colors
                color1 = np.array(rgb_colors[0])
                color2 = np.array(rgb_colors[1])

                for i in range(3):
                    gradient_array[:, :, i] = (
                        color1[i] * (1 - t) + color2[i] * t
                    ).astype(np.uint8)

            elif len(rgb_colors) >= 3:
                # Three-color gradient
                x_rot = x * cos_angle - y * sin_angle
                x_min, x_max = x_rot.min(), x_rot.max()

                if x_max != x_min:
                    t = (x_rot - x_min) / (x_max - x_min)
                else:
                    t = np.zeros_like(x_rot)

                # Interpolate through three colors
                color1 = np.array(rgb_colors[0])
                color2 = np.array(rgb_colors[1])
                color3 = np.array(rgb_colors[2])

                for i in range(3):
                    # First half: color1 -> color2
                    mask1 = t <= 0.5
                    t1 = np.clip(t * 2, 0, 1)
                    gradient_array[mask1, i] = (
                        color1[i] * (1 - t1[mask1]) + color2[i] * t1[mask1]
                    ).astype(np.uint8)

                    # Second half: color2 -> color3
                    mask2 = t > 0.5
                    t2 = np.clip((t - 0.5) * 2, 0, 1)
                    gradient_array[mask2, i] = (
                        color2[i] * (1 - t2[mask2]) + color3[i] * t2[mask2]
                    ).astype(np.uint8)

            # Convert to PIL Image
            gradient_img = Image.fromarray(gradient_array, 'RGB')
            return gradient_img.convert('RGBA')

        except Exception as e:
            print(f"Gradient creation failed: {e}")
            # Fallback to solid color
            return Image.new('RGBA', (width, height), self.hex_to_rgb(colors[0]) + (255,))

    def add_texture_background(
        self,
        image_bytes: bytes,
        texture_name: str = "wood"
    ) -> bytes:
        """
        Add texture background to transparent image

        Args:
            image_bytes: Image with transparent background
            texture_name: Name of texture (wood, fabric, concrete, paper, etc.)

        Returns:
            Image bytes with texture background
        """
        try:
            # Load transparent image
            foreground = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
            width, height = foreground.size

            # Generate procedural texture
            texture = self._generate_texture(width, height, texture_name)

            # Composite images
            result = Image.alpha_composite(texture, foreground)

            # Convert to RGB
            final = Image.new('RGB', result.size, (255, 255, 255))
            final.paste(result, mask=result.split()[3] if result.mode == 'RGBA' else None)

            # Save to bytes
            output_buffer = io.BytesIO()
            final.save(output_buffer, 'PNG', optimize=True)
            output_buffer.seek(0)

            print(f"✓ Added texture background: {texture_name}")
            return output_buffer.read()

        except Exception as e:
            print(f"✗ Texture background failed: {e}")
            return image_bytes

    def _generate_texture(
        self,
        width: int,
        height: int,
        texture_name: str
    ) -> Image.Image:
        """Generate procedural texture"""
        try:
            # Create noise-based texture
            noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)

            # Define base colors for different textures
            texture_colors = {
                'wood': (139, 90, 60),        # Brown
                'fabric': (200, 200, 220),    # Light gray-blue
                'concrete': (180, 180, 180),  # Gray
                'paper': (240, 235, 220),     # Off-white
                'marble': (245, 245, 250),    # White-gray
                'brick': (180, 100, 80),      # Red-brown
            }

            base_color = texture_colors.get(texture_name, (200, 200, 200))

            # Add base color to noise
            texture_array = noise.copy()
            for i in range(3):
                texture_array[:, :, i] = np.clip(
                    base_color[i] + noise[:, :, i] - 25,
                    0,
                    255
                ).astype(np.uint8)

            # Convert to PIL Image
            texture_img = Image.fromarray(texture_array, 'RGB')
            return texture_img.convert('RGBA')

        except Exception as e:
            print(f"Texture generation failed: {e}")
            # Fallback to solid gray
            return Image.new('RGBA', (width, height), (200, 200, 200, 255))
