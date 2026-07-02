@echo off
set VENV_DIR=venv
echo Checking for a virtual environment...
if not exist "%VENV_DIR%" (
    echo Creating a virtual environment...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo Error: failed to create a virtual environment.
        echo Make sure that Python 3.x and the venv module are installed.
        pause
        exit /b 1
    )
)
echo Activating the virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip was not found in the virtual environment.
    pause
    exit /b 1
)
echo We install dependencies...
pip install ^
    Flask==2.3.3 ^
    Werkzeug==2.3.7 ^
    Flask-SocketIO==5.3.6 ^
    gevent==24.2.1 ^
    gevent-websocket==0.10.1
if %errorlevel% neq 0 (
    echo Error when installing dependencies.
    pause
    exit /b 1
)
echo.
echo All dependencies are installed. Press any key to exit...
pause
