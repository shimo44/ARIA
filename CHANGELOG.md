## 🔄 **ARIA CHANGELOG**

### 🚀 Version `1.2.3` – *"Modular Expansion"*
**Release Date:** 2025-05-29  
**Build Type:** Desktop Modular Build

---

### 🚀 **New Features**
- **Modular Tray Integration**:
  - Moved all tray functionality to `tray.py`
  - Tray menu includes: `Start Listening`, `Stop Listening`, `Open GUI`, and `Quit`
  - Tooltip updates reflect Aria's listening state

- **Standalone GUI Module (`aria_gui.py`)**:
  - GUI controls: start/stop listening, restart Aria, exit, and close GUI (tray-only mode)
  - Text input field activates after first Aria voice response
  - Uses threads to keep UI responsive during processing

- **Smart Text Entry Unlocking**:
  - Prevents premature typing by disabling input until Aria speaks

---

### 📂 **Structural Improvements**
- `aria.py` is now streamlined to handle only core logic
- GUI and tray code fully modular and reusable
- Tray launches by default when running `aria.py`

---

### 🚧 **Startup Options**

#### ▶️ **Run in Tray Mode (Default)**
```bash
python aria.py
```

#### 💬 **Open GUI Window Only**
```bash
python aria_gui.py
```

#### 🔕 **Run Wake Listener (Headless)**
```bash
python wake_listener.py
```

#### ⚙️ **Call Aria from Python**
```python
from aria import ask_aria
ask_aria("What’s the weather today?")
```

---

### ✨ Next Up
- Tray watchdog
- Microphone input selector
- `.exe` packaging
