"""
Background Remover V1.3 Speed Optimized - Target: 40 seconds maximum
Ultra-fast processing with smart optimizations for speed

Performance Optimizations:
1. Dynamic image resizing based on complexity
2. Multi-threaded processing where possible
3. Memory-efficient operations
4. Faster AI model loading
5. Optimized post-processing pipeline
6. Smart caching system
"""

import os
import sys
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageEnhance
import time
import gc
import cv2
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure model directory for cross-machine compatibility
def _setup_model_directory():
    """
    Setup model directory with priority:
    1. Check for bundled models (in executable directory) - NO INTERNET NEEDED
    2. Use writable AppData location for downloaded models
    """
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            exe_dir = os.path.dirname(sys.executable)

            # Try multiple possible locations for bundled models
            possible_locations = [
                os.path.join(exe_dir, '_internal', 'models'),  # PyInstaller onedir
                os.path.join(exe_dir, 'models'),               # Direct bundling
                os.path.join(exe_dir, '..', 'models'),         # Parent directory
            ]

            for bundled_models_dir in possible_locations:
                if os.path.exists(bundled_models_dir) and os.path.isdir(bundled_models_dir):
                    # Check if there are actual model files
                    model_files = [f for f in os.listdir(bundled_models_dir) if f.endswith('.onnx')]
                    if model_files:
                        print(f"✓ Using bundled models (no internet required): {bundled_models_dir}")
                        os.environ['U2NET_HOME'] = bundled_models_dir
                        return bundled_models_dir

            # Fallback: Use AppData for model downloads (requires internet first time)
            model_dir = os.path.join(
                os.environ.get('LOCALAPPDATA', os.path.expanduser('~')),
                'BackgroundRemover',
                'models'
            )
            os.makedirs(model_dir, exist_ok=True)
            os.environ['U2NET_HOME'] = model_dir
            return model_dir

        else:
            # Running as script - check for pre-downloaded models first
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            bundled_models_dir = os.path.join(script_dir, 'models')

            if os.path.exists(bundled_models_dir) and os.path.isdir(bundled_models_dir):
                model_files = [f for f in os.listdir(bundled_models_dir) if f.endswith('.onnx')]
                if model_files:
                    print(f"✓ Using pre-downloaded models: {bundled_models_dir}")
                    os.environ['U2NET_HOME'] = bundled_models_dir
                    return bundled_models_dir

            # Fallback: Use standard location for downloads
            model_dir = os.path.join(os.path.expanduser('~'), '.u2net')
            os.makedirs(model_dir, exist_ok=True)
            os.environ['U2NET_HOME'] = model_dir
            return model_dir

    except Exception as e:
        print(f"Model directory setup warning: {e}")
        return None

# Initialize model directory on module load
_MODEL_DIR = _setup_model_directory()

