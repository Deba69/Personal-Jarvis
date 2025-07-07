"""
Jarvis Background Process
Runs Jarvis in the background and can be configured to start automatically on boot.
This version doesn't require Windows service framework, making it compatible with Microsoft Store Python.
"""

import os
import sys
import time
import threading
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from jarvis import JarvisAssistant

class JarvisBackground:
    def __init__(self):
        """Initialize Jarvis background process."""
        self.jarvis = None
        self.running = False
        
        # Setup logging
        log_dir = Path.home() / "AppData" / "Local" / "Jarvis" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "jarvis_background.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Create a flag file to indicate Jarvis is running
        self.flag_file = log_dir / "jarvis_running.flag"
        
    def start(self):
        """Start Jarvis background process."""
        self.logger.info("Starting Jarvis background process...")
        self.running = True
        
        # Create flag file
        self.flag_file.touch()
        
        try:
            # Initialize Jarvis
            self.jarvis = JarvisAssistant()
            self.logger.info("Jarvis initialized successfully")
            
            # Run Jarvis in a separate thread
            jarvis_thread = threading.Thread(target=self._run_jarvis, daemon=True)
            jarvis_thread.start()
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Error in Jarvis background process: {e}")
        finally:
            self.cleanup()
            
    def stop(self):
        """Stop Jarvis background process."""
        self.logger.info("Stopping Jarvis background process...")
        self.running = False
        if self.jarvis:
            self.jarvis.running = False
            
    def cleanup(self):
        """Clean up resources."""
        if self.jarvis:
            self.jarvis.cleanup()
        if self.flag_file.exists():
            self.flag_file.unlink()
        self.logger.info("Jarvis background process stopped")
        
    def _run_jarvis(self):
        """Run Jarvis in a separate thread."""
        try:
            self.logger.info("Jarvis is online and ready to assist you.")
            
            # Check if microphone is available
            if not self.jarvis.microphone_available:
                self.logger.error("Microphone not available. Jarvis will not be able to listen for commands.")
                return
            
            while self.jarvis.running and self.running:
                try:
                    # Listen for wake word
                    if self.jarvis.wake_word_available:
                        if self.jarvis.listen_for_wake_word():
                            self.logger.info("Wake word detected!")
                            self.jarvis.speak("Yes, I'm listening.")
                            # Listen for command
                            command = self.jarvis.listen_for_command()
                            self.jarvis.process_command(command)
                    else:
                        # Fallback: continuous listening without wake word
                        command = self.jarvis.listen_for_command()
                        self.jarvis.process_command(command)
                        
                except Exception as e:
                    self.logger.error(f"Error in Jarvis main loop: {e}")
                    time.sleep(1)
                    
        except Exception as e:
            self.logger.error(f"Error running Jarvis: {e}")

def create_startup_script():
    """Create a startup script that can be added to Windows startup."""
    current_dir = Path(__file__).parent.absolute()
    python_exe = sys.executable
    jarvis_script = current_dir / "jarvis_background.py"
    
    # Create batch file for startup
    startup_script = current_dir / "start_jarvis.bat"
    
    with open(startup_script, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'cd /d "{current_dir}"\n')
        f.write(f'"{python_exe}" "{jarvis_script}"\n')
        f.write(f'pause\n')
    
    return startup_script

def add_to_startup():
    """Add Jarvis to Windows startup."""
    try:
        startup_script = create_startup_script()
        
        # Get startup folder path
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        startup_folder.mkdir(parents=True, exist_ok=True)
        
        # Create shortcut in startup folder
        shortcut_path = startup_folder / "Jarvis.lnk"
        
        # Use PowerShell to create shortcut
        ps_script = f'''
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{startup_script}"
        $Shortcut.WorkingDirectory = "{startup_script.parent}"
        $Shortcut.Description = "Jarvis Voice Assistant"
        $Shortcut.Save()
        '''
        
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        
        print(f"[OK] Jarvis added to startup successfully!")
        print(f"[INFO] Startup script: {startup_script}")
        print(f"[INFO] Shortcut created: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to add to startup: {e}")
        return False

def remove_from_startup():
    """Remove Jarvis from Windows startup."""
    try:
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_folder / "Jarvis.lnk"
        
        if shortcut_path.exists():
            shortcut_path.unlink()
            print("[OK] Jarvis removed from startup successfully!")
        else:
            print("[INFO] Jarvis was not in startup")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to remove from startup: {e}")
        return False

def is_running():
    """Check if Jarvis is currently running."""
    log_dir = Path.home() / "AppData" / "Local" / "Jarvis" / "logs"
    flag_file = log_dir / "jarvis_running.flag"
    return flag_file.exists()

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            jarvis = JarvisBackground()
            try:
                jarvis.start()
            except KeyboardInterrupt:
                jarvis.stop()
        elif command == "install":
            add_to_startup()
        elif command == "uninstall":
            remove_from_startup()
        elif command == "status":
            if is_running():
                print("[OK] Jarvis is running")
            else:
                print("[INFO] Jarvis is not running")
        else:
            print(f"[ERROR] Unknown command: {command}")
            print("Available commands: start, install, uninstall, status")
    else:
        # Interactive mode
        print("=" * 60)
        print("[INFO] Jarvis Background Process")
        print("=" * 60)
        print("\nWhat would you like to do?")
        print("1. Start Jarvis in background")
        print("2. Add Jarvis to startup (auto-start on boot)")
        print("3. Remove Jarvis from startup")
        print("4. Check if Jarvis is running")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            jarvis = JarvisBackground()
            try:
                jarvis.start()
            except KeyboardInterrupt:
                jarvis.stop()
        elif choice == "2":
            add_to_startup()
        elif choice == "3":
            remove_from_startup()
        elif choice == "4":
            if is_running():
                print("[OK] Jarvis is running")
            else:
                print("[INFO] Jarvis is not running")
        elif choice == "5":
            print("[INFO] Goodbye!")
        else:
            print("[ERROR] Invalid choice!")

if __name__ == "__main__":
    main() 