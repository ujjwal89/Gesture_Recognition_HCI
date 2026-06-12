# Gesture Recognition HCI Framework 

An advanced human-computer interaction (HCI) software suite leveraging computer vision to control operating system inputs using real-time hand gestures.

## Core Architecture & Components
This ecosystem isolates the tracking computational overhead into a reusable interface module:

* **`HandTrackingModule.py`:** The fundamental pipeline built on **MediaPipe Hands** and **OpenCV**. It normalises RGB video streams, maps spatial coordinates for up to 21 multi-hand landmarks, calculates vector distances, and tracks finger states.
* **`VirtualMouse.py`:** Uses index and middle finger tracking logic to manipulate screen coordinates, featuring smoothed spatial interpolation (`np.interp`) and automated operating system click injections via `autopy`.
* **`virtualKeyboard.py`:** Renders a virtual keyboard overlay onto live video frames, processing intersection bounds to register structural typing events using `pynput`.
* **`VolumeGestureControl.py`:** Maps the Euclidean distance between a user's thumb and index finger to core system audio endpoints using the Windows Core Audio API (`pycaw`).

## Installation & Tech Stack
- **Language:** Python
- **Environment:** Desktop / Webcam execution
- **Libraries:** OpenCV-Python, MediaPipe, NumPy, PyCaw, Autopy, Pynput
