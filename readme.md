# YOLOv8 Person Detection & WhatsApp Alert System

This project is a Python-based security script that uses computer vision to detect people in real-time using a webcam. When a person is detected, it captures an image and sends it immediately to a specified WhatsApp number using the `pywhatkit` library.

## Features

* **Real-time Detection:** Uses YOLOv8 (You Only Look Once) for fast and accurate person detection.
* **WhatsApp Integration:** Automatically sends the captured image to a target phone number.
* **Flexible Modes:**
    * `single`: Detects once, sends an alert, and stops.
    * `continuous`: Keeps detecting and sending alerts at set intervals.
* **Smart Scheduling:** Set a time limit (e.g., run until 18:00) or an alert limit (e.g., max 5 alerts).
* **Connectivity Check:** Verifies internet connection before attempting to send alerts to prevent crashes.

## Prerequisites

You need Python 3.8+ installed(Created on Python 3.13.9 and not tested for backward compatability). You also need the following Python libraries:

* opencv-python
* ultralytics
* pywhatkit

## Installation

1.  Clone this repository or download the source code.
2.  Install the required dependencies:

```bash
pip install opencv-python ultralytics pywhatkit
```

*Note: The first time you run the script, `ultralytics` will automatically download the `yolov8n.pt` model file.*

## Usage

Run the script from the command line. The only required argument is the target phone number (with country code).

### Basic Example (Single Alert)

```bash
python main.py --number "+1234567890"
```

### Continuous Mode Example

Run continuously, checking every 10 seconds, stopping after 5 alerts are sent:

```bash
python main.py --number "+1234567890" --mode continuous --interval 10 --limit 5
```

### Time Limit Example

Run the script but automatically stop at 6:30 PM (18:30):

```bash
python main.py --number "+1234567890" --until "1830"
```

## Command Line Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--number` | String | **Required** | Target WhatsApp number with country code (e.g., "+919876543210"). |
| `--mode` | String | `single` | `single` (one alert then exit) or `continuous` (keep monitoring). |
| `--delay` | Int | `0` | Seconds to wait before starting the camera (useful for leaving the room). |
| `--out` | String | `detections` | Directory folder name to save captured images. |
| `--interval` | Int | `3` | Seconds to wait between detections in continuous mode. |
| `--limit` | Int | `5` | Maximum number of alerts to send in continuous mode. |
| `--until` | String | `None` | Stop time in 24h format HHMM (e.g., "1430" for 2:30 PM). |

## Important Notes

1.  **WhatsApp Web:** `pywhatkit` uses browser automation. You must have **WhatsApp Web logged in** on your default browser for this to work.
2.  **Browser Focus:** Do not minimize the browser window while the script is trying to send a message, as it requires active focus to upload the image.

<!-- end list -->