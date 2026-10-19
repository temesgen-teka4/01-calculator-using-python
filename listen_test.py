import speech_recognition as sr

# 1. Initialize the recognizer
recognizer = sr.Recognizer()

# 2. Use the microphone as the audio source
with sr.Microphone() as source:
    print("🎤 Adjusting for background noise... Please wait.")
    # Calibrates the microphone to the room's ambient noise level
    recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("🎙️ Listening... Speak something now!")
    # Capture the audio from your mic
    audio_data = recognizer.listen(source)
    print("⏳ Processing what you said...")

try:
    # 3. Use Google's speech recognition engine to convert audio to text
    text = recognizer.recognize_google(audio_data)
    print(f"✅ You said: '{text}'")

except sr.UnknownValueError:
    print("❌ Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print(f"❌ Could not request results from speech recognition service; {e}")