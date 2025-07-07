import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

sample_text = "Hello! This is the Jarvis assistant."

for idx, voice in enumerate(voices):
    print(f"Testing Voice {idx}: {voice.name}")
    engine.setProperty('voice', voice.id)
    engine.say(f"This is voice number {idx}. {sample_text}")
    engine.runAndWait()
    print('-' * 40) 