# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['conu/conu.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='CONU',
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
)

import os
import shutil
from conu.helpers import join_to_project_folder
os.mkdir(join_to_project_folder("dist\\conu"))
os.mkdir(join_to_project_folder("dist\\conu\\db"))
shutil.copyfile(join_to_project_folder("conu\\config.ini"), join_to_project_folder("dist\\conu\\config.ini"))
shutil.copyfile(join_to_project_folder("conu\\db\init.sql"), join_to_project_folder("dist\\conu\\db\\init.sql"))