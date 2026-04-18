# Adaptive Brightness Utility

## Overview
The Adaptive Brightness utility is a Python-based background application (`.pyw`) that automatically adjusts the computer's screen brightness based on ambient light conditions. It uses the device's webcam to sample light levels and sits quietly in the system tray.

## Key Features
* **Ambient Light Detection**: Uses OpenCV (`cv2`) to take multiple snapshots from the webcam, converting them to grayscale to calculate the median ambient light.
* **Smooth Transitions**: Adjusts the screen brightness step-by-step (`sbc`) to prevent jarring visual changes.
* **Reflection Correction**: Performs a secondary light measurement after the initial adjustment to compensate for the screen's own light reflecting onto the user/camera.
* **Power Awareness**: Pauses automatic adjustments when the device is running on battery power (`psutil`) to conserve energy.
* **System Tray Interface**: Provides a minimal UI via `pystray` to force a manual update or exit the application cleanly.

## Code Structure (`adaptive_brightness.pyw`)
* **`get_brightness_target()`**: Captures 5 webcam frames, calculates the median brightness, and maps it to a calibrated 10-100 screen brightness scale.
* **`apply_brightness(target)`**: Steps the current screen brightness toward the target value smoothly.
* **`process_brightness_adjustment()`**: Orchestrates the measurement and application process, including the reflection correction step.
* **`adaptive_logic()`**: The main background loop running on a separate thread. Checks power status and triggers adjustments every 5 minutes (300 seconds) if plugged in.
* **System Tray Logic**: `create_image()`, `manual_update()`, and `on_quit()` handle the generation of the tray icon and its context menu actions.

## Potential Improvements & Future Roadmap
Here are some suggestions to enhance the quality and robustness of the project:

1. **External Configuration**: 
   Move hardcoded constants (like `CHECK_INTERVAL`, `SAMPLE_COUNT`, and the calibration curve points) into a `config.json` file. This allows tweaking without editing the source code.
   
2. **Multi-Monitor Support**: 
   Update the `screen_brightness_control` logic to handle or specify secondary displays, as currently, it grabs the primary display's brightness index `[0]`.
   
3. **Logging System**: 
   Implement the standard `logging` library with a rolling log file instead of `print()` statements. Because this is a `.pyw` file (which runs without a console), standard `print` outputs are lost, making debugging difficult if it fails in the background.
   
4. **Graceful Camera Handling**: 
   If the camera is in use by another application (e.g., Zoom or Teams), `cv2.VideoCapture(0)` might fail or hang. Adding logic to gracefully skip adjustments when the camera is locked would improve stability.

5. **Dynamic Camera Device Selection**: 
   Allow the user to specify which camera index to use if multiple cameras are connected (e.g., a laptop lid closed with an external webcam plugged in).