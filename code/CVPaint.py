"""
CVPaint allows you to draw pictures using computer vision
AUTHORS: Rachel Won, Noah D'Souza, Chase Joyner
"""
import numpy as np
import imutils
import cv2
from PIL import Image
import pygame, sys
from pygame.locals import *

def home_screen(screen):
"""
instantiates the home screen in pygame before loading the CV2 window
the home screen contains the logo, instructions, and a start button
"""
    start = pygame.image.load('start.png')
    font = pygame.font.Font(None, 32)
    logo = pygame.image.load("CVPAINTLOGO.png")
    logo = pygame.transform.scale(logo, (250, 200))
    instructions = pygame.image.load('instructions.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #exit home screen if user clicks start button
                if pygame.mouse.get_pos() >= (225, 350):
                    if pygame.mouse.get_pos() <= (350,400):
                            running = False
                            return True
            if event.type == KEYDOWN: #can quit from the home screen with q
                if event.key == K_q:
                    pygame.quit()
                    cv2.destroyAllWindows()
                    return False
        screen.fill(pygame.Color(255, 255, 255))
        screen.blit(logo, (190,50)) #draw images/buttons on home screen
        screen.blit(start, (225,350))
        screen.blit(instructions, (175, 275))
        pygame.display.update()

def boundaries_and_initialize():
    """
    initializes all the constants needed for the drawing function and returns them
    """
    greenLower = (29, 86, 6)   # define the lower and upper boundaries of the "green"
    greenUpper = (64, 255, 255)
    pts = [((200,300),(255,255,255), 0)]
    blanks = []
    linecolor = (0,0,0)
    counter = 1
    radius = 11
    return greenLower, greenUpper, pts, linecolor, counter, blanks, radius

def pickColor(point):
    """
    returns the color in (RGB) the cursor is hovering over
    """
    x = point[0]
    y = point[1]
    depth = 40
    if 0 < x <= 72 and 0 < y <= depth:
        return (255, 255, 255) #eraser
    if 72 < x <= 138 and 0 < y <= depth:
        return (0,0,0) #black
    if 138 < x <= 204 and 0 < y <= depth:
        return (122,78,32) #brown
    if 204 < x <= 270 and 0 < y <= depth:
        return (242,0,255) #purple
    if 270 < x <= 336 and 0 < y <= depth:
        return (0,0,255) #blue
    if 336 < x <= 402 and 0 < y <= depth:
        return (63,255,0) #green
    if 402 < x <= 468 and 0 < y <= depth:
        return (255,250,0) #yellow
    if 468 < x <= 534 and 0 < y <= depth:
        return (255,174,0) #orange
    if 534 < x <= 600 and 0 < y <= depth:
        return (255,0,0) #red

def draw_color_bar(frame):
    """
    initialize and draw the colorbar on top of the drawing screen (in RGB)
    """
    depth = 35
    cv2.rectangle(frame, (0,0), (72,depth - 1), (0,0,0), 2)       # white/eraser
    cv2.rectangle(frame, (72,0), (138,depth), (0,0,0), -1)        # black
    cv2.rectangle(frame, (138,0), (204,depth), (122,78,32), -1)   # brown
    cv2.rectangle(frame, (204,0), (270,depth), (242,0,255), -1)   # violet/purple
    cv2.rectangle(frame, (270,0), (336,depth), (0,0,255), -1)     # blue
    cv2.rectangle(frame, (336,0), (402,depth), (63,255,0), -1)    # green
    cv2.rectangle(frame, (402,0), (468,depth), (255,250,0), -1)   # yellow
    cv2.rectangle(frame, (468,0), (534,depth), (255,174,0), -1)   # orange
    cv2.rectangle(frame, (534,0), (600,depth), (255,0,0), -1)     # red

def save_file(camera, frame):
    """
    gives the user an option to save their drawing or not
    takes user input from the command terminal
    saves the drawing as a png file in the images folder or destroys all windows
    user can name the png file
    """
    save = input("Would you like to save your drawing? Enter yes or no ")
    if save == "yes" or save == "y" or save == "ye" or save == "yes ": #accounting for typos
        name = input("What would you like to name your masterpiece? ")
        filename = 'images/' + name + '.png'
        cv2.imwrite(filename, cv2.flip(frame,1)) #saves the image as the last frame
        camera.release()
        pygame.quit()

        #reopen saved picture to display for user
        img = cv2.imread(filename, 1)
        b,g,r = cv2.split(img)  # get b,g,r
        rgb_img = cv2.merge([r,g,b]) #convert from bgr colorspace to rgb
        crop_img = rgb_img[36:450, 0:600] #crop out the colorbar
        cv2.imshow(filename, crop_img)
        cv2.imwrite(filename, crop_img)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()
        camera.release()
        pygame.quit() # cleanup the camera and close any open windows
    else:
        print("Thank you for trying CVPaint!")
        pygame.quit()
        camera.release()
        cv2.destroyAllWindows()

def draw(greenLower, greenUpper, pts, linecolor, counter, camera, screen, blanks, radius):
    """
    uses openCV inside the pygame window to track green object and draws
    spacebar toggles between drawing and not drawing
    """
    grabbed, frame = camera.read()
    frame1 = imutils.resize(frame, width=600)

    #find the green object and create a mask over it
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

    #check whether the user is in "drawing" mode or not
    if counter%2 == 0:
        pts.insert(0,(center, linecolor, counter))

    else:
        blanks.insert(0,(center, linecolor))

        #if user is not in drawing mode, still track the cursor
        #and change the color if hovering over the color bar
        if blanks[0][0] is not None:
            if 0 < blanks[0][0][1] <= 40:
                linecolor = pickColor(blanks[0][0])

    #change color
    if pts[0][0] is not None:
        if 0 < pts[0][0][1] <= 40:
            linecolor = pickColor(pts[0][0])

    for i in range(len(pts) - 1, 1, -1):
        # if either of the tracked points are None, ignore them
        if len(pts) == 0:
            continue
        if pts[i - 1][0] is None or pts[i][0] is None:
            continue
        # do not connect the last point before exiting "drawing mode" and
        # the first point after re-entering "drawing mode"
        if pts[i - 1][2] != pts[i][2]:
            continue
        #draw connecting lines
        cv2.line(frame1, pts[i][0], pts[i - 1][0], pts[i - 1][1], 3)

    if radius > 10:
        #if cursor is white, put a black frame around it
        if linecolor == (255,255,255):
            cv2.circle(frame1, center, 5, (0,0,0), 3)
        else:
            cv2.circle(frame1, center, 5, linecolor, -1)

    draw_color_bar(frame1)

    frame = np.rot90(frame1)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    pygame.display.update()

    #press q to exit
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                save_file(camera, frame1)
                return False, greenLower, greenUpper, pts, linecolor, counter, camera, screen, blanks, radius
            if event.key == K_SPACE:
                counter += 1
    return True, greenLower, greenUpper, pts, linecolor, counter, camera, screen, blanks, radius

if __name__ == '__main__':

    def main_loop():
        try:
            camera = cv2.VideoCapture(0)
            pygame.init()
            pygame.display.set_caption("CVPaint")
            screen = pygame.display.set_mode([600,450])
            flag = home_screen(screen)
            greenLower, greenUpper, pts, linecolor, counter, blanks, radius = boundaries_and_initialize()

            while flag:
                flag, greenLower, greenUpper, pts, linecolor, counter, camera, screen, blanks, radius = draw(greenLower, greenUpper, pts, linecolor, counter, camera, screen, blanks, radius)
        except KeyboardInterrupt:
            pygame.quit()
            cv2.destroyAllWindows()

main_loop()
