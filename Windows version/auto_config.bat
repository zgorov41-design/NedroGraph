@echo off
setlocal EnableDelayedExpansion

for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null} | Select-Object -First 1 -ExpandProperty IPv4Address).IPAddress"') do set "IP=%%A"

if not defined IP (
    echo Could not detect server IP
    exit /b 1
)

for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-WinSystemLocale).Name"') do set "LANG=%%A"

set "OLD_LANG="

if exist config.py (
    for /f "tokens=3 delims= " %%A in ('findstr /b "sys_lan" config.py') do set "OLD_LANG=%%~A"
)

if not defined OLD_LANG set "OLD_LANG=!LANG!"

(
    echo SERVER_IP = "!IP!"
    echo sys_lan = "!OLD_LANG!"
) > config.py

echo Server IP: !IP!
echo Windows language: !LANG!
echo config.py updated

endlocal