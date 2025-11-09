# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

# Get the site-packages directory for the current environment
import site
site_packages = site.getsitepackages()[0] if site.getsitepackages() else None

if not site_packages:
    # Fallback for virtual environments
    import onnxruntime
    site_packages = str(Path(onnxruntime.__file__).parent.parent)

print(f"DEBUG: Site packages: {site_packages}")

# Check for onnxruntime installation
onnx_path = os.path.join(site_packages, 'onnxruntime')
print(f"DEBUG: ONNX Runtime path: {onnx_path}")
print(f"DEBUG: ONNX Runtime exists: {os.path.exists(onnx_path)}")
print(f"DEBUG: Python executable: {sys.executable}")

block_cipher = None

# More comprehensive hidden imports for onnxruntime compatibility
hidden_imports = [
    'rembg',
    'rembg.__init__',
    'rembg.bg',
    'rembg.session_factory',
    'rembg.sessions',
    'rembg.sessions.base',
    'rembg.sessions.u2net',
    'rembg.sessions.u2netp',
    'rembg.sessions.silueta',
    'rembg.sessions.isnet',
    'rembg.sessions.birefnet',
    'rembg.sessions.sam',
    'rembg.new_session',
    'onnxruntime',
    'onnxruntime.capi',
    'onnxruntime.capi.onnxruntime_pybind11_state',
    'onnxruntime.capi._pybind_state',
    'onnxruntime.backend',
    'onnxruntime.backend.backend',
    'onnxruntime.providers',
    'onnxruntime.providers.cpu',
    'PIL',
    'PIL.Image',
    'PIL.ImageOps',
    'PIL.ImageFilter',
    'PIL._tkinter_finder',
    'PyQt6.QtCore',
    'PyQt6.QtWidgets',
    'PyQt6.QtGui',
    'cv2',
    'numpy',
    'skimage',
    'skimage.transform',
    'skimage.measure',
    'skimage.segmentation',
    'scipy',
    'scipy.ndimage',
    'scipy.sparse',
    'scipy.sparse.csgraph',
    'numba',
    'numba.core',
    'numba.core.types',
    'numba.typed',
    'llvmlite',
    'pooch',
    'requests',
    'tqdm',
    'huggingface_hub',
    'filelock',
    'typing_extensions',
    'packaging',
    'pkg_resources.py2_warn',
]

# Collect all ONNX Runtime binaries more comprehensively
binaries = []
datas = [
    ('assets/Icon SVGs/bg icon_256 x 256.svg', 'assets'),
    ('assets/Icon PNGs Corrected', 'assets/Icon PNGs'),  # Bundle corrected custom PNG icons
    ('assets/icon.ico', 'assets'),
    ('models', 'models'),  # Bundle pre-downloaded AI models (NO INTERNET NEEDED!)
]

# Add comprehensive ONNX Runtime support
if os.path.exists(onnx_path):
    print("DEBUG: Collecting ONNX Runtime binaries...")

    # Method 1: Collect all DLLs from onnxruntime directory
    for root, dirs, files in os.walk(onnx_path):
        for file in files:
            if file.endswith(('.dll', '.so', '.dylib', '.pyd')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, onnx_path)
                binaries.append((full_path, f'onnxruntime/{rel_path}'))
                print(f"DEBUG: Adding binary: {file}")

    # Method 2: Add data files for onnxruntime
    onnx_providers_path = os.path.join(onnx_path, 'providers')
    if os.path.exists(onnx_providers_path):
        datas.append((onnx_providers_path, 'onnxruntime/providers'))
        print("DEBUG: Added providers directory")

    # Method 3: Add any additional onnxruntime data
    for item in ['licenses', 'datasets']:
        item_path = os.path.join(onnx_path, item)
        if os.path.exists(item_path):
            datas.append((item_path, f'onnxruntime/{item}'))
            print(f"DEBUG: Added {item} directory")

print(f"DEBUG: Total binaries to include: {len(binaries)}")
print(f"DEBUG: Total data files to include: {len(datas)}")

a = Analysis(
    ['src/main_optimized.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook-onnxruntime.py'],
    excludes=[
        'matplotlib',
        'pandas',
        'torch',
        'torchvision'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out duplicate binaries to avoid conflicts
seen = set()
filtered_binaries = []
for binary in a.binaries:
    if binary[0] not in seen:
        seen.add(binary[0])
        filtered_binaries.append(binary)
    else:
        print(f"DEBUG: Skipping duplicate binary: {binary[1]}")

a.binaries = filtered_binaries
print(f"DEBUG: Final binary count after deduplication: {len(a.binaries)}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create ONE-FOLDER distribution (fixes onnxruntime DLL loading issues)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # CRITICAL: This makes it one-folder instead of one-file
    name='BackgroundRemover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression to reduce false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='version_info.txt'  # Add version information
)

# Create COLLECT to bundle everything into a folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='BackgroundRemover'
)
