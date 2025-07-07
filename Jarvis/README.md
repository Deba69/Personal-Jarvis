# Jarvis: Python Voice Assistant

Jarvis is a modular, voice-activated desktop assistant inspired by the fictional AI from Iron Man. The goal is to create a Python-based assistant capable of executing natural language commands for tasks such as:

- Opening applications
- Controlling system settings
- Performing web automation
- Getting weather information
- Setting timers and reminders

## 🚀 Features

### Core Capabilities
- **Voice Recognition**: Speech-to-text using Google's Speech Recognition API
- **Text-to-Speech**: Natural voice responses using pyttsx3
- **Wake Word Detection**: "Hey Jarvis" activation using Porcupine
- **Natural Language Processing**: Intent recognition and command parsing

### System Control (with Safety Features)
- **Browser Control**: Open web browsers and navigate to websites
- **Application Launch**: Open system applications (notepad, calculator, paint, etc.)
- **System Information**: Get detailed system specs and status
- **Volume Control**: Adjust system volume levels
- **Timer Functionality**: Set countdown timers with voice notifications
- **System Shutdown/Restart**: With double confirmation for safety

### Information Services
- **Time & Date**: Get current time and date information
- **Weather Information**: Real-time weather data using OpenWeatherMap API
- **System Status**: Memory usage, platform information

### Safety Features
- **Double Confirmation**: Critical operations require voice confirmation
- **Timeout Protection**: Automatic cancellation of pending operations
- **Error Handling**: Graceful fallbacks for failed operations
- **Cross-Platform Support**: Windows, macOS, and Linux compatibility

## 📋 Requirements

### Python Dependencies
```
SpeechRecognition
pyttsx3
pvporcupine
pyaudio
requests
```

### System Requirements
- Python 3.7 or higher
- Microphone and speakers
- Internet connection (for speech recognition and weather)

