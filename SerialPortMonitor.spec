# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['SerialPortMonitor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),   # include icon in the bundle
    ],
    hiddenimports=[
        'winotify',
        'winotify.audio'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SerialPortMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,     # required for single-file
    console=False,           # no console window
    icon='icon.ico'
)
