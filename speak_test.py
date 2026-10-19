import pyttsx3

# 1. Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# 2. Tell the engine what you want it to say
text_to_speak = "Hello Temesgen! The computer is ready to talk."
engine.say(text_to_speak)

# 3. Command the engine to process and play the audio
engine.runAndWait()