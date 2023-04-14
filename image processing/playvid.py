import cv2 as cv
vid = cv.VideoCapture('WhatsApp Video 2023-02-12 at 01.33.31.mp4')
while (vid.isOpened()):
    ret,frame= vid.read()
    cv.imshow('frame',frame)
    key = cv.waitKey(50)
    if key == 27:
        break
vid.release()
cv.destroyAllWindows()