# Configure onnxruntime for maximum speed
def _configure_onnxruntime():
    """Configure onnxruntime for maximum performance"""
    import os
    # Use optimal threading
    cpu_count = os.cpu_count() or 4  # Fallback to 4 if None
    os.environ['OMP_NUM_THREADS'] = str(max(1, cpu_count // 2))
    os.environ['MKL_NUM_THREADS'] = str(max(1, cpu_count // 2))
    # Enable optimizations
    os.environ['ORT_OPTIMIZE_LEVEL'] = '99'
    os.environ['ORT_ENABLE_OPTIMIZATIONS'] = '1'

try:
    _configure_onnxruntime()
except Exception as e:
    print(f"Warning: Could not configure onnxruntime: {e}")

class BackgroundRemoverV13SpeedOptimized:
    """
    Speed-optimized background remover targeting 40 seconds maximum
    """

    def __init__(self):
        """Initialize with caching and optimizations"""
        self.session = None
        self.model_type = 'u2net'  # Fastest model
        self.progress_callback = None
        self.start_time = None
        self.current_message_index = 0
        self.processing_cache = {}

        # Fast loading messages
        self.loading_messages = [
            "🚀 Initializing turbo mode...",
            "⚡ Charging speed boosters...",
            "🏃 Running background marathon...",
            "🎯 Targeting background pixels...",
            "✂️ Speed-cutting backgrounds...",
            "🌟 Almost done, hold tight...",
        ]

    def _update_progress(self, message):
        """Update progress with time tracking"""
        if self.progress_callback:
            elapsed = time.time() - self.start_time if self.start_time else 0
            self.progress_callback(f"{message} ({elapsed:.1f}s)")

        # Rotate through messages for variety
        if "Initializing" not in message:
            self.current_message_index = (self.current_message_index + 1) % len(self.loading_messages)

    def _get_image_complexity(self, image):
        """Analyze image complexity to determine optimal processing size"""
        try:
            # Convert to grayscale for analysis
            gray = image.convert('L')
            gray_array = np.array(gray)

            # Calculate edge density (complexity indicator)
            edges = cv2.Canny(gray_array, 50, 150)
            edge_density = np.count_nonzero(edges) / edges.size

            # Calculate variance (texture indicator)
            variance = np.var(gray_array)

            # Complexity score (0-1)
            complexity = min(1.0, (edge_density * 1000 + variance / 10000) / 2)

            return complexity
        except:
            return 0.5  # Default medium complexity

    def _calculate_optimal_size(self, original_size, complexity):
        """Calculate optimal processing size based on image complexity"""
        width, height = original_size
        total_pixels = width * height

        # Base size limits based on complexity
        if complexity < 0.3:  # Simple image
            max_pixels = 800 * 800  # Very fast processing
        elif complexity < 0.6:  # Medium complexity
            max_pixels = 1000 * 1000  # Balanced
        else:  # Complex image
            max_pixels = 1200 * 1200  # Higher quality needed

        # If image is already small enough, keep original
        if total_pixels <= max_pixels:
            return original_size

        # Calculate scaling factor
        scale_factor = (max_pixels / total_pixels) ** 0.5
        new_width = max(64, int(width * scale_factor))
        new_height = max(64, int(height * scale_factor))

        return (new_width, new_height)

    def _speed_optimized_session_init(self):
        """Initialize AI session with speed optimizations"""
        try:
            if self.session is not None:
                return True  # Already initialized

            self._update_progress("🚀 Initializing turbo mode...")

            # Use fastest model with optimizations
            self.session = new_session(
                self.model_type,
                providers=['CPUExecutionProvider']  # CPU is more reliable
            )

            return self.session is not None
        except Exception as e:
            print(f"Session initialization failed: {e}")
            return False

    def _speed_optimized_image_load(self, image_path):
        """Load image with speed optimizations"""
        try:
            self._update_progress("⚡ Loading image at light speed...")

            # Load image
            image = Image.open(image_path)
            original_size = image.size

            # Convert to RGB if needed (faster than RGBA)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Get file size for progress estimation
            file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

            return image, original_size, file_size_mb
        except Exception as e:
            print(f"Image loading failed: {e}")
            return None, None, 0

    def _speed_optimized_resize(self, image):
        """Resize image with complexity-based optimization"""
        try:
            original_size = image.size

            # Analyze complexity
            complexity = self._get_image_complexity(image)

            # Calculate optimal size
            optimal_size = self._calculate_optimal_size(original_size, complexity)

            # Resize if needed
            if optimal_size != original_size:
                self._update_progress(f"🏃 Smart resizing (complexity: {complexity:.2f})...")
                resized = image.resize(optimal_size, Image.Resampling.LANCZOS)
                return resized, original_size
            else:
                return image, original_size

        except Exception as e:
            print(f"Resize failed: {e}")
            return image, image.size

    def _speed_optimized_ai_removal(self, image):
        """AI background removal with speed optimizations"""
        try:
            self._update_progress("🎯 Targeting background pixels...")

            # Create cache key based on image characteristics
            cache_key = f"{image.size}_{hash(image.tobytes()[:1000])}"

            # Check cache (for repeated similar images)
            if cache_key in self.processing_cache:
                print("Using cached result for similar image")
                return self.processing_cache[cache_key]

            # Perform AI removal
            result = remove(image, session=self.session)

            # Cache result (limit cache size)
            if len(self.processing_cache) < 5:
                self.processing_cache[cache_key] = result

            return result

        except Exception as e:
            print(f"AI removal failed: {e}")
            # Fast fallback - simple edge-based mask
            return self._create_fast_fallback_mask(image)

    def _create_fast_fallback_mask(self, image):
        """Create fast fallback mask using edge detection"""
        try:
            result = image.convert('RGBA')
            gray = image.convert('L')

            # Simple edge-based masking
            edges = gray.filter(ImageFilter.FIND_EDGES)

            # Create alpha channel
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

    def _parallel_enhancement(self, alpha_channel, rgb_channels):
        """Parallel processing for hair enhancement"""
        try:
            self._update_progress("🧠 Multi-threaded pixel training...")

            height, width = alpha_channel.shape

            # Split image into sections for parallel processing
            sections = []
            cpu_count = os.cpu_count() or 4  # Fallback to 4 if None
            num_sections = min(4, max(1, cpu_count // 2))
            section_height = height // num_sections

            for i in range(num_sections):
                start_row = i * section_height
                end_row = height if i == num_sections - 1 else (i + 1) * section_height
                sections.append((start_row, end_row))

            # Process sections in parallel
            enhanced_sections = []

            def process_section(section_data):
                start_row, end_row = section_data
                section_alpha = self._enhance_alpha_section(
                    alpha_channel[start_row:end_row],
                    rgb_channels[start_row:end_row]
                )
                return section_alpha

            with ThreadPoolExecutor(max_workers=num_sections) as executor:
                enhanced_sections = list(executor.map(process_section, sections))

            # Combine sections
            enhanced_alpha = np.vstack(enhanced_sections)
            return enhanced_alpha

        except Exception as e:
            print(f"Parallel enhancement failed: {e}")
            return alpha_channel

    def _enhance_alpha_section(self, alpha_section, rgb_section):
        """Enhance alpha channel section"""
        try:
            # Fast morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            enhanced = cv2.morphologyEx(alpha_section, cv2.MORPH_CLOSE, kernel)
            enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, kernel)

            return enhanced
        except:
            return alpha_section

    def _speed_optimized_cleanup(self, alpha_channel):
        """Fast artifact cleanup"""
        try:
            self._update_progress("⚡ Lightning-fast cleanup...")

            # Fast bilateral filter for smoothing
            cleaned = cv2.bilateralFilter(alpha_channel, 5, 50, 50)

            # Quick noise removal
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)

            return cleaned
        except:
            return alpha_channel

    def remove_background(self, image_path, output_path=None, progress_callback=None):
        """
        Speed-optimized background removal - Target: 40 seconds maximum
        """
        self.start_time = time.time()
        self.progress_callback = progress_callback
        self.current_message_index = 0

        try:
            # Initialize session (cached after first use)
            if not self._speed_optimized_session_init():
                return False, "Failed to initialize AI model."

            # Load image
            image, original_size, input_size_mb = self._speed_optimized_image_load(image_path)
            if image is None:
                return False, "Failed to load image."

            # Smart resize based on complexity
            processed_image, original_size = self._speed_optimized_resize(image)

            # Generate output path
            if output_path is None:
                try:
                    from datetime import datetime
                    input_dir = os.path.dirname(os.path.abspath(image_path))
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    current_date = datetime.now().strftime("%Y%m%d")
                    output_path = os.path.join(input_dir, f"{base_name}_no_bg_{current_date}.png")
                except:
                    output_path = "output_no_bg_speed.png"

            # AI background removal (with caching)
            result_rgba = self._speed_optimized_ai_removal(processed_image)

            # Convert to arrays
            result_array = np.array(result_rgba)

            # Extract channels
            if len(result_array.shape) == 3 and result_array.shape[2] >= 4:
                rgb_channels = result_array[:, :, :3]
                alpha_channel = result_array[:, :, 3]
            else:
                rgb_channels = np.array(processed_image)
                alpha_channel = np.full(rgb_channels.shape[:2], 128, dtype=np.uint8)

            # Parallel enhancement
            enhanced_alpha = self._parallel_enhancement(alpha_channel, rgb_channels)

            # Fast cleanup
            cleaned_alpha = self._speed_optimized_cleanup(enhanced_alpha)

            # Resize back to original size if needed
            if processed_image.size != original_size:
                self._update_progress("🌟 Scaling to perfection...")
                # Resize RGB and alpha separately for speed
                rgb_pil = Image.fromarray(rgb_channels).resize(original_size, Image.Resampling.LANCZOS)
                alpha_pil = Image.fromarray(cleaned_alpha).resize(original_size, Image.Resampling.LANCZOS)

                rgb_channels = np.array(rgb_pil)
                cleaned_alpha = np.array(alpha_pil)

            # Final assembly
            self._update_progress("⚡ Final assembly...")
            final_rgba = np.dstack([rgb_channels, cleaned_alpha])
            final_image = Image.fromarray(final_rgba, 'RGBA')

            # Save with optimization
            final_image.save(output_path, 'PNG', optimize=True)

            processing_time = time.time() - self.start_time

            self._update_progress("✅ Speed processing complete!")

            print(f"\n🏆 SPEED OPTIMIZED V1.3 SUCCESS!")
            print(f"⚡ Processing Time: {processing_time:.1f}s")
            print(f"🎯 Target: 40s - {'ACHIEVED!' if processing_time <= 40 else 'EXCEEDED TARGET'}")

            success_message = (
                f"Background removed successfully!\n\n"
                f"⚡ Processing time: {processing_time:.1f} seconds\n"
                f"📁 Saved to: {output_path}\n"
                f"🎯 Speed target: {'✅ ACHIEVED' if processing_time <= 40 else '⚠️ Exceeded'} (40s max)"
            )

            return True, success_message

        except Exception as e:
            processing_time = time.time() - self.start_time if self.start_time else 0
            error_msg = f"Processing failed after {processing_time:.1f}s: {str(e)}"
            print(f"Error: {error_msg}")
            return False, error_msg

        finally:
            # Clean up memory
            gc.collect()

# Test function
if __name__ == "__main__":
    def progress_print(message):
        print(f"Progress: {message}")

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        remover = BackgroundRemoverV13SpeedOptimized()
        success, result = remover.remove_background(input_path, progress_callback=progress_print)

        if success:
            print(f"Success: {result}")
        else:
            print(f"Failed: {result}")
    else:
        print("Usage: python bg_remove_v1_3_speed.py <image_path>")
