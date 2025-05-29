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
from utils.config import DEBUG_MODE

init(autoreset=True)

# --- Logging with Debug Flag ---
def log_info(msg): print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + msg)
def log_success(msg): print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + msg)
def log_warning(msg): print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + msg)
def log_error(msg): print(Fore.RED + "[ERROR] " + Style.RESET_ALL + msg)
def log_speak(msg): print(Fore.MAGENTA + "[ARIA] " + Style.RESET_ALL + msg)
def debug(msg):
    if DEBUG_MODE:
        print(Fore.BLUE + "[DEBUG] " + Style.RESET_ALL + msg)

# --- Load environment ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Load Whisper ---
try:
    model = whisper.load_model("base")
    log_success("Whisper model loaded.")
except Exception as e:
    log_error(f"Whisper failed: {e}")
    model = None

# --- Audio Recording ---
def record_audio_vad(filename="audio.wav"):
    log_info("Starting smart voice-activated recording...")
    vad = VADAudio()
    audio = vad.read_audio()
    debug(f"Audio length: {len(audio)} bytes")
    # Estimate average signal level (crude volume check)
    if len(audio) > 0:
        avg_signal = sum(audio) / len(audio)
        debug(f"Audio byte mean (signal level): {avg_signal:.2f}")
    vad.save_wav(filename, audio)
    vad.close()
    log_success(f"Audio recorded to {filename}")
    return filename

# --- Transcription ---
def transcribe_audio(filename):
    if model is None:
        log_error("No Whisper model available.")
        return ""
    result = model.transcribe(filename, language="en")  # Force English
    debug(f"Raw Whisper output: {result}")
    log_info(f"Transcription: {result['text']}")
    return result["text"]

# --- Text-to-Speech ---
def speak_text(text):
    try:
        debug(f"Sending to ElevenLabs: {text}")
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

# --- GPT Response ---
def get_chatgpt_response(prompt):
    init_db()
    context = get_memory_entries()
    full_prompt = f"{context}\nUser: {prompt}\nAria:"
    debug(f"Full prompt sent to GPT: {full_prompt}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    reply = response.choices[0].message.content
    log_interaction(prompt, reply)
    return reply

# --- Command Handling ---
def handle_commands(prompt):
    p = prompt.lower()
    debug(f"Handling prompt: {p}")
    if "clear memory" in p:
        clear_memory()
        return "Memory has been cleared."
    elif "what do you remember" in p:
        return f"Here's what I remember:\n{get_memory_entries(limit=5)}"
    elif any(x in p for x in ["bye", "goodbye", "exit", "shutdown", "stop listening", "bye-bye"]):
        speak_text("Goodbye!")
        exit()
    return None

# --- Main ---
def main():
    log_info("=== Aria main() ===")
    audio_file = record_audio_vad()
    prompt = transcribe_audio(audio_file)
    log_info(f"User said: {prompt}")

    # === Extra input validation ===
    if not prompt.strip():
        log_warning("Empty speech detected.")
        return
    if len(prompt.strip()) < 4 or prompt.lower().strip() in ["l l l", "...", "umm", "hmm"]:
        log_warning("Likely invalid or unclear speech. Prompt discarded.")
        return

    command_response = handle_commands(prompt)
    if command_response:
        speak_text(command_response)
        return

    response = get_chatgpt_response(prompt)
    speak_text(response)
    log_info("=== Aria main() complete ===")

if __name__ == "__main__":
    main()
