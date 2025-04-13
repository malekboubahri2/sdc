from ultralytics import YOLO
import cv2
import time
import os
import secrets  # Pour générer un PIN sécurisé

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Define the folder where you want to store captured images
boat_detected_path = r"C:\Users\dakhl\Desktop\sight_project\boat_detected"
os.makedirs(boat_detected_path, exist_ok=True)

#Open camera
cap = cv2.VideoCapture(0)

boat_photos_taken = 0
last_detection_time = 0
capture_interval = 1  # seconds between photos

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated_frame = frame.copy()

    # Check if any boats are detected
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name == "boat":
                # Draw red bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(annotated_frame, class_name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                current_time = time.time()

                if boat_photos_taken < 4 and (current_time - last_detection_time) >= capture_interval:
                    boat_crop = frame[y1:y2, x1:x2]
                    
                    # Générer un code PIN aléatoire de 8 caractères hexadécimaux
                    pin_code = secrets.token_hex(4).upper()  # 4 bytes = 8 hex characters
                    
                    # Construire le nom de fichier
                    img_name = f"boat_{pin_code}.jpg"
                    img_path = os.path.join(boat_detected_path, img_name)

                    cv2.imwrite(img_path, boat_crop)
                    print(f"[INFO] Boat image captured and saved as {img_name}.")
                    boat_photos_taken += 1
                    last_detection_time = current_time

                break

        if boat_photos_taken >= 4 and (time.time() - last_detection_time) > 10:
            boat_photos_taken = 0
            print("[INFO] Ready for new boat detection.")

    # Show result
    cv2.imshow("Vessel1 Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
