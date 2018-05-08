[Home](index)  |  [Project Details](project_details)  |  [Project Evolution](evolution)  |  [About Us](about)

# Project Details

#### CVPaint uses computer vision to track an object to draw virtual pictures.

## Implementation Information
A big part of the code is keeping track of the points the cursor has traversed over. We were worried that storing them in one list would cause lag, so we tried to look for other options. During one of our Architectural Design Reviews, someone suggested that we look into using an occupancy grid, which is essentially a giant matrix which stores information. However, because we didn't want our points to be limited by the resolution of the grid, we decided to go back to using a list. The list ended up not lagging like we expected, but because we redrew every point in the list every time the screen updated, all of the points would change color when we tried to change color. We needed a good way to store information about the color of the points. So, we tracked our points using a single list of nested tuples, which contained all the information about the point, including (x,y) location, color, and mode (drawing or not).

<img src="https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/Profiles/SAD.png"/>

We decided to not split the model, view, and controller into different classes because all the variables were super codependent on each other so we would have had to pass many variables back and forth. We combined the controller and the view into a single loop that updated every time a new point was added to the list.
 
We also integrated OpenCV into pygame so our program would have a nice GUI for the home screen which the user could interact with.

## Results
`CVPaint` tracks a green object in real time and uses that as a cursor. The user first sees a homescreen which gives them instructions and a start button. Then the user can start drawing on the blank canvas. Spacebar allows the user to toggle between drawing or not drawing (akin to picking up a pencil off a paper). The user can change color even when not in drawing mode. The "color" at the very end is an eraser to erase any mistakes. At the very end, the program asks the user whether he/she want to save the drawing. If yes, then the colorbar is cropped from the drawing and saved as a png file under the user-dictated file name. 

![](https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/sample.gif)

`CVPaint` works really great under very specific lighting conditions: lots of natural lighting against a very simple backdrop. However, the cursor gets distracted in dim lighting or by anything else it considers "green."

<img src="https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/Profiles/group%20picture.png"/>

## Attribution
[Adrian Rosebrock](http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) for Open CV object tracking

[Sid Garimella and Amy Phung](https://github.com/AmyPhung/InteractiveProgramming/blob/master/Hand_Detection/HandDetection.py) for hand tracking
