import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv
from aria import main
from aria import speak_text

# Optional notification support
try:
    from plyer import notification
except ImportError:
    notification = None

# Load environment variables from .env file
load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")


def notify(title, message):
    if notification:
        notification.notify(
            title=title,
            message=message,
            app_name="Aria Assistant",
            timeout=3
        )


def listen_for_wake_word():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=["jarvis"]  # Replace with "aria" if using a trained keyword
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word...")
    notify("Aria Ready", "Listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                try:
                    speak_text("Hi, I’m listening.")
                    main()
                except Exception as e:
                    print("Error in main():", e)
                finally:
                    print("Main() completed. Returning to listening mode...")
                    notify("Listening Resumed", "Aria is listening again.")

    except KeyboardInterrupt:
        print("Stopping wake word listener...")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    listen_for_wake_word()
