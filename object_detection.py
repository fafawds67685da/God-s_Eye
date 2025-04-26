import torch
import cv2
import numpy as np

# Load YOLOv5 pre-trained model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# DroidCam video stream URL
url = 'http://172.16.17.138:4747/video'

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model(frame)
    detected_objects = results.pandas().xyxy[0]['name'].tolist()

    # Optionally, display the video feed with detected objects
    results.show()

    print("Detected objects:", detected_objects)

    # Send the classified objects to the agent
    # This part can be customized based on how you want to send the objects to the agent.

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
