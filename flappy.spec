# -*- mode: python ; coding: utf-8 -*-
import sys
import platform
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_all

# Collect all pygame resources and dependencies
pygame_data = collect_all('pygame')

a = Analysis(
    ['app.py'],
    datas=[
        ('assets', 'assets'),
        *pygame_data[0],  # Datas
    ],
    binaries=[*pygame_data[1]],  # Binaries
    hiddenimports=[
        *pygame_data[2],  # Hidden imports
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

if platform.system() == 'Darwin':
    exe = EXE(
        pyz,
        a.scripts,
        [],  # Exclude binaries from EXE for macOS
        exclude_binaries=True,  # Important for macOS bundling
        name='FlappyGame',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon='assets/images/pam.png',
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='FlappyGame',
    )
    
    app = BUNDLE(
        coll,
        name='FlappyGame.app',
        icon='assets/images/pam.png',
        bundle_identifier='com.manucodes.flappygame',
        info_plist={
            'CFBundleName': 'FlappyGame',
            'CFBundleDisplayName': 'Flappy Game',
            'CFBundleExecutable': 'FlappyGame',
            'CFBundlePackageType': 'APPL',
            'CFBundleShortVersionString': '1.0.0',
            'LSMinimumSystemVersion': '10.13.0',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
        },
    )
elif platform.system() == 'Windows':
    from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct
    exe = EXE(
        name='FlappyGame-Win',
        version=VSVersionInfo(
            ffi=FixedFileInfo(filevers=(1,0,0,0), prodvers=(1,0,0,0)),
            kids=[StringFileInfo([StringTable('040904B0', [
                StringStruct('ProductName', 'Flappy Game'),
                StringStruct('FileDescription', 'Flappy Game'),
                StringStruct('LegalCopyright', '© 2024 Manu Codes')])])]
        ),
        **base_options
    ) 