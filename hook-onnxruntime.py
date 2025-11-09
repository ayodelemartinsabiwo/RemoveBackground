"""
PyInstaller runtime hook for onnxruntime

This hook ensures that ONNX Runtime loads correctly in the PyInstaller environment
by setting up the necessary environment variables and paths.
"""

import os
import sys

def pyi_rth_onnxruntime():
    """Runtime hook to ensure onnxruntime loads correctly"""

    # Set environment variables for onnxruntime stability
    os.environ['ORT_DISABLE_ALL_LOGS'] = '1'  # Disable logging to reduce overhead
    os.environ['OMP_NUM_THREADS'] = '1'       # Force single-threaded execution
    os.environ['ORT_ENABLE_PERF_COUNTERS'] = '0'  # Disable performance counters

    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        bundle_dir = getattr(sys, '_MEIPASS')  # Use getattr to avoid type checker issues
        onnx_dir = os.path.join(bundle_dir, 'onnxruntime')

        print(f"DEBUG: PyInstaller bundle directory: {bundle_dir}")
        print(f"DEBUG: Looking for ONNX Runtime at: {onnx_dir}")

        if os.path.exists(onnx_dir):
            print("DEBUG: ONNX Runtime directory found in bundle")

            # Add onnxruntime directory to PATH for DLL loading
            current_path = os.environ.get('PATH', '')
            if onnx_dir not in current_path:
                os.environ['PATH'] = f"{onnx_dir};{current_path}"
                print(f"DEBUG: Added {onnx_dir} to PATH")

            # Also add any subdirectories that might contain DLLs
            for root, dirs, files in os.walk(onnx_dir):
                for file in files:
                    if file.endswith('.dll'):
                        dll_dir = root
                        if dll_dir not in current_path:
                            os.environ['PATH'] = f"{dll_dir};{os.environ['PATH']}"
                            print(f"DEBUG: Added DLL directory to PATH: {dll_dir}")
                        break
        else:
            print("DEBUG: ONNX Runtime directory not found in bundle")

        # Set additional environment variables for stability
        os.environ['ONNXRUNTIME_LOG_SEVERITY_LEVEL'] = '4'  # Errors only
        os.environ['ORT_TENSORRT_UNAVAILABLE'] = '1'        # Disable TensorRT

        print("DEBUG: ONNX Runtime environment setup complete")

# Execute the hook
try:
    pyi_rth_onnxruntime()
    print("DEBUG: ONNX Runtime hook executed successfully")
except Exception as e:
    print(f"DEBUG: ONNX Runtime hook failed: {e}")
