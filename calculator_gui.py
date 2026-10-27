import tkinter as tk
from tkinter import messagebox
import math
import pyttsx3
import threading
import speech_recognition as sr

class AccessibleVoiceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Accessible Voice Calculator")
        self.root.geometry("400x600")
        self.root.config(bg="#1E1E2E")
        self.root.resizable(False, False)

        # Initialize TTS Engine safely in a background thread handler
        self.tts_lock = threading.Lock()
        
        # Expression variables
        self.expression = ""
        self.result_var = tk.StringVar(value="0")

        self.create_widgets()
        self.speak("Voice calculator ready.")

    def speak(self, text):
        """Spokes text out loud asynchronously so it never freezes the GUI."""
        def _speak():
            with self.tts_lock:
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 175) # Comfortable speaking speed
                    engine.say(str(text))
                    engine.runAndWait()
                except Exception as e:
                    print(f"TTS Error: {e}")
        
        threading.Thread(target=_speak, daemon=True).start()

    def create_widgets(self):
        # --- Display Screen ---
        display_frame = tk.Frame(self.root, bg="#181825", bd=2, relief=tk.SOLID)
        display_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_label = tk.Label(
            display_frame, 
            textvariable=self.result_var, 
            font=("Consolas", 28, "bold"), 
            bg="#181825", 
            fg="#89B4FA", 
            anchor="e", 
            justify="right"
        )
        self.display_label.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Keypad Frame ---
        btn_frame = tk.Frame(self.root, bg="#1E1E2E")
        btn_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Button layout definition: (Text, Row, Column, Spoken Name)
        buttons = [
            ("C", 0, 0, "Clear"), ("(", 0, 1, "Open parenthesis"), (")", 0, 2, "Close parenthesis"), ("÷", 0, 3, "Divided by"),
            ("7", 1, 0, "7"), ("8", 1, 1, "8"), ("9", 1, 2, "9"), ("×", 1, 3, "Times"),
            ("4", 2, 0, "4"), ("5", 2, 1, "5"), ("6", 2, 2, "6"), ("-", 2, 3, "Minus"),
            ("1", 3, 0, "1"), ("2", 3, 1, "2"), ("3", 3, 2, "3"), ("+", 3, 3, "Plus"),
            ("±", 4, 0, "Plus minus"), ("0", 4, 1, "0"), (".", 4, 2, "Point"), ("=", 4, 3, "Equals")
        ]

        for (text, row, col, spoken_name) in buttons:
            btn = tk.Button(
                btn_frame, 
                text=text, 
                font=("Arial", 18, "bold"), 
                bg="#313244", 
                fg="#CDD6F4", 
                activebackground="#89B4FA",
                activeforeground="#11111B",
                bd=0,
                command=lambda t=text, s=spoken_name: self.on_button_click(t, s)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        # Configure grid weights for uniform resizing
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        # --- Voice Command Button ---
        voice_btn = tk.Button(
            self.root, 
            text="🎙️ Speak Expression", 
            font=("Arial", 14, "bold"), 
            bg="#89B4FA", 
            fg="#11111B", 
            bd=0,
            command=self.listen_voice_input
        )
        voice_btn.pack(fill="x", padx=20, pady=15)

    def on_button_click(self, char, spoken_name):
        """Handles button interaction, updates display, and triggers audio feedback."""
        # Speak the button name out loud immediately
        self.speak(spoken_name)

        if char == "C":
            self.expression = ""
            self.result_var.set("0")
        elif char == "=":
            self.calculate()
        elif char == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.result_var.set(self.expression)
        else:
            # Map visual symbols to valid python operators
            op_map = {'×': '*', '÷': '/'}
            actual_char = op_map.get(char, char)
            self.expression += actual_char
            self.result_var.set(self.expression)

    def calculate(self):
        """Evaluates mathematical expression safely and speaks the result."""
        try:
            # Evaluate expression safely
            res = eval(self.expression, {"__builtins__": None}, {"math": math})
            formatted_res = f"{res:.6g}" if isinstance(res, float) else str(res)
            self.result_var.set(formatted_res)
            self.expression = formatted_res
            
            # Speak the result out loud
            self.speak(f"Equals {formatted_res}")
        except ZeroDivisionError:
            self.result_var.set("Error")
            self.speak("Error. Division by zero.")
            self.expression = ""
        except Exception:
            self.result_var.set("Error")
            self.speak("Syntax error.")
            self.expression = ""

    def listen_voice_input(self):
        """Listens for voice commands through the microphone."""
        self.speak("Listening...")
        def _listen():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    
                    # Parse spoken text into math expression
                    parsed = text.lower().replace("times", "*").replace("multiplied by", "*")\
                                        .replace("divided by", "/").replace("plus", "+")\
                                        .replace("minus", "-").replace(" ", "")
                    
                    self.root.after(0, lambda: self.apply_voice_result(text, parsed))
                except sr.WaitTimeoutError:
                    self.speak("Listening timed out.")
                except sr.UnknownValueError:
                    self.speak("Could not understand audio.")
                except Exception as e:
                    self.speak("Speech recognition error.")
                    print(e)

        threading.Thread(target=_listen, daemon=True).start()

    def apply_voice_result(self, raw_text, parsed_expr):
        self.speak(f"You said {raw_text}")
        self.expression = parsed_expr
        self.calculate()

if __name__ == "__main__":
    root = tk.Tk()
    app = AccessibleVoiceCalculator(root)
    root.mainloop()