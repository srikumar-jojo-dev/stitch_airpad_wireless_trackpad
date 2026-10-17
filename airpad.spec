# -*- mode: python -*-
# PyInstaller spec for the AirPad Windows desktop build.

a = Analysis(
    ['server.py'],
    pathex=['.'],
    binaries=[],
    datas=[('web', 'web')],
    hiddenimports=[
        'server',
        'server.server',
        'aiohttp',
        'pynput',
        'pycaw',
        'comtypes',
        'qrcode',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AirPad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AirPad',
)
