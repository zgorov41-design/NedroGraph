@echo off
setlocal

for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null} | Select-Object -First 1 -ExpandProperty IPv4Address).IPAddress"') do set "IP=%%A"

if "%IP%"=="" (
    echo Could not detect server IP
    exit /b 1
)

for /f "delims=" %%L in ('powershell.exe -NoProfile -Command "(Get-WinSystemLocale).Name"') do set "LANG=%%L"

echo SERVER_IP = "%IP%" > config.py
echo sys_lan = "%LANG%" >> config.py

echo Server IP: %IP%
echo Windows language: %LANG%
echo config.py updated

endlocal
exit /b 0