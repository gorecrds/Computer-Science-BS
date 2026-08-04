"""
gui.py

A simple desktop window that shows a live transcript of your computer's
audio output. Built on top of SystemAudioTranscriber (transcribe.py).

Run
---
    python gui.py

Requires transcribe.py (and its dependencies) to be in the same folder.
"""

import queue
import threading
import tkinter as tk
from tkinter import ttk

from transcribe import SystemAudioTranscriber
from audio_transcriber import OpenRouterInsights

# --- Temporary: hardcoded for local testing only ---------------------------
# Paste your real OpenRouter key between the quotes below. Do NOT commit this
# file to git or share it with the key filled in -- switch back to the
# OPENROUTER_API_KEY environment variable (see insights.py) once you're done
# testing.
OPENROUTER_API_KEY = ""
# -----------------------------------------------------------------------

 
class TranscriberGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Live Audio Transcriber")
        self.root.geometry("700x500")
        self.root.attributes("-alpha", 0.9)  # 1.0 = fully opaque, 0.0 = invisible
 
        self.transcriber: SystemAudioTranscriber | None = None
        self.transcriber_thread: threading.Thread | None = None
 
        # Thread-safe hand-off: the transcriber's background thread calls
        # on_transcript(), which just queues text. The Tkinter main loop
        # polls this queue and updates the UI -- Tkinter widgets must only
        # ever be touched from the main thread.
        self._text_queue: "queue.Queue" = queue.Queue()
 
        self._build_ui()
        self._poll_queue()
 
    # ------------------------------------------------------------------ #
    # UI layout
    # ------------------------------------------------------------------ #
 
    def _build_ui(self):
        controls = ttk.Frame(self.root, padding=10)
        controls.pack(fill="x")
 
        self.start_button = ttk.Button(controls, text="Start Listening", command=self.start)
        self.start_button.pack(side="left", padx=(0, 8))
 
        self.stop_button = ttk.Button(controls, text="Stop", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=(0, 8))
 
        self.clear_button = ttk.Button(controls, text="Clear", command=self.clear_transcript)
        self.clear_button.pack(side="left", padx=(0, 8))
 
        self.topmost_var = tk.BooleanVar(value=False)
        topmost_check = ttk.Checkbutton(
            controls, text="Always on top", variable=self.topmost_var, command=self._toggle_topmost
        )
        topmost_check.pack(side="left", padx=(16, 0))
 
        self.insights_var = tk.BooleanVar(value=False)
        insights_check = ttk.Checkbutton(
            controls, text="Enable Insights (OpenRouter)", variable=self.insights_var
        )
        insights_check.pack(side="left", padx=(16, 0))
 
        opacity_frame = ttk.Frame(self.root, padding=(10, 0))
        opacity_frame.pack(fill="x")
 
        ttk.Label(opacity_frame, text="Transparency:").pack(side="left")
        self.opacity_var = tk.DoubleVar(value=0.9)
        opacity_slider = ttk.Scale(
            opacity_frame, from_=0.2, to=1.0, orient="horizontal",
            variable=self.opacity_var, command=self._on_opacity_change,
        )
        opacity_slider.pack(side="left", fill="x", expand=True, padx=8)
 
        self.status_var = tk.StringVar(value="Idle")
        status_label = ttk.Label(self.root, textvariable=self.status_var, padding=(10, 0))
        status_label.pack(fill="x")
 
        text_frame = ttk.Frame(self.root, padding=10)
        text_frame.pack(fill="both", expand=True)
 
        self.text_widget = tk.Text(text_frame, wrap="word", font=("Segoe UI", 11))
        self.text_widget.pack(side="left", fill="both", expand=True)
        self.text_widget.tag_configure(
            "insight", font=("Segoe UI", 10, "italic"), foreground="#3a6ea5", lmargin1=24, lmargin2=24
        )
 
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=scrollbar.set)
        self.text_widget.config(state="disabled")
 
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
 
    # ------------------------------------------------------------------ #
    # Window appearance
    # ------------------------------------------------------------------ #
 
    def _on_opacity_change(self, value):
        self.root.attributes("-alpha", float(value))
 
    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())
 
    # ------------------------------------------------------------------ #
    # Transcriber control
    # ------------------------------------------------------------------ #
 
    def start(self):
        if self.transcriber_thread and self.transcriber_thread.is_alive():
            return
 
        insights = None
        if self.insights_var.get():
            try:
                insights = OpenRouterInsights(
                    api_key=OPENROUTER_API_KEY,
                    model="nvidia/nemotron-3-nano-30b-a3b:free",
                )
            except ValueError as e:
                self.status_var.set(str(e))
                return
 
        self.status_var.set("Loading model and starting capture...")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
 
        self.transcriber = SystemAudioTranscriber(
            model_size="base",
            on_transcript=self._on_transcript,
            insights=insights,
            on_insight=self._on_insight,
        )
 
        # start() blocks (runs the capture/transcribe loop), so it needs
        # its own thread to keep the GUI responsive.
        self.transcriber_thread = threading.Thread(target=self._run_transcriber, daemon=True)
        self.transcriber_thread.start()
 
    def _run_transcriber(self):
        try:
            self.transcriber.start()
        except Exception as e:
            self._text_queue.put(("__error__", "", str(e)))
 
    def stop(self):
        if self.transcriber:
            self.transcriber.stop()
        self.status_var.set("Idle")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def _on_transcript(self, text: str, timestamp: str):
        # Called from the transcriber's background thread -- do NOT touch
        # Tkinter widgets here directly.
        # print(f"[{timestamp}] {text}", flush=True)   # command-line output
        self._text_queue.put(("transcript", timestamp, text))


    def _on_insight(self, text: str, timestamp: str):
        # Also called from a background thread -- same rule applies.
        #print(f"  -> insight [{timestamp}]: {text}", flush=True)
        self._text_queue.put(("insight", timestamp, text))
 
    def _poll_queue(self):
        """Runs on the Tkinter main loop, checks for new lines every 200ms,
        and safely updates the text widget. Handles both transcript and
        insight lines, plus error signals -- all funneled through the same
        queue since only the main thread may touch Tkinter widgets."""
        try:
            while True:
                kind, timestamp, text = self._text_queue.get_nowait()
 
                if kind == "__error__":
                    self.status_var.set(f"Error: {text}")
                    self.start_button.config(state="normal")
                    self.stop_button.config(state="disabled")
                    continue
 
                self.status_var.set("Listening...")
                self.text_widget.config(state="normal")
                if kind == "insight":
                    self.text_widget.insert("end", f"  -> {text}\n", "insight")
                else:
                    self.text_widget.insert("end", f"[{timestamp}] {text}\n")
                self.text_widget.see("end")
                self.text_widget.config(state="disabled")
        except queue.Empty:
            pass
        finally:
            self.root.after(200, self._poll_queue)
 
    # ------------------------------------------------------------------ #
    # Toolbar actions
    # ------------------------------------------------------------------ #
 
    def clear_transcript(self):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.config(state="disabled")
 
    def _on_close(self):
        if self.transcriber:
            self.transcriber.stop()
        self.root.destroy()
 
 
def main():
    root = tk.Tk()
    app = TranscriberGUI(root)
    root.mainloop()
 
 
if __name__ == "__main__":
    main()