# -*- mode: python ; coding: utf-8 -*-
"""
Distribution-Safe Build Configuration for Background Remover V1.2 Bulletproof
Optimized to prevent extraction and framework errors on clean Windows systems
"""

block_cipher = None

a = Analysis(
    ['src/main_optimized.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Essential assets only
        ('assets/icon.ico', 'assets'),
        # Essential AI model dependencies
        ('.venv/Lib/site-packages/rembg', 'rembg'),
        ('.venv/Lib/site-packages/onnxruntime', 'onnxruntime'),
    ],
    hiddenimports=[
        # Core AI processing - minimal required imports only
        'rembg',
        'rembg.bg',
        'rembg.session_factory',
        'rembg.sessions.base',
        'rembg.sessions.u2net',
        'rembg.sessions.birefnet',
        'rembg.new_session',

        # ONNX Runtime essentials
        'onnxruntime',
        'onnxruntime.capi',
        'onnxruntime.backend',

        # Image processing essentials
        'PIL',
        'PIL.Image',
        'PIL.ImageOps',
        'PIL.ImageFilter',

        # GUI essentials - minimal PyQt6
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',

        # Computer vision essentials
        'cv2',
        'numpy',

        # Standard library modules needed by dependencies
        'urllib',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
        'http',
        'http.client',
        'socket',
        'ssl',
        'json',
        'time',
        'os',
        'gc',
        'datetime',
        'collections',
        'functools',
        'itertools',
        'importlib',
        'pathlib',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude the most problematic components
        'scipy.ndimage',           # Causes morphology extraction errors
        'skimage.morphology',      # Causes _misc_cy.cp312-win_amd64.pyd extraction errors
        'skimage.segmentation',
        'skimage.transform',
        'skimage.measure',

        # Exclude WebView components that cause framework errors
        'PyQt6.QtWebEngine',       # Causes WebViewHost.exe framework errors
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebChannel',

        # Exclude heavy ML components we definitely don't use
        'torch',
        'torchvision',
        'tensorflow',
        'transformers',
        'tokenizers',
        'matplotlib',
        'pandas',

        # Exclude unused system components
        'tkinter',                 # We use PyQt6, not tkinter
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
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
