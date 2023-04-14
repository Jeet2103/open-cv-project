# AEIE FINAL CODE 1
# ©SOUMYAJIT DATTA


# importing the required libraries
import cv2 as cv
import numpy as np
import time
import serial


# establishing serial communication with arduino
arduino = serial.Serial('com7',9600)
time.sleep(2)


# initializing variables
contour_x = contour_y = 0
max = cnt = 0
max_red = max_green = 0




# ENTER THE HSV VALUES BELOW BEFORE STARTING THE BOT

# *********** HSV OF LANE ***********
lower_lane = np.array([4, 0, 0])
upper_lane = np.array([40, 255, 43])

# *********** HSV OF RED SIGNAL ***********
lower_red = np.array([0, 128, 236])
upper_red = np.array([17, 176, 255])





# starting the camera
cam = cv.VideoCapture(0)

# entering the loop for the video
while (True):

    # reading the fps
    fps = cam.get(cv.CAP_PROP_FPS)
    fps = str(int(fps)) + 'fps'

    # reading the frame from the camera output
    ret, frame = cam.read()

    # flipping the frame
    frame = cv.flip(frame, 1)

    # reading the total height and total height of the frame
    tw = frame.shape[1]
    th = frame.shape[0]

    # establishing values to appropriately place the grid lines for detecting the location of the lane
    w5_14 = int(5 / 14 * tw)  # left grid
    w9_14 = int(9 / 14 * tw)  # right grid
    h8_10 = int(8 / 10 * th)  # bottom grid

    # drawing the grid lines on the frame
    cv.line(frame, (w5_14, 0), (w5_14, th), (0, 0, 0), 2)
    cv.line(frame, (w9_14, 0), (w9_14, th), (0, 0, 0), 2)
    cv.line(frame, (0, h8_10), (tw, h8_10), (0, 0, 0), 2)

    # ********** OPERATIONS FOR LANE DETECTION **********

    # cropping the bottom part of the frame for lane detection
    bottom_frame = frame[int((8 / 10) * (th)):th, 0:tw]

    # converting bottom frame from bgr to hsv and thresholding it according to the hsv values entered at the beginning of the code
    lane_hsv = cv.cvtColor(bottom_frame, cv.COLOR_BGR2HSV)
    lane_threshold = cv.inRange(lane_hsv, lower_lane, upper_lane)

    # performing morphological operations on the lane threshold
    kernel = np.ones((5, 5), np.uint8)
    lane_threshold_eroded = cv.erode(lane_threshold, kernel)

    # drawing contours on the morphologically eroded image
    lane_contours, h = cv.findContours(lane_threshold_eroded, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # ********** OPERATIONS FOR SIGNAL DETECTION **********

    # cropping the Top part of the frame for signal detection
    top_frame = frame[0:int((8 / 10) * (th)), 0:tw]

    # converting Top frame from bgr to hsv and thresholding it according to the hsv values entered at the beginning of the code
    red_hsv = cv.cvtColor(top_frame, cv.COLOR_BGR2HSV)
    red_threshold = cv.inRange(red_hsv, lower_red, upper_red)

    # performing morphological operations on the red signal threshold
    red_threshold_eroded = cv.erode(red_threshold, kernel)

    # drawing contours on the morphologically eroded image
    red_contours, _ = cv.findContours(red_threshold_eroded, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # finding red blobs from the red contours
    red_blobs = [cv.contourArea(c) for c in red_contours]

    # ********** Determining whether the signal is Red or Not Red **********

    if len(red_blobs) > 0:

        # changing the value of signal variable to Red
        signal = 'Red'

        # finding the max contour by area
        cnt = red_contours[np.argmax(red_blobs)]

        # drawing a rectangle around the red light from the signal
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(top_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    else:

        # if signal is not red the value of the signal variable is changed to Not Red
        signal = 'Not Red'

    # ********** Detecting the Lane **********

    # if the length of the lane_contours array is not null

    if len(lane_contours) != 0:

        # if a lane is detected

        areas = [cv.contourArea(c) for c in lane_contours]
        max = np.argmax(areas)
        cnt = lane_contours[max]

        # calculating the centroid of the lane contour with max area

        M = cv.moments(cnt)
        if (M['m00'] != 0):
            contour_x = int(M['m10'] / M['m00'])
            contour_y = int(M['m01'] / M['m00'])

            # drawing a circle marker on the centre of the max lane contour
            cv.circle(bottom_frame, (contour_x, contour_y), 4, (0, 0, 255), -2)
            x, y, w, h = cv.boundingRect(cnt)

            # drawing a rectangle marker around the detected lane

            cv.rectangle(bottom_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # ********** MAIN MOVEMENT CONTROL OF THE BOT **********

            # if the signal is red the bot is stopped

            if signal == "Red":
                robot_movement = "Stopped"
                arduino.write(b'RS')

            # else the bot continues to move

            else:

                # if the lane is on the left grid of the bottom frame

                if (contour_x < w5_14):

                    # the robot moves left

                    location = "Left"
                    arduino.write(b'L')
                    robot_movement = "Left"

                # if the lane is on the middle grid of the bottom frame

                elif (contour_x > w5_14 and contour_x < w9_14):

                    # the robot moves forward

                    location = "Centre"
                    arduino.write(b'F')
                    robot_movement = "Forward"

                # if the lane is on the right grid of the bottom frame

                elif (contour_x > w9_14):

                    # the robot moves right
                    location = "Right"
                    arduino.write(b'R')
                    robot_movement = "Right"

    # if NO lane is detected

    else:

        # the robot stops

        arduino.write(b'LS')
        location = "Not Found"
        robot_movement = "Stopped"


    # ********** PUTTING TEXT ON THE TOP LEFT OF THE FRAME **********

    cv.putText(frame, ("<FRONT CAM>"), (240, 22), cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1, cv.LINE_AA)
    cv.putText(frame, ("FPS: " + fps), (6, 18), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 125), 1, cv.LINE_AA)
    cv.putText(frame, ("LANE LOCATION: " + location), (6, 38), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 125), 1, cv.LINE_AA)
    cv.putText(frame, ("ROBOT MOVEMENT: " + robot_movement), (6, 58), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 125), 1,
               cv.LINE_AA)
    cv.putText(frame, ("SIGNAL STATUS: " + signal), (6, 78), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 125), 1,
               cv.LINE_AA)

    # displaying the final frame

    cv.imshow('Frame', frame)

    # if the escape key is pressed then the loop breaks,the video is paused and the robot is stopped

    if cv.waitKey(30) == 27:
        arduino.write(b'S')
        break

# the camera is released and the windows are closed

cam.release()
cv.destroyAllWindows()