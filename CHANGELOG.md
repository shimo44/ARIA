# Changelog

All notable changes to this project will be documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and adheres to [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2025-05-28

### Added
- 🎉 Initial launch of **Aria Desktop Assistant**

#### Core Features
- **Wake word detection** using Porcupine to activate assistant
- **Audio recording** with `sounddevice` for fixed duration (5 seconds default)
- **Speech-to-text transcription** using the Whisper ASR model (`base`)
- **Text generation** using OpenAI GPT-3.5-turbo (`chat.completions.create`)
- **Text-to-speech** audio response generation via ElevenLabs API
- **Audio playback** using `pydub` with `play()` function
- **System tray interface** via Pystray with start/stop controls and tooltip updates
- **Desktop notifications** using Plyer to signal assistant state

#### Memory & Logging
- **Conversation logging** using SQLite in `aria_memory.db`
- **Memory recall and clearing commands** (`what do you remember`, `clear memory`)
- **Basic command handler** for voice-based shutdown and state transitions

---

### Files Introduced
- `aria.py` –
