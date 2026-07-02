@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set VENV_DIR=venv
set APP_FILE=app.py

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    py -3.12 -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create venv.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment found.
)

call "%VENV_DIR%\Scripts\activate.bat"

if not exist "%APP_FILE%" (
    echo ERROR: File '%APP_FILE%' not found in the current directory.
    echo Please run this script from the folder where app.py is located.
    pause
    exit /b 1
)

echo Launching: python "%APP_FILE%"
echo Press Ctrl+C to stop
echo.
python "%APP_FILE%"

if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%.
) else (
    echo.
    echo Application stopped normally.
)

echo.
echo Press Enter to close the terminal...
pause
endlocal