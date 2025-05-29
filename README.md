# ARIA.EXE – Desktop AI Assistant

**ARIA** is a local, privacy-focused AI voice assistant powered by Whisper, GPT-4, and ElevenLabs. It listens for wake words, responds naturally, remembers what you say, and lives quietly in your system tray.

---

## 🚀 Features

- ✅ Wake-word activated voice assistant (“Hey Aria”)
- 🎤 Whisper for accurate speech-to-text
- 🧠 GPT-4 via OpenAI API for intelligent responses
- 🔊 ElevenLabs for realistic voice replies
- 📌 Tray icon for one-click control (start/stop/quit)
- 💾 Persistent memory with SQLite
- 🔔 Desktop notifications and tooltips

---

## 📂 Folder Structure

```
aria/
│
├── aria.py                  # Main assistant logic with memory, commands
├── wake_listener.py         # Wake word detection (Porcupine)
├── tray.py                  # Tray icon to control Aria
│
├── utils/
│   └── logger.py            # Chat logging + SQLite memory
│
├── assets/
│   └── icon.png             # Icon for tray (64x64 PNG)
│
├── audio/                   # Optional audio recordings
├── config/                  # Reserved for .env/config
└── logs/
    ├── chatlog.txt          # Raw text memory log
    └── memory.db            # SQLite persistent memory
```

---

## 🔐 Required API Keys

Set these in your environment or securely load them:

- `OPENAI_API_KEY` – for ChatGPT/GPT-4
- `ELEVENLABS_API_KEY` – for voice synthesis
- `VOICE_ID` – ElevenLabs voice profile ID
- `ACCESS_KEY` – Picovoice Porcupine wake word key

---

## 🛠 Installation

Install required packages:

```bash
pip install openai whisper elevenlabs pvporcupine pyaudio sounddevice soundfile pydub simpleaudio pystray pillow plyer python-dotenv
```

Run the tray assistant:

```bash
python tray.py
```

Start manually without tray:

```bash
python aria.py
```

---

## 💡 What You Can Ask Aria

Aria uses GPT-4 to generate intelligent, conversational responses to spoken prompts.

### 🔍 Examples:
- "What is the capital of France?"
- "Tell me a short story about a robot."
- "Summarize the plot of The Matrix."
- "How do I start a business?"
- "Explain quantum physics in simple terms."
- "What’s the difference between Python and JavaScript?"
- "Give me a productivity tip."
- "Recite a motivational quote."
- "Tell me a joke."
- "Define resilience."

### ✅ Special Voice Commands:
- "Clear memory" → wipes chatlog and memory database
- "What do you remember" → recalls last 5 chat entries
- "Goodbye" → exits Aria assistant cleanly

### ⛔ Current Limitations:
- No live data (weather, stocks, news, time)
- No wake word training (uses preset keyword)
- No local file system access or automation (yet)

---

## 📜 License

© 2025 Hidden Leaf Networks LLC. All rights reserved.
