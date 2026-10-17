@echo off
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"
taskkill /IM AirPad.exe /F >nul 2>&1
echo AirPad server stopped.
pause
