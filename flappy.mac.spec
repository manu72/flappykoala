# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all pygame resources and dependencies
pygame_data = collect_all('pygame')

a = Analysis(
    ['app.py'],
    pathex=[],
    datas=[
        ('assets', 'assets'),
        ('assets/AppIcon.icns', '.'),  # Add icon to root of bundle
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
    [],
    exclude_binaries=True,
    name='FlappyGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/AppIcon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='FlappyGame'
)

# Bundle configuration with complete icon settings
app = BUNDLE(
    coll,
    name='FlappyGame.app',
    icon='assets/AppIcon.icns',
    bundle_identifier='com.manucodes.flappygame',
    info_plist={
        'CFBundleName': 'FlappyGame',
        'CFBundleDisplayName': 'Flappy Game',
        'CFBundleExecutable': 'FlappyGame',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIconFile': 'AppIcon.icns',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
    }
) 