# Hand gesture-keyboard interrupter
A real time Python application that uses computer vision and hand gesture detection to control keyboard inputs. The system tracks a single hand, detects simple gestures (open/closed and left/right/center position), and maps them to keyboard actions.

## 📌 Project Overview

This project captures live video from a webcam, detects hand landmarks using **MediaPipe**, and interprets hand gestures to simulate keyboard inputs via **PyAutoGUI**. It is designed as a simple and modular **Human–Computer Interaction (HCI)** prototype.

## 🧠 How the System Works

The application is divided into three logical modules:
- 1.hand_tracking.py # Hand detection & landmark extraction
- 2. gesture_detection.py # Gesture logic and spatial analysis
- 3. main.py # Application loop and keyboard control
 
## 🔍 Module Breakdown

### 1. Hand Tracking (`hand_tracking.py`)
- Uses **MediaPipe Hands** for real-time hand landmark detection
- Processes webcam frames using OpenCV
- Detects up to one hand by default
- Draws 21 hand landmarks and connections on the video feed

**Responsibilities**
- Frame preprocessing (BGR → RGB)
- Hand landmark detection
- Landmark visualization

### 2. Gesture Detection (`gesture_detection.py`)

#### Hand Open / Closed Detection
- Computes distances between:
  - Thumb tip
  - Index finger tip
  - Middle finger tip
- If distances exceed a fixed threshold, the hand is considered **open**
- Otherwise, the hand is considered **closed**

#### Hand Direction Detection
- Uses the **wrist landmark (index 0)** to determine horizontal position
- Frame is divided into three regions:
  - Left
  - Center
  - Right

### 3. Main Application (`main.py`)
- Captures webcam feed
- Calls hand tracking and gesture detection modules
- Maps gestures to keyboard actions
- Uses cooldown logic to prevent repeated key triggering
- Displays real-time gesture state on the video feed

## 🎮 Gesture to Key Mapping

| Gesture Condition | Keyboard Action |
|------------------|-----------------|
| Hand Open | Press `W`, release `S` |
| Hand Closed | Press `S`, release `W` |
| Hand Left | Press `A`, release `D` |
| Hand Right | Press `D`, release `A` |
| Hand Center | Release `A` and `D` |

> Forward/backward movement is controlled by hand open/close,  
> while left/right steering is controlled by horizontal hand position.

## ⏱️ Control Logic

- **Cooldown period**: 0.2 seconds between actions  
- **Target frame rate**: 60 FPS  
- Prevents accidental rapid key presses  
- Maintains independent state tracking for:
  - Hand open/closed
  - Direction (left/right/center)

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – video capture and visualization
- **MediaPipe** – real-time hand landmark detection
- **PyAutoGUI** – keyboard input simulation
