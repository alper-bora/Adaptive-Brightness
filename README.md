# Adaptive Brightness Control

A Python-based utility that automatically adjusts your system's screen brightness based on ambient light levels captured by your webcam.

## Overview

Adaptive Brightness Control acts as a closed-loop feedback system to provide a comfortable viewing experience. It continuously monitors ambient light, processes the input to filter out sudden changes, and smoothly adjusts the screen brightness to an optimal level. 

## Features

- **Ambient Light Sensing:** Uses the connected webcam to sample environmental light levels.
- **Smart Filtering:** Applies median filtering to multiple image samples to ignore temporary light spikes or movement.
- **Smooth Transitions:** Gradually fades brightness levels to prevent jarring changes.
- **Feedback Correction:** Performs secondary measurements to account for screen glare and reflection, ensuring accurate calibration.
- **Battery Awareness:** Conserves energy by pausing automatic adjustments when the device is running on battery power.
- **System Tray Integration:** Runs quietly in the background with a convenient system tray icon for manual overrides and exit controls.

## Prerequisites

- Python 3.x
- A connected webcam

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alper-bora/Adaptive-Brightness.git
   cd Adaptive-Brightness
   ```

2. Install the required dependencies:
   ```bash
   pip install opencv-python screen-brightness-control numpy pystray pillow psutil
   ```

## Usage

Run the script using python:

```bash
python adaptive_brightness.pyw
```

*Note: The `.pyw` extension allows the script to run in the background without opening a persistent console window.*

Once running, you will see a sun icon in your system tray. You can right-click this icon to manually trigger an update or to exit the application.

## Technologies Used

- **OpenCV (`cv2`):** Frame capture and image processing.
- **NumPy:** Statistical calculations (median filtering).
- **Screen Brightness Control:** Hardware-level brightness adjustments.
- **PyStray & Pillow:** System tray interface.
- **Psutil:** Battery state monitoring.
