import cv2 as cv
import numpy as np
cam = cv.VideoCapture(0)
while True:
    ret,frame = cam.read()
    tw = frame.shape[1]
    th = frame.shape[0]
    w5_14 = int(5 / 14 * tw)
    w9_14 = int(9 / 14 * tw)
    h8_10 = int(8 / 10 * th)
    cv.line(frame, (w5_14, 0), (w5_14, th), (0, 255, 0), 3)
    cv.line(frame, (w9_14, 0), (w9_14, th), (0, 255, 0), 3)
    cv.line(frame, (0, h8_10), (tw, h8_10), (0, 255, 0), 3)
    bottom_frame = frame[int((8 / 10) * (th)):th, 0:tw]
    frame1=cv.cvtColor(bottom_frame,cv.COLOR_BGR2GRAY)
    ret, thresh1 = cv.threshold(frame1,75, 255, cv.THRESH_BINARY_INV)
    cv.imshow('Frame', frame)
    contours1, h = cv.findContours(thresh1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    if len(contours1)!=0:
        areas = [cv.contourArea(c) for c in contours1]
        max=np.argmax(areas)
        cnt=contours1[max]
        M = cv.moments(cnt)
        if(M['m00']!= 0):
            contour_x = int(M['m10']/M['m00'])
            contour_y = int(M['m01'] / M['m00'])
            cv.circle(frame1,(contour_x,contour_y),4,(0,0,255),-1)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv.imshow('Frame', frame)

            key = cv.waitKey(24)
            if key == 27:
                break
cam.release()
cv.destroyAllWindows()

