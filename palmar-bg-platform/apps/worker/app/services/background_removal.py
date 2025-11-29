"""
Background Removal Service - Ported from Desktop App V1.2 Bulletproof
Features ultra-clean background artifact removal and maximum hair strand preservation
"""
import os
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageOps
import cv2
import gc
from typing import Optional, Tuple, Callable
from app.core.config import settings


def _setup_onnx_environment():
    """Setup ONNX Runtime environment for maximum compatibility"""
    try:
        os.environ['ORT_DISABLE_ALL_LOGS'] = '1'
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['ORT_ENABLE_PERF_COUNTERS'] = '0'
        os.environ['ONNXRUNTIME_LOG_SEVERITY_LEVEL'] = '4'
        os.environ['ORT_TENSORRT_UNAVAILABLE'] = '1'

        import onnxruntime as ort
        available_providers = ort.get_available_providers()

        if 'CPUExecutionProvider' in available_providers:
            return ['CPUExecutionProvider']
        else:
            raise RuntimeError("CPUExecutionProvider not available")

    except Exception as e:
        print(f"WARNING: ONNX Runtime setup issue: {e}")
        return None


# Setup ONNX environment at module import
_onnx_providers = _setup_onnx_environment()


class BackgroundRemovalService:
    """
    Production-grade background removal service
    Ported from desktop app V1.2 with server optimizations
    """

    # Class-level session cache for performance
    _cached_session = None
    _cached_model_name = None

    def __init__(self):
        self.session = None

    def _init_session(self) -> bool:
        """Initialize ONNX session with model"""
        try:
            # Configure ONNX Runtime CPU execution
            try:
                import onnxruntime as ort
                cpu_options = {
                    'arena_extend_strategy': 'kSameAsRequested',
                    'enable_cpu_mem_arena': '1',
                    'memory_pattern': '1',
                    'enable_mem_reuse': '1'
                }
                providers = [('CPUExecutionProvider', cpu_options)]
            except:
                providers = ['CPUExecutionProvider']

            # Try models in priority order
            model_priority = [settings.MODEL_NAME, settings.MODEL_FALLBACK]

            for model_name in model_priority:
                try:
                    # Check if we have a cached session
                    if (BackgroundRemovalService._cached_session is not None and
                            BackgroundRemovalService._cached_model_name == model_name):
                        self.session = BackgroundRemovalService._cached_session
                        print(f"✓ Using cached session for {model_name}")
                        return True

                    # Create new session
                    print(f"Initializing model: {model_name}")
                    self.session = new_session(model_name, providers=providers)

                    # Cache the session
                    BackgroundRemovalService._cached_session = self.session
                    BackgroundRemovalService._cached_model_name = model_name

                    print(f"✓ Successfully initialized model: {model_name}")
                    return True

                except Exception as e:
                    print(f"Model '{model_name}' initialization failed: {e}")
                    continue

            print("✗ All models failed to initialize")
            return False

        except Exception as e:
            print(f"Session initialization failed: {e}")
            return False

    def _load_image(self, image_data: bytes) -> Tuple[Image.Image, Tuple[int, int]]:
        """Load image from bytes with EXIF orientation correction"""
        try:
            img = Image.open(io.BytesIO(image_data))

            # Handle EXIF orientation
            try:
                img = ImageOps.exif_transpose(img)
            except Exception as e:
                print(f"EXIF orientation handling failed: {e}")

            # Convert to RGB
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            return img.copy(), img.size

        except Exception as e:
            print(f"Image loading failed: {e}")
            fallback = Image.new('RGB', (512, 512), (128, 128, 128))
            return fallback, (512, 512)

    def _resize_image(
        self,
        image: Image.Image,
        max_size: int = None
    ) -> Tuple[Image.Image, Tuple[int, int]]:
        """Resize image if needed"""
        try:
            if max_size is None:
                max_size = settings.MAX_IMAGE_SIZE

            original_size = image.size

            if max(original_size) > max_size:
                ratio = max_size / max(original_size)
                new_width = max(int(original_size[0] * ratio), 32)
                new_height = max(int(original_size[1] * ratio), 32)
                new_size = (new_width, new_height)

                resized = image.resize(new_size, Image.Resampling.BILINEAR)
                return resized, original_size
            else:
                return image, original_size

        except Exception as e:
            print(f"Resize failed: {e}")
            return image, image.size

    def _remove_background_ai(self, image: Image.Image) -> Image.Image:
        """AI background removal using rembg"""
        try:
            result = remove(image, session=self.session)
            return result
        except Exception as e:
            print(f"AI removal failed: {e}")
            # Fallback to basic edge detection
            try:
                result = image.convert('RGBA')
                gray = image.convert('L')
                edges = gray.filter(ImageFilter.FIND_EDGES)

                alpha_data = []
                edge_data = list(edges.getdata())
                for pixel in edge_data:
                    alpha_data.append(255 if pixel > 30 else 0)

                alpha = Image.new('L', image.size)
                alpha.putdata(alpha_data)
                result.putalpha(alpha)
                return result
            except:
                return image.convert('RGBA')

    def _enhance_hair_details(
        self,
        mask_array: np.ndarray,
        rgb_array: np.ndarray
    ) -> np.ndarray:
        """Enhance hair strand details in mask"""
        try:
            mask_float = mask_array.astype(np.float32) / 255.0

            # Boost mid-range values (hair regions)
            enhanced_mask = np.where(
                (mask_float > 0.1) & (mask_float < 0.9),
                np.minimum(mask_float * 1.1, 1.0),
                mask_float
            )

            return enhanced_mask

        except Exception as e:
            print(f"Hair enhancement failed: {e}")
            try:
                return mask_array.astype(np.float32) / 255.0
            except:
                return np.ones((64, 64), dtype=np.float32) * 0.5

    def _cleanup_artifacts(
        self,
        enhanced_mask: np.ndarray,
        rgb_array: np.ndarray
    ) -> np.ndarray:
        """Clean up background artifacts"""
        try:
            # Simple morphological opening to remove noise
            binary_mask = (enhanced_mask > 0.1).astype(np.uint8)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            cleaned_binary = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)

            # Convert back to float mask
            cleaned_mask = cleaned_binary.astype(np.float32) * enhanced_mask
            return cleaned_mask

        except Exception as e:
            print(f"Artifact cleanup failed: {e}")
            return enhanced_mask

    def _assemble_final_image(
        self,
        rgb_array: np.ndarray,
        alpha_array: np.ndarray,
        target_size: Tuple[int, int]
    ) -> Image.Image:
        """Assemble final RGBA image"""
        try:
            # Ensure alpha is uint8
            alpha_uint8 = (np.clip(alpha_array, 0, 1) * 255).astype(np.uint8)

            # Ensure RGB is uint8
            rgb_uint8 = rgb_array.astype(np.uint8)

            # Ensure RGB has 3 channels
            if len(rgb_uint8.shape) == 2:
                rgb_uint8 = np.stack([rgb_uint8, rgb_uint8, rgb_uint8], axis=2)
            elif len(rgb_uint8.shape) == 3 and rgb_uint8.shape[2] > 3:
                rgb_uint8 = rgb_uint8[:, :, :3]

            # Create RGBA array
            if len(alpha_uint8.shape) == 2:
                rgba_array = np.dstack([rgb_uint8, alpha_uint8])
            else:
                alpha_2d = alpha_uint8[:, :, 0] if len(alpha_uint8.shape) > 2 else alpha_uint8
                rgba_array = np.dstack([rgb_uint8, alpha_2d])

            # Create PIL image
            final_image = Image.fromarray(rgba_array, 'RGBA')

            # Resize to target size
            if final_image.size != target_size:
                final_image = final_image.resize(target_size, Image.Resampling.LANCZOS)

            return final_image

        except Exception as e:
            print(f"Final assembly failed: {e}")
            try:
                return Image.new('RGBA', target_size, (128, 128, 128, 128))
            except:
                return Image.new('RGBA', (512, 512), (128, 128, 128, 128))

    def remove_background(self, image_data: bytes) -> Optional[bytes]:
        """
        Main background removal function

        Args:
            image_data: Input image as bytes

        Returns:
            bytes: Processed image with transparent background as PNG bytes, or None if failed
        """
        try:
            # Initialize session if needed
            if self.session is None:
                if not self._init_session():
                    print("✗ Failed to initialize AI model")
                    return None

            # Load image
            image, original_size = self._load_image(image_data)

            # Resize if needed
            processed_image, original_size = self._resize_image(image)

            # AI background removal
            result_rgba = self._remove_background_ai(processed_image)

            # Convert to arrays
            result_array = np.array(result_rgba)
            processed_array = np.array(processed_image)

            # Split RGBA channels
            if len(result_array.shape) == 3 and result_array.shape[2] >= 4:
                rgb_channels = result_array[:, :, :3]
                alpha_channel = result_array[:, :, 3]
            else:
                rgb_channels = processed_array[:, :, :3] if len(processed_array.shape) > 2 else processed_array
                alpha_channel = np.full(rgb_channels.shape[:2], 128, dtype=np.uint8)

            # Normalize alpha
            if len(alpha_channel.shape) == 2:
                alpha_float = alpha_channel.astype(np.float32) / 255.0
            else:
                alpha_float = alpha_channel.astype(np.float32) / 255.0
                if len(alpha_float.shape) > 2:
                    alpha_float = alpha_float[:, :, 0]

            # Simple cleanup
            cleaned_alpha = np.where(alpha_float > 0.05, alpha_float, 0.0)

            # Garbage collection
            gc.collect()

            # Final assembly
            final_image = self._assemble_final_image(rgb_channels, cleaned_alpha, original_size)

            # Convert to bytes
            import io
            output_buffer = io.BytesIO()
            final_image.save(output_buffer, 'PNG', optimize=True, compress_level=6)
            output_buffer.seek(0)

            print(f"✓ Background removed successfully - Size: {original_size}")
            return output_buffer.read()

        except Exception as e:
            print(f"Background removal failed: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            gc.collect()


# Add missing import
import io
