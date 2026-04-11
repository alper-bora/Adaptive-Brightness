# Adaptive Brightness Control 💡

An intelligent Python script that adjusts your laptop's screen brightness based on ambient light levels using your webcam. 

This project was developed by a first-year **Electrical and Electronics Engineering** student at **Dokuz Eylül University**. It combines basic signal processing concepts with computer vision to create a more comfortable working environment.

## 🚀 How it Works (The Engineering Logic)

As EEE students, we can think of this system as a **Closed-Loop Feedback System**:

1.  **Sensing (Input):** The webcam captures a set of images (samples).
2.  **Signal Processing:** 
    *   The images are converted to **Grayscale** to calculate average intensity.
    *   A **Median Filter** is applied to 5 samples to remove "noise" (like a sudden flash or movement).
3.  **Control Logic (Mapping):** The calculated ambient light value is mapped to a brightness percentage (10% to 100%) using a linear calibration formula.
4.  **Actuation (Output):** The script uses the `screen_brightness_control` library to adjust the hardware.
5.  **Feedback Correction:** After the first adjustment, the script takes a *second* measurement to account for the light reflected from the screen itself, ensuring higher accuracy.

## 🛠️ Built With

*   **Python:** The core language.
*   **OpenCV (`cv2`):** For capturing and processing webcam frames.
*   **NumPy:** For mathematical operations and median calculations.
*   **Screen Brightness Control:** To interface with Windows/Monitor hardware.
*   **PyStray & Pillow:** To create a neat System Tray icon so the script runs quietly in the background.

## 📦 Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/alper-bora/Adaptive-Brightness.git
   ```
2. **Install dependencies:**
   ```bash
   pip install opencv-python screen-brightness-control numpy pystray pillow psutil
   ```
3. **Run the script:**
   ```bash
   python adaptive_brightness.pyw
   ```
   *(The `.pyw` extension ensures it runs without an annoying console window appearing!)*

## ⚙️ Features

*   **Battery Awareness:** Only performs adjustments when the laptop is plugged in to save energy.
*   **Smooth Transitions:** Brightness doesn't "jump"—it fades smoothly to the target level.
*   **Manual Override:** Right-click the sun icon in your system tray to "Update Now" or Exit.

---
*Learning by doing — DEÜ EEE* 🐾
