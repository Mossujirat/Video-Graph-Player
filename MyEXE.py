import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--name=%s' %'Video-Graph-Player',
    '--onefile',
    '--windowed',
    '--add-data=D:\\MTEC Project\\Coding\\Video-Graph\\asset\\autoButton.png;asset',
    '--icon=D:\\MTEC Project\\Coding\\Video-Graph\\asset\\Logo.ico',
    os.path.join('Video-Graph-Player.py'),
])