# Google vs Vosk Speech Recognition Guide

## 🎯 **Recommendation: Use Google Speech Recognition**

Based on your testing, **Google Speech Recognition is more accurate** and is now set as the default.

## 📊 **Comparison**

| Feature | Google Speech Recognition | Vosk (Offline) |
|---------|---------------------------|----------------|
| **Accuracy** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| **Internet Required** | ❌ Yes | ✅ No |
| **Cost** | ✅ Free (60 min/day) | ✅ Free |
| **Privacy** | ❌ Data sent to Google | ✅ Local processing |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Slower |
| **Background Noise** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |

## 💰 **Google API Costs**

- **Free Tier**: 60 minutes per day (1,800 minutes per month)
- **After Free Tier**: $0.006 per 15 seconds
- **Daily Usage**: You'd need to use it for **hours every day** to hit the limit
- **Monthly Cost**: Even with heavy usage, typically under $1/month

## 🚀 **Auto-Start Setup**

### **Option 1: Quick Setup (Recommended)**
```bash
cd Jarvis
python autostart_setup.py
```
Then choose option 1 (Registry startup)

### **Option 2: Manual Setup**

1. **Create Startup Folder Shortcut:**
   - Press `Windows + R`
   - Type: `shell:startup`
   - Press Enter
   - Create a shortcut to your `jarvis.py` file

2. **Task Scheduler (More Reliable):**
   - Open Task Scheduler
   - Create Basic Task
   - Name: "Jarvis Assistant"
   - Trigger: At startup
   - Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\your\jarvis.py`

## 🔧 **Current Configuration**

Jarvis is now configured to:
1. **Use Google Speech Recognition by default**
2. **Fall back to Vosk if Google fails**
3. **Start automatically on boot** (after running autostart setup)

## 🎯 **Usage Tips**

### **Best Practices:**
- Speak clearly and at normal volume
- Minimize background noise
- Use consistent wake word: "Hey Jarvis"
- Wait for "Yes, I'm listening" before giving commands

### **Common Commands:**
```
"Hey Jarvis, what time is it?"
"Hey Jarvis, open browser"
"Hey Jarvis, what's the weather like?"
"Hey Jarvis, set timer for 30 seconds"
"Hey Jarvis, system information"
```

## 🔄 **Switching Between Systems**

If you want to switch back to Vosk:
1. Edit `jarvis.py`
2. Change the `listen_for_command()` method to use Vosk first
3. Or set an environment variable: `export JARVIS_USE_VOSK=true`

## 📈 **Performance Monitoring**

To monitor Google API usage:
1. Check your Google Cloud Console
2. Look for "Speech-to-Text API" usage
3. Set up billing alerts if needed

## 🛠️ **Troubleshooting**

### **If Google API fails:**
- Check internet connection
- Verify microphone permissions
- Jarvis will automatically fall back to Vosk

### **If auto-start doesn't work:**
- Run `autostart_setup.py` as administrator
- Check Windows startup folder
- Verify Python path in startup script

---

**Bottom Line:** Google Speech Recognition is more accurate and the free tier is generous. Use it for the best experience! 🎉 