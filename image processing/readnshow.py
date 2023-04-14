import cv2 as cv
import numpy as np
img=cv.imread("Iron-Man.jpg")
print(img.shape)
for i in range(0,667):
    for j in range(0,1200):
        if img[i,j].sum() <20:
            img[i,j] = [255,255,255]

cv.imshow("iron",img)
cv.waitKey(0)
cv.destroyAllWindows()