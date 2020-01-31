# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Video-Graph-Player3.py'],
             pathex=['D:\\MTEC Project\\Coding\\Video-Graph'],
             binaries=[],
             datas=[('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\autoButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\backwardButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\fallButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\fileButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\forwardButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\matchingButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\openButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\pauseButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\Logo3.ico','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\slapButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\startButton.png','asset'),
                ('D:\\MTEC Project\\Coding\\Video-Graph\\asset\\personalButton.png','asset')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Falling-Graph-Analysis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, icon='D:\\MTEC Project\\Coding\\Video-Graph\\asset\\Logo3.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Falling-Graph-Analysis')
