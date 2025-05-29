import os
import tempfile
from dotenv import load_dotenv
from colorama import init, Fore, Style
from utils.vad_audio import VADAudio
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import requests
import whisper
from utils.logger import log_interaction, get_memory_entries, init_db, clear_memory

init(autoreset=True)

def log_info(msg): print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + msg)
def log_success(msg): print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + msg)
def log_warning(msg): print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + msg)
def log_error(msg): print(Fore.RED + "[ERROR] " + Style.RESET_ALL + msg)
def log_speak(msg): print(Fore.MAGENTA + "[ARIA] " + Style.RESET_ALL + msg)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    model = whisper.load_model("base")
    log_success("Whisper model loaded.")
except Exception as e:
    log_error(f"Whisper failed: {e}")
    model = None

def record_audio_vad(filename="audio.wav"):
    log_info("Starting smart voice-activated recording...")
    vad = VADAudio()
    audio = vad.read_audio()
    vad.save_wav(filename, audio)
    vad.close()
    log_success(f"Audio recorded to {filename}")
    return filename

def transcribe_audio(filename):
    if model is None:
        log_error("No Whisper model available.")
        return ""
    result = model.transcribe(filename)
    log_info(f"Transcription: {result['text']}")
    return result["text"]

def speak_text(text):
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            json={"text": text}
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(response.content)
            path = temp_audio.name
        log_speak(text)
        audio = AudioSegment.from_file(path, format="mp3")
        play(audio)
        os.remove(path)
    except Exception as e:
        log_error(f"TTS failed: {e}")

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

def handle_commands(prompt):
    p = prompt.lower()
    if "clear memory" in p:
        clear_memory()
        return "Memory has been cleared."
    elif "what do you remember" in p:
        return f"Here's what I remember:\n{get_memory_entries(limit=5)}"
    elif any(x in p for x in ["bye", "goodbye", "exit", "shutdown", "stop listening", "bye-bye"]):
        speak_text("Goodbye!")
        exit()
    return None

def main():
    log_info("=== Aria main() ===")
    audio_file = record_audio_vad()
    prompt = transcribe_audio(audio_file)
    log_info(f"User said: {prompt}")

    if not prompt.strip():
        log_warning("Empty speech detected.")
        return

    command_response = handle_commands(prompt)
    if command_response:
        speak_text(command_response)
        return

    response = get_chatgpt_response(prompt)
    speak_text(response)
    log_info("=== Aria main() complete ===")
