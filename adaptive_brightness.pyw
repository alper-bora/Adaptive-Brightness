import cv2
import screen_brightness_control as sbc
import numpy as np
import time
import threading
import psutil
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# SETTINGS
CHECK_INTERVAL = 300
SAMPLE_COUNT = 5
SMOOTH_DELAY = 0.05
running = True


def create_image():
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.ellipse([16, 16, 48, 48], fill=(255, 200, 0))
    return image


def get_brightness_target():
    """Takes 5 samples, returns the median of them, then maps it to a range of 10-100."""
    try:
        cap = cv2.VideoCapture(0)
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

        # Calibrated mapping from 2-70 to 10-100
        target = (median_light - 2) * (50 - 10) / (61 - 2) + 10
        return int(max(10, min(100, target)))
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
            process_brightness_adjustment()

            # Wait for CHECK_INTERVAL seconds before checking again
            for _ in range(CHECK_INTERVAL):
                if not running: break
                time.sleep(1)
        else:
            time.sleep(10)  # Checking if the device is plugged in every 10 seconds


def on_quit(icon_item):
    global running
    running = False
    icon_item.stop()


if __name__ == "__main__":
    thread = threading.Thread(target=adaptive_logic, daemon=True)
    thread.start()

    icon = Icon("AdaptiveBrightness", create_image(), menu=Menu(
        MenuItem("Update Now", lambda: threading.Thread(target=manual_update).start()),
        MenuItem("Exit", on_quit)
    ))
    icon.run()