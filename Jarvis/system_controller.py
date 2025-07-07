"""
System Controller for Jarvis
Handles system control operations with enhanced safety features.
"""

import subprocess
import platform
import os
import time
import threading
from typing import Dict, Optional, Callable

class SystemController:
    def __init__(self):
        """Initialize system controller."""
        self.system = platform.system()
        self.pending_operations = {}
        self.safety_timeout = 30  # seconds to wait for confirmation
        
    def open_browser(self, url: str = "https://www.google.com") -> Dict:
        """Open web browser with specified URL."""
        try:
            webbrowser.open(url)
            return {
                'success': True,
                'message': f"Opening browser to {url}",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open browser: {str(e)}",
                'action': 'speak'
            }
    
    def open_application(self, app_name: str) -> Dict:
        """Open a specific application."""
        try:
            if self.system == "Windows":
                # Windows application opening
                if app_name.lower() in ['notepad', 'notepad.exe']:
                    subprocess.Popen(['notepad.exe'])
                elif app_name.lower() in ['calculator', 'calc', 'calc.exe']:
                    subprocess.Popen(['calc.exe'])
                elif app_name.lower() in ['paint', 'mspaint', 'mspaint.exe']:
                    subprocess.Popen(['mspaint.exe'])
                else:
                    # Try to open with default handler
                    subprocess.Popen(['start', app_name], shell=True)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', app_name])
            else:  # Linux
                subprocess.Popen([app_name])
            
            return {
                'success': True,
                'message': f"Opening {app_name}",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open {app_name}: {str(e)}",
                'action': 'speak'
            }
    
    def shutdown_system(self, delay: int = 0) -> Dict:
        """Safely shutdown the system."""
        try:
            if self.system == "Windows":
                if delay > 0:
                    subprocess.run(["shutdown", "/s", "/t", str(delay)], check=True)
                else:
                    subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            elif self.system == "Darwin":  # macOS
                if delay > 0:
                    subprocess.run(["shutdown", "-h", "+" + str(delay//60)], check=True)
                else:
                    subprocess.run(["shutdown", "-h", "now"], check=True)
            else:  # Linux
                if delay > 0:
                    subprocess.run(["shutdown", "-h", "+" + str(delay//60)], check=True)
                else:
                    subprocess.run(["shutdown", "-h", "now"], check=True)
            
            return {
                'success': True,
                'message': f"System will shutdown in {delay} seconds" if delay > 0 else "Shutting down system now",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to shutdown system: {str(e)}",
                'action': 'speak'
            }
    
    def restart_system(self, delay: int = 0) -> Dict:
        """Safely restart the system."""
        try:
            if self.system == "Windows":
                if delay > 0:
                    subprocess.run(["shutdown", "/r", "/t", str(delay)], check=True)
                else:
                    subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            elif self.system == "Darwin":  # macOS
                if delay > 0:
                    subprocess.run(["shutdown", "-r", "+" + str(delay//60)], check=True)
                else:
                    subprocess.run(["shutdown", "-r", "now"], check=True)
            else:  # Linux
                if delay > 0:
                    subprocess.run(["shutdown", "-r", "+" + str(delay//60)], check=True)
                else:
                    subprocess.run(["shutdown", "-r", "now"], check=True)
            
            return {
                'success': True,
                'message': f"System will restart in {delay} seconds" if delay > 0 else "Restarting system now",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to restart system: {str(e)}",
                'action': 'speak'
            }
    
    def cancel_pending_operation(self, operation_id: str) -> Dict:
        """Cancel a pending system operation."""
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/a"], check=True)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["killall", "shutdown"], check=True)
            else:  # Linux
                subprocess.run(["shutdown", "-c"], check=True)
            
            return {
                'success': True,
                'message': "Pending system operation cancelled",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to cancel operation: {str(e)}",
                'action': 'speak'
            }
    
    def get_system_info(self) -> Dict:
        """Get basic system information."""
        try:
            info = {
                'system': self.system,
                'platform': platform.platform(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
            
            # Get memory info if available
            try:
                import psutil
                memory = psutil.virtual_memory()
                info['memory_total'] = f"{memory.total // (1024**3)} GB"
                info['memory_available'] = f"{memory.available // (1024**3)} GB"
                info['memory_percent'] = f"{memory.percent}%"
            except ImportError:
                info['memory'] = "Memory info not available (psutil not installed)"
            
            return {
                'success': True,
                'info': info,
                'message': f"System: {self.system}, Platform: {platform.platform()}",
                'action': 'speak'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get system info: {str(e)}",
                'action': 'speak'
            }
    
    def set_volume(self, level: int) -> Dict:
        """Set system volume (0-100)."""
        try:
            if self.system == "Windows":
                # Windows volume control using PowerShell
                script = f'(New-Object -ComObject WScript.Shell).SendKeys([char]173); (New-Object -ComObject WScript.Shell).SendKeys([char]174); (New-Object -ComObject WScript.Shell).SendKeys([char]175);'
                subprocess.run(["powershell", "-Command", script], check=True)
                return {
                    'success': True,
                    'message': f"Volume set to {level}%",
                    'action': 'speak'
                }
            elif self.system == "Darwin":  # macOS
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"], check=True)
                return {
                    'success': True,
                    'message': f"Volume set to {level}%",
                    'action': 'speak'
                }
            else:  # Linux
                subprocess.run(["amixer", "set", "Master", f"{level}%"], check=True)
                return {
                    'success': True,
                    'message': f"Volume set to {level}%",
                    'action': 'speak'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to set volume: {str(e)}",
                'action': 'speak'
            }
    
    def create_safety_timer(self, operation: str, callback: Callable) -> str:
        """Create a safety timer for critical operations."""
        operation_id = f"{operation}_{int(time.time())}"
        
        def safety_timeout():
            time.sleep(self.safety_timeout)
            if operation_id in self.pending_operations:
                del self.pending_operations[operation_id]
                callback(operation_id)
        
        self.pending_operations[operation_id] = {
            'operation': operation,
            'start_time': time.time(),
            'timer': threading.Timer(self.safety_timeout, safety_timeout)
        }
        self.pending_operations[operation_id]['timer'].start()
        
        return operation_id
    
    def confirm_operation(self, operation_id: str) -> bool:
        """Confirm a pending operation."""
        if operation_id in self.pending_operations:
            operation_data = self.pending_operations[operation_id]
            operation_data['timer'].cancel()
            del self.pending_operations[operation_id]
            return True
        return False
    
    def get_pending_operations(self) -> Dict:
        """Get list of pending operations."""
        return {k: v['operation'] for k, v in self.pending_operations.items()}

# Import webbrowser for browser operations
import webbrowser 