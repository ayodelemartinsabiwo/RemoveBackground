"""
Model Management Utilities
Handles compressed model decompression and management for the Background Remover application.
"""

import os
import sys
import gzip
import shutil
from pathlib import Path

def decompress_models():
    """
    Decompress models from compressed format to the executable's directory.
    Returns True if models are ready, False if there's an issue.
    """
    try:
        # Use models directory next to the executable (for PyInstaller bundle)
        # or next to the script (for development)

        # Check if we're running from PyInstaller bundle
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            # Running from PyInstaller - models should be next to the executable
            executable_dir = Path(sys.executable).parent
            models_dir = executable_dir / 'models'
            print(f"DEBUG: PyInstaller mode - executable: {sys.executable}")
            print(f"DEBUG: PyInstaller mode - models dir: {models_dir}")
        else:
            # Development mode - use models directory in project root
            models_dir = Path(__file__).parent.parent / 'models'
            print(f"DEBUG: Development mode - models dir: {models_dir}")

        # Try to create models directory
        try:
            models_dir.mkdir(parents=True, exist_ok=True)
            print(f"DEBUG: Successfully created/verified models directory: {models_dir}")
        except Exception as e:
            print(f"ERROR: Failed to create models directory {models_dir}: {e}")
            return False

        # Set U2NET_HOME to models directory next to executable
        os.environ['U2NET_HOME'] = str(models_dir)

        # Check if models already exist
        if any(models_dir.glob('*.onnx')):
            print(f"DEBUG: Using existing models: {models_dir}")
            return True

        # Check if we're running from PyInstaller bundle and need to decompress
        if meipass:
            # Running from PyInstaller - check for compressed models in _internal
            compressed_models_dir = Path(meipass) / 'models_compressed'
            print(f"DEBUG: Looking for compressed models in: {compressed_models_dir}")

            if compressed_models_dir.exists():
                print(f"DEBUG: Found compressed models directory")
                compressed_files = list(compressed_models_dir.glob('*.onnx.gz'))
                print(f"DEBUG: Found {len(compressed_files)} compressed model files: {[f.name for f in compressed_files]}")

                if not compressed_files:
                    print(f"ERROR: No compressed model files found in {compressed_models_dir}")
                    return False

                print(f"DEBUG: Decompressing models to: {models_dir}")

                for compressed_file in compressed_files:
                    model_name = compressed_file.stem  # Remove .gz extension
                    output_path = models_dir / model_name

                    # Skip if already exists and is newer than compressed
                    if output_path.exists() and output_path.stat().st_mtime > compressed_file.stat().st_mtime:
                        print(f"DEBUG: Skipping {model_name} - already exists and is newer")
                        continue

                    print(f"DEBUG: Decompressing {model_name}...")
                    try:
                        with gzip.open(compressed_file, 'rb') as f_in:
                            with open(output_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        print(f"DEBUG: Successfully decompressed {model_name}")
                    except Exception as e:
                        print(f"ERROR: Failed to decompress {model_name}: {e}")
                        return False

                print("DEBUG: Model decompression completed")
                return True
            else:
                print(f"ERROR: Compressed models directory not found: {compressed_models_dir}")
                return False

        # Development mode - models should already exist in local models directory
        if models_dir.exists() and any(models_dir.glob('*.onnx')):
            print(f"DEBUG: Using existing models: {models_dir}")
            return True

        # Models will be downloaded on first use by rembg
        print(f"DEBUG: Models will be downloaded to: {models_dir}")
        return True

    except Exception as e:
        print(f"ERROR: Model setup failed: {e}")
        return False

def ensure_models_ready():
    """
    Ensure models are ready for use.
    This function should be called before starting background removal.
    PERFORMANCE OPTIMIZED: Skip if models already exist
    """
    # Get models directory (next to executable or in development)
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        # Running from PyInstaller bundle
        executable_dir = Path(sys.executable).parent
        models_dir = executable_dir / 'models'
    else:
        # Development mode
        models_dir = Path(__file__).parent.parent / 'models'

    # PERFORMANCE OPTIMIZATION: Quick check if models already exist
    if models_dir.exists():
        required_models = ['birefnet-portrait.onnx', 'u2net.onnx', 'isnet-general-use.onnx']
        existing_models = [model for model in required_models if (models_dir / model).exists()]

        if len(existing_models) >= 1:  # At least one model exists
            print(f"✓ Using existing models: {models_dir}")
            return True

    # If no models exist, decompress them
    print(f"DEBUG: Models not found, decompressing...")
    return decompress_models()

if __name__ == "__main__":
    # Test the decompression function
    import sys
    result = decompress_models()
    print(f"Model preparation result: {result}")
