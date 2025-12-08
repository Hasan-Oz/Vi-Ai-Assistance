import os
import sys
import time
import subprocess
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 1. UPDATED WAKE WORD
WAKE_WORD = "jarvis"

if not API_KEY:
    print("ERROR: API Key missing in .env file")
    sys.exit(1)

genai.configure(api_key=API_KEY)

USER_NAME = "Hasan"
# 2. UPDATED ASSISTANT NAME
ASSISTANT_NAME = "Jarvis"

# --- VOICE INITIALIZATION ---
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_found = False
    
    # Try to find a British/English voice
    for voice in voices:
        if "GB" in voice.id or "UK" in voice.id or "english-uk" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            voice_found = True
            break
            
    if not voice_found:
        engine.setProperty('voice', voices[0].id)

    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    print("[Voice Engine]: initialized.")

except Exception as e:
    print(f"[Voice Engine]: Failed. Error: {e}")
    engine = None

r = sr.Recognizer()

# --- FUNCTIONS ---

def speak(text):
    """Vocalizes text."""
    clean_text = text.replace("*", "").replace("#", "")
    print(f"\n[{ASSISTANT_NAME}]: {clean_text}")
    if engine:
        engine.say(clean_text)
        engine.runAndWait()

def listen():
    """Listens for user input."""
    with sr.Microphone() as source:
        print(f"\n[{ASSISTANT_NAME} is Listening]...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""

    try:
        print("[System]: Recognizing...")
        data = r.recognize_google(audio)
        return data.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("[System]: Speech Service Down.")
        return ""

def open_application(command):
    if "code" in command:
        speak("Opening Visual Studio Code.")
        subprocess.Popen("code", shell=True)
    elif "chrome" in command or "google" in command:
        speak("Opening Chrome.")
        subprocess.Popen("start chrome", shell=True)

def get_response(prompt):
    models_to_try = [
        "models/gemini-flash-latest",
        "models/gemini-2.0-flash-lite-preview-02-05",
        "models/gemini-1.5-flash",
        "models/gemini-pro"
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=f"You are {ASSISTANT_NAME}, an AI assistant for {USER_NAME}. Be polite, concise (max 2 sentences), and professional."
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue 
            
    return "I am unable to access any AI models."

def jarvis_core(prompt):
    if not API_KEY:
        speak("My API key is missing.")
        return
    response_text = get_response(prompt)
    speak(response_text)

# --- MAIN LOOP ---
def main_loop():
    speak(f"{ASSISTANT_NAME} Online.")
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

    while True:
        raw_input = listen()
        if not raw_input: continue

        # --- WAKE WORD CHECK ---
        if WAKE_WORD not in raw_input:
            print(f"[System]: Ignored '{raw_input}' (No Wake Word)")
            continue
        
        # Strip "jarvis" from the command
        command = raw_input.replace(WAKE_WORD, "").strip()
        print(f"[USER Command]: {command}")

        if not command:
            speak("Yes, Sir?")
            continue

        # --- COMMANDS ---

        # 1. STOP THE SCRIPT
        if any(word in command for word in ["shutdown", "shut down", "stop", "exit", "quit", "terminate"]):
            speak("Disconnecting. Goodbye, Sir.")
            break 

        # 2. Local Apps
        if "open" in command and ("code" in command or "chrome" in command):
            open_application(command)
            continue

        # 3. Time & Date
        if "time" in command:
            now = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {now}, Sir.")
            continue

        if "date" in command:
            today = datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}.")
            continue 

        # 4. AI Core
        jarvis_core(command)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[System]: Process terminated by user.")
        sys.exit(0)