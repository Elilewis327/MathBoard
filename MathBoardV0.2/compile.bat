pyinstaller gui.py -i icon.ico --onefile -w
rd /s /q build
DEL /Q gui.spec
move dist\gui.exe Mathboard.exe
rd /q dist

