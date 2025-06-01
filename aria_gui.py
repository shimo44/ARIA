import tkinter as tk
from tkinter import messagebox
from threading import Thread
from aria import ask_aria, start_listening, stop_listening, shutdown_aria, speak_text

aria_spoken = False  # GUI flag to unlock text input

class AriaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aria Assistant")
        self.root.geometry("400x300")

        ctrl = tk.Frame(root)
        ctrl.pack(pady=10)

        tk.Button(ctrl, text="🎙 Start Listening", command=self.start_listening).grid(row=0, column=0, padx=5)
        tk.Button(ctrl, text="🔇 Stop Listening", command=self.stop_listening).grid(row=0, column=1, padx=5)
        tk.Button(ctrl, text="🔁 Restart Aria", command=self.restart_aria).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(ctrl, text="❌ Exit Aria", command=self.exit_aria).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(ctrl, text="🛑 Close GUI", command=self.close_gui).grid(row=2, columnspan=2, pady=5)

        self.text_entry = tk.Entry(root, width=50, state="disabled")
        self.text_entry.pack(pady=10)

        self.submit_btn = tk.Button(root, text="Send to Aria", state="disabled", command=self.send_question)
        self.submit_btn.pack()

        self.status_label = tk.Label(root, text="Waiting for Aria to respond...")
        self.status_label.pack(pady=10)

        # Trigger greeting
        Thread(target=self.greet_user).start()

    def greet_user(self):
        speak_text("Hello! I'm ready to assist you.")
        self.enable_text_mode()

    def enable_text_mode(self):
        global aria_spoken
        if aria_spoken:
            self.text_entry.config(state="normal")
            self.submit_btn.config(state="normal")
            self.status_label.config(text="You can now type your questions.")

    def start_listening(self):
        Thread(target=self._start_and_flag).start()

    def _start_and_flag(self):
        global aria_spoken
        start_listening()
        aria_spoken = True
        self.enable_text_mode()

    def stop_listening(self):
        stop_listening()

    def restart_aria(self):
        stop_listening()
        start_listening()
        self.status_label.config(text="Aria restarted.")

    def send_question(self):
        question = self.text_entry.get()
        if question.strip():
            self.status_label.config(text="Thinking...")
            Thread(target=self._ask_aria_thread, args=(question,)).start()

    def _ask_aria_thread(self, question):
        response = ask_aria(question)
        self.status_label.config(text="Aria: " + response)
        self.enable_text_mode()

    def exit_aria(self):
        shutdown_aria()

    def close_gui(self):
        self.root.withdraw()
        messagebox.showinfo("Tray Mode", "GUI closed. Aria is running in tray mode.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AriaGUI(root)
    root.mainloop()
