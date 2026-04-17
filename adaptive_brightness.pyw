import cv2
import screen_brightness_control as sbc
import numpy as np
import time
import threading
import psutil
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk
import os
import sys
import json

# DEFAULT SETTINGS
CHECK_INTERVAL = 300
SAMPLE_COUNT = 5
SMOOTH_DELAY = 0.05
CAMERA_INDEX = 0
CALIB_MIN_LIGHT = 2.0
CALIB_MAX_LIGHT = 61.0
CALIB_MIN_BRIGHT = 10
CALIB_MAX_BRIGHT = 50
running = True

def get_settings_path():
    """Returns a portable path for the settings file (next to the executable or script)."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'adaptive_brightness_settings.json')

def load_settings():
    global CHECK_INTERVAL, CAMERA_INDEX, CALIB_MIN_LIGHT, CALIB_MAX_LIGHT, CALIB_MIN_BRIGHT, CALIB_MAX_BRIGHT
    path = get_settings_path()
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
                CHECK_INTERVAL = settings.get("CHECK_INTERVAL", CHECK_INTERVAL)
                CAMERA_INDEX = settings.get("CAMERA_INDEX", CAMERA_INDEX)
                CALIB_MIN_LIGHT = settings.get("CALIB_MIN_LIGHT", CALIB_MIN_LIGHT)
                CALIB_MAX_LIGHT = settings.get("CALIB_MAX_LIGHT", CALIB_MAX_LIGHT)
                CALIB_MIN_BRIGHT = settings.get("CALIB_MIN_BRIGHT", CALIB_MIN_BRIGHT)
                CALIB_MAX_BRIGHT = settings.get("CALIB_MAX_BRIGHT", CALIB_MAX_BRIGHT)
        except Exception as e:
            print("Error loading settings:", e)

def save_settings_to_file():
    path = get_settings_path()
    settings = {
        "CHECK_INTERVAL": CHECK_INTERVAL,
        "CAMERA_INDEX": CAMERA_INDEX,
        "CALIB_MIN_LIGHT": CALIB_MIN_LIGHT,
        "CALIB_MAX_LIGHT": CALIB_MAX_LIGHT,
        "CALIB_MIN_BRIGHT": CALIB_MIN_BRIGHT,
        "CALIB_MAX_BRIGHT": CALIB_MAX_BRIGHT
    }
    try:
        with open(path, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print("Error saving settings:", e)

# Load saved settings before building the UI
load_settings()

# --- UI SETUP ---
root = tk.Tk()
root.title("Adaptive Brightness Settings")
root.geometry("380x530")
# Hide the window on startup and when user clicks the red X
root.protocol("WM_DELETE_WINDOW", root.withdraw)
root.withdraw()

def show_settings(icon_item=None, item=None):
    # root.after() is used to ensure thread safety when called from the tray's thread
    root.after(0, root.deiconify)
    root.after(0, root.lift)
    root.after(0, root.focus_force)

status_var = tk.StringVar(value="Status: Initializing...")

def update_status(msg):
    """Thread-safe way to update the status label on the UI."""
    root.after(0, lambda: status_var.set(msg))

def apply_settings():
    global CHECK_INTERVAL, CAMERA_INDEX, CALIB_MIN_LIGHT, CALIB_MAX_LIGHT, CALIB_MIN_BRIGHT, CALIB_MAX_BRIGHT
    try:
        new_interval = int(interval_var.get())
        CHECK_INTERVAL = max(10, new_interval) # prevent crazy low polling numbers
        CAMERA_INDEX = int(camera_var.get())
        CALIB_MIN_LIGHT = float(min_light_var.get())
        CALIB_MAX_LIGHT = float(max_light_var.get())
        CALIB_MIN_BRIGHT = int(min_bright_var.get())
        CALIB_MAX_BRIGHT = int(max_bright_var.get())
        
        save_settings_to_file()
        update_status("Status: Settings Applied & Saved!")
    except ValueError:
        update_status("Status: Invalid input in settings!")
        pass

def reset_settings():
    global CHECK_INTERVAL, CAMERA_INDEX, CALIB_MIN_LIGHT, CALIB_MAX_LIGHT, CALIB_MIN_BRIGHT, CALIB_MAX_BRIGHT
    CHECK_INTERVAL = 300
    CAMERA_INDEX = 0
    CALIB_MIN_LIGHT = 2.0
    CALIB_MAX_LIGHT = 61.0
    CALIB_MIN_BRIGHT = 10
    CALIB_MAX_BRIGHT = 50
    
    interval_var.set(str(CHECK_INTERVAL))
    camera_var.set(str(CAMERA_INDEX))
    min_light_var.set(str(CALIB_MIN_LIGHT))
    max_light_var.set(str(CALIB_MAX_LIGHT))
    min_bright_var.set(str(CALIB_MIN_BRIGHT))
    max_bright_var.set(str(CALIB_MAX_BRIGHT))
    
    save_settings_to_file()
    update_status("Status: Settings Reset to Defaults!")

# Build the UI elements
ttk.Label(root, text="Adaptive Brightness Setup", font=("Arial", 12, "bold")).pack(pady=10)
ttk.Label(root, textvariable=status_var, foreground="blue").pack(pady=5)

settings_frame = ttk.Frame(root)
settings_frame.pack(pady=10)

ttk.Label(settings_frame, text="Check Interval (seconds):").grid(row=0, column=0, padx=5)
interval_var = tk.StringVar(value=str(CHECK_INTERVAL))
ttk.Entry(settings_frame, textvariable=interval_var, width=10).grid(row=0, column=1, padx=5)

ttk.Label(settings_frame, text="Camera Index:").grid(row=1, column=0, padx=5, pady=5)
camera_var = tk.StringVar(value=str(CAMERA_INDEX))
ttk.Combobox(settings_frame, textvariable=camera_var, values=["0", "1", "2"], width=8, state="readonly").grid(row=1, column=1, padx=5, pady=5)

calib_frame = ttk.LabelFrame(root, text="Calibration Settings")
calib_frame.pack(pady=10, padx=15, fill="x")

ttk.Label(calib_frame, text="Min Light (Raw):").grid(row=0, column=0, padx=5, pady=5)
min_light_var = tk.StringVar(value=str(CALIB_MIN_LIGHT))
ttk.Entry(calib_frame, textvariable=min_light_var, width=8).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(calib_frame, text="Max Light (Raw):").grid(row=0, column=2, padx=5, pady=5)
max_light_var = tk.StringVar(value=str(CALIB_MAX_LIGHT))
ttk.Entry(calib_frame, textvariable=max_light_var, width=8).grid(row=0, column=3, padx=5, pady=5)

ttk.Label(calib_frame, text="Min Brightness (%):").grid(row=1, column=0, padx=5, pady=5)
min_bright_var = tk.StringVar(value=str(CALIB_MIN_BRIGHT))
ttk.Entry(calib_frame, textvariable=min_bright_var, width=8).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(calib_frame, text="Max Brightness (%):").grid(row=1, column=2, padx=5, pady=5)
max_bright_var = tk.StringVar(value=str(CALIB_MAX_BRIGHT))
ttk.Entry(calib_frame, textvariable=max_bright_var, width=8).grid(row=1, column=3, padx=5, pady=5)

ttk.Button(root, text="Apply Changes", command=apply_settings).pack(pady=5)
ttk.Button(root, text="Reset to Defaults", command=reset_settings).pack(pady=5)

ttk.Button(root, text="Hide to System Tray", command=root.withdraw).pack(pady=5)
# --- END UI SETUP ---


def create_image():
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.ellipse([16, 16, 48, 48], fill=(255, 200, 0))
    return image


def get_brightness_target():
    """Takes 5 samples, returns the median of them, then maps it based on calibration."""
    try:
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened(): return None

        samples = []
        for _ in range(SAMPLE_COUNT):
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                samples.append(np.mean(gray))
            time.sleep(0.5)
        cap.release()

        if not samples: return None

        median_light = np.median(samples)

        # Dynamic mapping based on user calibration
        divisor = max(1.0, (CALIB_MAX_LIGHT - CALIB_MIN_LIGHT))
        target = (median_light - CALIB_MIN_LIGHT) * (CALIB_MAX_BRIGHT - CALIB_MIN_BRIGHT) / divisor + CALIB_MIN_BRIGHT
        return int(max(CALIB_MIN_BRIGHT, min(100, target)))
    except Exception as e:
        print(f"Error: {e}")
        return None


def apply_brightness(target):
    """Step-by-step brightness adjustment to target brightness."""
    try:
        current = sbc.get_brightness()[0]
        if target != current:
            step = 1 if target > current else -1
            for b in range(current, target + step, step):
                if not running: break
                sbc.set_brightness(b)
                time.sleep(SMOOTH_DELAY)
            update_status(f"Status: Applied Brightness {target}%")
    except Exception as e:
        print(f"Brightness Application Error: {e}")


def process_brightness_adjustment():
    """Core logic to apply brightness and do a secondary measurement to account for screen reflection."""
    target = get_brightness_target()
    if target is not None:
        apply_brightness(target)
        
        # apply_brightness blocks until brightness transition is fully completed.
        # Now perform a second measurement to correct reflection from current screen brightness.
        target2 = get_brightness_target()
        if target2 is not None:
            apply_brightness(target2)

def manual_update():
    """Manually updating the brightness."""
    process_brightness_adjustment()


def adaptive_logic():
    global running
    while running:
        battery = psutil.sensors_battery()
        is_plugged = battery.power_plugged if battery else True

        if is_plugged:
            update_status("Status: Running...")
            process_brightness_adjustment()

            # Wait for CHECK_INTERVAL seconds before checking again
            for _ in range(CHECK_INTERVAL):
                if not running: break
                time.sleep(1)
        else:
            update_status("Status: Paused (On Battery)")
            time.sleep(10)  # Checking if the device is plugged in every 10 seconds


def on_quit(icon_item=None, item=None):
    global running
    running = False
    if icon_item:
        icon_item.stop()
    root.after(0, root.destroy) # Safely close the UI


if __name__ == "__main__":
    thread = threading.Thread(target=adaptive_logic, daemon=True)
    thread.start()

    icon = Icon("AdaptiveBrightness", create_image(), menu=Menu(
        MenuItem("Settings", show_settings),
        MenuItem("Update Now", lambda: threading.Thread(target=manual_update).start()),
        MenuItem("Exit", on_quit)
    ))
    
    # Run pystray in a background thread
    threading.Thread(target=icon.run, daemon=True).start()
    
    # Run Tkinter in the main thread (required for Windows/macOS GUIs)
    root.mainloop()