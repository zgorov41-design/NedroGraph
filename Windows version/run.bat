@echo off
chcp 65001 >nul
setlocal

set "VENV_DIR=venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3.12 -m venv "%VENV_DIR%"

    if errorlevel 1 (
        echo ERROR: Failed to create venv.
        pause
        exit /b 1
    )
)

if not exist "app.py" (
    echo ERROR: app.py not found.
    pause
    exit /b 1
)

if not exist "GUI_Nedrograph.py" (
    echo ERROR: GUI_Nedrograph.py not found.
    pause
    exit /b 1
)

echo Starting server...
start "NedroGraph Server" "%VENV_DIR%\Scripts\python.exe" "app.py"

timeout /t 2 /nobreak >nul

echo Starting GUI...
"%VENV_DIR%\Scripts\python.exe" "GUI_Nedrograph.py"

if errorlevel 1 (
    echo.
    echo GUI exited with an error.
    pause
)

endlocal
