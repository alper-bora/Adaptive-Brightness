# Adaptive Brightness Control

A Python-based utility that automatically adjusts your system's screen brightness based on ambient light levels captured by your webcam.

## Overview

Adaptive Brightness Control acts as a closed-loop feedback system to provide a comfortable viewing experience. It continuously monitors ambient light, processes the input to filter out sudden changes, and smoothly adjusts the screen brightness to an optimal level.

## Features

- **Ambient Light Sensing:** Uses the connected webcam to sample environmental light levels.
- **Settings GUI:** A user-friendly interface to customize camera selection, check intervals, and brightness calibration.
- **Smart Filtering:** Applies median filtering to multiple image samples to ignore temporary light spikes or movement.
- **Smooth Transitions:** Gradually fades brightness levels to prevent jarring changes.
- **Persistent Configuration:** Automatically saves and loads your preferences from a JSON file (`adaptive_brightness_settings.json`).
- **Battery Awareness:** Conserves energy by pausing automatic adjustments when the device is running on battery power.
- **System Tray Integration:** Runs quietly in the background with a convenient system tray icon for manual overrides, settings access, and exit controls.
- **Windows Startup Support:** Includes a deployment script to easily build a standalone executable and add it to your Windows Startup folder.

## Prerequisites

- Python 3.x
- A connected webcam
- Windows OS (for brightness control and startup deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alper-bora/Adaptive-Brightness.git
   cd Adaptive-Brightness
   ```

2. Install the required dependencies:
   ```bash
   pip install opencv-python screen-brightness-control numpy pystray pillow psutil pyinstaller
   ```

## Usage

Run the script using python:

```bash
python adaptive_brightness.pyw
```

*Note: The `.pyw` extension allows the script to run in the background without opening a persistent console window.*

Once running, you will see a sun icon in your system tray. You can right-click this icon to:
- **Update Now:** Manually trigger a brightness adjustment.
- **Settings:** Open the configuration GUI to adjust parameters.
- **Exit:** Close the application.

## Deployment (Windows)

To build a standalone executable and add it to your Windows Startup folder, run the deployment script:

```bash
python deploy.py
```

Follow the prompts to build and deploy. This will create a single `.exe` file in the `dist` folder and copy it to your startup directory (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`).

## Technologies Used

- **OpenCV (`cv2`):** Frame capture and image processing.
- **Tkinter:** Settings GUI for user customization.
- **NumPy:** Statistical calculations (median filtering).
- **Screen Brightness Control:** Hardware-level brightness adjustments.
- **PyStray & Pillow:** System tray interface.
- **Psutil:** Battery state monitoring.
- **PyInstaller:** Standalone executable building.
