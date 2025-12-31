@echo off
echo ========================================================
echo      Local AI Assistant - Launcher
echo ========================================================
echo.

echo [1/2] Checking/Installing dependencies...
pip install -r src/requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies. Please check your Python installation and internet connection.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Launching Application...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed or failed to start.
    pause
)
