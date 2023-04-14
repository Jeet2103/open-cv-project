import cv2 as cv
import numpy as np
import time
import serial
arduino = serial.Serial('com7',9600)
time.sleep(2)
areas=[]
contour_x=contour_y=0
cam = cv.VideoCapture(0)
lower_color = np.array([15,10,10])
upper_color = np.array([25,80,80])
while(True):
    fps = cam.get(cv.CAP_PROP_FPS)
    fps=str(int(fps))+'fps'
    ret, frame = cam.read()
    frame = cv.flip(frame,1)
    frame = cv.resize(frame, (720,720), interpolation=cv.INTER_AREA)
    tw=frame.shape[1]
    th=frame.shape[0]
    w5_14 = int(5/14 * tw)
    w9_14 = int(9/14 * tw)
    h8_10 = int(8/10 * th)
    cv.line(frame,(w5_14,0),(w5_14,th),(0,255,0),3)
    cv.line(frame, (w9_14, 0), (w9_14, th), (0, 255, 0), 3)
    cv.line(frame, (0, h8_10), (tw, h8_10), (0, 255, 0), 3)

    bottom_frame=frame[int((8/10)*(th)):th,0:tw]
    img_smooth = cv.GaussianBlur(bottom_frame,(7,7),0)
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
            cv.circle(bottom_frame,(contour_x,contour_y),4,(0,0,255),-1)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(bottom_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if (contour_x < w5_14):
            location = "left"
            arduino.write(b'R')
        elif (contour_x > w5_14 and contour_x < w9_14):
            location = "on-Lane"
            arduino.write(b'F')
        elif (contour_x > w9_14):
            location = "bottomright"
            arduino.write(b'L')
        print(location)
    else:
        arduino.write(b'S')
        print("lane not found")

    image = cv.putText(frame,fps,(8,35), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)
    cv.imshow('Frame',frame)
    if cv.waitKey(30)==27:
        arduino.write(b'S')
        break
cam.release()
cv.destroyAllWindows()
