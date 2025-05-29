from pystray import Icon, Menu, MenuItem
from PIL import Image
import subprocess
import os
import sys
from plyer import notification

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
WAKE_SCRIPT = os.path.join(os.path.dirname(__file__), "wake_listener.py")

listener_process = None
aria_icon = None

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Aria Assistant",
        timeout=3
    )

def update_tooltip(status):
    if aria_icon:
        aria_icon.title = f"Aria Assistant ({status})"

def start_listening(icon, item):
    global listener_process
    if listener_process is None or listener_process.poll() is not None:
        listener_process = subprocess.Popen([sys.executable, WAKE_SCRIPT])
        update_tooltip("Listening")
        notify("Aria Activated", "Wake word listener is running.")
        print("Aria is now listening...")

def stop_listening(icon, item):
    global listener_process
    if listener_process and listener_process.poll() is None:
        listener_process.terminate()
        listener_process = None
        update_tooltip("Idle")
        notify("Aria Paused", "Wake word listener has been stopped.")
        print("Aria has stopped listening.")

def quit_app(icon, item):
    stop_listening(icon, item)
    icon.stop()

def create_icon():
    global aria_icon
    try:
        icon_image = Image.open(ICON_PATH)
    except FileNotFoundError:
        icon_image = Image.new("RGB", (64, 64), "gray")

    aria_icon = Icon("Aria", icon_image)
    aria_icon.menu = Menu(
        MenuItem("Start Listening", start_listening),
        MenuItem("Stop Listening", stop_listening),
        MenuItem("Quit", quit_app)
    )
    update_tooltip("Idle")
    return aria_icon

if __name__ == "__main__":
    create_icon().run()
