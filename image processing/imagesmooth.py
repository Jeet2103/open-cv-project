import cv2 as cv
from matplotlib import pyplot as pt
img = cv.imread('download.jpeg')
blur =cv.blur(img,(30,30))
gaussian_blur = cv.GaussianBlur(img,(15,15),0)
median_blur = cv.medianBlur(img,5)
bilateram_filter = cv.bilateralFilter(img,30,120,120)
pt.subplot(231)
pt.imshow(img)
pt.title('original')
pt.xticks([])
pt.yticks([])

pt.subplot(232)
pt.imshow(blur)
pt.title('blur')
pt.xticks([])
pt.yticks([])

pt.subplot(233)
pt.imshow(gaussian_blur)
pt.title('gaussian_blur')
pt.xticks([])
pt.yticks([])

pt.subplot(234)
pt.imshow(median_blur)
pt.title('median')
pt.xticks([])
pt.yticks([])

pt.subplot(235)
pt.imshow(bilateram_filter)
pt.title('bilateram')
pt.xticks([])
pt.yticks([])

pt.show()