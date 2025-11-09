# Mouse_cam
Mouse control using real-time hand detection. Move the cursor, click, and interact with your computer using gestures.

<img src="example.png" alt="Screenshot" width="400">

## Functions

- Hand detection (1 hand, 21 landmarks)  
- Adaptive cursor movement with smoothing  
- Precision mode (thumb & middle finger close)  
- Click detection (thumb & index finger tip)  
- Movement speed boost based on hand speed  
- On-screen status display (precision mode, movement, boost)  
- Real-time GUI with camera feed  

## Usage/Installation

1. Open a terminal (Git Bash, PowerShell, or CMD).  
2. Clone the repository:

```bash
git clone https://github.com/rodin04/Mouse_cam.git
```

3. Navigate to the project folder.
```bash
cd your_folder_path!!!
```

4. Install requirements.txt
```bash
pip install -r requirements.txt
```

## Start programm

1. Open a terminal (Git Bash, PowerShell, or CMD).
2. Navigate to the project folder.
```bash
cd your_folder_path!!!
```
3. Start python script
```bash
python mouse_cam.py
```

## Requirements

- Python 3.12+  
- OpenCV 4.8+ (`opencv-python==4.8.1.78`)  
- MediaPipe 0.10+ (`mediapipe==0.10.21`)  
- NumPy 1.24+ (`numpy==1.24.3`)  
- PyAutoGUI 0.9+ (`pyautogui==0.9.53`)  












