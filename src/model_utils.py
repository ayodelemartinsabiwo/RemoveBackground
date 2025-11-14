#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model utilities for Background Remover
Handles compressed model files and ensures models are ready for use
"""

import os
import sys
import gzip
import shutil
from pathlib import Path
from typing import cast

def get_models_directory():
    """Get the models directory path"""
    # Check if we're in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # We're in a PyInstaller bundle - compressed models are in _internal
        base_dir = os.path.dirname(sys.executable)
        models_compressed_dir = os.path.join(base_dir, '_internal', 'models_compressed')

        # Use user's AppData for decompressed models (writable without admin rights)
        user_data_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'BackgroundRemover', 'models')
        models_dir = user_data_dir
    else:
        # We're running from source
        base_dir = Path(__file__).parent.parent
        models_compressed_dir = base_dir / 'models_compressed'
        models_dir = base_dir / 'models'

    print(f"DEBUG - PyInstaller bundle detected: {hasattr(sys, '_MEIPASS')}")
    if hasattr(sys, '_MEIPASS'):
        print(f"DEBUG - sys._MEIPASS: {getattr(sys, '_MEIPASS', 'Not found')}")
        print(f"DEBUG - sys.executable: {sys.executable}")
        print(f"DEBUG - models_compressed_dir: {models_compressed_dir}")
        print(f"DEBUG - models_dir: {models_dir}")

    return str(models_dir), str(models_compressed_dir)

def decompress_model(compressed_path, output_path):
    """Decompress a gzip-compressed model file"""
    try:
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                # Copy in chunks to handle large files efficiently
                while True:
                    chunk = cast(bytes, f_in.read(8192))
                    if not chunk:
                        break
                    f_out.write(chunk)
        return True
    except Exception as e:
        print(f"Error decompressing {compressed_path}: {e}")
        return False

def ensure_models_ready():
    """Ensure all required models are decompressed and ready for use"""
    models_dir, models_compressed_dir = get_models_directory()

    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)

    # Required models mapping: compressed_name -> decompressed_name
    required_models = {
        'birefnet-portrait.onnx.gz': 'birefnet-portrait.onnx',
        'u2net.onnx.gz': 'u2net.onnx'
    }

    all_ready = True

    for compressed_name, decompressed_name in required_models.items():
        compressed_path = os.path.join(models_compressed_dir, compressed_name)
        decompressed_path = os.path.join(models_dir, decompressed_name)

        # Check if decompressed model already exists and is valid
        if os.path.exists(decompressed_path) and os.path.getsize(decompressed_path) > 0:
            continue

        # Check if compressed model exists
        if not os.path.exists(compressed_path):
            print(f"Missing compressed model: {compressed_path}")
            all_ready = False
            continue

        # Decompress the model
        print(f"Decompressing {compressed_name}...")
        if decompress_model(compressed_path, decompressed_path):
            print(f"Successfully decompressed {decompressed_name}")
        else:
            print(f"Failed to decompress {compressed_name}")
            all_ready = False

    return all_ready

def get_model_path(model_name):
    """Get the full path to a specific model"""
    models_dir, _ = get_models_directory()
    return os.path.join(models_dir, model_name)

def cleanup_models():
    """Clean up decompressed models (useful for testing)"""
    models_dir, _ = get_models_directory()
    if os.path.exists(models_dir):
        shutil.rmtree(models_dir)
        print(f"Cleaned up models directory: {models_dir}")

if __name__ == '__main__':
    # Test the model utilities
    print("Testing model utilities...")
    models_dir, compressed_dir = get_models_directory()
    print(f"Models directory: {models_dir}")
    print(f"Compressed models directory: {compressed_dir}")

    if ensure_models_ready():
        print("All models are ready!")
    else:
        print("Some models are missing or failed to decompress.")
