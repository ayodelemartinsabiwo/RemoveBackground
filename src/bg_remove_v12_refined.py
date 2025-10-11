"""
V12: REFINED SELECTIVE EXPANSION - Smart Edge Recovery
User Feedback: V11 expansion adds blur halo (blue circle)
Root Cause: Expanding EVERYWHERE instead of only in originally-blurred areas
Solution: Detect which edges were originally blurred, expand ONLY those
"""

import os
import sys
from pathlib import Path

_LIBRARY_CACHE = {
    'rembg_remove': None,
    'PIL_Image': None,
    'loaded': False
}

class OptimizedBackgroundRemoverV12:
    """
    V12: REFINED SELECTIVE EXPANSION
    - Analyze ORIGINAL image to find blurred edges
    - Expand ONLY where original had blur/bokeh
    - Keep sharp edges sharp (no artificial blur)
    - Ultra-aggressive artifact cleanup (from V11)
    """

    def __init__(self):
        self._rembg_loaded = _LIBRARY_CACHE['loaded']
        self._rembg_remove = _LIBRARY_CACHE['rembg_remove']
        self._PIL_Image = _LIBRARY_CACHE['PIL_Image']
        self._session = None

    def _load_rembg_libraries(self, progress_callback=None):
        """Load libraries"""
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

            import os
            os.environ['OMP_NUM_THREADS'] = '4'
            os.environ['MKL_NUM_THREADS'] = '4'
            os.environ['OPENBLAS_NUM_THREADS'] = '4'

            from rembg import remove, new_session
            from PIL import Image

            if progress_callback:
                progress_callback("Waking up the pixel wizards... 🎯")

            session = new_session("birefnet-portrait")

            if progress_callback:
                progress_callback("AI wizards are ready! ✨")

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
        """Preload model"""
        try:
            success = self._load_rembg_libraries(progress_callback)
            if progress_callback:
                progress_callback("AI magic is ready!")
            return True
        except Exception:
            return False

    def remove_background(self, input_path, progress_callback=None):
        """Remove background with refined selective expansion"""
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

            success = self._process_image(input_path, output_path, progress_callback)

            if success:
                return True, output_path
            else:
                return False, "Background removal failed"

        except Exception as e:
            return False, f"Error during processing: {str(e)}"

    def _generate_output_path(self, input_path):
        """Generate output path"""
        path = Path(input_path)
        output_name = f"{path.stem}_no_bg{path.suffix}"
        return str(path.parent / output_name)

    def _detect_originally_blurred_edges(self, original_img, alpha_mask):
        """
        INTELLIGENT BLUR DETECTION
        Detect which edges in ORIGINAL image were blurred
        Only expand those specific edges (not sharp ones)
        """
        try:
            import numpy as np
            from scipy.ndimage import gaussian_filter, sobel, binary_dilation, laplace

            # Convert original to grayscale
            original_array = np.array(original_img.convert('RGB'))
            gray = 0.299 * original_array[:,:,0] + 0.587 * original_array[:,:,1] + 0.114 * original_array[:,:,2]
            gray = gray.astype(float) / 255.0

            alpha = alpha_mask.astype(float) / 255.0

            # Find subject edges in alpha mask
            grad_alpha_x = sobel(alpha, axis=1)
            grad_alpha_y = sobel(alpha, axis=0)
            alpha_edges = np.hypot(grad_alpha_x, grad_alpha_y) > 0.02
            alpha_edge_zone = binary_dilation(alpha_edges, iterations=3)

            # Measure sharpness in original image at edge locations
            laplacian = laplace(gray)
            laplacian_abs = np.abs(laplacian)

            # Smooth laplacian to get local sharpness
            sharpness_map = gaussian_filter(laplacian_abs, sigma=2.0)

            # At edge locations, classify as sharp or blurred
            # Low laplacian = blurred edge
            # High laplacian = sharp edge
            blurred_threshold = 0.015  # Tune this

            alpha_edge_zone_bool = np.asarray(alpha_edge_zone, dtype=bool)
            blurred_edges = alpha_edge_zone_bool & (sharpness_map < blurred_threshold)
            sharp_edges = alpha_edge_zone_bool & (sharpness_map >= blurred_threshold)

            return blurred_edges, sharp_edges, sharpness_map

        except Exception as e:
            import numpy as np
            print(f"Blur detection warning: {e}")
            return np.zeros_like(alpha_mask, dtype=bool), np.zeros_like(alpha_mask, dtype=bool), None

    def _selective_edge_expansion(self, img, original_img):
        """
        SELECTIVE EXPANSION
        Expand ONLY edges that were originally blurred
        Keep sharp edges untouched (no artificial blur)
        """
        try:
            import numpy as np
            from scipy.ndimage import binary_dilation, gaussian_filter, grey_dilation

            img_array = np.array(img)

            if img_array.shape[2] != 4:
                return img

            alpha = img_array[:, :, 3]

            # Detect which edges were originally blurred
            blurred_edges, sharp_edges, sharpness_map = self._detect_originally_blurred_edges(
                original_img, alpha
            )

            if sharpness_map is not None:
                alpha_float = alpha.astype(float) / 255.0

                # Expand only in blurred edge zones
                if np.any(blurred_edges):
                    # Calculate adaptive expansion based on local blur
                    # More blurred = more expansion
                    blur_strength = 1.0 - (sharpness_map / (np.max(sharpness_map) + 1e-6))
                    blur_strength = np.clip(blur_strength, 0.0, 1.0)

                    # Expansion iterations: 2-4 pixels based on blur
                    expansion_map = (blur_strength * 3.0 + 1.0).astype(int)  # 1-4 iterations
                    expansion_map[~blurred_edges] = 0  # No expansion outside blurred edges

                    # Apply variable expansion
                    alpha_expanded = alpha_float.copy()
                    for iterations in range(1, 5):
                        expand_mask = expansion_map >= iterations
                        if np.any(expand_mask):
                            expanded_region = grey_dilation(alpha_float, size=(3, 3))
                            alpha_expanded = np.where(
                                expand_mask,
                                np.maximum(alpha_expanded, expanded_region * 0.75),
                                alpha_expanded
                            )

                    # Smooth expansion boundary
                    expansion_zone = (alpha_expanded > alpha_float) & blurred_edges
                    if np.any(expansion_zone):
                        alpha_smooth = gaussian_filter(alpha_expanded, sigma=1.2)
                        alpha_expanded = np.where(
                            expansion_zone,
                            alpha_expanded * 0.5 + alpha_smooth * 0.5,
                            alpha_expanded
                        )

                    img_array[:, :, 3] = (alpha_expanded * 255).astype(np.uint8)

            return self._PIL_Image.fromarray(img_array, 'RGBA')

        except Exception as e:
            print(f"Selective expansion warning: {e}")
            return img

    def _ultra_aggressive_artifact_cleanup(self, img, original_img):
        """Ultra-aggressive artifact cleanup (from V11)"""
        try:
            import numpy as np
            from scipy.ndimage import label, gaussian_filter, binary_dilation, distance_transform_edt

            img_array = np.array(img)
            original_array = np.array(original_img)

            if img_array.shape[2] != 4:
                return img

            rgb = img_array[:, :, :3].astype(float) / 255.0
            alpha = img_array[:, :, 3].astype(float) / 255.0
            original_rgb = original_array[:, :, :3].astype(float) / 255.0

            # Background color
            bg_mask = alpha < 0.04
            if np.sum(bg_mask) > 80:
                bg_color = np.array([
                    np.median(original_rgb[bg_mask, 0]),
                    np.median(original_rgb[bg_mask, 1]),
                    np.median(original_rgb[bg_mask, 2])
                ])
            else:
                bg_color = np.array([0.82, 0.82, 0.82])

            # Color and brightness analysis
            color_diff = np.sqrt(
                (rgb[:,:,0] - bg_color[0])**2 +
                (rgb[:,:,1] - bg_color[1])**2 +
                (rgb[:,:,2] - bg_color[2])**2
            )
            similar_to_bg = color_diff < 0.32

            brightness = 0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]

            rgb_max = np.maximum(np.maximum(rgb[:,:,0], rgb[:,:,1]), rgb[:,:,2])
            rgb_min = np.minimum(np.minimum(rgb[:,:,0], rgb[:,:,1]), rgb[:,:,2])
            saturation = np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0)

            # Spatial context
            solid_subject = alpha > 0.85
            connected_subject = binary_dilation(solid_subject, iterations=6)

            # Distance from subject
            subject_edge_dilation = binary_dilation(solid_subject, iterations=1)
            subject_edge = subject_edge_dilation & np.logical_not(solid_subject)
            distance_from_subject = np.asarray(distance_transform_edt(np.logical_not(subject_edge)), dtype=float)

            # 5-PASS CLEANUP

            # Pass 1: Gap artifacts
            gap_artifacts = (
                np.logical_not(connected_subject) &
                (brightness > 0.55) &
                (saturation < 0.30) &
                (alpha > 0.01) & (alpha < 0.65)
            )
            alpha[gap_artifacts] *= 0.05

            # Pass 2: Hair-body interface
            semi_transparent = (alpha > 0.05) & (alpha < 0.85)
            hair_region = binary_dilation(semi_transparent, iterations=3)
            hair_region_bool = np.asarray(hair_region, dtype=bool)
            solid_hair = (alpha > 0.80) & hair_region_bool
            hair_boundary = binary_dilation(solid_hair, iterations=3) & np.logical_not(solid_hair)

            interface_artifacts = (
                hair_boundary &
                np.logical_not(connected_subject) &
                (brightness > 0.50) &
                (alpha > 0.02) & (alpha < 0.60)
            )
            alpha[interface_artifacts] *= 0.08

            # Pass 3: Labeled regions
            isolated_bright = np.logical_not(connected_subject) & (brightness > 0.60) & (alpha > 0.01)
            labeled, num_features = label(isolated_bright)  # type: ignore

            for i in range(1, num_features + 1):
                region = labeled == i
                region_size = np.sum(region)
                region_brightness = np.mean(brightness[region])

                if region_size < 300:
                    alpha[region] = 0.0
                elif region_size < 600:
                    if region_brightness > 0.72:
                        alpha[region] = 0.0
                    else:
                        alpha[region] *= 0.10
                elif region_size < 1000:
                    if region_brightness > 0.78:
                        alpha[region] *= 0.12
                    else:
                        alpha[region] *= 0.35
                elif region_size < 1800:
                    if region_brightness > 0.72:
                        alpha[region] *= 0.20
                    else:
                        alpha[region] *= 0.45

            # Pass 4: Grey semi-transparent
            grey_semi = (
                (saturation < 0.25) &
                (brightness > 0.45) &
                (alpha > 0.02) & (alpha < 0.65) &
                np.logical_not(solid_subject)
            )
            alpha[grey_semi] *= 0.12

            # Pass 5: Distance-based
            far_from_subject = (distance_from_subject > 5) & (alpha > 0.01) & (alpha < 0.55) & (brightness > 0.50)
            alpha[far_from_subject] *= 0.15

            # Additional passes
            extreme_bright = (brightness > 0.80) & (alpha > 0.01) & (alpha < 0.50)
            alpha[extreme_bright] = 0.0

            white_grey = (brightness > 0.75) & (saturation < 0.18) & (alpha > 0.01) & (alpha < 0.60)
            alpha[white_grey] *= 0.10

            return self._PIL_Image.fromarray(
                np.dstack((rgb * 255, alpha * 255)).astype(np.uint8),
                'RGBA'
            )

        except Exception as e:
            print(f"Artifact cleanup warning: {e}")
            return img

    def _refined_edge_smoothing(self, img, original_img):
        """
        REFINED EDGE SMOOTHING
        Smooth edges WITHOUT creating blur halo
        Use original image sharpness as guide
        """
        try:
            import numpy as np
            from scipy.ndimage import gaussian_filter, sobel, binary_dilation, label, laplace

            img_array = np.array(img)

            if img_array.shape[2] != 4:
                return img

            alpha = img_array[:, :, 3].astype(float) / 255.0

            # Detect originally blurred vs sharp edges
            blurred_edges, sharp_edges, sharpness_map = self._detect_originally_blurred_edges(
                original_img, (alpha * 255).astype(np.uint8)
            )

            # Small object detection
            solid = alpha > 0.90
            labeled_objects, num_objects = label(solid)  # type: ignore

            small_objects = np.zeros_like(alpha, dtype=bool)
            for i in range(1, num_objects + 1):
                region = labeled_objects == i
                region_size = np.sum(region)
                if region_size < 800:
                    small_obj_expanded = binary_dilation(region, iterations=5)
                    small_objects = small_objects | np.asarray(small_obj_expanded, dtype=bool)

            # Edge detection
            grad_x = sobel(alpha, axis=1)
            grad_y = sobel(alpha, axis=0)
            edge_magnitude = np.hypot(grad_x, grad_y)

            edges = edge_magnitude > 0.018
            edge_zone = binary_dilation(edges, iterations=2)

            # Multi-scale smoothing with CONSERVATIVE sigmas
            alpha_smooth_fine = gaussian_filter(alpha, sigma=0.30)  # Reduced
            alpha_smooth_medium = gaussian_filter(alpha, sigma=0.45)  # Reduced
            alpha_smooth_strong = gaussian_filter(alpha, sigma=0.60)  # Reduced
            alpha_smooth_extra = gaussian_filter(alpha, sigma=0.75)  # Reduced

            # Edge classification
            weak_edges = (edge_magnitude > 0.018) & (edge_magnitude <= 0.10)
            weak_zone = binary_dilation(weak_edges, iterations=2)

            medium_edges = (edge_magnitude > 0.10) & (edge_magnitude <= 0.25)
            medium_zone = binary_dilation(medium_edges, iterations=2)

            strong_edges = edge_magnitude > 0.25
            strong_zone = binary_dilation(strong_edges, iterations=3)

            # ADAPTIVE blending based on original edge sharpness
            alpha_refined = alpha.copy()

            # If edge was originally sharp, use LESS smoothing
            # If edge was originally blurred, use MORE smoothing
            sharp_reduction = 0.7  # Multiply blend by 0.7 for sharp edges

            # Weak edges
            weak_blend = 0.45  # Base blend (reduced from 0.52)
            weak_blend_sharp = weak_blend * sharp_reduction
            weak_blend_final = np.where(sharp_edges, weak_blend_sharp, weak_blend)

            alpha_refined = np.where(
                weak_zone & np.logical_not(small_objects),
                alpha * (1 - weak_blend) + alpha_smooth_fine * weak_blend,
                alpha_refined
            )

            # Medium edges
            medium_blend = 0.60  # Reduced from 0.68
            medium_blend_sharp = medium_blend * sharp_reduction

            alpha_refined = np.where(
                medium_zone & np.logical_not(small_objects) & sharp_edges,
                alpha * (1 - medium_blend_sharp) + alpha_smooth_medium * medium_blend_sharp,
                alpha_refined
            )

            alpha_refined = np.where(
                medium_zone & np.logical_not(small_objects) & np.logical_not(sharp_edges),
                alpha * (1 - medium_blend) + alpha_smooth_medium * medium_blend,
                alpha_refined
            )

            # Strong edges
            strong_blend = 0.72  # Reduced from 0.80
            strong_blend_sharp = strong_blend * sharp_reduction

            alpha_refined = np.where(
                strong_zone & np.logical_not(small_objects) & sharp_edges,
                alpha * (1 - strong_blend_sharp) + alpha_smooth_strong * strong_blend_sharp,
                alpha_refined
            )

            alpha_refined = np.where(
                strong_zone & np.logical_not(small_objects) & np.logical_not(sharp_edges),
                alpha * (1 - strong_blend) + alpha_smooth_strong * strong_blend,
                alpha_refined
            )

            # Small objects - reduced smoothing
            small_obj_blend = 0.82  # Reduced from 0.88
            edge_zone_bool = np.asarray(edge_zone, dtype=bool)

            alpha_refined = np.where(
                small_objects & edge_zone_bool,
                alpha * (1 - small_obj_blend) + alpha_smooth_extra * small_obj_blend,
                alpha_refined
            )

            # Light global polish (only on semi-transparent)
            global_polish = 0.15  # Reduced from 0.22
            semi_trans = (alpha_refined > 0.05) & (alpha_refined < 0.95)

            if np.any(semi_trans):
                alpha_polished = gaussian_filter(alpha_refined, sigma=0.16)
                alpha_refined = np.where(
                    semi_trans,
                    alpha_refined * (1 - global_polish) + alpha_polished * global_polish,
                    alpha_refined
                )

            # Final cleanup
            alpha_refined[alpha_refined < 0.008] = 0.0
            alpha_refined[alpha_refined > 0.992] = 1.0
            alpha_refined = np.clip(alpha_refined, 0.0, 1.0)

            img_array[:, :, 3] = (alpha_refined * 255).astype(np.uint8)

            return self._PIL_Image.fromarray(img_array, 'RGBA')

        except Exception as e:
            print(f"Edge smoothing warning: {e}")
            return img

    def _process_image(self, input_path, output_path, progress_callback=None):
        """Process with refined selective expansion"""
        try:
            original_img = self._PIL_Image.open(input_path)
            img = original_img.copy()

            if not self._rembg_remove or not self._session:
                raise ValueError("Model not initialized")

            if progress_callback:
                progress_callback("Teaching pixels to let go of the background... 🎨")

            # BiRefNet
            output_img = self._rembg_remove(
                img,
                session=self._session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=246,
                alpha_matting_background_threshold=7,
                alpha_matting_erode_size=12,
                post_process_mask=True
            )

            if output_img is None:
                raise ValueError("Background removal returned None")

            if progress_callback:
                progress_callback("Finding the fuzzy edges... 🔍")

            if progress_callback:
                progress_callback("Gently expanding the soft edges... 📏")

            # SELECTIVE expansion (only where original was blurred)
            output_img = self._selective_edge_expansion(output_img, original_img)

            if progress_callback:
                progress_callback("Sweeping away the pixel dust... 🧹")

            # Artifact cleanup
            output_img = self._ultra_aggressive_artifact_cleanup(output_img, original_img)

            if progress_callback:
                progress_callback("Hugging the edges for that perfect look... 🤗")

            # Refined smoothing
            output_img = self._refined_edge_smoothing(output_img, original_img)

            if progress_callback:
                progress_callback("✅ REFINED processing complete! Clean edges, no blur halo!")

            if hasattr(output_img, 'save'):
                output_img.save(
                    output_path,
                    'PNG',
                    optimize=True,
                    compress_level=6
                )
                return True
            else:
                raise ValueError("Output image is invalid")

        except Exception as e:
            print(f"Processing error: {e}")
            return False

__all__ = ['OptimizedBackgroundRemoverV12']
