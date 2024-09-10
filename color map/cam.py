import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, change it if you have multiple cameras

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Capture the video frame by frame
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Live Feed', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()






