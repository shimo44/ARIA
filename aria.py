# --- Environment & Config ---
import os
import sys
import shutil
import time
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# --- External APIs ---
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
import requests

# --- Audio & Media ---
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# --- Whisper (Speech-to-Text) ---
try:
    import whisper
except Exception as e:
    print("❌ Failed to load Whisper:", e)
    sys.exit(1)

# --- Internal Modules ---
from utils.logger import (
    log_interaction,
    get_memory_entries,
    init_db,
    clear_memory
)

# --- System Checks ---
def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("❌ FFmpeg not found. Please install FFmpeg and add it to your system PATH.")
        print("Download: https://ffmpeg.org/download.html")
        sys.exit(1)

def debug_log(label, msg):
    if DEBUG_MODE:
        print(f"[DEBUG] {label}: {msg}")

# --- Core Functions ---
def record_audio(filename="audio.wav", duration=5, samplerate=44100):
    print("[INFO] Listening...")
    try:
        sd.default.reset()
        start = time.time()
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        sf.write(filename, audio_data, samplerate)
        elapsed = time.time() - start
        print(f"[SUCCESS] Audio recorded to: {filename}")
        debug_log("Recording duration", f"{elapsed:.2f}s")
        return filename
    except Exception as e:
        print("[ERROR] Recording failed:", e)
        return None

def transcribe_audio(filename):
    debug_log("Loading Whisper model", "base")
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    debug_log("Raw Whisper output", str(result))
    print(f"[INFO] Transcription result: {result['text']}")
    return result["text"]

def get_chatgpt_response(prompt):
    init_db()
    context = get_memory_entries()
    full_prompt = f"{context}\nUser: {prompt}\nAria:"

    start = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    reply = response.choices[0].message.content
    elapsed = time.time() - start

    log_interaction(prompt, reply)
    debug_log("GPT latency", f"{elapsed:.2f}s")
    debug_log("GPT response", reply)
    return reply

def speak_text(text):
    try:
        debug_log("Sending to ElevenLabs", text)
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            json={"text": text}
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(response.content)
            path = temp_audio.name

        print(f"[ARIA] {text}")
        audio = AudioSegment.from_file(path, format="mp3")
        play(audio)
        os.remove(path)
    except Exception as e:
        print("[ERROR] Text-to-speech failed:", e)

def handle_commands(prompt):
    lower_prompt = prompt.lower()

    if "clear memory" in lower_prompt:
        clear_memory()
        return "Memory has been cleared."

    elif "what do you remember" in lower_prompt:
        memory = get_memory_entries(limit=5)
        return f"Here's what I remember:\n{memory}"

    elif any(cmd in lower_prompt for cmd in ["bye", "goodbye", "exit", "shutdown", "stop listening", "bye-bye"]):
        speak_text("Goodbye!")
        exit()

    return None

# --- Main Loop ---
def main():
    print("[INFO] === Aria main() starting ===")
    check_ffmpeg()

    audio_file = record_audio()
    if not audio_file:
        print("[WARNING] No audio recorded. Skipping response.")
        return

    prompt = transcribe_audio(audio_file)
    print(f"[INFO] User said: {prompt}")

    if not prompt.strip():
        print("[WARNING] Empty speech detected. Skipping.")
        return

    command_response = handle_commands(prompt)
    if command_response:
        print(f"[ARIA] (Command) {command_response}")
        speak_text(command_response)
        print("[INFO] === Aria main() finished ===")
        return

    response = get_chatgpt_response(prompt)
    speak_text(response)
    print("[INFO] === Aria main() finished ===")
