@echo off
echo ========================================
echo    Jarvis Voice Assistant Uninstaller
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
echo Uninstalling Jarvis Windows Service...
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
echo 📁 Working directory: %SCRIPT_DIR%

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Stop and remove the service
python install_service.py uninstall
if %errorLevel% neq 0 (
    echo ❌ Failed to uninstall service
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Uninstallation Complete!
echo ========================================
echo.
echo ✅ Jarvis Windows Service has been removed
echo.
echo 📋 What was removed:
echo    - Jarvis Windows Service
echo    - Automatic startup on boot
echo    - Background service process
echo.
echo 📝 Note: Log files are still available at:
echo    %APPDATA%\Local\Jarvis\logs\
echo.
echo 🎤 You can still run Jarvis manually with: python jarvis.py
echo.
pause 