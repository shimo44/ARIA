# --- Environment & Config ---
import os
import sys
import shutil
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

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
import datetime

# --- Whisper (Speech-to-Text) ---
try:
    import whisper
    model = whisper.load_model("base")
except Exception as e:
    print("\u274c Failed to load Whisper:", e)
    model = None

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
        print("\u274c FFmpeg not found. Please install FFmpeg and add it to your system PATH.")
        print("Download: https://ffmpeg.org/download.html")
        sys.exit(1)

# --- Core Functions ---
def record_audio(filename="audio.wav", duration=5, samplerate=44100):
    print("Listening...")
    try:
        sd.default.reset()
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        sf.write(filename, audio_data, samplerate)
        print(f"Audio recorded to: {filename}")
        return filename
    except Exception as e:
        print("Recording failed:", e)
        return None

def transcribe_audio(filename):
    if model is None:
        print("\u274c Whisper model not loaded. Cannot transcribe.")
        return ""
    result = model.transcribe(filename)
    print(f"Transcription result: {result['text']}")
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
    print(f"GPT Response: {reply}")
    log_interaction(prompt, reply)
    return reply

def speak_text(text):
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        json={"text": text}
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio.write(response.content)
        temp_audio_path = temp_audio.name

    print(f"Speaking this text: {text}")
    audio = AudioSegment.from_file(temp_audio_path, format="mp3")
    play(audio)
    os.remove(temp_audio_path)

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
    print("=== Aria main() starting ===")
    check_ffmpeg()

    audio_file = record_audio()
    if not audio_file:
        print("No audio recorded. Skipping response.")
        return

    prompt = transcribe_audio(audio_file)
    print(f"User said: {prompt}")

    if not prompt.strip():
        print("\u274c No speech detected. Skipping response.")
        return

    command_response = handle_commands(prompt)
    if command_response:
        print(f"Aria (Command): {command_response}")
        speak_text(command_response)
        print("=== Aria main() finished ===")
        return

    response = get_chatgpt_response(prompt)
    print(f"Aria: {response}")
    speak_text(response)
    print("=== Aria main() finished ===")
