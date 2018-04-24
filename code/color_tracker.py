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

# define the lower and upper boundaries of the "green"
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

def pickColor(point):
    x = point[0]
    y = point[1]
    if 0 < x <= 75 and 0 < y <= 45:
        #eraser
        return (255, 255, 255)
    if 75 < x <= 150 and 0 < y <= 45:
        #black
        return (0,0,0)
    if 150 < x <= 225 and 0 < y <= 45:
        #purple
        return (255,0,242)
    if 150 < x <= 300 and 0 < y <= 45:
        #blue
        return (255,0,0)
    if 300 < x <= 375 and 0 < y <= 45:
        #green
        return (0,255,63)
    if 375 < x <= 450 and 0 < y <= 45:
        #yellow
        return (0,250,255)
    if 450 < x <= 525 and 0 < y <= 45:
        #orange
        return (0,174,255)
    if 525 < x <= 600 and 0 < y <= 45:
        #red
        return (0,0,255)
# keep looping
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
            cv2.circle(frame, (int(x), int(y)), int(radius),
                 (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 255, 0), -1)

    # update the points queue
    #pts.appendleft(center)
    pts.insert(0,center)
    # loop over the set of tracked points
    cv2.rectangle(frame, (0,0), (600,450), (255,255,255), -1)

    # initialize the colorbar (REMEMBER BGR NOT RGB)
    cv2.rectangle(frame, (0,0), (75,49), (0,0,0), 2)           # white/eraser
    cv2.rectangle(frame, (75,0), (150,50), (0,0,0), -1)        # black
    cv2.rectangle(frame, (150,0), (225,50), (255,0,242), -1)   # violet/purple
    cv2.rectangle(frame, (225,0), (300,50), (255,0,0), -1)     # blue
    cv2.rectangle(frame, (300,0), (375,50), (0,255,63), -1)    # green
    cv2.rectangle(frame, (375,0), (450,50), (0,250,255), -1)   # yellow
    cv2.rectangle(frame, (450,0), (525,50), (0,174,255), -1)   # orange
    cv2.rectangle(frame, (525,0), (600,50), (0,0,255), -1)     # red
    linecolor = (0,0,0)
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        if 0 < pts[i][0] <= 600 and 0 < pts[i][1] <= 50:
            linecolor = pickColor(pts[i])
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], linecolor, thickness)

    #flip_frame = cv2.flip(frame,1)
    # show the frame to our screen
    cv2.imshow("Frame", cv2.flip(frame,1))
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

cv2.imwrite('code/images/oof.png', cv2.flip(frame,1))
# cleanup the camera and close any open windows

camera.release()
cv2.destroyAllWindows()




















# oh shiiii waddup
