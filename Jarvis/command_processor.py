"""
Command Processing Framework for Jarvis
Handles intent recognition and command routing for different types of requests.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Callable
import webbrowser
import subprocess
import platform
import os

# Import weather service
try:
    from weather_service import WeatherService, FallbackWeatherService
    weather_service = WeatherService()
    if not weather_service.is_api_key_valid():
        weather_service = FallbackWeatherService()
except ImportError:
    # Create a simple fallback if weather service is not available
    class SimpleFallbackWeather:
        def get_weather_simple(self, location):
            return f"I can't provide weather information for {location} right now. Weather service is not configured."
    weather_service = SimpleFallbackWeather()

# Import system controller
try:
    from system_controller import SystemController
    system_controller = SystemController()
except ImportError:
    # Create a simple fallback if system controller is not available
    class SimpleFallbackSystem:
        def open_browser(self, url="https://www.google.com"):
            try:
                webbrowser.open(url)
                return {'success': True, 'message': f"Opening browser to {url}", 'action': 'speak'}
            except Exception as e:
                return {'success': False, 'message': f"Failed to open browser: {str(e)}", 'action': 'speak'}
        
        def open_application(self, app_name):
            return {'success': False, 'message': f"System controller not available. Cannot open {app_name}.", 'action': 'speak'}
        
        def get_system_info(self):
            return {'success': True, 'message': f"System: {platform.system()}, Platform: {platform.platform()}", 'action': 'speak'}
    
    system_controller = SimpleFallbackSystem()

class CommandProcessor:
    def __init__(self):
        """Initialize the command processor with command patterns and handlers."""
        self.command_patterns = {
            # Time and date commands
            'time': [
                r'\bwhat\s+time\s+(?:is\s+)?(?:it\s+)?\b',
                r'\bcurrent\s+time\b',
                r'\btell\s+me\s+the\s+time\b',
                r'\btime\s+(?:please|now)\b',
                r'\bwhat\s+time\b'
            ],
            'date': [
                r'\bwhat\s+date\s+(?:is\s+)?(?:it\s+)?\b',
                r'\bcurrent\s+date\b',
                r'\btell\s+me\s+the\s+date\b',
                r'\bwhat\s+day\s+is\s+it\b',
                r'\bdate\s+(?:please|today)\b'
            ],
            
            # Weather commands
            'weather': [
                r'\bweather\b',
                r'\bweather\s+in\b',
                r'\bhow\s+is\s+the\s+weather\b',
                r'\btemperature\b',
                r'\bwhat\s+weather\b'
            ],
            
            # System control commands
            'open_browser': [
                r'\bopen\s+browser\b',
                r'\bopen\s+chrome\b',
                r'\bopen\s+firefox\b',
                r'\blaunch\s+browser\b',
                r'\bgo\s+to\s+google\b',
                r'\bstart\s+browser\b'
            ],
            'open_app': [
                r'\bopen\s+(notepad|calculator|paint|word|excel)\b',
                r'\blaunch\s+(notepad|calculator|paint|word|excel)\b',
                r'\bstart\s+(notepad|calculator|paint|word|excel)\b'
            ],
            'system_info': [
                r'\bsystem\s+info\b',
                r'\bsystem\s+information\b',
                r'\bcomputer\s+info\b',
                r'\bwhat\s+system\s+am\s+i\s+running\b'
            ],
            'shutdown': [
                r'\bshutdown\b',
                r'\bshut\s+down\b',
                r'\bturn\s+off\s+computer\b',
                r'\bpower\s+off\b',
                r'\bturn\s+off\s+pc\b'
            ],
            'restart': [
                r'\brestart\b',
                r'\breboot\b',
                r'\brestart\s+computer\b',
                r'\brestart\s+pc\b'
            ],
            'cancel_operation': [
                r'\bcancel\s+(shutdown|restart)\b',
                r'\bstop\s+(shutdown|restart)\b',
                r'\babort\s+(shutdown|restart)\b'
            ],
            
            # Timer commands
            'timer': [
                r'\bset\s+timer\b',
                r'\btimer\s+for\b',
                r'\bcountdown\s+for\b',
                r'\bremind\s+me\s+in\b',
                r'\bwake\s+me\s+up\s+in\b'
            ],
            
            # Volume control commands
            'volume': [
                r'\bset\s+volume\b',
                r'\bvolume\s+(up|down|to)\b',
                r'\bturn\s+(up|down)\s+volume\b',
                r'\bchange\s+volume\b'
            ],
            
            # Greeting commands
            'greeting': [
                r'\bhello\b',
                r'\bhi\b',
                r'\bhey\b',
                r'\bgood\s+morning\b',
                r'\bgood\s+afternoon\b',
                r'\bgood\s+evening\b'
            ],
            
            # Exit commands
            'exit': [
                r'\bgoodbye\b',
                r'\bbye\b',
                r'\bexit\b',
                r'\bquit\b',
                r'\bstop\s+jarvis\b'
            ]
        }
        
        # Initialize command handlers
        self.command_handlers = {
            'time': self.get_time,
            'date': self.get_date,
            'weather': self.get_weather,
            'open_browser': self.open_browser,
            'open_app': self.open_application,
            'system_info': self.get_system_info,
            'shutdown': self.shutdown_system,
            'restart': self.restart_system,
            'cancel_operation': self.cancel_operation,
            'timer': self.set_timer,
            'volume': self.set_volume,
            'greeting': self.greeting,
            'exit': self.exit_command
        }
        
        # Safety confirmation state
        self.pending_confirmation = None
        self.confirmation_count = 0

    def extract_intent(self, command: str) -> Optional[str]:
        """Extract the intent from a voice command."""
        command = command.lower().strip()
        
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return intent
        
        return None

    def extract_parameters(self, command: str, intent: str) -> Dict:
        """Extract parameters from the command."""
        params = {}
        command = command.lower().strip()
        
        if intent == 'timer':
            # Extract time duration from timer commands
            time_patterns = [
                r'(\d+)\s*(second|seconds|sec|s)\b',
                r'(\d+)\s*(minute|minutes|min|m)\b',
                r'(\d+)\s*(hour|hours|hr|h)\b'
            ]
            
            for pattern in time_patterns:
                match = re.search(pattern, command)
                if match:
                    value = int(match.group(1))
                    unit = match.group(2)
                    if unit in ['second', 'seconds', 'sec', 's']:
                        params['duration'] = value
                        params['unit'] = 'seconds'
                    elif unit in ['minute', 'minutes', 'min', 'm']:
                        params['duration'] = value * 60
                        params['unit'] = 'seconds'
                    elif unit in ['hour', 'hours', 'hr', 'h']:
                        params['duration'] = value * 3600
                        params['unit'] = 'seconds'
                    break
        
        elif intent == 'weather':
            # Extract location from weather commands
            location_pattern = r'weather\s+(?:in\s+)?([a-zA-Z\s,]+?)(?:\s+please|\s+now|\s+today)?$'
            match = re.search(location_pattern, command)
            if match:
                params['location'] = match.group(1).strip()
            else:
                # Default location patterns
                if 'current' in command or 'here' in command:
                    params['location'] = 'current location'
                else:
                    params['location'] = 'current location'  # Default to current location
        
        return params

    def process_command(self, command: str) -> Dict:
        """Process a voice command and return response data."""
        intent = self.extract_intent(command)
        params = self.extract_parameters(command, intent)
        
        if intent and intent in self.command_handlers:
            handler = self.command_handlers[intent]
            return handler(command, params)
        else:
            return {
                'response': "I'm sorry, I didn't understand that command. Could you please repeat?",
                'action': 'speak',
                'requires_confirmation': False
            }

    # Command Handlers
    def get_time(self, command: str, params: Dict) -> Dict:
        """Handle time requests."""
        current_time = datetime.now().strftime("%I:%M %p")
        return {
            'response': f"The current time is {current_time}",
            'action': 'speak',
            'requires_confirmation': False
        }

    def get_date(self, command: str, params: Dict) -> Dict:
        """Handle date requests."""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return {
            'response': f"Today is {current_date}",
            'action': 'speak',
            'requires_confirmation': False
        }

    def get_weather(self, command: str, params: Dict) -> Dict:
        """Handle weather requests."""
        location = params.get('location', 'current location')
        
        # Get weather information
        weather_response = weather_service.get_weather_simple(location)
        
        return {
            'response': weather_response,
            'action': 'speak',
            'requires_confirmation': False
        }

    def open_browser(self, command: str, params: Dict) -> Dict:
        """Handle browser opening requests."""
        try:
            webbrowser.open('https://www.google.com')
            return {
                'response': "Opening your default web browser.",
                'action': 'speak',
                'requires_confirmation': False
            }
        except Exception as e:
            return {
                'response': f"Sorry, I couldn't open the browser. Error: {str(e)}",
                'action': 'speak',
                'requires_confirmation': False
            }

    def open_application(self, command: str, params: Dict) -> Dict:
        """Handle application opening requests."""
        app_name = command.split()[2] if len(command.split()) > 2 else 'notepad'
        return system_controller.open_application(app_name)

    def get_system_info(self, command: str, params: Dict) -> Dict:
        """Handle system information requests."""
        return system_controller.get_system_info()

    def shutdown_system(self, command: str, params: Dict) -> Dict:
        """Handle system shutdown requests with safety confirmations."""
        if self.pending_confirmation != 'shutdown':
            self.pending_confirmation = 'shutdown'
            self.confirmation_count = 1
            return {
                'response': "I heard you want to shutdown the computer. This is a critical operation. Please confirm by saying 'yes, shutdown' or 'confirm shutdown'.",
                'action': 'speak',
                'requires_confirmation': True,
                'confirmation_type': 'shutdown'
            }
        else:
            self.pending_confirmation = None
            self.confirmation_count = 0
            return {
                'response': "Shutdown confirmed. Shutting down the system in 5 seconds.",
                'action': 'shutdown',
                'requires_confirmation': False
            }

    def restart_system(self, command: str, params: Dict) -> Dict:
        """Handle system restart requests with safety confirmations."""
        if self.pending_confirmation != 'restart':
            self.pending_confirmation = 'restart'
            self.confirmation_count = 1
            return {
                'response': "I heard you want to restart the computer. This is a critical operation. Please confirm by saying 'yes, restart' or 'confirm restart'.",
                'action': 'speak',
                'requires_confirmation': True,
                'confirmation_type': 'restart'
            }
        else:
            self.pending_confirmation = None
            self.confirmation_count = 0
            return {
                'response': "Restart confirmed. Restarting the system in 5 seconds.",
                'action': 'restart',
                'requires_confirmation': False
            }

    def cancel_operation(self, command: str, params: Dict) -> Dict:
        """Handle operation cancellation requests."""
        operation = command.split()[2] if len(command.split()) > 2 else 'shutdown'
        if operation == 'shutdown':
            return self.shutdown_system(command, params)
        elif operation == 'restart':
            return self.restart_system(command, params)
        else:
            return {
                'response': "I'm sorry, I didn't understand the operation to cancel.",
                'action': 'speak',
                'requires_confirmation': False
            }

    def set_timer(self, command: str, params: Dict) -> Dict:
        """Handle timer requests."""
        duration = params.get('duration')
        if duration:
            return {
                'response': f"Setting a timer for {duration} seconds.",
                'action': 'timer',
                'duration': duration,
                'requires_confirmation': False
            }
        else:
            return {
                'response': "Please specify the timer duration. For example, 'set timer for 30 seconds'.",
                'action': 'speak',
                'requires_confirmation': False
            }

    def set_volume(self, command: str, params: Dict) -> Dict:
        """Handle volume control requests."""
        # Implementation of volume control logic
        return {
            'response': "Volume control logic not implemented yet.",
            'action': 'speak',
            'requires_confirmation': False
        }

    def greeting(self, command: str, params: Dict) -> Dict:
        """Handle greeting requests."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning! How can I help you today?"
        elif 12 <= hour < 17:
            greeting = "Good afternoon! How can I help you today?"
        else:
            greeting = "Good evening! How can I help you today?"
        
        return {
            'response': greeting,
            'action': 'speak',
            'requires_confirmation': False
        }

    def exit_command(self, command: str, params: Dict) -> Dict:
        """Handle exit requests."""
        return {
            'response': "Goodbye! Have a great day!",
            'action': 'exit',
            'requires_confirmation': False
        }

    def reset_confirmation_state(self):
        """Reset the confirmation state."""
        self.pending_confirmation = None
        self.confirmation_count = 0 