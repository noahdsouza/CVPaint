# import the necessary packages
# cv2.rectangle(frame, (0,0), (100,100), (255,255,255), -1)
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from PIL import Image


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the green
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#pts = deque(maxlen=args["buffer"])
pts = []
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# function pickColor finds cursor's place in color bar to change paint color
def pickColor(point):
    x = point[0]
    y = point[1]
    # color_num = 0
    if 0 < x <= 75 and 0 < y <= 45:
        #eraser
        color_num = 0
        return (255, 255, 255)
    if 75 < x <= 150 and 0 < y <= 45:
        #black
        color_num = 1
        return (0,0,0)
    if 150 < x <= 225 and 0 < y <= 45:
        #purple
        color_num = 2
        return (255,0,242)
    if 150 < x <= 300 and 0 < y <= 45:
        #blue
        color_num = 3
        return (255,0,0)
    if 300 < x <= 375 and 0 < y <= 45:
        #green
        color_num = 4
        return (0,255,63)
    if 375 < x <= 450 and 0 < y <= 45:
        #yellow
        color_num = 5
        return (0,250,255)
    if 450 < x <= 525 and 0 < y <= 45:
        #orange
        color_num = 6
        return (0,174,255)
    if 525 < x <= 600 and 0 < y <= 45:
        #red
        color_num = 7
        return (0,0,255)
# keep looping this

linecolor = (0,0,0)
space_counter = 0
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    quit_key = cv2.waitKey(1) & 0xFF
    pause_key = cv2.waitKey(1) & 0xFF
    # create a counter for the number of times the space bar is pressed
    if pause_key == ord("p"):
        space_counter = space_counter+1
        # print(space_counter)
    # # only make points and draw if the space bar is pressed an even amount of times
    # if space_counter%2 == 0:

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), linecolor, 2)
            cv2.circle(frame, center, 5, linecolor, -1)

    # update the points queue
    #pts.appendleft(center)
    # only make points and draw if the space bar is pressed an even amount of times
    if space_counter%2 == 0:
        pts.insert(0,center)
    # loop over the set of tracked points
    # cv2.rectangle(frame, (0,0), (600,450), (255,255,255), -1)

    # initialize the colorbar (REMEMBER BGR NOT RGB)
    cv2.rectangle(frame, (0,0), (75,49), (0,0,0), 2)           # white/eraser
    cv2.rectangle(frame, (75,0), (150,50), (0,0,0), -1)        # black
    cv2.rectangle(frame, (150,0), (225,50), (255,0,242), -1)   # violet/purple
    cv2.rectangle(frame, (225,0), (300,50), (255,0,0), -1)     # blue
    cv2.rectangle(frame, (300,0), (375,50), (0,255,63), -1)    # green
    cv2.rectangle(frame, (375,0), (450,50), (0,250,255), -1)   # yellow
    cv2.rectangle(frame, (450,0), (525,50), (0,174,255), -1)   # orange
    cv2.rectangle(frame, (525,0), (600,50), (0,0,255), -1)     # red

    # if pts[0] is not None:
    #     if 0 < pts[0][1] <= 45:
    #         linecolor = pickColor(pts[0])
    #         # print("change?")
    #         # print(linecolor)

    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        if pts[0] is not None:
            if 0 < pts[0][1] <= 45:
                linecolor = pickColor(pts[0])

        # nah we good --> # otherwise, compute the thickness of the line and
        # draw the connecting lines
        # thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], linecolor, 2)
        # print("current")
        # print(linecolor)

    #flip_frame = cv2.flip(frame,1)
    # show the frame to our screen
    cv2.imshow("Frame", cv2.flip(frame,1))
    # quit_key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if quit_key == ord("q"):
        break

#user can input the name of the file when saving
name = input("What would you like to name your masterpiece? ")
filename = 'images/' + name + '.png'
cv2.imwrite(filename, cv2.flip(frame,1))
# cleanup the camera and close any open windows

camera.release()
cv2.destroyAllWindows()




















# oh shiiii waddup
