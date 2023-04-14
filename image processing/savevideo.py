import cv2 as cv
vid = cv.VideoCapture(0)
fourcc = cv.VideoWriter_fourcc(*'XVID')
output = cv.VideoWriter('output_video.avi',fourcc,20.0,(640,480))
while (vid.isOpened()):
    ret,frame = vid.read()
    if ret == True :
        cv.imshow('frame',frame)
        output.write(frame)
        key = cv.waitKey(1)
        if key == ord ('q'):
            print(" Saved video...")
            break
    else:
        print("Error....")
vid.release()
output.release()
cv.destroyAllWindows()




