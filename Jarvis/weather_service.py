"""
Weather Service for Jarvis
Handles weather information requests using OpenWeatherMap API.
"""

import requests
import json
from typing import Dict, Optional
from datetime import datetime

class WeatherService:
    def __init__(self, api_key: str = None):
        """Initialize weather service with API key."""
        # You can get a free API key from https://openweathermap.org/api
        self.api_key = api_key or "af1ca91aac9ed173997de7d34a7f69ad"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, location: str) -> Dict:
        """Get weather information for a location."""
        try:
            # Build the API request
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_weather_data(data)
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Network error: {str(e)}",
                'response': f"Sorry, I couldn't fetch weather data due to a network error."
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f"Invalid response: {str(e)}",
                'response': f"Sorry, I received invalid weather data."
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unknown error: {str(e)}",
                'response': f"Sorry, I encountered an error while fetching weather data."
            }
    
    def _parse_weather_data(self, data: Dict) -> Dict:
        """Parse weather data from API response."""
        try:
            # Extract basic information
            city = data.get('name', 'Unknown')
            country = data.get('sys', {}).get('country', '')
            location = f"{city}, {country}" if country else city
            
            # Extract weather conditions
            weather_main = data.get('weather', [{}])[0].get('main', 'Unknown')
            weather_desc = data.get('weather', [{}])[0].get('description', 'Unknown')
            
            # Extract temperature and humidity
            main_data = data.get('main', {})
            temp = main_data.get('temp')
            humidity = main_data.get('humidity')
            feels_like = main_data.get('feels_like')
            
            # Extract wind information
            wind_data = data.get('wind', {})
            wind_speed = wind_data.get('speed')
            
            # Format the response
            if temp is not None:
                temp_text = f"{temp:.1f}°C"
                feels_like_text = f"{feels_like:.1f}°C" if feels_like else "N/A"
            else:
                temp_text = "N/A"
                feels_like_text = "N/A"
            
            wind_text = f"{wind_speed:.1f} m/s" if wind_speed else "N/A"
            humidity_text = f"{humidity}%" if humidity else "N/A"
            
            # Create a natural language response
            response = f"The weather in {location} is {weather_desc}. "
            response += f"Temperature is {temp_text}"
            if feels_like and abs(temp - feels_like) > 2:
                response += f", but it feels like {feels_like_text}. "
            else:
                response += ". "
            response += f"Humidity is {humidity_text} and wind speed is {wind_text}."
            
            return {
                'success': True,
                'location': location,
                'temperature': temp_text,
                'feels_like': feels_like_text,
                'humidity': humidity_text,
                'wind_speed': wind_text,
                'description': weather_desc,
                'response': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Data parsing error: {str(e)}",
                'response': f"Sorry, I couldn't parse the weather data properly."
            }
    
    def get_weather_simple(self, location: str) -> str:
        """Get a simple weather response string."""
        weather_data = self.get_weather(location)
        return weather_data.get('response', "Sorry, I couldn't get the weather information.")
    
    def is_api_key_valid(self) -> bool:
        """Check if the API key is valid."""
        return self.api_key and self.api_key != "YOUR_OPENWEATHERMAP_API_KEY"

# Fallback weather service for when API is not available
class FallbackWeatherService:
    """Fallback weather service that provides basic responses."""
    
    def get_weather(self, location: str) -> Dict:
        """Provide a fallback weather response."""
        return {
            'success': False,
            'error': 'API key not configured',
            'response': f"I can't provide weather information for {location} right now. "
                       f"To enable weather features, please get a free API key from "
                       f"OpenWeatherMap and configure it in the weather service."
        }
    
    def get_weather_simple(self, location: str) -> str:
        """Get a simple fallback weather response."""
        return self.get_weather(location)['response']
    
    def is_api_key_valid(self) -> bool:
        """Always returns False for fallback service."""
        return False 