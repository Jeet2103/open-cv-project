import cv2 as cv
from matplotlib import pyplot as pt
cam = cv.VideoCapture(0)
while True:
    ret,frame = cam.read()
    img_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imshow('frame',frame)
    key = cv.waitKey(24)
    if key == 27:
        pt.imshow(img_RGB)
        pt.xticks([])
        pt.yticks([])
        break

pt.show()
cam.release()
cv.destroyAllWindows()

