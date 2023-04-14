import cv2 as cv
import numpy as nm
from matplotlib import pyplot as pt
vdo = cv.VideoCapture(0)
lower_yellow = nm.array([45,103,99])
upper_yellow = nm.array([57,200,182])
while (True):
    ret,frame = vdo.read()
    # smooth
    img_smooth = cv.GaussianBlur(frame,(7,7),0)
    #hsv
    img_hsv = cv.cvtColor(img_smooth,cv.COLOR_BGR2HSV)
    #threshold
    img_thresh = cv.inRange(img_hsv,lower_yellow, upper_yellow)
    #find contours
    contours,heirarchy = cv.findContours(img_thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    # Find the index of the largest contour
    if (len(contours)!= 0 ):
        areas = [cv.contourArea(c) for c in contours]
        max_index = nm.argmax(areas)
        cnt = contours[max_index]
        x_bound, y_bound,w_bound, h_bound = cv.boundingRect(cnt)
        cv.rectangle(frame,(x_bound,y_bound),(x_bound+w_bound,y_bound+h_bound),(255,0,0))



    cv.imshow('frame',frame)
    if cv.waitKey(10)==27:
        break

# img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
# pt.xticks([])
# pt.yticks([])
# pt.imshow(img_rgb)
# pt.show()
vdo.release()
cv.destroyAllWindows()
# 25,56,111
#218,77,43