#trafficsignaldetection1


import cv2 as cv
import numpy as np
# import serial
import time
from matplotlib import pyplot as plt
# arduino = serial.Serial('com7',9600)
# time.sleep(2)
max_red=max_green=0
cam = cv.VideoCapture(0)
lower_red = np.array([0,0,244])
upper_red = np.array([4,12,255])
# lower_yellow = np.array([0,0,0])
# upper_yellow = np.array([0,0,0])
# lower_green = np.array([27,26,153])
# upper_green = np.array([41,255,255])
while(True):
    fps = cam.get(cv.CAP_PROP_FPS)
    fps=str(int(fps))+'fps'
    ret, frame = cam.read()
    frame = cv.flip(frame,1)
    # frame = cv.resize(frame, (720,720), interpolation=cv.INTER_AREA)
    img_smooth = cv.GaussianBlur(frame,(7,7),0)
    img_hsv = cv.cvtColor(img_smooth,cv.COLOR_BGR2HSV)
    red_signal = cv.inRange(img_hsv,lower_red,upper_red)
    # green_signal = cv.inRange(img_hsv, lower_green, upper_green)
    contours_red, h = cv.findContours(red_signal, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # contours_green, h = cv.findContours(green_signal, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    if len(contours_red)!=0:
        areas_red = [cv.contourArea(c) for c in contours_red]
        max_red = np.argmax(areas_red)
    else:
        max_red = 0
    # if len(contours_green)!=0:
    #     areas_green = [cv.contourArea(c) for c in contours_green]
    #     max_green = np.argmax(areas_green)
    #     print(max_green)
    # else:
    #     max_green = 0


    if max_red!=0:
        print("RED SIGNAL")
    # elif max_green>max_red:
    #     print("GREEN SIGNAL")
    else:
        print("NO RED SIGNAL")
    image = cv.putText(frame,fps,(8,35), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)
    cv.imshow('Robot Vision',frame)
    if cv.waitKey(30)==27:
        break

cam.release()
cv.destroyAllWindows()