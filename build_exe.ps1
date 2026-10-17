$ErrorActionPreference = 'Stop'

python -m pip install --upgrade pip pyinstaller
python -m PyInstaller --clean --noconfirm .\airpad.spec

Write-Host "Build complete. Output directory: .\dist\AirPad"
Write-Host "Executable: .\dist\AirPad\AirPad.exe"
