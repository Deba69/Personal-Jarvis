import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("Available voices:")
for idx, voice in enumerate(voices):
    print(f"Voice {idx}:")
    print(f"  Name: {voice.name}")
    print(f"  ID: {voice.id}")
    print(f"  Languages: {voice.languages}")
    print(f"  Gender: {getattr(voice, 'gender', 'Unknown')}")
    print(f"  Age: {getattr(voice, 'age', 'Unknown')}")
    print('-' * 40) 