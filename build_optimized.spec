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
try:
    import onnxruntime
    onnx_path = os.path.dirname(onnxruntime.__file__)
    print(f"DEBUG: ONNX Runtime path: {onnx_path}")
    print(f"DEBUG: ONNX Runtime exists: {os.path.exists(onnx_path)}")
except ImportError:
    onnx_path = os.path.join(site_packages, 'onnxruntime')
    print(f"DEBUG: ONNX Runtime path (fallback): {onnx_path}")
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
    # Network dependencies for rembg
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
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
    'scipy._lib',
    'scipy._lib._util',
    'scipy._lib._array_api',
    'scipy._lib._docscrape',
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
    'pydoc',
    # Our custom modules
    'model_utils',
]

# Enhanced binaries and data collection with aggressive size optimization
binaries = []
datas = [
    ('assets/Icon SVGs/bg icon_256 x 256.svg', 'assets'),
    ('assets/Icon PNGs Corrected', 'assets/Icon PNGs'),  # Bundle corrected custom PNG icons
    ('assets/icon.ico', 'assets'),
]

# Ensure rembg package is included
try:
    import rembg
    rembg_path = os.path.dirname(rembg.__file__)
    if os.path.exists(rembg_path):
        datas.append((rembg_path, 'rembg'))
        print(f"DEBUG: Including rembg package from: {rembg_path}")
except ImportError:
    print("WARNING: rembg not found - will be downloaded at runtime")

# Include other critical packages
critical_packages = ['requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna']
for package_name in critical_packages:
    try:
        pkg = __import__(package_name)
        pkg_path = os.path.dirname(pkg.__file__)
        if os.path.exists(pkg_path):
            datas.append((pkg_path, package_name))
            print(f"DEBUG: Including {package_name} package from: {pkg_path}")
    except ImportError:
        print(f"WARNING: {package_name} not found")

# Handle AI models with aggressive compression strategy - COMPRESSED MODELS ONLY
models_dir = 'models'
if os.path.exists(models_dir):
    # BiRefNet compression strategy - preserve quality while reducing size dramatically
    import gzip
    import shutil

    compressed_models_dir = 'models_compressed'
    os.makedirs(compressed_models_dir, exist_ok=True)

    for model_file in os.listdir(models_dir):
        if model_file.endswith('.onnx'):
            original_path = os.path.join(models_dir, model_file)
            compressed_path = os.path.join(compressed_models_dir, f"{model_file}.gz")

            # Check if compressed version exists and is newer
            if not os.path.exists(compressed_path) or os.path.getmtime(original_path) > os.path.getmtime(compressed_path):
                print(f"DEBUG: Compressing {model_file}...")
                with open(original_path, 'rb') as f_in:
                    with gzip.open(compressed_path, 'wb', compresslevel=9) as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Show compression ratio
                original_size = os.path.getsize(original_path)
                compressed_size = os.path.getsize(compressed_path)
                ratio = (1 - compressed_size / original_size) * 100
                print(f"DEBUG: {model_file} compressed by {ratio:.1f}% ({original_size/1024/1024:.1f}MB -> {compressed_size/1024/1024:.1f}MB)")

    # CRITICAL: Include ONLY compressed models to save ~1.1GB
    datas.append((compressed_models_dir, 'models_compressed'))
    print("DEBUG: Using ONLY compressed models for maximum size optimization")
else:
    print("DEBUG: Models directory not found - runtime model download will be used")

