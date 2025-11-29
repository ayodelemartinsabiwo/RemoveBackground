"""
Image Optimization Service
Handles multi-resolution output generation and file size optimization
"""
from PIL import Image
from typing import Dict, Tuple
import io
from app.core.config import settings


class ImageOptimizationService:
    """Service for generating optimized multi-resolution outputs"""

    @staticmethod
    def resize_to_resolution(
        image: Image.Image,
        target_size: int,
        maintain_aspect: bool = True
    ) -> Image.Image:
        """
        Resize image to target resolution

        Args:
            image: PIL Image to resize
            target_size: Target size for the longer dimension
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            Resized PIL Image
        """
        original_width, original_height = image.size

        if maintain_aspect:
            # Calculate new dimensions maintaining aspect ratio
            if original_width > original_height:
                new_width = target_size
                new_height = int((target_size / original_width) * original_height)
            else:
                new_height = target_size
                new_width = int((target_size / original_height) * original_width)
        else:
            new_width = target_size
            new_height = target_size

        # Ensure minimum size
        new_width = max(new_width, 32)
        new_height = max(new_height, 32)

        # Resize using high-quality Lanczos resampling
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return resized

    @staticmethod
    def optimize_file_size(image: Image.Image, quality: int = 85) -> bytes:
        """
        Optimize image file size

        Args:
            image: PIL Image to optimize
            quality: JPEG quality for optimization (1-100)

        Returns:
            Optimized image as bytes
        """
        output_buffer = io.BytesIO()

        if image.mode == 'RGBA':
            # For RGBA (transparent background), use PNG with optimization
            image.save(
                output_buffer,
                'PNG',
                optimize=True,
                compress_level=6
            )
        else:
            # For RGB, can use JPEG for better compression
            image.save(
                output_buffer,
                'JPEG',
                quality=quality,
                optimize=True
            )

        output_buffer.seek(0)
        return output_buffer.read()

    def generate_multi_resolution(
        self,
        image_bytes: bytes
    ) -> Dict[str, bytes]:
        """
        Generate small, HD, and ultra-HD versions

        Args:
            image_bytes: Original image as bytes

        Returns:
            Dict with keys 'small', 'hd', 'ultra_hd' containing image bytes
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))

            results = {}

            # Small resolution (free tier)
            small_image = self.resize_to_resolution(image, settings.SMALL_RESOLUTION)
            results['small'] = self.optimize_file_size(small_image, quality=85)

            # HD resolution
            hd_image = self.resize_to_resolution(image, settings.HD_RESOLUTION)
            results['hd'] = self.optimize_file_size(hd_image, quality=90)

            # Ultra HD resolution
            ultra_hd_image = self.resize_to_resolution(image, settings.ULTRA_HD_RESOLUTION)
            results['ultra_hd'] = self.optimize_file_size(ultra_hd_image, quality=95)

            print(f"✓ Generated multi-resolution outputs:")
            print(f"  Small: {len(results['small']) / 1024:.1f} KB")
            print(f"  HD: {len(results['hd']) / 1024:.1f} KB")
            print(f"  Ultra HD: {len(results['ultra_hd']) / 1024:.1f} KB")

            return results

        except Exception as e:
            print(f"✗ Multi-resolution generation failed: {e}")
            return {}

    @staticmethod
    def apply_gamma_correction(image: Image.Image, gamma: float = 1.2) -> Image.Image:
        """
        Apply gamma correction to brighten image

        Args:
            image: PIL Image
            gamma: Gamma value (> 1 brightens, < 1 darkens)

        Returns:
            Gamma-corrected image
        """
        try:
            import numpy as np

            # Convert to array
            img_array = np.array(image).astype(np.float32) / 255.0

            # Apply gamma correction
            corrected = np.power(img_array, 1.0 / gamma)

            # Convert back to uint8
            corrected = (corrected * 255).astype(np.uint8)

            return Image.fromarray(corrected, image.mode)

        except Exception as e:
            print(f"Gamma correction failed: {e}")
            return image
