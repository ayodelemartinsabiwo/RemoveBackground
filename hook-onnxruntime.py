"""
PyInstaller runtime hook for onnxruntime

This hook ensures that ONNX Runtime loads correctly in the PyInstaller environment
by setting up the necessary environment variables and paths.
"""

import os
import sys
import ctypes
from pathlib import Path

def pyi_rth_onnxruntime():
    """Runtime hook to ensure onnxruntime loads correctly"""

    # Set environment variables for onnxruntime stability
    os.environ['ORT_DISABLE_ALL_LOGS'] = '1'  # Disable logging to reduce overhead
    os.environ['OMP_NUM_THREADS'] = '1'       # Force single-threaded execution
    os.environ['ORT_ENABLE_PERF_COUNTERS'] = '0'  # Disable performance counters

    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        bundle_dir = getattr(sys, '_MEIPASS')  # Use getattr to avoid type checker issues
        bundle_path = Path(bundle_dir)

        print(f"DEBUG: PyInstaller bundle directory: {bundle_dir}")

        # Method 1: Add to PATH
        current_path = os.environ.get('PATH', '')
        if bundle_dir not in current_path:
            os.environ['PATH'] = f"{bundle_dir};{current_path}"
            print(f"DEBUG: Added bundle root directory to PATH: {bundle_dir}")

        # Method 2: Use os.add_dll_directory() for Windows 10+
        try:
            if hasattr(os, 'add_dll_directory'):
                os.add_dll_directory(bundle_dir)
                print(f"DEBUG: Added DLL directory using os.add_dll_directory: {bundle_dir}")
        except Exception as e:
            print(f"DEBUG: Failed to add DLL directory: {e}")

        # Method 3: Preload critical ONNX Runtime DLLs
        dll_names = [
            'onnxruntime.dll',
            'onnxruntime_providers_shared.dll'
        ]

        for dll_name in dll_names:
            dll_path = bundle_path / dll_name
            if dll_path.exists():
                try:
                    # Preload the DLL
                    handle = ctypes.WinDLL(str(dll_path))
                    print(f"DEBUG: Successfully preloaded {dll_name}")
                except Exception as e:
                    print(f"DEBUG: Failed to preload {dll_name}: {e}")
            else:
                print(f"DEBUG: {dll_name} not found at {dll_path}")

        # Also check for onnxruntime subdirectory
        onnx_dir = os.path.join(bundle_dir, 'onnxruntime')
        if os.path.exists(onnx_dir):
            print("DEBUG: ONNX Runtime directory found in bundle")
            if onnx_dir not in current_path:
                os.environ['PATH'] = f"{onnx_dir};{os.environ['PATH']}"
                print(f"DEBUG: Added {onnx_dir} to PATH")

            # Add DLL directory if available
            try:
                if hasattr(os, 'add_dll_directory'):
                    os.add_dll_directory(onnx_dir)
                    print(f"DEBUG: Added ONNX directory using os.add_dll_directory: {onnx_dir}")
            except Exception as e:
                print(f"DEBUG: Failed to add ONNX DLL directory: {e}")
        else:
            print("DEBUG: ONNX Runtime directory not found in bundle, DLLs should be in root")

        # Set additional environment variables for stability
        os.environ['ONNXRUNTIME_LOG_SEVERITY_LEVEL'] = '4'  # Errors only
        os.environ['ORT_TENSORRT_UNAVAILABLE'] = '1'        # Disable TensorRT
        os.environ['ORT_ENABLE_CPU_FP16_OPS'] = '0'         # Disable FP16 ops that might cause issues

        print("DEBUG: ONNX Runtime environment setup complete")

# Execute the hook
try:
    pyi_rth_onnxruntime()
    print("DEBUG: ONNX Runtime hook executed successfully")
except Exception as e:
    print(f"DEBUG: ONNX Runtime hook failed: {e}")
