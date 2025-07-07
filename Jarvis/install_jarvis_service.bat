@echo off
echo ========================================
echo    Jarvis Voice Assistant Installer
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ This script requires Administrator privileges
    echo.
    echo Please right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo Installing Jarvis as a Windows Service...
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
echo 📁 Working directory: %SCRIPT_DIR%

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found in current directory
    echo Current directory: %CD%
    echo Please make sure you're running this from the Jarvis folder
    pause
    exit /b 1
)

echo ✅ requirements.txt found
echo.

REM Check if PyAudio is already installed
echo Checking if PyAudio is already installed...
python -c "import pyaudio; print('PyAudio version:', pyaudio.__version__)" >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ PyAudio is already installed
) else (
    echo Installing PyAudio...
    pip install pyaudio
    if %errorLevel% neq 0 (
        echo ❌ Failed to install PyAudio
        echo You may need to install Visual Studio Build Tools
        pause
        exit /b 1
    )
    echo ✅ PyAudio installed
)

echo.

REM Install other dependencies
echo Installing other Python dependencies...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Install the service
echo Installing Jarvis Windows Service...
python install_service.py install
if %errorLevel% neq 0 (
    echo ❌ Failed to install service
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo 🎉 Jarvis is now installed as a Windows service!
echo.
echo 📋 What happens now:
echo    - Jarvis will start automatically when Windows boots
echo    - It runs in the background listening for "Hey Jarvis"
echo    - You can speak commands without manually starting the program
echo.
echo 🔧 Service Management:
echo    - Check status: python jarvis_service.py status
echo    - Stop service: python jarvis_service.py stop
echo    - Start service: python jarvis_service.py start
echo    - Remove service: python jarvis_service.py remove
echo.
echo 📝 Logs: %APPDATA%\Local\Jarvis\logs\jarvis_service.log
echo.
echo 🎤 Make sure your microphone permissions are enabled in Windows Settings
echo.
pause 