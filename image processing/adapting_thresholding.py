import cv2 as cv
from matplotlib import pyplot as pip
img = cv.imread('PXL_20230213_103529146.jpg',0)
img = cv.medianBlur(img,5)
# cv.imshow("original_image",img)
ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
titles = ['original_image','threshold_image','adapting_threshold_mean','adapting_threshold_gaussian']
images = [img,th1,th2,th3]
for i in range(4):
    pip.subplot(2,2,i+1)
    pip.imshow(images[i], 'gray')
    pip.title(titles[i])
    pip.xticks([])
    pip.yticks([])
pip.show()
# cv.imshow(,th1)
# cv.imshow('adapting_threshold_mean',th2)
# cv.imshow('adapting_threshold_gaussian',th3)
cv.waitKey(0)
cv.destroyAllWindows()