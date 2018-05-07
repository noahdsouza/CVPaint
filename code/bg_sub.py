import cv2
print(cv2.__version__)
import numpy as np
import time

#Open Camera object
camera = cv2.VideoCapture(0)

def nothing(x):
    pass

# Function to find angle between two vectors
def Angle(v1,v2):
    dot = np.dot(v1,v2)
    x_modulus = np.sqrt((v1*v1).sum())
    y_modulus = np.sqrt((v2*v2).sum())
    cos_angle = dot / x_modulus / y_modulus
    angle = np.degrees(np.arccos(cos_angle))
    return angle

# Function to find distance between two points in a list of lists
def FindDistance(A,B):
    return np.sqrt(np.power((A[0][0]-B[0][0]),2) + np.power((A[0][1]-B[0][1]),2))


# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'HSV_TrackBar',0,179,nothing)
cv2.createTrackbar('s', 'HSV_TrackBar',0,255,nothing)
cv2.createTrackbar('v', 'HSV_TrackBar',0,255,nothing)
areas = []

while(1):
    #Measure execution time
    start_time = time.time()

    #Capture frames from the camera
    grabbed, frame = camera.read()
    frame = cv2.flip(frame,1)

    #Blur the image
    blur = cv2.blur(frame,(3,3))

 	#Convert to HSV color space
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    #Create a binary image with where white will be skin colors and rest is black
    mask2 = cv2.inRange(hsv,np.array([2,50,50]),np.array([15,255,255])) #for skin colors
    #tolerance = 30
    #mask2 = cv2.inRange(hsv,np.array([60-tolerance,50,50]),np.array([60+tolerance,255,255]))#for green objects

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

    #Draw Contours
    #cv2.drawContours(frame, cnt, -1, (122,122,0), 3)
    #cv2.imshow('Dilation',median)

	#Find Max contour area (Assume that hand is in the frame)
    max_area=100
    ci=0
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i

	#Largest area contour
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
    # print(centerMass)

    #Draw center mass
    cv2.circle(frame,centerMass,7,[100,0,255],2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Center',tuple(centerMass),font,2,(255,255,255),2)

    #Print x and y coordinates
    cv2.putText(frame,str(cx),(100,200),font,2,(255,255,255),2)
    cv2.putText(frame,str(cy),(100,300),font,2,(255,255,255),2)

    #Print bounding rectangle
    #x,y,w,h = cv2.boundingRect(cnts)
    #img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.drawContours(frame,[hull],-1,(255,255,255),2)
    area = cv2.contourArea(hull)
    print(area)
    areas.append(area)

    ##### Show final image ########
    cv2.namedWindow('Dilation')
    cv2.imshow('Dilation',frame)
    cv2.moveWindow('Dilation',200,200)
    ###############################

    #Print execution time
    #print time.time()-start_time

    #close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


camera.release()
cv2.destroyAllWindows()
print('MAXIMUM',max(areas))
print('MINIMUM',min(areas))
print(type(area))
