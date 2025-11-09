#!/usr/bin/env python3
"""
Advanced Model Compression Script
Tries multiple compression methods to minimize model size while preserving quality
"""
import os
import zipfile
import tempfile
from pathlib import Path

def compress_model_ultra(model_path, output_path):
    """Apply ultra compression using LZMA (highest compression ratio)"""
    print(f"Compressing {model_path} with LZMA ultra compression...")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_LZMA, compresslevel=9) as zf:
        zf.write(model_path, os.path.basename(model_path))
    
    original_size = os.path.getsize(model_path) / (1024 * 1024)
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    compression_ratio = (1 - compressed_size / original_size) * 100
    
    print(f"Original size: {original_size:.1f} MB")
    print(f"Compressed size: {compressed_size:.1f} MB")
    print(f"Compression ratio: {compression_ratio:.1f}%")
    
    return compressed_size

def main():
    # First, decompress the current zip to get the original model back
    models_dir = Path("models")
    zip_path = models_dir / "birefnet-portrait.zip"
    onnx_path = models_dir / "birefnet-portrait.onnx"
    
    if zip_path.exists() and not onnx_path.exists():
        print("Extracting original model for re-compression...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extract('birefnet-portrait.onnx', models_dir)
    
    if not onnx_path.exists():
        print("Error: Original model file not found!")
        return
    
    # Try ultra compression
    ultra_path = models_dir / "birefnet-portrait-ultra.zip"
    final_size = compress_model_ultra(onnx_path, ultra_path)
    
    # Replace the original compressed file if ultra compression is better
    if ultra_path.exists():
        current_size = os.path.getsize(zip_path) / (1024 * 1024)
        if final_size < current_size:
            print(f"Ultra compression is better! Saved {current_size - final_size:.1f} MB more")
            os.replace(ultra_path, zip_path)
        else:
            print("Original compression was already optimal")
            os.remove(ultra_path)
    
    # Clean up the uncompressed model
    if onnx_path.exists():
        os.remove(onnx_path)
        print("Cleaned up uncompressed model file")

if __name__ == "__main__":
    main()