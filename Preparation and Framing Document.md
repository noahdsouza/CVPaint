# Architectural Review 2

### Background and context 
We pivoted from using the Kinect because we felt like it would take a long time to find the depth values using the point cloud, and most documentation we found used C++ rather than Python. Also, we learned that a lot of the Kinect packages worked only in Windows. It was hard to add and rig a 3D model into Python. Our pivot was to continue using to use OpenCV, but having it use hand and object detection to create a CV paint program. We found that is was easier and more plausible to do than doing the OpenCV through the kinect.

### Key questions:
From this review, we would like to learn if it was a good idea to pivot from doing our Kinect code to just working with OpenCV and creating a paint-like program. We have already made the decision to pivot, but we want to know what could be some good next steps for us for our program. We want to know if it would be plausible to use different colored balls to change the color of the brush stroke that is being made on the screen. Our code already can draw green strokes when a green object is within range of the camera. One issue we found with this is if the camera finds a different source of green other than the object we are using, then stroke will begin to fidget and move across the screen, attempting to focus on one object. We would like to know if there was any method to reduce this feedback. One solution we had was changing the color value to a different shade of a color, however this may not work because we use a range of shades for a particular color. Are there any suggestions to fix this. One other idea we wanted to implement was having two paint cursors appear at the same time. This would be a stretch goal is we have time, since implementing another cursor would mean we would have to increase the number of objects that need to be detected through the camera, and fixing the prior issue with the color feedback. 

How should we prevent the camera from losing focus our cursor if it detects the color somewhere else? 

Would changing the color values or creating an array of colors be a good approach?

What is the best way to store pixel data?

Was it a good idea to pivot this late in the project to something new, and do you think we can accomplish this project?

How might we go about implementing a second cursor?
    
### Agenda for technical review session:
We will start by creating a function that will utilize OpenCV through the laptop camera in python. From there, since we already have some code made for drawing the stroke already, we will likely start implementing other features into the program to have it use more colors and save pictures that have been made.


