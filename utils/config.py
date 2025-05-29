import os
from dotenv import load_dotenv

load_dotenv()

# === General Debugging Control ===
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# === Individual Debug Flags ===
DEBUG_TIMING = os.getenv("DEBUG_TIMING", "false").lower() == "true"
DEBUG_TRANSCRIPT = os.getenv("DEBUG_TRANSCRIPT", "false").lower() == "true"
DEBUG_PROMPT_FLOW = os.getenv("DEBUG_PROMPT_FLOW", "false").lower() == "true"
DEBUG_TTS = os.getenv("DEBUG_TTS", "false").lower() == "true"
DEBUG_MEMORY = os.getenv("DEBUG_MEMORY", "false").lower() == "true"
DEBUG_VAD_ERRORS = os.getenv("DEBUG_VAD_ERRORS", "false").lower() == "true"

# === Whisper Model Setting ===
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "base")
