"""
Test script for Jarvis Assistant
Verifies that all components are working correctly.
"""

import sys
import os
import time
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
        return False
    
    try:
        import pvporcupine
        print("✅ pvporcupine imported successfully")
    except ImportError as e:
        print(f"❌ pvporcupine import failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ pyaudio imported successfully")
    except ImportError as e:
        print(f"❌ pyaudio import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    return True

def test_jarvis_modules():
    """Test that Jarvis modules can be imported."""
    print("\nTesting Jarvis modules...")
    
    try:
        from config import Config, get_config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config module import failed: {e}")
        return False
    
    try:
        from command_processor import CommandProcessor
        print("✅ CommandProcessor imported successfully")
    except ImportError as e:
        print(f"❌ CommandProcessor import failed: {e}")
        return False
    
    try:
        from weather_service import WeatherService, FallbackWeatherService
        print("✅ WeatherService imported successfully")
    except ImportError as e:
        print(f"❌ WeatherService import failed: {e}")
        return False
    
    try:
        from system_controller import SystemController
        print("✅ SystemController imported successfully")
    except ImportError as e:
        print(f"❌ SystemController import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration system."""
    print("\nTesting configuration...")
    
    try:
        from config import get_config
        config = get_config()
        
        print(f"✅ Configuration loaded successfully")
        print(f"   - Speech timeout: {config.speech_timeout}s")
        print(f"   - TTS rate: {config.tts_rate} wpm")
        print(f"   - Safety timeout: {config.safety_timeout}s")
        
        # Test API key detection
        porcupine_configured = config.is_porcupine_configured()
        weather_configured = config.is_weather_configured()
        
        print(f"   - Porcupine configured: {'✅' if porcupine_configured else '❌'}")
        print(f"   - Weather API configured: {'✅' if weather_configured else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_command_processor():
    """Test command processing functionality."""
    print("\nTesting command processor...")
    
    try:
        from command_processor import CommandProcessor
        processor = CommandProcessor()
        
        # Test basic commands
        test_commands = [
            "what time is it",
            "what's the date",
            "hello",
            "open browser",
            "set timer for 30 seconds"
        ]
        
        for command in test_commands:
            result = processor.process_command(command)
            if result and 'response' in result:
                print(f"✅ Command '{command}' processed successfully")
            else:
                print(f"❌ Command '{command}' failed to process")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Command processor test failed: {e}")
        return False

def test_weather_service():
    """Test weather service functionality."""
    print("\nTesting weather service...")
    
    try:
        from weather_service import WeatherService, FallbackWeatherService
        from config import get_config
        
        config = get_config()
        
        if config.is_weather_configured():
            weather_service = WeatherService(config.weather_api_key)
            print("✅ Weather service with API key")
        else:
            weather_service = FallbackWeatherService()
            print("✅ Weather service with fallback mode")
        
        # Test weather request
        response = weather_service.get_weather_simple("test location")
        if response:
            print("✅ Weather service responding correctly")
            return True
        else:
            print("❌ Weather service not responding")
            return False
            
    except Exception as e:
        print(f"❌ Weather service test failed: {e}")
        return False

def test_system_controller():
    """Test system controller functionality."""
    print("\nTesting system controller...")
    
    try:
        from system_controller import SystemController
        controller = SystemController()
        
        # Test system info
        info = controller.get_system_info()
        if info and info.get('success'):
            print("✅ System controller working correctly")
            print(f"   - System: {info.get('info', {}).get('system', 'Unknown')}")
            return True
        else:
            print("❌ System controller not responding")
            return False
            
    except Exception as e:
        print(f"❌ System controller test failed: {e}")
        return False

def test_audio_devices():
    """Test audio device availability."""
    print("\nTesting audio devices...")
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        
        # Check input devices
        input_devices = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        # Check output devices
        output_devices = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(device_info['name'])
        
        p.terminate()
        
        if input_devices:
            print(f"✅ Input devices found: {len(input_devices)}")
            print(f"   - Default: {input_devices[0]}")
        else:
            print("❌ No input devices found")
            return False
        
        if output_devices:
            print(f"✅ Output devices found: {len(output_devices)}")
            print(f"   - Default: {output_devices[0]}")
        else:
            print("❌ No output devices found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Jarvis Assistant Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Module Test", test_jarvis_modules),
        ("Configuration Test", test_configuration),
        ("Command Processor Test", test_command_processor),
        ("Weather Service Test", test_weather_service),
        ("System Controller Test", test_system_controller),
        ("Audio Devices Test", test_audio_devices)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Jarvis is ready to use.")
        print("\nTo start Jarvis, run:")
        print("   python jarvis.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Configure API keys in config.py or environment variables")
        print("3. Check microphone and speaker connections")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 