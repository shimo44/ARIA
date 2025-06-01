<p align="left">
  <img src="./assets/icon.jpg" alt="Aria Icon" width="100" style="float: left; margin-right: 15px;"/>
</p>

# Aria Assistant

Aria is a local desktop AI assistant powered by OpenAI, Whisper, and ElevenLabs. It can listen to your voice, respond naturally, and now offers GUI and tray integration for seamless control.

---

## 🌟 Features
- Wake word detection via `wake_listener.py`
- Voice-to-text transcription with Whisper
- ChatGPT-based natural language replies
- Text-to-speech using ElevenLabs
- GUI with command buttons and type-to-ask
- System tray menu for minimal operation

---

## 🔄 Version History

### [1.2.3 - Modular Expansion](./CHANGELOG.md)
- GUI and tray split into `aria_gui.py` and `tray.py`
- Text entry unlocks after Aria speaks
- Default tray-based launcher from `aria.py`

### [1.2.2.5 - VAD Removal](./archive/aria-1.2.2.5.py)
- Voice Activity Detection removed
- Audio input consolidated to main logic
- Refactored for upcoming modular split

### [1.1.0 - Stable Build](./archive/aria-1.1.0.py)
- Working Whisper/STT and ElevenLabs integration
- Console-based loop with wake control

---

## 🚧 How to Run

### ▶️ Start in Tray Mode
```bash
python aria.py
```

### 💬 Open the GUI
```bash
python aria_gui.py
```

### 🔕 Run Wake Listener Only
```bash
python wake_listener.py
```

---

## ⚙️ Development Notes
- Python 3.9+ recommended
- Requires `ffmpeg` in system path
- .env file with API keys: `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `VOICE_ID`, `ACCESS_KEY`

---

## 🎓 License
MIT License

---

## 🚀 Coming Soon
- `.exe` packaging
- Tray watchdog for process health
- Mic source selector
- Command memory timeline