# Add comprehensive ONNX Runtime support
if os.path.exists(onnx_path):
    print("DEBUG: Collecting ONNX Runtime binaries...")

    # Critical: Add the main ONNX Runtime DLLs from capi directory
    capi_path = os.path.join(onnx_path, 'capi')
    if os.path.exists(capi_path):
        print("DEBUG: Found ONNX Runtime capi directory")
        for file in os.listdir(capi_path):
            if file.endswith(('.dll', '.pyd')):
                full_path = os.path.join(capi_path, file)
                # Put DLLs directly in the root of the bundle for easier loading
                binaries.append((full_path, '.'))
                print(f"DEBUG: Adding critical ONNX Runtime binary: {file} -> root")

    # Add common Visual C++ runtime DLLs that ONNX Runtime might need
    system32 = r'C:\Windows\System32'
    vc_dlls = ['vcruntime140.dll', 'vcruntime140_1.dll', 'msvcp140.dll', 'msvcp140_1.dll']
    for dll_name in vc_dlls:
        dll_path = os.path.join(system32, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))
            print(f"DEBUG: Adding VC++ runtime DLL: {dll_name} -> root")
        else:
            print(f"DEBUG: VC++ runtime DLL not found: {dll_name}")

    # Method 1: Collect all remaining DLLs from onnxruntime directory
    for root, dirs, files in os.walk(onnx_path):
        for file in files:
            if file.endswith(('.dll', '.so', '.dylib', '.pyd')):
                full_path = os.path.join(root, file)
                # Skip if already added from capi
                if 'capi' in root and file.endswith(('.dll', '.pyd')):
                    continue
                rel_path = os.path.relpath(full_path, onnx_path)
                binaries.append((full_path, f'onnxruntime/{rel_path}'))
                print(f"DEBUG: Adding binary: {file}")

    # Method 2: Add data files for onnxruntime
    onnx_providers_path = os.path.join(onnx_path, 'providers')
    if os.path.exists(onnx_providers_path):
        datas.append((onnx_providers_path, 'onnxruntime/providers'))
        print("DEBUG: Added providers directory")

    # Method 3: Add any additional onnxruntime data
    for item in ['datasets']:  # Remove licenses to save space
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
    runtime_hooks=['pyi_rth_override_pkgres.py', 'hook-onnxruntime.py'],
    excludes=[
        # Large packages not needed for background removal
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.backends',
        'pandas',
        'torch',
        'torch.nn',
        'torch.optim',
        'torchvision',
        'tensorflow',
        'keras',
        'jupyter',
        'notebook',
        'IPython',
        'sphinx',
        'pytest',
        'setuptools',
        'setuptools._vendor',
        'pkg_resources',
        'pkg_resources._vendor',
        'pkg_resources.extern',
        'wheel',
        'pip',
        # Development and testing modules
        'unittest',
        'doctest',
        'pdb',
        'profile',
        'cProfile',
        'pstats',
        # Documentation and help (keep pydoc - needed by scipy)
        'help',
        # Unnecessary GUI toolkits (we use PyQt6)
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'wx',
        'gtk',
        # Large scientific libraries not used
        'sympy',
        'matplotlib.font_manager',
        'plotly',
        'seaborn',
        # Additional size optimizations - remove unused components
        'jinja2',
        'markupsafe',
        'babel',
        'pytz',
        'dateutil',
        'cryptography',
        'cffi',
        'pycparser',
        # Keep these - required by rembg for model downloads
        # 'charset_normalizer',
        # 'idna',
        # 'urllib3',
        # 'requests',
        # 'certifi',
        # Remove large translation files and unused PyQt components
        'PyQt6.QtPrintSupport',
        'PyQt6.QtSql',
        'PyQt6.QtNetwork',
        'PyQt6.Qt6.translations',
        # Remove unused scientific computing modules
        'statsmodels',
        'patsy',
        'openpyxl',
        'xlrd',
        'xlwt',
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
    strip=False,  # Disable symbol stripping (strip tool not available on Windows)
    upx=True,  # Enable UPX compression for size optimization
    upx_exclude=[
        # Exclude ONNX Runtime from UPX to prevent corruption
        'onnxruntime*.dll',
        'onnxruntime_providers_*.dll',
        '*.onnx',
        # Exclude Qt libraries that may have issues with UPX
        'Qt6Core.dll',
        'Qt6Gui.dll',
        'Qt6Widgets.dll',
    ],
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

# Aggressive data filtering to minimize installer size
filtered_datas = []
excluded_count = 0
for item in a.datas:
    # Skip original models folder since we use compressed ones - CRITICAL for size
    if (item[1].startswith('models/') or item[1].startswith('models\\') or
        item[0].endswith('.onnx')):  # Extra safety to exclude any .onnx files
        print(f"DEBUG: Excluding uncompressed model: {item[1]}")
        excluded_count += 1
        continue

    # Skip large translation files and unnecessary data
    if (item[1].startswith('PyQt6/Qt6/translations/') or
        item[1].startswith('PyQt6\\Qt6\\translations\\') or
        'translations' in item[1] or
        item[1].startswith('jsonschema_specifications/') or
        item[1].startswith('jsonschema_specifications\\') or
        item[1].endswith('.qm') or  # Qt translation files
        item[1].endswith('.ts') or  # Translation source files
        'test' in item[1].lower() or
        'example' in item[1].lower()):
        print(f"DEBUG: Excluding large/unnecessary file: {item[1]}")
        excluded_count += 1
        continue

    filtered_datas.append(item)

print(f"DEBUG: Excluded {excluded_count} unnecessary data files for size optimization")

# Create COLLECT to bundle everything into a folder with size optimization
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    filtered_datas,  # Use filtered data to exclude duplicate models
    strip=False,  # Disable symbol stripping (strip tool not available on Windows)
    upx=True,   # Enable aggressive UPX compression for maximum size reduction
    upx_exclude=[
        # Exclude only absolutely critical files from UPX compression
        'onnxruntime*.dll',
        'onnxruntime_providers_*.dll',
        'onnxruntime*.pyd',
        '*.onnx',
        '*.onnx.gz',  # Don't compress already compressed models
        'python312.dll',  # Main Python DLL
        # Allow UPX on most Qt files - they usually work fine
        'Qt6Core.dll',  # Keep this excluded for stability
    ],
    name='BackgroundRemover'
)

print("DEBUG: Build completed with size optimization enabled")
print("DEBUG: - Compressed models used for smaller installer")
print("DEBUG: - UPX compression enabled (excluding critical files)")
print("DEBUG: - Symbol stripping enabled for size reduction")
print("DEBUG: - Unnecessary packages excluded from build")
