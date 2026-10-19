import speech_recognition as sr
import pyttsx3

# Initialize the Text-to-Speech engine (The Mouth)
engine = pyttsx3.init()

def speak(text):
    """A helper function to make the computer speak out loud"""
    print(f"🤖 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """A helper function to listen to your voice and turn it into text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        print("🎙️ Listening for your math problem... (e.g., '10 plus 5')")
        audio = recognizer.listen(source)
        
    try:
        print("⏳ Translating your voice...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: '{text}'")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said. Please try again.")
        return None
    except sr.RequestError:
        speak("Network connection error. Check your internet.")
        return None

def calculate(command):
    """Simple text parser to handle basic math operations"""
    # Replace common spoken words with math operators
    command = command.replace("plus", "+").replace("add", "+")
    command = command.replace("minus", "-").replace("subtract", "-")
    command = command.replace("times", "*").replace("multiplied by", "*").replace("multiplied", "*")
    command = command.replace("divided by", "/").replace("divide", "/")
    
    # Filter out anything that isn't a number or safe math symbol
    # (A basic and safe way to evaluate simple expressions in Python)
    allowed_chars = "0123456789+-*/. "
    cleaned_command = "".join([char for char in command if char in allowed_chars])
    
    try:
        # eval() safely calculates our cleaned math string
        result = eval(cleaned_command)
        return result
    except Exception as e:
        print(f"Calculation Error: {e}")
        return None

# --- Main Program Loop ---
if __name__ == "__main__":
    speak("Voice calculator is online.")
    
    # Listen for a command
    spoken_text = listen()
    
    if spoken_text:
        # Calculate the result
        answer = calculate(spoken_text)
        
        if answer is not None:
            response_text = f"The answer is {answer}"
            print(f"✨ Result: {response_text}")
            speak(response_text)
        else:
            speak("I couldn't find a valid math problem in that sentence.")