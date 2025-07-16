import time
import threading
import tkinter as tk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

# --- Global Variables ---
clicking_thread = None
typing_thread = None
is_running = False
mouse = MouseController()
keyboard = KeyboardController()

# --- Core Automation Functions ---

def auto_clicker():
    """Function to handle continuous mouse clicking."""
    global is_running
    click_interval = float(interval_entry.get())
    while is_running:
        mouse.click(Button.left, 1)
        time.sleep(click_interval)

def auto_typer():
    """Function to handle continuous keyboard typing."""
    global is_running
    key_to_press = key_entry.get()
    type_interval = float(type_interval_entry.get())
    
    if not key_to_press:
        print("Key to press cannot be empty.")
        return
        
    while is_running:
        keyboard.press(key_to_press[0])
        keyboard.release(key_to_press[0])
        time.sleep(type_interval)

# --- Control Functions ---

def start_automation():
    """Starts both the auto-clicker and auto-typer threads."""
    global is_running, clicking_thread, typing_thread
    if not is_running:
        try:
            float(interval_entry.get())
            float(type_interval_entry.get())
        except ValueError:
            status_label.config(text="Error: Invalid interval value.", fg="red")
            return
            
        is_running = True
        status_label.config(text="Status: Running...", fg="green")
        
        if float(interval_entry.get()) > 0:
            clicking_thread = threading.Thread(target=auto_clicker, daemon=True)
            clicking_thread.start()
            
        if float(type_interval_entry.get()) > 0 and key_entry.get():
            typing_thread = threading.Thread(target=auto_typer, daemon=True)
            typing_thread.start()
            
def stop_automation():
    """Stops the automation threads."""
    global is_running
    if is_running:
        is_running = False
        status_label.config(text="Status: Stopped", fg="red")

# --- GUI Setup (Updated for KMclicker) ---
window = tk.Tk()
window.title("KMclicker") # <-- Updated Title
window.geometry("400x300")
window.configure(bg="#2E2E2E")

# --- Title ---
title_label = tk.Label(window, text="KMclicker", font=("Helvetica", 18, "bold"), bg="#2E2E2E", fg="#FFFFFF") # <-- Updated Label
title_label.pack(pady=10)

# --- Mouse Settings Frame ---
mouse_frame = tk.Frame(window, bg="#2E2E2E")
mouse_frame.pack(pady=5, padx=20, fill='x')

interval_label = tk.Label(mouse_frame, text="Mouse Click Interval (s):", bg="#2E2E2E", fg="#FFFFFF")
interval_label.pack(side=tk.LEFT)

interval_entry = tk.Entry(mouse_frame, width=10)
interval_entry.pack(side=tk.RIGHT)
interval_entry.insert(0, "1")

# --- Keyboard Settings Frame ---
key_frame = tk.Frame(window, bg="#2E2E2E")
key_frame.pack(pady=5, padx=20, fill='x')

key_label = tk.Label(key_frame, text="Key to Press:", bg="#2E2E2E", fg="#FFFFFF")
key_label.pack(side=tk.LEFT)

key_entry = tk.Entry(key_frame, width=10)
key_entry.pack(side=tk.RIGHT)
key_entry.insert(0, "w")

type_interval_frame = tk.Frame(window, bg="#2E2E2E")
type_interval_frame.pack(pady=5, padx=20, fill='x')

type_interval_label = tk.Label(type_interval_frame, text="Key Press Interval (s):", bg="#2E2E2E", fg="#FFFFFF")
type_interval_label.pack(side=tk.LEFT)

type_interval_entry = tk.Entry(type_interval_frame, width=10)
type_interval_entry.pack(side=tk.RIGHT)
type_interval_entry.insert(0, "2")

# --- Control Buttons Frame ---
button_frame = tk.Frame(window, bg="#2E2E2E")
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", command=start_automation, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_automation, bg="#F44336", fg="white", font=("Helvetica", 10, "bold"))
stop_button.pack(side=tk.LEFT, padx=10)

# --- Status Label ---
status_label = tk.Label(window, text="Status: Stopped", font=("Helvetica", 10), bg="#2E2E2E", fg="red")
status_label.pack(pady=10)

# --- Run the application ---
if __name__ == "__main__":
    window.mainloop()