## Changelog 

### 1.2.2.5 - VAD Removal + Stability Reversion (2025-05-29)
- Reverted from VAD-based audio capture to fixed-length streaming microphone recording.
- Temporarily deprecated `SimpleAudio` module plans; logic now lives directly in `aria.py` and `wake_listener.py`.
- Enforced minimum recording duration threshold (1.8s) to filter out false activations.
- Audio signal strength (RMS) tracking and debug logs retained.
- Fixes issues where Aria captured ambient sound or cut off user speech too early.
- Improved transcription reliability post-Whisper reinstall.

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
