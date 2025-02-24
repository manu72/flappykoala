# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os

# Collect all pygame resources and dependencies
pygame_data = collect_all('pygame')

a = Analysis(
    ['app.py'],
    pathex=[],
    datas=[
        ('assets', 'assets'),
    ],
    binaries=pygame_data[1],  # Pygame binaries
    hiddenimports=[
        'pygame.base',
        'pygame.constants',
        'pygame.display',
        'pygame.draw',
        'pygame.event',
        'pygame.font',
        'pygame.image',
        'pygame.mixer',
        'pygame.mixer_music',
    ],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FlappyGame',
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
    icon=os.path.join('assets', 'AppIcon.ico')
) 