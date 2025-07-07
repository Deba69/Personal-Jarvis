"""
Jarvis: Python Voice Assistant
Main entry point for the assistant. Handles voice input, text-to-speech, and command processing.
"""

import speech_recognition as sr
import pyttsx3
import pvporcupine
import pyaudio
import time
import threading
import subprocess
import platform
import os
from datetime import datetime
from command_processor import CommandProcessor

# Try to import Vosk for better speech recognition
try:
    import vosk
    VOSK_AVAILABLE = True
    print("[OK] Vosk speech recognition available")
except ImportError:
    VOSK_AVAILABLE = False
    print("[WARNING] Vosk not available, using Google Speech Recognition")

# Replace with your Porcupine Access Key from https://console.picovoice.ai/
PORCUPINE_ACCESS_KEY = "KKyC6QjCjoAvip84bsLMJ6O4EmrCKmsk5rds9pnYdGI+YmqG3wj6IA=="

class JarvisAssistant:
    def __init__(self):
        """Initialize Jarvis assistant with speech recognition and TTS."""
        self.recognizer = sr.Recognizer()
        
        # Initialize Vosk model if available
        self.vosk_model = None
        self.vosk_recognizer = None
        if VOSK_AVAILABLE:
            try:
                model_path = os.path.join(os.path.dirname(__file__), "models")
                if os.path.exists(model_path):
                    self.vosk_model = vosk.Model(model_path)
                    self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
                    print("[OK] Vosk model loaded successfully")
                else:
                    print("[WARNING] Vosk model not found in models directory")
            except Exception as e:
                print(f"[WARNING] Could not load Vosk model: {e}")
        
        # Initialize microphone with better error handling
        try:
            self.microphone = sr.Microphone()
            # Test microphone access
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            self.microphone_available = True
            print("[OK] Microphone initialized successfully")
        except Exception as e:
            print(f"[ERROR] Microphone initialization failed: {e}")
            print("[INFO] Please check microphone permissions in Windows Settings")
            self.microphone = None
            self.microphone_available = False
        
        self.engine = pyttsx3.init()
        self.command_processor = CommandProcessor()
        
        # Configure TTS engine
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
        
        # Get available voices and set a good one
        voices = self.engine.getProperty('voices')
        if voices and len(voices) > 2:
            # Set to Microsoft Zira Desktop (voice index 2)
            self.engine.setProperty('voice', voices[2].id)
        elif voices:
            self.engine.setProperty('voice', voices[0].id)  # Fallback to first available voice
        
        # Initialize wake word detection
        try:
            self.porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
                keyword_paths=None,
        keywords=["jarvis"]
    )
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            self.wake_word_available = True
            print("[OK] Wake word detection initialized")
        except Exception as e:
            print(f"[WARNING] Wake word detection not available: {e}")
            self.wake_word_available = False
        
        self.is_listening = False
        self.running = True
        self.active_timer = None

    def speak(self, text):
        """Convert text to speech."""
        print(f"Jarvis: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError as e:
            print(f"TTS error: {e} (ignoring)")

    def listen_for_wake_word(self):
        """Listen for wake word using Porcupine."""
        if not self.wake_word_available:
            return False
            
        try:
            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = memoryview(pcm)
            pcm = [int.from_bytes(pcm[i:i+2], 'little', signed=True) for i in range(0, len(pcm), 2)]
            result = self.porcupine.process(pcm)
            return result >= 0
        except Exception as e:
            print(f"Error in wake word detection: {e}")
            return False

    def listen_for_command(self):
        """Listen for voice command and convert to text."""
        if not self.microphone_available:
            print("[ERROR] Microphone not available. Please check permissions.")
            self.speak("I cannot access your microphone. Please check your microphone permissions in Windows Settings.")
            return None
        
        # Use Google Speech Recognition by default (more accurate)
        # Fall back to Vosk only if Google fails
        try:
            return self._listen_with_google()
        except Exception as e:
            print(f"Google Speech Recognition failed: {e}")
            if self.vosk_recognizer:
                print("Falling back to Vosk...")
                return self._listen_with_vosk()
            else:
                return None
    
    def _listen_with_vosk(self):
        """Listen for command using Vosk (offline)."""
        try:
            print("Listening for command (Vosk)...")
            
            # Set up audio stream for Vosk
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000
            )
            
            # Listen for audio
            audio_data = b""
            silence_threshold = 0
            silence_counter = 0
            
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                audio_data += data
                
                # Process with Vosk
                if self.vosk_recognizer.AcceptWaveform(data):
                    result = self.vosk_recognizer.Result()
                    if result and '"text"' in result:
                        import json
                        result_json = json.loads(result)
                        text = result_json.get('text', '').strip()
                        if text:
                            print(f"You said: {text}")
                            stream.stop_stream()
                            stream.close()
                            p.terminate()
                            return text.lower()
                
                # Check for silence to stop listening
                silence_counter += 1
                if silence_counter > 20:  # About 2.5 seconds of silence
                    break
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Get final result
            final_result = self.vosk_recognizer.FinalResult()
            if final_result and '"text"' in final_result:
                import json
                result_json = json.loads(final_result)
                text = result_json.get('text', '').strip()
                if text:
                    print(f"You said: {text}")
                    return text.lower()
            
            print("No speech detected")
            return None
            
        except Exception as e:
            print(f"Error in Vosk speech recognition: {e}")
            return None
    
    def _listen_with_google(self):
        """Listen for command using Google Speech Recognition."""
        try:
            with self.microphone as source:
                print("Listening for command (Google)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Processing command...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None

    def execute_action(self, result):
        """Execute the action based on command processor result."""
        action = result.get('action', 'speak')
        response = result.get('response', '')
        
        if action == 'speak':
            self.speak(response)
        elif action == 'exit':
            self.speak(response)
            self.running = False
        elif action == 'timer':
            duration = result.get('duration', 30)
            self.speak(response)
            self.start_timer(duration)
        elif action == 'shutdown':
            self.speak(response)
            time.sleep(5)  # Give user time to cancel
            self.shutdown_system()
        elif action == 'restart':
            self.speak(response)
            time.sleep(5)  # Give user time to cancel
            self.restart_system()
        elif action == 'cancel_operation':
            self.speak(response)
            # Try to cancel any pending system operations
            try:
                if platform.system() == "Windows":
                    subprocess.run(["shutdown", "/a"], check=True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["killall", "shutdown"], check=True)
                else:  # Linux
                    subprocess.run(["shutdown", "-c"], check=True)
                self.speak("System operation cancelled successfully.")
            except Exception as e:
                self.speak("No pending system operations to cancel.")
        elif action == 'volume_up':
            self.speak(response)
            # Implement volume up logic
            self.speak("Volume up functionality not fully implemented yet.")
        elif action == 'volume_down':
            self.speak(response)
            # Implement volume down logic
            self.speak("Volume down functionality not fully implemented yet.")
        else:
            self.speak(response)

    def start_timer(self, duration):
        """Start a timer in a separate thread."""
        if self.active_timer and self.active_timer.is_alive():
            self.speak("There's already an active timer. I'll start a new one.")
        
        self.active_timer = threading.Timer(duration, self.timer_finished)
        self.active_timer.start()
        print(f"Timer started for {duration} seconds")

    def timer_finished(self):
        """Called when timer finishes."""
        self.speak("Timer finished! Time's up!")

    def shutdown_system(self):
        """Safely shutdown the system."""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                subprocess.run(["shutdown", "-h", "now"], check=True)
        except Exception as e:
            print(f"Error shutting down system: {e}")
            self.speak("Sorry, I couldn't shutdown the system. Please do it manually.")

    def restart_system(self):
        """Safely restart the system."""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                subprocess.run(["shutdown", "-r", "now"], check=True)
        except Exception as e:
            print(f"Error restarting system: {e}")
            self.speak("Sorry, I couldn't restart the system. Please do it manually.")

    def process_command(self, command):
        """Process the voice command using the command processor."""
        if not command:
            return
        
        # Check for confirmation commands
        if self.command_processor.pending_confirmation:
            if any(word in command for word in ['yes', 'confirm', 'proceed', 'okay', 'ok']):
                # Process the pending confirmation
                if self.command_processor.pending_confirmation == 'shutdown':
                    result = self.command_processor.shutdown_system(command, {})
                elif self.command_processor.pending_confirmation == 'restart':
                    result = self.command_processor.restart_system(command, {})
                else:
                    result = self.command_processor.process_command(command)
            else:
                # User didn't confirm, reset state
                self.command_processor.reset_confirmation_state()
                self.speak("Operation cancelled.")
                return
        else:
            # Process normal command
            result = self.command_processor.process_command(command)
        
        # Execute the action
        self.execute_action(result)

    def run(self):
        """Main loop for Jarvis assistant."""
        self.speak("Jarvis is online and ready to assist you.")
        
        # Check if microphone is available
        if not self.microphone_available:
            print("\n" + "="*60)
            print("[ERROR] MICROPHONE NOT AVAILABLE")
            print("="*60)
            print("To fix this issue:")
            print("1. Press Windows + I to open Settings")
            print("2. Go to Privacy & Security → Microphone")
            print("3. Turn ON 'Microphone access'")
            print("4. Turn ON 'Let apps access your microphone'")
            print("5. Turn ON 'Let desktop apps access your microphone'")
            print("6. Find 'Python' in the app list and turn it ON")
            print("7. Restart this program")
            print("="*60)
            
            # Provide a simple text-based interface as fallback
            print("\n[INFO] Fallback Mode: Text-based commands")
            print("Type your commands (or 'exit' to quit):")
            
            while self.running:
                try:
                    command = input("You: ").lower().strip()
                    if command in ['exit', 'quit', 'bye']:
                        self.speak("Goodbye! Have a great day!")
                        break
                    
                    self.process_command(command)
                except KeyboardInterrupt:
                    print("\nShutting down Jarvis...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
            
            return
        
        while self.running:
            try:
                # Listen for wake word
                if self.wake_word_available:
                    if self.listen_for_wake_word():
                        print("Wake word detected!")
                        self.speak("Yes, I'm listening.")
                        # Listen for command
                        command = self.listen_for_command()
                        self.process_command(command)
                else:
                    # Fallback: continuous listening without wake word
                    print("Listening for commands... (Press Ctrl+C to exit)")
                    command = self.listen_for_command()
                    self.process_command(command)
                    
            except KeyboardInterrupt:
                print("\nShutting down Jarvis...")
                self.running = False
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)

    def cleanup(self):
        """Clean up resources."""
        if self.active_timer and self.active_timer.is_alive():
            self.active_timer.cancel()
        if self.wake_word_available:
            self.audio_stream.close()
            self.pa.terminate()
            self.porcupine.delete()

def main():
    """Main entry point."""
    jarvis = JarvisAssistant()
    try:
        jarvis.run()
    finally:
        jarvis.cleanup()

if __name__ == "__main__":
    main() 