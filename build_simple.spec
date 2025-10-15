# -*- mode: python ; coding: utf-8 -*-
"""
Simple Distribution Build Configuration for Background Remover V1.2 Bulletproof
Minimalist approach - include only what we need, minimal exclusions
"""

block_cipher = None

a = Analysis(
    ['src/main_optimized.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Essential assets only
        ('assets/icon.ico', 'assets'),
    ],
    hiddenimports=[
        # Core application modules
        'rembg',
        'onnxruntime',
        'PIL',
        'PIL.Image',
        'PIL.ImageOps',
        'PIL.ImageFilter',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'cv2',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude the specific problematic modules
        'PyQt6.QtWebEngine',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'tkinter',
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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='version_info.txt',
    uac_admin=False,
    uac_uiaccess=False,
    manifest='app.manifest',
)
