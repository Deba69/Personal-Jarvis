"""
Jarvis Windows Service
Runs Jarvis as a Windows service for automatic startup and background operation.
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import threading
import logging
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from jarvis import JarvisAssistant

class JarvisService(win32serviceutil.ServiceFramework):
    _svc_name_ = "JarvisAssistant"
    _svc_display_name_ = "Jarvis Voice Assistant"
    _svc_description_ = "Jarvis voice assistant that runs in the background and responds to wake word 'hey jarvis'"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.jarvis = None
        self.running = False
        
        # Setup logging
        log_dir = Path.home() / "AppData" / "Local" / "Jarvis" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "jarvis_service.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def SvcStop(self):
        """Stop the service."""
        self.logger.info("Stopping Jarvis service...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False
        if self.jarvis:
            self.jarvis.running = False

    def SvcDoRun(self):
        """Run the service."""
        self.logger.info("Starting Jarvis service...")
        self.running = True
        
        try:
            # Initialize Jarvis
            self.jarvis = JarvisAssistant()
            self.logger.info("Jarvis initialized successfully")
            
            # Run Jarvis in a separate thread
            jarvis_thread = threading.Thread(target=self._run_jarvis, daemon=True)
            jarvis_thread.start()
            
            # Wait for stop event
            while self.running:
                # Check if service should stop
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in Jarvis service: {e}")
        finally:
            if self.jarvis:
                self.jarvis.cleanup()
            self.logger.info("Jarvis service stopped")

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

def main():
    """Main entry point for the service."""
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(JarvisService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(JarvisService)

if __name__ == '__main__':
    main() 