@echo off
echo ========================================
echo    Jarvis Background Process Installer
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
echo [INFO] Working directory: %SCRIPT_DIR%

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in current directory
    echo Current directory: %CD%
    echo Please make sure you're running this from the Jarvis folder
    pause
    exit /b 1
)

echo [OK] requirements.txt found
echo.

REM Check if PyAudio is already installed
echo [INFO] Checking if PyAudio is already installed...
python -c "import pyaudio; print('PyAudio version:', pyaudio.__version__)" >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] PyAudio is already installed
) else (
    echo [INFO] Installing PyAudio...
    pip install pyaudio
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to install PyAudio
        echo You may need to install Visual Studio Build Tools
        pause
        exit /b 1
    )
    echo [OK] PyAudio installed
)

echo.

REM Install other dependencies
echo [INFO] Installing other Python dependencies...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Install Jarvis to startup
echo [INFO] Installing Jarvis to startup...
python jarvis_background.py install
if %errorLevel% neq 0 (
    echo [ERROR] Failed to add Jarvis to startup
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo [SUCCESS] Jarvis is now installed and will start automatically on boot!
echo.
echo [INFO] What happens now:
echo    - Jarvis will start automatically when Windows boots
echo    - It runs in the background listening for "Hey Jarvis"
echo    - You can speak commands without manually starting the program
echo.
echo [INFO] Background Process Management:
echo    - Check status: python jarvis_background.py status
echo    - Start manually: python jarvis_background.py start
echo    - Remove from startup: python jarvis_background.py uninstall
echo.
echo [INFO] Logs: %%APPDATA%%\Local\Jarvis\logs\jarvis_background.log
echo.
echo [INFO] Make sure your microphone permissions are enabled in Windows Settings
echo.
echo [INFO] To test Jarvis now, run: python jarvis_background.py start
echo.
pause 