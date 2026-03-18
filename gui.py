import tkinter as tk
import monitor

def start_logging():
    monitor.logging_enabled = True
    status_label.config(text="Status: ON", fg="green")

def stop_logging():
    monitor.logging_enabled = False
    status_label.config(text="Status: OFF", fg="red")

def launch():
    monitor.start_background()

    root = tk.Tk()
    root.title("User Activity Monitor")
    root.geometry("300x200")

    global status_label

    status_label = tk.Label(root, text="Status: OFF", fg="red")
    status_label.pack(pady=10)

    start_btn = tk.Button(root, text="Start", command=start_logging)
    start_btn.pack(pady=5)

    stop_btn = tk.Button(root, text="Stop", command=stop_logging)
    stop_btn.pack(pady=5)

    root.mainloop()