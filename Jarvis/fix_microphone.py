"""
Microphone Permission Fixer for Jarvis
Helps fix microphone permission issues on Windows.
"""

import os
import subprocess
import sys

def open_windows_settings():
    """Open Windows microphone settings."""
    print("🔧 Opening Windows Microphone Settings...")
    
    try:
        # Try to open microphone settings directly
        subprocess.run(["start", "ms-settings:privacy-microphone"], shell=True)
        print("✅ Windows Settings opened to microphone privacy settings")
        return True
    except Exception as e:
        print(f"❌ Could not open settings automatically: {e}")
        print("Please open manually:")
        print("1. Press Windows + I")
        print("2. Go to Privacy & Security → Microphone")
        return False

def check_python_permissions():
    """Check if Python has microphone permissions."""
    print("\n🔍 Checking Python Microphone Permissions...")
    
    try:
        import speech_recognition as sr
        
        # Try to initialize microphone
        mic = sr.Microphone()
        with mic as source:
            print("✅ Microphone access test successful!")
            return True
    except Exception as e:
        print(f"❌ Microphone access test failed: {e}")
        return False

def show_fix_instructions():
    """Show detailed fix instructions."""
    print("\n" + "="*60)
    print("🔧 MICROPHONE PERMISSION FIX INSTRUCTIONS")
    print("="*60)
    print()
    print("📋 Step-by-Step Instructions:")
    print()
    print("1️⃣  Open Windows Settings:")
    print("   • Press Windows + I")
    print("   • OR right-click Start Menu → Settings")
    print()
    print("2️⃣  Navigate to Microphone Settings:")
    print("   • Click 'Privacy & Security' in left sidebar")
    print("   • Click 'Microphone'")
    print("   • OR search for 'microphone' in settings search")
    print()
    print("3️⃣  Enable Microphone Access:")
    print("   • Turn ON 'Microphone access'")
    print("   • Turn ON 'Let apps access your microphone'")
    print("   • Turn ON 'Let desktop apps access your microphone'")
    print()
    print("4️⃣  Enable Python Access:")
    print("   • Scroll down to 'Choose which apps can access your microphone'")
    print("   • Find 'Python' or 'python.exe' in the list")
    print("   • Turn ON the switch next to Python")
    print()
    print("5️⃣  Alternative Method (if Python not listed):")
    print("   • Click 'Choose which apps can access your microphone'")
    print("   • Click 'Add an app'")
    print("   • Browse to your Python installation")
    print("   • Usually found in: C:\\Users\\[username]\\AppData\\Local\\Programs\\Python\\")
    print()
    print("6️⃣  Restart Required:")
    print("   • Close this program")
    print("   • Restart your computer (recommended)")
    print("   • Run Jarvis again: python jarvis.py")
    print()
    print("="*60)

def test_microphone_after_fix():
    """Test microphone after user has applied fixes."""
    print("\n🧪 Testing Microphone After Fix...")
    print("="*40)
    
    input("Press Enter after you've applied the permission fixes...")
    
    if check_python_permissions():
        print("\n🎉 SUCCESS! Microphone is now working!")
        print("You can now run Jarvis with: python jarvis.py")
        return True
    else:
        print("\n❌ Microphone still not working.")
        print("Please try:")
        print("1. Restart your computer")
        print("2. Check if microphone is not muted")
        print("3. Try a different microphone")
        return False

def main():
    """Main function."""
    print("🎤 Jarvis Microphone Permission Fixer")
    print("="*50)
    
    # Check current status
    print("🔍 Checking current microphone status...")
    current_status = check_python_permissions()
    
    if current_status:
        print("\n✅ Microphone is already working!")
        print("You can run Jarvis with: python jarvis.py")
        return
    
    # Show instructions
    show_fix_instructions()
    
    # Offer to open settings
    print("\n🚀 Quick Actions:")
    print("1. Open Windows Settings automatically")
    print("2. Show instructions again")
    print("3. Test microphone after applying fixes")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            open_windows_settings()
        elif choice == "2":
            show_fix_instructions()
        elif choice == "3":
            test_microphone_after_fix()
            break
        elif choice == "4":
            print("Goodbye! Remember to fix the permissions before running Jarvis.")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main() 