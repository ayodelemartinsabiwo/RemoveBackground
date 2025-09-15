# -*- mode: python ; coding: utf-8 -*-
# Optimized PyInstaller build specification for reduced file size and false positive prevention

block_cipher = None

# Optimized Analysis with aggressive exclusions
a = Analysis(
    ['src/main_optimized.py'],  # Use optimized main file
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icon.ico', 'assets'),
    ],
    hiddenimports=[
        # Only essential imports
        'rembg',
        'onnxruntime',
        'PIL',
        'PIL.Image',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={
        # Configure specific hooks for size optimization
        'matplotlib': {
            'backends': ['Agg'],  # Only include Agg backend if matplotlib is used
        }
    },
    runtime_hooks=[],
    excludes=[
        # Aggressive exclusion of large, unnecessary modules
        'matplotlib',
        'matplotlib.pyplot',
        'scipy.spatial.cKDTree',
        'scipy.sparse',
        'scipy.linalg.lapack',
        'scipy.special._ufuncs',
        'pandas',
        'pandas.plotting',
        'pandas.io.formats.style',
        'numpy.random._examples',
        'numpy.tests',
        'tkinter',
        'IPython',
        'jupyter',
        'notebook',
        'sklearn',
        'tensorflow',
        'torch.distributions',
        'torch.nn.modules',
        'torchvision.datasets',
        'torchvision.models',
        'test',
        'tests',
        'testing',
        'unittest',
        'doctest',
        'lib2to3',
        'pdb',
        'profile',
        'pstats',
        'cProfile',
        'xml',
        'xmlrpc',
        'urllib.request',
        'urllib.parse',
        'http.server',
        'email',
        'calendar',
        'locale',
        'gettext',
        'curses',
        'asyncio',
        'multiprocessing.dummy',
        'concurrent.futures',
        'distutils',
        'setuptools',
        'pip',
        'wheel',
        'pytz',
        'dateutil',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,  # Keep False for better compression
)

# Filter out debug and test files
a.pure = [x for x in a.pure if not any(exclude in x[0] for exclude in ['test', 'debug', '_test'])]

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
    strip=True,  # Enable stripping for size reduction
    upx=False,  # Keep UPX disabled to prevent false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='version_info.txt'  # Professional version info
)
