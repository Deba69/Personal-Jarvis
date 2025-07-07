"""
Simple Microphone Test for Jarvis
Tests if microphone is working and accessible.
"""

import pyaudio
import wave
import time

def test_microphone():
    """Test microphone access and recording."""
    print("🎤 Testing Microphone Access...")
    print("=" * 40)
    
    try:
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # List available audio devices
        print("📋 Available Audio Devices:")
        print("-" * 20)
        
        input_devices = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append((i, device_info))
                print(f"Input Device {i}: {device_info['name']}")
        
        if not input_devices:
            print("❌ No input devices found!")
            return False
        
        # Use the first available input device
        device_index = input_devices[0][0]
        device_name = input_devices[0][1]['name']
        
        print(f"\n🎯 Using device: {device_name}")
        
        # Test recording
        print("\n🎙️  Testing recording (5 seconds)...")
        print("Please speak into your microphone...")
        
        # Recording parameters
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        
        # Open stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK
        )
        
        print("🔴 Recording started...")
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            # Show progress
            if i % 10 == 0:
                print(f"Recording... {i//10 + 1}/5 seconds")
        
        print("✅ Recording completed!")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Save the recorded data as a WAV file
        output_filename = "test_recording.wav"
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"💾 Recording saved as: {output_filename}")
        
        # Clean up
        p.terminate()
        
        print("\n✅ Microphone test completed successfully!")
        print("🎉 Your microphone is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Microphone test failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check microphone permissions in Windows Settings")
        print("2. Make sure microphone is not muted")
        print("3. Try a different microphone if available")
        print("4. Restart your computer and try again")
        
        return False

def check_permissions():
    """Check microphone permissions."""
    print("\n🔐 Checking Microphone Permissions...")
    print("=" * 40)
    
    print("To enable microphone access:")
    print("1. Press Windows + I to open Settings")
    print("2. Go to Privacy & Security → Microphone")
    print("3. Turn ON 'Microphone access'")
    print("4. Turn ON 'Let apps access your microphone'")
    print("5. Turn ON 'Let desktop apps access your microphone'")
    print("6. Find 'Python' in the app list and turn it ON")
    
    print("\nAlternative method:")
    print("1. Right-click on Start Menu")
    print("2. Select 'Settings'")
    print("3. Search for 'microphone'")
    print("4. Click on 'Microphone privacy settings'")
    print("5. Enable all microphone permissions")

if __name__ == "__main__":
    print("🎤 Jarvis Microphone Test")
    print("=" * 40)
    
    # Check permissions first
    check_permissions()
    
    # Test microphone
    input("\nPress Enter to test microphone recording...")
    success = test_microphone()
    
    if success:
        print("\n🎉 Great! Your microphone is working.")
        print("You can now run Jarvis with: python jarvis.py")
    else:
        print("\n⚠️  Please fix the microphone issues before running Jarvis.")
    
    input("\nPress Enter to exit...") 