import cv2 as cv
# from matplotlib import pyplot as pt
img = cv.imread("35903FC900000578-3654952-image-a-103_1466627943675.jpg")
cv.imshow("messi",img)
# img1imshow(img_RGB)
# pt.show()
ball = img[260:327,878:946]
# ball=([255,255,255])
img[260:327,78:146] = ball
cv.imshow('white',img)


cv.waitKey(0)
cv.destroyAllWindows()