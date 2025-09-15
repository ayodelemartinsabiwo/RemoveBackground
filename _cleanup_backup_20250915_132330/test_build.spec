# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Simple test build to isolate rembg issue
a = Analysis(
    ['test_rembg.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'rembg',
        'rembg.bg',
        'rembg.session_factory',
        'rembg.sessions',
        'rembg.sessions.base',
        'rembg.sessions.u2net',
        'onnxruntime',
        'PIL',
        'PIL.Image',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='test_rembg',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
