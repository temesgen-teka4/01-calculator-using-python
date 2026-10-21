import speech_recognition as sr
import pyttsx3
import math

def speak(text):
    """A helper function to make the computer speak out loud and re-bind to active audio"""
    print(f"🤖 Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    """A helper function to listen to your voice and turn it into text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        print("🎙️ Listening...")
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
    """Advanced text parser supporting arithmetic, exponents, roots, and mod"""
    # 1. Basic Arithmetic
    command = command.replace("plus", "+").replace("add", "+")
    command = command.replace("minus", "-").replace("subtract", "-")
    command = command.replace("times", "*").replace("multiplied by", "*").replace("multiplied", "*")
    command = command.replace("divided by", "/").replace("divide", "/")
    
    # 2. Advanced Operations (Powers & Modulus)
    command = command.replace("to the power of", "**").replace("power of", "**").replace("power", "**")
    command = command.replace("squared", "**2").replace("cubed", "**3")
    command = command.replace("modulus", "%").replace("mod", "%")
    
    # 3. Handle Square Roots Spoken Phrases (e.g., "square root of 25" -> "math.sqrt(25)")
    if "square root of" in command:
        command = command.replace("square root of", "math.sqrt(") + ")"
    elif "sqrt of" in command:
        command = command.replace("sqrt of", "math.sqrt(") + ")"

    # Filter out unsafe characters while keeping numbers, math symbols, and math module syntax
    allowed_chars = "0123456789+-*/().mathsqrtt "
    cleaned_command = "".join([char for char in command if char in allowed_chars])
    
    try:
        # Senior Dev Practice: Restrict eval() scope for security, 
        # giving it access ONLY to basic math and Python's built-in 'math' module.
        safe_context = {
            "__builtins__": None,
            "math": math
        }
        
        result = eval(cleaned_command, safe_context, {})
        return result
    except Exception as e:
        print(f"Calculation Error: {e}")
        return None

# --- Main Conversational Program Loop ---
if __name__ == "__main__":
    speak("Advanced voice calculator is online. What would you like to calculate?")
    
    while True:
        spoken_text = listen()
        
        if spoken_text:
            exit_keywords = ['quit', 'q', 'exit', 'stop', 'goodbye']
            if any(keyword in spoken_text for keyword in exit_keywords):
                speak("Goodbye! Calculator is shutting down.")
                break
            
            answer = calculate(spoken_text)
            
            if answer is not None:
                # Format floating point numbers nicely if they are whole numbers
                if isinstance(answer, float) and answer.is_integer():
                    answer = int(answer)
                    
                response_text = f"The answer is {answer}"
                print(f"✨ Result: {response_text}")
                speak(f"{response_text}. What is your next calculation, or say exit to finish?")
            else:
                speak("I couldn't find a valid math problem in that sentence. Please try another one.")