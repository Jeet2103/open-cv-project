# AEIE1


import cv2 as cv
import numpy as np

import time
import serial
arduino = serial.Serial('com7',9600)
time.sleep(2)


contour_x = contour_y = 0
max = cnt = 0
max_red=max_green=0

lower_lane = np.array([4, 0, 0])
upper_lane = np.array([40, 255, 43])
lower_red = np.array([0, 128,236])
upper_red = np.array([17,176,255])


cam = cv.VideoCapture(0)

while (True):
    fps = cam.get(cv.CAP_PROP_FPS)
    fps = str(int(fps)) + 'fps'
    ret, frame = cam.read()
    frame = cv.flip(frame, 1)

    tw = frame.shape[1]
    th = frame.shape[0]
    w5_14 = int(5 / 14 * tw)
    w9_14 = int(9 / 14 * tw)
    h8_10 = int(8 / 10 * th)
    cv.line(frame, (w5_14, 0), (w5_14, th), (0, 255, 0), 3)
    cv.line(frame, (w9_14, 0), (w9_14, th), (0, 255, 0), 3)
    cv.line(frame, (0, h8_10), (tw, h8_10), (0, 255, 0), 3)

    bottom_frame = frame[int((8 / 10) * (th)):th, 0:tw]
    lane_hsv = cv.cvtColor(bottom_frame, cv.COLOR_BGR2HSV)
    lane_threshold = cv.inRange(lane_hsv, lower_lane, upper_lane)
    kernel = np.ones((5, 5), np.uint8)
    lane_threshold_eroded = cv.erode(lane_threshold, kernel)
    lane_contours, h = cv.findContours(lane_threshold_eroded, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    top_frame = frame[0:int((8 / 10) * (th)), 0:tw]
    red_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    red_mask = cv.inRange(red_hsv, lower_red, upper_red)
    red_mask = cv.erode(red_mask, kernel)
    red_contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    red_blobs = [cv.contourArea(c) for c in red_contours]
    if len(red_blobs) != 0:
        max_red = np.argmax(red_blobs)
    else:
        max_red = 0

    if max_red>0:
        signal='red'
        print(signal)
        cnt=red_contours[max_red]
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(top_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(top_frame, 'RED', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    else:
        signal='not red'
    if len(lane_contours) != 0:
        areas = [cv.contourArea(c) for c in lane_contours]
        max = np.argmax(areas)
        cnt = lane_contours[max]
        M = cv.moments(cnt)
        if (M['m00'] != 0):
            contour_x = int(M['m10'] / M['m00'])
            contour_y = int(M['m01'] / M['m00'])
            cv.circle(bottom_frame, (contour_x, contour_y), 4, (0, 0, 255), -1)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(bottom_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if (contour_x < w5_14 and signal=='not red'):
                # location = "left"
                cv.putText(bottom_frame, "Lane on Left", (x + w + 5, y + h - 8), cv.FONT_HERSHEY_PLAIN, 0.8,
                           (0, 0, 255), 1, cv.LINE_AA)
                arduino.write(b'R')
            elif (contour_x > w5_14 and contour_x < w9_14 and signal=='not red'):
                # location = "on-Lane"
                cv.putText(bottom_frame, "Lane in Centre", (x + w + 5, y + h - 8), cv.FONT_HERSHEY_PLAIN, 0.8,
                           (0, 0, 255), 1, cv.LINE_AA)
                arduino.write(b'F')
            elif (contour_x > w9_14 and signal=='not red'):
                # location = "right"
                cv.putText(bottom_frame, "Lane on Right", (x + w + 5, y + h - 8), cv.FONT_HERSHEY_PLAIN, 0.8,
                           (0, 0, 255), 1, cv.LINE_AA)
                arduino.write(b'L')
            # print(location)
    else:
        cv.putText(frame, "NO Lane :(", (int(th / 2), int(tw / 2)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                   cv.LINE_AA)
        arduino.write(b'S')
        # print("lane not found")

    cv.putText(frame, fps, (8, 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
    cv.imshow('Frame', frame)
    if cv.waitKey(30) == 27:
        arduino.write(b'S')
        break
cam.release()
cv.destroyAllWindows()