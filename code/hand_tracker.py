import numpy as np
import imutils
import cv2
from PIL import Image
import pygame, sys
from pygame.locals import *

def home_screen():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    start = pygame.Rect(300, 300, 50, 50)
    font = pygame.font.Font(None, 32)
    pygame.display.set_caption("CVPaint")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() >= (300,300):
                    if pygame.mouse.get_pos() <= (350,350):
                            running = False
        screen.fill(pygame.Color(255, 255, 255))
        pygame.draw.rect(screen, [255, 0, 0], start)  # draw button
        pygame.display.update()
    pygame.quit();

def boundaries_and_initialize():
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    pts = []
    camera = cv2.VideoCapture(0)
    return greenLower, greenUpper, pts, camera

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
def paint(greenLower, greenUpper, pts, camera):
    linecolor = (0,0,0)
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        #Blur the image
        blur = cv2.blur(frame,(3,3))
        #Convert to HSV color space
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        #Create a binary image with where white will be skin colors and rest is black
        mask2 = cv2.inRange(hsv,np.array([2,50,50]),np.array([15,255,255])) #for skin colors
        #Kernel matrices for morphological transformation
        kernel_square = np.ones((11,11),np.uint8)
        kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        #Perform morphological transformations to filter out the background noise
        #Dilation increase skin color area
        #Erosion increase skin color area
        dilation = cv2.dilate(mask2,kernel_ellipse,iterations = 1)
        erosion = cv2.erode(dilation,kernel_square,iterations = 1)
        dilation2 = cv2.dilate(erosion,kernel_ellipse,iterations = 1)
        filtered = cv2.medianBlur(dilation2,5)
        kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
        dilation2 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
        kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dilation3 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
        median = cv2.medianBlur(dilation2,5)
        grabbed,thresh = cv2.threshold(median,127,255,0)
        #Find contours of the filtered frame
        uhhh, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #Find Max contour area (Assume that hand is in the frame)
        max_area=100
        ci=0
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        if ci>=len(contours): #Passes if color cannot be found
            pass
        else:
            cnts = contours[ci]
        #Find convex hull
        hull = cv2.convexHull(cnts)
        #Find moments of the largest contour
        moments = cv2.moments(cnts)
        #Central mass of first order moments
        if moments['m00']!=0:
            cx = int(moments['m10']/moments['m00']) # cx = M10/M00
            cy = int(moments['m01']/moments['m00']) # cy = M01/M00
        centerMass=(cx,cy)
        # Find area of contour for thickness calculations
        contourArea = cv2.contourArea(hull)
        thiccness = int(((contourArea-500)/16638.8889)+2)

        # color space
        frame = imutils.resize(frame, width=600)
        center = None
        center = centerMass

        # update the points queue
        pts.insert(0,(center, linecolor, thiccness))
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

        if pts[0][0] is not None:
            if 0 < pts[0][0][1] <= 45:
                linecolor = pickColor(pts[0][0])


        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1][0] is None or pts[i][0] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            # thiccness = int(((contourArea-500)/16638.8889)+2)
            cv2.line(frame, pts[i - 1][0], pts[i][0], pts[i][1], pts[i][2])

        #flip_frame = cv2.flip(frame,1)
        # show the frame to our screen
        cv2.imshow("Frame", cv2.flip(frame,1))
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

def save_file(camera):
    #user can input the name of the file when saving
    save = input("Would you like to save your drawing? Enter yes or no ")
    if save == "yes" or save == "y" or save == "ye" or save == "yes ":
        name = input("What would you like to name your masterpiece? ")
        filename = 'images/' + name + '.png'
        cv2.imwrite(filename, cv2.flip(frame,1))
        camera.release()
        cv2.destroyAllWindows()
        img = Image.open(filename)
        img.show()
    # cleanup the camera and close any open windows
    else:
        camera.release()
        cv2.destroyAllWindows()

print("press q to quit")
home_screen()
lower, upper, pts, camera = boundaries_and_initialize()
paint(lower, upper, pts, camera)
save_file(camera)
