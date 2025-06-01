# aria.py — version 1.2.3 (modular GUI/tray)

import os
import sys
import shutil
import time
import tempfile
import requests
from dotenv import load_dotenv

# --- Audio & Media ---
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play

# --- Whisper (Speech-to-Text) ---
try:
    import whisper
except Exception as e:
    print("\u274c Failed to load Whisper:", e)
    sys.exit(1)

# --- External APIs ---
from openai import OpenAI

# --- Internal Modules ---
from utils.logger import log_interaction, get_memory_entries, init_db, clear_memory

# --- Environment ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

client = OpenAI(api_key=OPENAI_API_KEY)
aria_spoken = False  # External GUI can toggle this

# --- Utilities ---
def debug_log(label, msg):
    if DEBUG_MODE:
        print(f"[DEBUG] {label}: {msg}")

def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("\u274c FFmpeg not found. Please install and add to PATH.")
        sys.exit(1)

# --- Core Aria Functions ---
def record_audio(filename="audio.wav", duration=5, samplerate=44100):
    try:
        print("[INFO] Listening...")
        sd.default.reset()
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        sf.write(filename, audio_data, samplerate)
        print(f"[SUCCESS] Audio recorded to: {filename}")
        return filename
    except Exception as e:
        print("[ERROR] Recording failed:", e)
        return None

def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(f"[INFO] Transcription result: {result['text']}")
    return result["text"]

def get_chatgpt_response(prompt):
    init_db()
    context = get_memory_entries()
    full_prompt = f"{context}\nUser: {prompt}\nAria:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    reply = response.choices[0].message.content
    log_interaction(prompt, reply)
    return reply

def speak_text(text):
    global aria_spoken
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            json={"text": text}
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(response.content)
            path = temp_audio.name

        audio = AudioSegment.from_file(path, format="mp3")
        play(audio)
        os.remove(path)
        print(f"[ARIA] {text}")
        aria_spoken = True
    except Exception as e:
        print("[ERROR] TTS failed:", e)

def handle_commands(prompt):
    lower = prompt.lower()
    if "clear memory" in lower:
        clear_memory()
        return "Memory cleared."
    elif "what do you remember" in lower:
        return f"Here's what I remember:\n{get_memory_entries(limit=5)}"
    elif any(x in lower for x in ["bye", "exit", "shutdown", "stop listening"]):
        speak_text("Goodbye!")
        sys.exit()
    return None

def ask_aria(text):
    command_response = handle_commands(text)
    if command_response:
        speak_text(command_response)
        return command_response
    response = get_chatgpt_response(text)
    speak_text(response)
    return response

def start_listening():
    audio_file = record_audio()
    if audio_file:
        prompt = transcribe_audio(audio_file)
        if prompt.strip():
            return ask_aria(prompt)
    return None

def stop_listening():
    print("[INFO] Stopping listening (no-op for now).")

def shutdown_aria():
    print("[INFO] Aria shutting down.")
    sys.exit()

# --- Entry Point ---
if __name__ == "__main__":
    print("[INFO] Starting Aria in tray mode...")
    import tray
    tray.create_icon().run()
