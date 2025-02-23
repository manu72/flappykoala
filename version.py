from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

VSVersionInfo_data = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([StringTable('040904B0', [
            StringStruct('FileDescription', 'Flappy Game'),
            StringStruct('FileVersion', '1.0.0'),
            StringStruct('InternalName', 'flappy'),
            StringStruct('LegalCopyright', '© 2024 Manu Codes'),
            StringStruct('OriginalFilename', 'FlappyGame.exe'),
            StringStruct('ProductName', 'Flappy Game'),
            StringStruct('ProductVersion', '1.0.0')])]),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
) 