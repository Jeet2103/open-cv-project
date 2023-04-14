import cv2 as cv
from matplotlib import pyplot as pt
img = cv.imread("WIN_20230205_20_04_38_Pro.jpg")
cv.imshow('BGR',img)
img_HSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
cv.imshow('HSV',img_HSV)
img_RGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
img_HSV_RGB = cv.cvtColor(img_HSV,cv.COLOR_BGR2RGB)
pt.imshow(img_RGB)
title = ['image1' , 'image2']
images = [ img_RGB,img_HSV_RGB]
pt.axis('off')
for i in range(2):
    pt.subplot(1,2,i+1)
    pt.title(title[i])
    pt.imshow(images[i])
    pt.xticks([])
    pt.yticks([])


pt.show()
cv.waitKey(0)
cv.destroyAllWindows()
