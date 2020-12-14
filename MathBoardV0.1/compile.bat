pyinstaller gui.py
MD Mathboard
rd /s /q build
DEL /Q gui.spec
MOVE dist Mathboard\dist
COPY icon.png Mathboard\dist\gui\icon.png