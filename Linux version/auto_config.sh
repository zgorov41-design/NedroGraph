@echo off
setlocal

for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null} | Select-Object -First 1 -ExpandProperty IPv4Address).IPAddress"') do set "IP=%%A"

if "%IP%"=="" (
    echo Could not detect server IP
    pause
    exit /b
)

echo SERVER_IP = "%IP%" > config.py

echo.
echo Server IP: %IP%
echo config.py updated
echo.

python server.py