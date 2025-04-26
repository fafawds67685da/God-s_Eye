import torch
import cv2
import numpy as np
import requests
import os
import time
from datetime import datetime

# Load YOLOv8 pre-trained model
from ultralytics import YOLO

model = YOLO('yolov8s.pt')

# Use Laptop Camera (usually device 0)
cap = cv2.VideoCapture(0)

# Create folder to save frames
save_folder = "captured_frames"
os.makedirs(save_folder, exist_ok=True)

# Save frame every n seconds
save_interval = 2  # seconds
last_save_time = time.time()

# Photo counter
photo_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    current_time = time.time()

    if current_time - last_save_time >= save_interval:
        # Run object detection
        results = model(frame)

        # Extract detections
        boxes = results[0].boxes.xyxy.cpu().numpy()
        labels = results[0].boxes.cls.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()

        # Get detected object names
        detected_objects = [model.names[int(cls)] for cls in labels]

        # Draw bounding boxes
        for box, label, conf in zip(boxes, labels, confidences):
            x1, y1, x2, y2 = map(int, box)
            class_name = model.names[int(label)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Save the frame with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_folder}/frame_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        photo_counter += 1  # Increment counter

        print(f"[{photo_counter}] Saved: {filename}")
        print("Detected objects:", detected_objects)

        # Send only the first detected object (class) to the agent
        try:
            if detected_objects:
                detected_class = detected_objects[-1]  # last detected object
                response = requests.post(
                    'http://127.0.0.1:5001/detect',
                    json={'objects': [detected_class]}  
                )
                # agent_response = response.json().get('response', 'No response from agent.')
                # print("Agent response:", agent_response)
        except Exception as e:
            print(f"Error sending data to agent: {e}")

        last_save_time = current_time

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting loop.")
        break

cap.release()
cv2.destroyAllWindows()
