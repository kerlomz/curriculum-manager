# -*- mode: python -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='Zhou4315')

console = False
added_files = [('resource/author.png', 'resource'), ('resource/icon.ico', 'resource'), ('nat.exe', '.')]
a = Analysis(['main.py'],
             pathex=['D:\\Workplace\\PyCharm Projects\\Curriculum\\curriculum-manager'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='client',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=console,
          icon='resource/icon.ico')

