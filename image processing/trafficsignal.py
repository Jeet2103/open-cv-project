import cv2 as cv
import numpy as np

max_red=max_green=0
# Define the color ranges for red and green signals in HSV format
red_lower = np.array([0, 128,236])
red_upper = np.array([17,176,255])
# green_lower = np.array([54,83,191])
# green_upper = np.array([88,245, 255])

# Create a video camture object for the default camera
cam = cv.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cam.read()

    # Convert the frame to HSV format
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Create binary masks for the red and green signals
    red_mask = cv.inRange(hsv, red_lower, red_upper)
    # green_mask = cv.inRange(hsv, green_lower, green_upper)


    # Apply morphological operations to the masks
    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv.erode(red_mask, kernel)
    # red_mask = cv.dilate(red_mask, kernel)
    # green_mask = cv.erode(green_mask, kernel)
    # green_mask = cv.dilate(green_mask, kernel)

    # Find contours in the masks
    red_contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # green_contours, _ = cv.findContours(green_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter the contours based on size and shape
    red_blobs = [cv.contourArea(c) for c in red_contours]
    if len(red_blobs)!=0:
        max_red=np.argmax(red_blobs)
    else:
        max_red=0
    # green_blobs = [cv.contourArea(c) for c in green_contours]
    # if len(green_blobs)!=0:
    #     max_green=np.argmax(green_blobs)

    if max_red>0:
        print('red signal')
        cnt=red_contours[max_red]
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(frame, 'RED', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    else:
        print('no red signal')
    # Draw bounding boxes around the filtered blobs
    # for c in red_blobs:
    #     x, y, w, h = cv.boundingRect(c)
    #     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #     cv.putText(frame, 'RED', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    # for c in green_blobs:
    #     x, y, w, h = cv.boundingRect(c)
    #     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     cv.putText(frame, 'GREEN', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv.imshow('Traffic Signal Detection', frame)
    if cv.waitKey(2)==27:
        break
cam.release()
cv.destroyAllWindows()