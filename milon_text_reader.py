"""
Milon's Study & Creator Text Reader
----------------------------------
A small Windows desktop app: type or paste text, choose a speech speed,
and let your computer read it aloud.

Install once:
    py -m pip install pyttsx3

Run:
    py milon_text_reader.py
"""

import threading
import tkinter as tk
from tkinter import messagebox
import pyttsx3


class TextReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Milon's Text Reader")
        self.root.geometry("720x520")
        self.root.minsize(560, 420)
        self.root.configure(bg="#101827")

        self.is_speaking = False
        self.engine = None

        title = tk.Label(
            root, text="TEXT READER", font=("Segoe UI", 21, "bold"),
            fg="#7dd3fc", bg="#101827"
        )
        title.pack(pady=(18, 3))

        subtitle = tk.Label(
            root, text="Paste your study notes, ideas, or scripts below.",
            font=("Segoe UI", 10), fg="#cbd5e1", bg="#101827"
        )
        subtitle.pack(pady=(0, 12))

        self.text_box = tk.Text(
            root, wrap="word", font=("Segoe UI", 12),
            bg="#1e293b", fg="#f8fafc", insertbackground="white",
            relief="flat", padx=12, pady=12, undo=True
        )
        self.text_box.pack(fill="both", expand=True, padx=20, pady=5)
        self.text_box.insert(
            "1.0",
            "Welcome! Type or paste your text here, then press Speak."
        )

        settings = tk.Frame(root, bg="#101827")
        settings.pack(fill="x", padx=22, pady=(10, 4))

        tk.Label(
            settings, text="Speech speed", fg="#e2e8f0",
            bg="#101827", font=("Segoe UI", 10)
        ).pack(side="left")

        self.speed = tk.IntVar(value=170)
        tk.Scale(
            settings, from_=100, to=250, orient="horizontal",
            variable=self.speed, length=210, bg="#101827",
            fg="#e2e8f0", troughcolor="#334155",
            highlightthickness=0, activebackground="#38bdf8"
        ).pack(side="left", padx=10)

        buttons = tk.Frame(root, bg="#101827")
        buttons.pack(pady=12)

        tk.Button(
            buttons, text="▶  SPEAK", command=self.speak,
            font=("Segoe UI", 11, "bold"), bg="#0284c7", fg="white",
            activebackground="#0369a1", activeforeground="white",
            relief="flat", padx=22, pady=10, cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            buttons, text="■  STOP", command=self.stop,
            font=("Segoe UI", 11, "bold"), bg="#475569", fg="white",
            activebackground="#334155", activeforeground="white",
            relief="flat", padx=22, pady=10, cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            buttons, text="CLEAR", command=self.clear,
            font=("Segoe UI", 11, "bold"), bg="#334155", fg="white",
            activebackground="#1e293b", activeforeground="white",
            relief="flat", padx=22, pady=10, cursor="hand2"
        ).pack(side="left", padx=6)

        self.status = tk.Label(
            root, text="Ready • Windows built-in voices",
            font=("Segoe UI", 9), fg="#94a3b8", bg="#101827"
        )
        self.status.pack(pady=(0, 12))

    def speak(self):
        text = self.text_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("No text", "Please type or paste some text first.")
            return
        if self.is_speaking:
            return

        self.is_speaking = True
        self.status.config(text="Speaking…", fg="#7dd3fc")
        threading.Thread(
            target=self._speak_worker, args=(text, self.speed.get()),
            daemon=True
        ).start()

    def _speak_worker(self, text, rate):
        try:
            engine = pyttsx3.init()
            self.engine = engine
            engine.setProperty("rate", rate)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            self.root.after(0, lambda: self.status.config(
                text="Finished • Ready for more text", fg="#86efac"
            ))
        except Exception as error:
            self.root.after(0, lambda: messagebox.showerror(
                "Speech error", f"Could not start speech:\n{error}"
            ))
        finally:
            self.engine = None
            self.is_speaking = False

    def stop(self):
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass
        self.is_speaking = False
        self.status.config(text="Stopped", fg="#fca5a5")

    def clear(self):
        self.stop()
        self.text_box.delete("1.0", "end")
        self.status.config(text="Text cleared • Ready", fg="#94a3b8")


if __name__ == "__main__":
    window = tk.Tk()
    app = TextReaderApp(window)
    window.mainloop()