### Optional Dependencies
- `psutil` (for detailed system information)
- `spacy` or `nltk` (for advanced NLP)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Jarvis
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys** (Optional but recommended):
   
   **For Wake Word Detection (Porcupine)**:
   - Get a free API key from [Picovoice Console](https://console.picovoice.ai/)
   - Set environment variable: `export PORCUPINE_ACCESS_KEY="your_key_here"`
   
   **For Weather Information (OpenWeatherMap)**:
   - Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Set environment variable: `export OPENWEATHERMAP_API_KEY="your_key_here"`

4. **Install as Windows Service** (for automatic startup):
   ```bash
   # Run as Administrator
   python install_service.py install
   ```

   Or manually:
   ```bash
   # Run as Administrator
   python jarvis_service.py install
   python jarvis_service.py start
   ```

5. **Run Jarvis**:
   ```bash
   python jarvis.py
   ```

## 🎯 Usage Examples

### Basic Commands
```
"Hey Jarvis, what time is it?"
"Hey Jarvis, what's the date today?"
"Hey Jarvis, hello"
"Hey Jarvis, goodbye"
```

### Weather Information
```
"Hey Jarvis, what's the weather like?"
"Hey Jarvis, weather in New York"
"Hey Jarvis, temperature in London"
```

### System Control
```
"Hey Jarvis, open browser"
"Hey Jarvis, open notepad"
"Hey Jarvis, open calculator"
"Hey Jarvis, system information"
"Hey Jarvis, set volume to 50"
```

### Timer Functionality
```
"Hey Jarvis, set timer for 30 seconds"
"Hey Jarvis, timer for 5 minutes"
"Hey Jarvis, wake me up in 1 hour"
```

### System Operations (with Safety Confirmation)
```
"Hey Jarvis, shutdown computer"
"Hey Jarvis, restart computer"
"Hey Jarvis, cancel shutdown"
```

## 🔧 Configuration

The assistant can be configured through the `config.py` file or environment variables:

### Key Settings
- **Speech Recognition**: Timeout, phrase limits, noise adjustment
- **Text-to-Speech**: Speech rate, volume, voice selection
- **Safety**: Confirmation timeouts, operation delays
- **Features**: Enable/disable specific capabilities

### Environment Variables
```bash
export PORCUPINE_ACCESS_KEY="your_porcupine_key"
export OPENWEATHERMAP_API_KEY="your_weather_key"
export JARVIS_LOG_LEVEL="INFO"
```

## 🏗️ Project Structure

```
Jarvis/
├── jarvis.py              # Main application entry point
├── command_processor.py   # Command parsing and intent recognition
├── weather_service.py     # Weather API integration
├── system_controller.py   # System control operations
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── install_service.py     # Service installation script
└── README.md            # This file
```

## 🔒 Safety Features

### Critical Operation Protection
- **Double Confirmation**: System shutdown/restart requires voice confirmation
- **Timeout Protection**: Pending operations auto-cancel after 30 seconds
- **Error Handling**: Graceful fallbacks prevent system damage
- **Platform Detection**: Automatic OS-specific command selection

### Example Safety Flow
1. User: "Hey Jarvis, shutdown computer"
2. Jarvis: "I heard you want to shutdown the computer. This is a critical operation. Please confirm by saying 'yes, shutdown' or 'confirm shutdown'."
3. User: "Yes, shutdown"
4. Jarvis: "Shutdown confirmed. Shutting down the system in 5 seconds."

## 🐛 Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**:
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install python3-pyaudio
```

**"Porcupine access key not configured"**:
- Get a free key from [Picovoice Console](https://console.picovoice.ai/)
- Set the environment variable or update config.py

**"Weather API not working"**:
- Get a free key from [OpenWeatherMap](https://openweathermap.org/api)
- Set the environment variable or update config.py

**"Microphone not detected"**:
- Check microphone permissions
- Ensure microphone is set as default input device
- Test with system audio settings

### Debug Mode
Enable debug logging by setting `JARVIS_LOG_LEVEL="DEBUG"` environment variable.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Porcupine**: Wake word detection by Picovoice
- **Google Speech Recognition**: Speech-to-text conversion
- **OpenWeatherMap**: Weather data API
- **pyttsx3**: Text-to-speech functionality

## 🚀 Future Enhancements

- [ ] Web search integration
- [ ] Email and calendar management
- [ ] Smart home device control
- [ ] Music playback control
- [ ] Advanced NLP with spaCy
- [ ] Custom wake word training
- [ ] GUI interface
- [ ] Plugin system for extensibility

---

**Note**: This is a personal assistant project. Use system control features responsibly and always ensure you have proper backups before performing critical operations.

### As a Windows Service (Recommended)

Once installed as a service, Jarvis will:
- Start automatically when Windows boots
- Run in the background continuously
- Listen for the wake word "Hey Jarvis"
- Respond to voice commands without manual intervention

**Service Management**:
```bash
# Check service status
python jarvis_service.py status

# Stop the service
python jarvis_service.py stop

# Start the service
python jarvis_service.py start

# Restart the service
python jarvis_service.py restart

# Remove the service
python jarvis_service.py remove
```

### Manual Mode

Run Jarvis manually for testing:
```bash
python jarvis.py
```

## Voice Commands

### Basic Commands
- **"Hey Jarvis"** - Wake word to activate
- **"What time is it?"** - Get current time
- **"What's the weather?"** - Get weather information
- **"Set a timer for X minutes"** - Set a timer
- **"Cancel timer"** - Cancel active timer

### System Commands
- **"Shutdown computer"** - Shutdown the system
- **"Restart computer"** - Restart the system
- **"Cancel operation"** - Cancel pending system operations
- **"Volume up/down"** - Adjust system volume

### Exit Commands
- **"Goodbye"** - Exit Jarvis
- **"Exit"** - Exit Jarvis
- **"Stop listening"** - Exit Jarvis

## Configuration

### Microphone Settings

If Jarvis can't access your microphone:

1. **Windows Settings** → **Privacy & Security** → **Microphone**
2. Enable **"Microphone access"**
3. Enable **"Let apps access your microphone"**
4. Enable **"Let desktop apps access your microphone"**
5. Find **Python** in the app list and enable it

### Wake Word Detection

The wake word detection uses Porcupine with a free access key. For production use, consider:
- Getting your own access key from [Picovoice Console](https://console.picovoice.ai/)
- Training custom wake words
- Adjusting sensitivity settings

## Troubleshooting

### Service Issues

1. **Check logs**: `%APPDATA%\Local\Jarvis\logs\jarvis_service.log`
2. **Verify microphone permissions**
3. **Run as Administrator** when installing/removing service
4. **Check Windows Services** (services.msc) for "Jarvis Voice Assistant"

### Common Problems

- **"Microphone not available"**: Check Windows microphone permissions
- **"Wake word detection not available"**: Verify Porcupine installation
- **"Service failed to start"**: Check logs and run as Administrator

## File Structure

```
Jarvis/
├── jarvis.py              # Main Jarvis application
├── jarvis_service.py      # Windows service wrapper
├── install_service.py     # Service installation script
├── command_processor.py   # Command processing logic
├── system_controller.py   # System control functions
├── weather_service.py     # Weather API integration
├── requirements.txt       # Python dependencies
├── models/               # Vosk speech recognition models
└── README.md            # This file
```

## Development

### Adding New Commands

1. Edit `command_processor.py` to add new command patterns
2. Implement corresponding functions in `system_controller.py`
3. Test with voice commands

### Customizing Wake Word

1. Get access key from [Picovoice Console](https://console.picovoice.ai/)
2. Update `PORCUPINE_ACCESS_KEY` in `jarvis.py`
3. Optionally train custom wake words

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `%APPDATA%\Local\Jarvis\logs\`
3. Verify all dependencies are installed correctly 