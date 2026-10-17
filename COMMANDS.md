# AirPad Commands

Start: .\server\venv\Scripts\python.exe server\server.py
Free port 8080: Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Stop app: taskkill /IM AirPad.exe /F
Push: git add . ; git commit -m "message" ; git push
Firewall (admin PowerShell): netsh advfirewall firewall add rule name="AirPad" dir=in action=allow protocol=TCP localport=8080
