"""
Configuration file for Jarvis Assistant
Centralizes all settings and API keys for easy management.
"""

import os
from typing import Optional

class Config:
    """Configuration class for Jarvis Assistant."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        # Speech Recognition Settings
        self.speech_timeout = 5  # seconds to wait for speech
        self.phrase_time_limit = 10  # maximum length of a phrase
        self.ambient_noise_duration = 0.5  # seconds to adjust for ambient noise
        
        # Text-to-Speech Settings
        self.tts_rate = 150  # speech rate (words per minute)
        self.tts_volume = 0.9  # volume level (0.0 to 1.0)
        
        # Wake Word Settings
        self.wake_word = "jarvis"
        self.porcupine_access_key = self._get_env_or_default(
            "PORCUPINE_ACCESS_KEY", 
            "YOUR_PORCUPINE_ACCESS_KEY"
        )
        
        # Weather API Settings
        self.weather_api_key = self._get_env_or_default(
            "OPENWEATHERMAP_API_KEY", 
            "af1ca91aac9ed173997de7d34a7f69ad"
        )
        self.weather_units = "metric"  # metric or imperial
        self.default_location = "current location"
        
        # System Control Settings
        self.safety_timeout = 30  # seconds to wait for confirmation
        self.shutdown_delay = 5  # seconds before actual shutdown
        self.max_timer_duration = 3600  # maximum timer duration in seconds
        
        # Logging Settings
        self.enable_logging = True
        self.log_level = "INFO"  # DEBUG, INFO, WARNING, ERROR
        self.log_file = "jarvis.log"
        
        # Feature Flags
        self.enable_wake_word = True
        self.enable_weather = True
        self.enable_system_control = True
        self.enable_timer = True
        self.enable_volume_control = True
        
        # Audio Settings
        self.audio_sample_rate = 16000
        self.audio_channels = 1
        self.audio_format = "paInt16"
        
    def _get_env_or_default(self, env_var: str, default: str) -> str:
        """Get environment variable or return default value."""
        return os.getenv(env_var, default)
    
    def is_porcupine_configured(self) -> bool:
        """Check if Porcupine wake word detection is properly configured."""
        return (self.porcupine_access_key and 
                self.porcupine_access_key != "KKyC6QjCjoAvip84bsLMJ6O4EmrCKmsk5rds9pnYdGI+YmqG3wj6IA==")
    
    def is_weather_configured(self) -> bool:
        """Check if weather API is properly configured."""
        return (self.weather_api_key and 
                self.weather_api_key != "YOUR_OPENWEATHERMAP_API_KEY")
    
    def get_weather_service_config(self) -> dict:
        """Get weather service configuration."""
        return {
            'api_key': self.weather_api_key,
            'units': self.weather_units,
            'default_location': self.default_location
        }
    
    def get_speech_config(self) -> dict:
        """Get speech recognition configuration."""
        return {
            'timeout': self.speech_timeout,
            'phrase_time_limit': self.phrase_time_limit,
            'ambient_noise_duration': self.ambient_noise_duration
        }
    
    def get_tts_config(self) -> dict:
        """Get text-to-speech configuration."""
        return {
            'rate': self.tts_rate,
            'volume': self.tts_volume
        }
    
    def get_system_config(self) -> dict:
        """Get system control configuration."""
        return {
            'safety_timeout': self.safety_timeout,
            'shutdown_delay': self.shutdown_delay,
            'max_timer_duration': self.max_timer_duration
        }

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance."""
    return config 
 