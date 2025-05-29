import collections
import webrtcvad
import pyaudio
import wave
import sounddevice as sd
import traceback
import struct

# === SET MANUAL DEVICE INDEX IF NEEDED ===
INPUT_DEVICE_INDEX = 9  # 👈 set this to your actual mic device index
sd.default.device = (INPUT_DEVICE_INDEX, None)

class VADAudio:
    def __init__(self, aggressiveness=3, input_rate=16000, frame_duration=30, padding_duration=1500):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = input_rate
        self.frame_duration = frame_duration  # ms
        self.bytes_per_sample = 2  # 16-bit audio
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000) * self.bytes_per_sample  # 960
        self.chunk_duration = frame_duration  # same as frame_duration for consistency
        self.chunk_size = int(self.sample_rate * self.chunk_duration / 1000) * self.bytes_per_sample
        self.padding_duration = padding_duration
        self.num_padding_frames = int(self.padding_duration / self.chunk_duration)
        self.ring_buffer = collections.deque(maxlen=self.num_padding_frames)
        self.triggered = False
        self.frames = []

        print(f"[DEBUG] VAD initialized with {self.sample_rate} Hz, frame size: {self.frame_size} bytes")

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,  # ✅ force mono
            rate=self.sample_rate,
            input=True,
            input_device_index=INPUT_DEVICE_INDEX,
            frames_per_buffer=int(self.frame_size / self.bytes_per_sample)
        )

    def read_audio(self):
        try:
            while True:
                try:
                    frame = self.stream.read(int(self.frame_size / self.bytes_per_sample), exception_on_overflow=False)
                except Exception as e:
                    print(f"[ERROR] Failed to read from microphone: {e}")
                    break

                if len(frame) != self.frame_size:
                    print(f"[VAD WARNING] Skipping frame due to incorrect size: got {len(frame)} bytes, expected {self.frame_size}")
                    continue

                try:
                    pcm_data = struct.unpack(f"{len(frame) // self.bytes_per_sample}h", frame)
                    raw_bytes = struct.pack(f"{len(pcm_data)}h", *pcm_data)
                    is_speech = self.vad.is_speech(raw_bytes, self.sample_rate)
                except Exception as e:
                    print(f"[VAD WARNING] Skipped frame due to VAD error: {e}")
                    continue

                if not self.triggered:
                    self.ring_buffer.append((frame, is_speech))
                    num_voiced = len([f for f, speech in self.ring_buffer if speech])
                    if num_voiced > 0.9 * self.ring_buffer.maxlen:
                        self.triggered = True
                        for f, s in self.ring_buffer:
                            self.frames.append(f)
                        self.ring_buffer.clear()
                else:
                    self.frames.append(frame)
                    self.ring_buffer.append((frame, is_speech))
                    num_unvoiced = len([f for f, speech in self.ring_buffer if not speech])
                    if num_unvoiced > 0.9 * self.ring_buffer.maxlen:
                        break

            return b''.join(self.frames)

        except Exception as e:
            print(f"[FATAL ERROR] Unexpected error in read_audio: {e}")
            return b""

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def save_wav(self, path, data):
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(data)
