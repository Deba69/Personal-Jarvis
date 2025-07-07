"""
Install Jarvis as a Windows Service
This script installs Jarvis as a Windows service that starts automatically on boot.
"""

import os
import sys
import subprocess
import ctypes
from pathlib import Path

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_service():
    """Install Jarvis as a Windows service."""
    print("[INFO] Installing Jarvis as a Windows Service...")
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    service_script = current_dir / "jarvis_service.py"
    
    if not service_script.exists():
        print("[ERROR] Error: jarvis_service.py not found!")
        return False
    
    try:
        # Install the service using Python's win32serviceutil
        cmd = [
            sys.executable,
            str(service_script),
            "install"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            print("[OK] Service installed successfully!")
            
            # Start the service
            print("[INFO] Starting Jarvis service...")
            start_cmd = [
                sys.executable,
                str(service_script),
                "start"
            ]
            
            start_result = subprocess.run(start_cmd, capture_output=True, text=True, cwd=current_dir)
            
            if start_result.returncode == 0:
                print("[OK] Jarvis service started successfully!")
                print("\n[SUCCESS] Jarvis is now running as a Windows service!")
                print("[INFO] Service Details:")
                print("   - Name: JarvisAssistant")
                print("   - Display Name: Jarvis Voice Assistant")
                print("   - Auto-start: Yes (starts on boot)")
                print("   - Status: Running")
                print("\n[INFO] Service Management:")
                print("   - To stop: python jarvis_service.py stop")
                print("   - To start: python jarvis_service.py start")
                print("   - To restart: python jarvis_service.py restart")
                print("   - To remove: python jarvis_service.py remove")
                print("\n[INFO] Logs are saved to: %APPDATA%\\Local\\Jarvis\\logs\\jarvis_service.log")
                return True
            else:
                print(f"[WARNING] Service installed but failed to start: {start_result.stderr}")
                return False
        else:
            print(f"[ERROR] Failed to install service: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error installing service: {e}")
        return False

def uninstall_service():
    """Uninstall Jarvis Windows service."""
    print("[INFO] Uninstalling Jarvis Windows Service...")
    
    current_dir = Path(__file__).parent.absolute()
    service_script = current_dir / "jarvis_service.py"
    
    try:
        # Stop the service first
        stop_cmd = [
            sys.executable,
            str(service_script),
            "stop"
        ]
        
        subprocess.run(stop_cmd, capture_output=True, text=True, cwd=current_dir)
        
        # Remove the service
        remove_cmd = [
            sys.executable,
            str(service_script),
            "remove"
        ]
        
        result = subprocess.run(remove_cmd, capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            print("[OK] Service uninstalled successfully!")
            return True
        else:
            print(f"[ERROR] Failed to uninstall service: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error uninstalling service: {e}")
        return False

def check_service_status():
    """Check the status of the Jarvis service."""
    print("[INFO] Checking Jarvis service status...")
    
    current_dir = Path(__file__).parent.absolute()
    service_script = current_dir / "jarvis_service.py"
    
    try:
        cmd = [
            sys.executable,
            str(service_script),
            "status"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            print("[OK] Jarvis service is running")
            return True
        else:
            print("[ERROR] Jarvis service is not running")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error checking service status: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("[INFO] Jarvis Windows Service Installer")
    print("=" * 60)
    
    # Check if running as administrator
    if not is_admin():
        print("[ERROR] This script requires administrator privileges!")
        print("[INFO] Please run this script as Administrator:")
        print("   1. Right-click on this script")
        print("   2. Select 'Run as administrator'")
        return
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            install_service()
        elif command == "uninstall":
            uninstall_service()
        elif command == "status":
            check_service_status()
        else:
            print(f"[ERROR] Unknown command: {command}")
            print("Available commands: install, uninstall, status")
    else:
        # Interactive mode
        print("\nWhat would you like to do?")
        print("1. Install Jarvis as a Windows service")
        print("2. Uninstall Jarvis Windows service")
        print("3. Check service status")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            install_service()
        elif choice == "2":
            uninstall_service()
        elif choice == "3":
            check_service_status()
        elif choice == "4":
            print("[INFO] Goodbye!")
        else:
            print("[ERROR] Invalid choice!")

if __name__ == "__main__":
    main() 