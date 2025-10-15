# -*- mode: python ; coding: utf-8 -*-

"""
Enhanced PyInstaller spec file for Background Remover V1.2 Bulletproof
Fixes distribution issues on clean Windows systems:
1. Removes WebView dependencies that cause Microsoft.Internal.Framework.Udk.dll errors
2. Properly packages scikit-image binary dependencies
3. Ensures compatibility across Windows versions
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# Collect all necessary data files and binaries
rembg_datas = collect_data_files('rembg')
onnxruntime_datas = collect_data_files('onnxruntime')
skimage_datas = collect_data_files('skimage')
cv2_datas = collect_data_files('cv2')

# Collect dynamic libraries
onnxruntime_binaries = collect_dynamic_libs('onnxruntime')
cv2_binaries = collect_dynamic_libs('cv2')
skimage_binaries = collect_dynamic_libs('skimage')

# Collect all submodules to ensure complete packaging
rembg_hiddenimports = collect_submodules('rembg')
skimage_hiddenimports = collect_submodules('skimage')
scipy_hiddenimports = collect_submodules('scipy')

a = Analysis(
    ['src/main_optimized.py'],
    pathex=[],
    binaries=onnxruntime_binaries + cv2_binaries + skimage_binaries,
    datas=[
        ('assets/Icon SVGs/bg icon_256 x 256.svg', 'assets'),
        ('assets/Icon PNGs Corrected', 'assets/Icon PNGs'),
        ('assets/icon.ico', 'assets'),
    ] + rembg_datas + onnxruntime_datas + skimage_datas + cv2_datas,
    hiddenimports=[
        # Core application imports
        'bg_remove_v1_2_bulletproof',
        'context_menu',
        'gui_styles',
        'loader_window',
        'support_dialog',
        'window_utils',

        # Rembg and dependencies
        'rembg',
        'rembg.bg',
        'rembg.session_factory',
        'rembg.sessions.base',
        'rembg.sessions.u2net',
        'rembg.sessions.u2netp',
        'rembg.sessions.silueta',
        'rembg.sessions.isnet',
        'rembg.sessions.sam',
        'rembg.sessions.birefnet',
        'rembg.new_session',

        # ONNX Runtime
        'onnxruntime',
        'onnxruntime.capi',
        'onnxruntime.capi.onnxruntime_pybind11_state',
        'onnxruntime.backend',

        # PIL/Pillow
        'PIL',
        'PIL.Image',
        'PIL.ImageOps',
        'PIL.ImageFilter',
        'PIL.ImageEnhance',
        'PIL.ExifTags',

        # PyQt6 (minimal set to avoid WebView dependencies)
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',

        # OpenCV
        'cv2',

        # NumPy
        'numpy',
        'numpy.core',
        'numpy.lib',

        # Core scientific libraries with complete submodules

        # Date/time handling
        'datetime',

        # System libraries
        'subprocess',
        'os',
        'sys',
        'gc',
        'time',
        'pathlib',

    ] + rembg_hiddenimports + skimage_hiddenimports + scipy_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude WebView components that cause framework dependency issues
        'PyQt6.QtWebEngine',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebChannel',
        'PyQt6.QtWebSockets',
        'PyQt6.QtNetwork',
        'PyQt6.QtPrintSupport',
        'PyQt6.QtMultimedia',
        'PyQt6.QtMultimediaWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'PyQt6.QtPositioning',
        'PyQt6.QtQml',
        'PyQt6.QtQuick',
        'PyQt6.QtQuickWidgets',
        'PyQt6.QtSensors',
        'PyQt6.QtSerialPort',
        'PyQt6.QtSql',
        'PyQt6.QtTest',
        'PyQt6.QtTextToSpeech',

        # Exclude other potential problematic modules
        'matplotlib',
        'tkinter',
        'unittest',
        'test',
        'tests',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',

        # Exclude development tools
        'pdb',
        'pydoc',
        'doctest',
        'inspect',
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='assets/icon.ico',
    manifest='app.manifest',
)
