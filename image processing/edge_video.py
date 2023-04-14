import cv2 as cv
from matplotlib import pyplot as pt
vid = cv.VideoCapture(0)
while (1):
    ret,frame = vid.read()
    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(frame,50,100)
    cv.imshow('nice',edges)

    if cv.waitKey(20)== 27:
        break
vid.release()
cv.destroyAllWindows()



