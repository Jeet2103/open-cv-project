#LORD OF COLOR DETECTION


import cv2 as cv
import numpy as np
cam=cv.VideoCapture(0)
cam.set(1,640)
cam.set(2,480)
def empty(a):
    pass

cv.namedWindow("HSV")
cv.resizeWindow("HSV",640,240)
cv.createTrackbar("HUE min","HSV",0,179,empty)
cv.createTrackbar("HUE max","HSV",179,179,empty)
cv.createTrackbar("SAT min","HSV",0,255,empty)
cv.createTrackbar("SAT max","HSV",255,255,empty)
cv.createTrackbar("VALUE min","HSV",0,255,empty)
cv.createTrackbar("VALUE max","HSV",255,255,empty)


while True:
    b,img=cam.read()
    # img=cv.resize(img, (640,480), interpolation=cv.INTER_AREA)

    img_hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)

    HUE_min=cv.getTrackbarPos("HUE min", "HSV")
    HUE_max=cv.getTrackbarPos("HUE max", "HSV")
    SAT_min=cv.getTrackbarPos("SAT min", "HSV")
    SAT_max=cv.getTrackbarPos("SAT max", "HSV")
    VALUE_min=cv.getTrackbarPos("VALUE min", "HSV")
    VALUE_max=cv.getTrackbarPos("VALUE max", "HSV")

    lower = np.array([HUE_min,SAT_min,VALUE_min])
    upper = np.array([HUE_max,SAT_max,VALUE_max])

    mask = cv.inRange(img_hsv,lower,upper)
    result = cv.bitwise_and(img,img,mask=mask)
    mask=cv.cvtColor(mask,cv.COLOR_GRAY2BGR)
    hstack = np.hstack([mask,result])
    cv.imshow('COLOR PICKER',hstack)

    k=cv.waitKey(2)
    if k==27:
        break



cam.release()

cv.destroyAllWindows()