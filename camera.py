import torch
import cv2
import numpy as np
import requests
import os
import time
from datetime import datetime

# Load YOLOv5 pre-trained model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

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
        detected_objects = results.pandas().xyxy[0]['name'].tolist()

        # Draw bounding boxes
        for *box, conf, cls in results.xyxy[0]:
            label = model.names[int(cls)]
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
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
            detected_class = detected_objects[-1]  # Use only the first detected object
            response = requests.post(
                'http://127.0.0.1:5001/detect',
                json={'objects': [detected_class]}  # Send only the first class as a list
            )
           # agent_response = response.json().get('response', 'No response from agent.')
            #print("Agent response:", agent_response)
        except Exception as e:
            print(f"Error sending data to agent: {e}")

        last_save_time = current_time

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting loop.")
        break

cap.release()
cv2.destroyAllWindows()
