"""
PyInstaller hook for winotify
Este hook asegura que todos los módulos y recursos de winotify sean incluidos en el ejecutable
"""

from PyInstaller.utils.hooks import collect_all

# Recolectar todos los módulos, datos y binarios de winotify
datas, binaries, hiddenimports = collect_all('winotify')
