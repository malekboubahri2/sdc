import tkinter as tk
import threading
import time
import os
import subprocess
import cv2

# === CONFIG ===
SAVE_DIR = r"C:\Users\dakhl\Desktop\sight_project\boat_detected"
SCRIPT_PATHS = [
    r"C:\Users\dakhl\Desktop\sight_project\illegal_fishing_cam0.py",
    r"C:\Users\dakhl\Desktop\sight_project\illegal_fishing_cam1.py"
]
CAMERA_IDS = [0, 1]

# Initial state
detection_flags = [False, False]
last_detected_time = [0, 0]
show_live = [False, False]

# === FUNCTIONS ===
def launch_detection_scripts():
    for script in SCRIPT_PATHS:
        subprocess.Popen(["python", script], creationflags=subprocess.CREATE_NO_WINDOW)

def monitor_folder():
    previous_files = set(os.listdir(SAVE_DIR))
    while True:
        current_files = set(os.listdir(SAVE_DIR))
        new_files = current_files - previous_files
        current_time = time.time()

        for f in new_files:
            if "boat_" in f and f.endswith(".jpg"):
                # Example: boat_XXXXXXXX.jpg => determine cam ID from file name or pattern
                # Here we assume filenames contain 'cam0' or 'cam1' if needed
                # Otherwise we alternate to simulate (since detection script names don't encode cam ID)
                cam_index = 0 if time.time() % 2 < 1 else 1
                detection_flags[cam_index] = True
                last_detected_time[cam_index] = current_time

        for i in range(2):
            if current_time - last_detected_time[i] > 10:
                detection_flags[i] = False

        previous_files = current_files
        time.sleep(1)

def blink_buttons():
    for i in range(1):
        if detection_flags[i]:
            current = buttons[i].cget("bg")
            buttons[i].config(bg="red" if current == "white" else "white")
        else:
            buttons[i].config(bg="lightgray")
    root.after(500, blink_buttons)

'''def show_camera_live(cam_id):
    show_live[cam_id] = True
    cap = cv2.VideoCapture(CAMERA_IDS[cam_id])
    win_name = f"Camera {cam_id + 1}"

    while show_live[cam_id]:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            show_live[cam_id] = False
            cv2.destroyWindow(win_name)
            break
    cap.release()'''

# === GUI SETUP ===
root = tk.Tk()
root.title("Surveillance Interface")
root.geometry("300x200")
buttons = []

btn0 = tk.Button(root, text="Camera 0", bg="lightgray", font=("Arial", 16))
btn0.pack(pady=20)
buttons.append(btn0)

btn1 = tk.Button(root, text="Camera 1", bg="lightgray", font=("Arial", 16) )
btn1.pack(pady=20)
buttons.append(btn1)

# === START THREADS ===
threading.Thread(target=launch_detection_scripts, daemon=True).start()
threading.Thread(target=monitor_folder, daemon=True).start()
blink_buttons()

root.mainloop()
