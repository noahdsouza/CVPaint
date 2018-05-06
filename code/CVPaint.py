import numpy as np
import imutils
import cv2
from PIL import Image
import pygame, sys
from pygame.locals import *

def home_screen(screen):
    start = pygame.image.load('start.png')
    font = pygame.font.Font(None, 32)
    logo = pygame.image.load("CVPAINTLOGO.png")
    logo = pygame.transform.scale(logo, (250, 200))
    instructions = pygame.image.load('instructions.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() >= (225, 350):
                    if pygame.mouse.get_pos() <= (350,400):
                            running = False
                            return True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    cv2.destroyAllWindows()
                    return False
        screen.fill(pygame.Color(255, 255, 255))
        screen.blit(logo, (190,50))
        screen.blit(start, (225,350))  # draw button
        screen.blit(instructions, (175, 275))
        pygame.display.update()

def boundaries_and_initialize():
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    pts = []
    linecolor = (0,0,0)
    counter = 0
    return greenLower, greenUpper, pts, linecolor, counter

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
        return (242,0,255)
    if 150 < x <= 300 and 0 < y <= 45:
        #blue
        return (0,0,255)
    if 300 < x <= 375 and 0 < y <= 45:
        #green
        return (63,255,0)
    if 375 < x <= 450 and 0 < y <= 45:
        #yellow
        return (255,250,0)
    if 450 < x <= 525 and 0 < y <= 45:
        #orange
        return (255,174,0)
    if 525 < x <= 600 and 0 < y <= 45:
        #red
        return (255,0,0)

def draw_color_bar(frame):
    # initialize the colorbar (in RGB)
    cv2.rectangle(frame, (0,0), (75,49), (0,0,0), 2)           # white/eraser
    cv2.rectangle(frame, (75,0), (150,50), (0,0,0), -1)        # black
    cv2.rectangle(frame, (150,0), (225,50), (242,0,255), -1)   # violet/purple
    cv2.rectangle(frame, (225,0), (300,50), (0,0,255), -1)     # blue
    cv2.rectangle(frame, (300,0), (375,50), (63,255,0), -1)    # green
    cv2.rectangle(frame, (375,0), (450,50), (255,250,0), -1)   # yellow
    cv2.rectangle(frame, (450,0), (525,50), (255,174,0), -1)   # orange
    cv2.rectangle(frame, (525,0), (600,50), (255,0,0), -1)     # red

def save_file(camera, frame):
    #user can input the name of the file when saving
    save = input("Would you like to save your drawing? Enter yes or no ")
    if save == "yes" or save == "y" or save == "ye" or save == "yes ":
        name = input("What would you like to name your masterpiece? ")
        filename = 'images/' + name + '.png'
        cv2.imwrite(filename, cv2.flip(frame,1))
        camera.release()
        pygame.quit()
        cv2.destroyAllWindows()
        img = Image.open(filename)
        img.show()
    # cleanup the camera and close any open windows
    else:
        pygame.quit()
        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    def main_loop():
        try:
            camera = cv2.VideoCapture(0)
            pygame.init()
            pygame.display.set_caption("CVPaint")
            screen = pygame.display.set_mode([600,450])
            flag = home_screen(screen)
            greenLower, greenUpper, pts, linecolor, counter = boundaries_and_initialize()

            while flag:
                grabbed, frame = camera.read()
                frame1 = imutils.resize(frame, width=600)

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, greenLower, greenUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # find contours in the mask and initialize the current
                # (x, y) center of the ball
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
                cv2.rectangle(frame1, (0,0), (600,450), (255,255,255), -1)
                # only proceed if at least one contour was found
                if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = ((int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])))

                    # only proceed if the radius meets a minimum size
                    if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        #cv2.circle(frame1, (int(x), int(y)), int(radius), linecolor, 2)
                        cv2.circle(frame1, center, 5, linecolor, -1)

                # update the points queue
                if counter%2 == 0:
                    pts.insert(0,(center, linecolor))
                # loop over the set of tracked points

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
                    #thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                    cv2.line(frame1, pts[i - 1][0], pts[i][0], pts[i][1], 3)

                draw_color_bar(frame1)

                frame = np.rot90(frame1)
                frame = pygame.surfarray.make_surface(frame)
                screen.blit(frame, (0,0))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_q:
                            flag = False
                            save_file(camera, frame1)
                        if event.key == K_SPACE:
                            counter += 1

        except KeyboardInterrupt:
            pygame.quit()
            cv2.destroyAllWindows()

main_loop()
