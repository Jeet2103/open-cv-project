import cv2 as cv
from matplotlib import pyplot as pt
img = cv.imread('WhatsApp Image 2023-02-14 at 02.21.31.jpg',0)
edges = cv.Canny(img,50,100)
cv.imshow('original',img)
cv.imshow('edges',edges)
pt.subplot(111)
pt.imshow(edges,'gray')
pt.xticks([])
pt.yticks([])
pt.show()
cv.waitKey(0)
cv.destroyAllWindows()