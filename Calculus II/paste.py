import time
import random
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui
import pyperclip


def clean_text(text: str) -> str:
    return re.sub(r"(\r?\n)[ \t]+", r"\1", text)


def run_typing(delay_seconds: int, min_delay: float, max_delay: float, stop_event: threading.Event) -> None:
    text = pyperclip.paste()
    if not text:
        raise RuntimeError("Clipboard is empty. Copy something first.")

    text = clean_text(text)

    pyautogui.FAILSAFE = True

    # Focus delay (but allow cancel during the countdown)
    for _ in range(delay_seconds * 10):
        if stop_event.is_set():
            return
        time.sleep(0.1)

    for ch in text:
        if stop_event.is_set():
            return
        pyautogui.write(ch)  # FailSafeException can be raised here
        time.sleep(random.uniform(min_delay, max_delay))


root = tk.Tk()
root.title("iM Bluetooth Keyboard")

main = ttk.Frame(root, padding=12)
main.grid(row=0, column=0, sticky="nsew")

ttk.Label(main, text="iM Bluetooth Keyboard", font=("Segoe UI", 14, "bold")).grid(
    row=0, column=0, columnspan=2, sticky="w"
)

ttk.Label(main, text="Focus delay (seconds):").grid(row=1, column=0, sticky="w", pady=(10, 2))
delay_var = tk.StringVar(value="4")
ttk.Entry(main, textvariable=delay_var, width=10).grid(row=1, column=1, sticky="w", pady=(10, 2))

ttk.Label(main, text="Min char delay (seconds):").grid(row=2, column=0, sticky="w", pady=2)
min_var = tk.StringVar(value="0.01")
ttk.Entry(main, textvariable=min_var, width=10).grid(row=2, column=1, sticky="w", pady=2)

ttk.Label(main, text="Max char delay (seconds):").grid(row=3, column=0, sticky="w", pady=2)
max_var = tk.StringVar(value="0.5")
ttk.Entry(main, textvariable=max_var, width=10).grid(row=3, column=1, sticky="w", pady=2)

status_var = tk.StringVar(value="Ready.")
ttk.Label(main, textvariable=status_var).grid(row=6, column=0, columnspan=2, sticky="w")

ttk.Label(
    main,
    text="Tip: PyAutoGUI FailSafe is ON.\nMove mouse to top-left corner to stop.",
    foreground="gray"
).grid(row=7, column=0, columnspan=2, sticky="w", pady=(8, 0))

stop_event = threading.Event()


def ui_set_status(text: str) -> None:
    status_var.set(text)


def on_click_stop() -> None:
    stop_event.set()
    ui_set_status("Stopping...")


def on_click_run() -> None:
    try:
        delay_seconds = int(delay_var.get())
        min_delay = float(min_var.get())
        max_delay = float(max_var.get())
        if min_delay < 0 or max_delay < 0 or max_delay < min_delay:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid settings", "Check your delay values.")
        return

    stop_event.clear()
    run_btn.config(state="disabled")
    stop_btn.config(state="normal")
    ui_set_status("Running... (move mouse to top-left corner or click Stop)")

    def worker_thread():
        try:
            run_typing(delay_seconds, min_delay, max_delay, stop_event)
            # If stop_event was set, treat as aborted
            if stop_event.is_set():
                root.after(0, ui_set_status, "Aborted.")
            else:
                root.after(0, ui_set_status, "Done.")
        except pyautogui.FailSafeException:
            root.after(0, ui_set_status, "Aborted (FailSafe).")
        except Exception as e:
            # Show errors safely from UI thread
            root.after(0, ui_set_status, f"Error: {e}")
            root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            root.after(0, run_btn.config, {"state": "normal"})
            root.after(0, stop_btn.config, {"state": "disabled"})

    threading.Thread(target=worker_thread, daemon=True).start()


run_btn = ttk.Button(main, text="Run (Type Clipboard)", command=on_click_run)
run_btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 6))

stop_btn = ttk.Button(main, text="Stop", command=on_click_stop, state="disabled")
stop_btn.grid(row=5, column=0, columnspan=2, sticky="ew")

root.resizable(False, False)
root.mainloop()
