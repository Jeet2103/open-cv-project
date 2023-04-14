import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
areas=[]
cam = cv.VideoCapture(0)
lower_blue = np.array([5,150,100])
upper_blue = np.array([15,255,255])
while(True):
    ret, frame = cam.read()
    frame = cv.flip(frame,1)
    frame = cv.resize(frame, (720,720), interpolation=cv.INTER_AREA)
    tw=frame.shape[1]
    th=frame.shape[0]
    w1_3 = int(1/3 * tw)
    w2_3 = int(2/3 * tw)
    h1_3 = int(1/3 * th)
    h2_3 = int(2/3 * th)
    cv.rectangle(frame, (0, 0), (0 + tw, 0 + th), (0, 0, 255), 3)
    cv.line(frame,(w1_3,0),(w1_3,th),(0,0,255),3)
    cv.line(frame, (w2_3, 0), (w2_3, th), (0, 0, 255), 3)
    cv.line(frame, (0, h1_3), (tw, h1_3), (0, 0, 255), 3)
    cv.line(frame, (0, h2_3), (tw, h2_3), (0, 0, 255), 3)
    img_smooth = cv.GaussianBlur(frame,(7,7),0)
    img_hsv = cv.cvtColor(img_smooth,cv.COLOR_BGR2HSV)
    img_threshold = cv.inRange(img_hsv,lower_blue,upper_blue)
    contours, h = cv.findContours(img_threshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    if len(contours)!=0:
        areas = [cv.contourArea(c) for c in contours]
        max=np.argmax(areas)
        cnt=contours[max]
        M = cv.moments(cnt)
        if(M['m00']!= 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv.circle(frame,(cx,cy),4,(0,255,0),-1)
        if(cx<w1_3 and cy<w1_3):
            location = "topleft"
        elif(cx<w2_3 and cx>w1_3 and cy<w1_3):
            location = "topmid"
        elif(cx>2_3 and cy<w1_3):
            location = "topright"
        elif(cx<w1_3 and cy>w1_3 and cy<w2_3):
            location = "midleft"
        elif (cx < w2_3 and cx>w1_3 and cy>w1_3 and cy<w2_3):
            location = "midmid"
        elif (cx > 2_3 and cy>w1_3 and cy<w2_3):
            location = "midright"
        elif (cx < w1_3 and cy > w2_3):
            location = "bottomleft"
        elif (cx > w1_3 and cx < w2_3 and cy > w2_3):
            location = "bottommid"
        elif (cx > w2_3 and cy > w2_3):
            location = "bottomright"
        print(location)
    cv.imshow('Frame',frame)
    if cv.waitKey(5)==27:
        break
# img_RGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
# plt.imshow(img_RGB)
# plt.show()
cam.set(cv.CAP_PROP_EXPOSURE, 0)
cam.release()
cv.destroyAllWindows()