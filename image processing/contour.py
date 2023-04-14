import cv2 as cv
import numpy as nm
img = cv.imread('WhatsApp Image 2023-02-15 at 01.31.08.jpg')
img_gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret,thresh = cv.threshold(img_gray,127,255,0)
contours,hierachy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(img,contours,-1,(255,0,0,),3)
# cv.drawContours(img,contours,1,(0,255,0),3)
# cv.drawContours(img,contours,5,(0,0,255),3)

cnt = contours[6]
cv.drawContours(img,[cnt],-1,(0,0,255),3)

cv.imshow('contours',img)
cv.waitKey(0)
cv.destroyAllWindows()