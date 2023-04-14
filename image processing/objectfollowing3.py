import cv2 as cv
import numpy as np
import serial
import time
from matplotlib import pyplot as plt
# arduino = serial.Serial('com3',9600)
# time.sleep(2)
areas=[]
contour_x=contour_y=0
cam = cv.VideoCapture(0)
lower_color = np.array([0,7,245])
upper_color = np.array([4,20,255])
while(True):
    fps = cam.get(cv.CAP_PROP_FPS)
    fps=str(int(fps))+'fps'
    ret, frame = cam.read()
    frame = cv.flip(frame,1)
    # frame = cv.resize(frame, (720,720), interpolation=cv.INTER_AREA)
    tw=frame.shape[1]
    th=frame.shape[0]
    w1_3 = int(1/3 * tw)
    w2_3 = int(2/3 * tw)
    w3_7 = int(3/7 * tw)
    w4_7 = int(4/7 * tw)
    h1_3 = int(1/3 * th)
    h2_3 = int(2/3 * th)
    h5_6 = int(5/6 * th)
    cv.rectangle(frame, (0, 0), (0 + tw, 0 + th), (0, 255, 0), 3)
    cv.line(frame,(w1_3,0),(w1_3,th),(0,255,0),3)
    cv.line(frame, (w2_3, 0), (w2_3, th), (0, 255, 0), 3)
    cv.line(frame, (0, h2_3), (tw, h2_3), (0, 255, 0), 3)

    img_smooth = cv.GaussianBlur(frame,(7,7),0)
    img_hsv = cv.cvtColor(img_smooth,cv.COLOR_BGR2HSV)
    img_threshold = cv.inRange(img_hsv,lower_color,upper_color)
    contours, h = cv.findContours(img_threshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    if len(contours)!=0:
        areas = [cv.contourArea(c) for c in contours]
        max=np.argmax(areas)
        cnt=contours[max]
        M = cv.moments(cnt)
        if(M['m00']!= 0):
            contour_x = int(M['m10']/M['m00'])
            contour_y = int(M['m01'] / M['m00'])
            cv.circle(frame,(contour_x,contour_y),4,(0,0,255),-1)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if(contour_x<w1_3 and contour_y<h5_6):
            location = "topleft"
            # arduino.write(b'R')
        elif(contour_x<w2_3 and contour_x>w1_3 and contour_y<h5_6):
            location = "topmid"
            # arduino.write(b'F')
        elif(contour_x>2_3 and contour_y<h5_6):
            location = "topright"
            # arduino.write(b'L')
        elif (contour_x < w3_7 and contour_y > h5_6):
            location = "bottomleft"
            # arduino.write(b'R')
        elif (contour_x > w3_7 and contour_x < w4_7 and contour_y > h5_6):
            location = "bottommid"
            # arduino.write(b'S')
        elif (contour_x > w4_7 and contour_y > h5_6):
            location = "bottomright"
            # arduino.write(b'L')
        print(location)
    image = cv.putText(frame,fps,(8,35), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)
    cv.imshow('Frame',frame)
    if cv.waitKey(30)==27:
        # arduino.write(b'S')
        break
cam.release()
cv.destroyAllWindows()
