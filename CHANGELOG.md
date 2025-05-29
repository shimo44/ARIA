## Changelog

### 1.3.0 - Tray Icon Resilience + Launcher Stability (Upcoming)
- Enhanced `tray.py` with safe process relaunching.
- Improved logging and crash recovery mechanisms.
- Unified stop/start control via tray menu.
- Added fallback icon image when asset is missing.

### 1.2.2 - Whisper + VAD Refactor & Logging Overhaul (2025-05-29)
- Introduced detailed logging to all components, including `aria.py`, VAD, and tray launcher.
- Integrated robust error handling and device diagnostics for microphone/VAD failures.
- Rebuilt `vad_audio.py` to:
  - Validate frame size before VAD processing.
  - Enforce mono PCM audio streams.
  - Auto-handle broken frames with recovery logs.
- Whisper integration setbacks:
  - Encountered repeated `NoneType` and frame errors tied to `ctypes.CDLL`.
  - Resolved by isolating faulty environments and performing a clean install.
  - Issues related to default Python interpreter misalignment resolved.
- VAD reliability setbacks:
  - Frame size mismatches (e.g., got 1920 bytes, expected 960) traced to channel count mismatches.
  - Fixed by enforcing mono input and byte-level validation.

### 1.1.1 - Audio Recording Persistence Fix (2025-05-27)
- Fixed `aria.main()` not looping back into listening after a response.
- Ensured persistent microphone readiness following each completed response.
- Whisper feedback speech log now returns clarified errors.

### 1.1.0 - Initial Launch Release (2025-05-26)
- Aria AI Desktop Tray Assistant debut.
- Includes:
  - Wake word listener.
  - Speech-to-text (Whisper).
  - Text-to-speech (ElevenLabs).
  - Command handling.
  - Tray icon controls for start/stop/quit.
