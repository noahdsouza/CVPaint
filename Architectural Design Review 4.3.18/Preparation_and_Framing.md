**Background and Context**

The Kinect uses an infrared tracking system that tracks most of the movements of an individual that is in front of it. It utilizes skeletal tracking in order to follow the motion of the user, and is able to track up to two people at the same time. In comparison, OpenCV recognizes the movement that is in front of the camera, however it interprets everything based on positive and negative space. Positive space is relative and is indicated on the screen as the color white, while anything that is negative space shown as black space


**Risk Identification and Mitigation**

| Identification                                                           | Mitigation                                                                            |
|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Getting the Kinect to work with OpenCV                                   | Utilizing the openNI package                                                          |
| Tracking the motion through the Kinect and projecting it on the computer | Using the Kinect’s infrared camera to detect movements and create a skeletal tracking |
| Aligning a two dimensional with the motion                               | Creating a class that will assign an image on a joint on the skeletal tracking        |


**Software Architecture Discussion**

We are currently planning on making a single program containing many different classes which interact in a manner akin to the model-view-controller structure commonly used in pygames. We will have a class(es) dedicated to user-input. The user-input is similar to the controller class, but instead of keyboard presses, it will be movement that the camera/kinect picks up. The model class will interpret the movement, overlay, and animate the image. The view class will display every frame of the movement, updating real time. 
We’re wondering if implementing this entire structure in a single file would be effective or if splitting things into different files (i.e a camera file and an animation file) and importing things would be more useful. If so, what are good strategies to delineate between files?


**Key Questions**

We would like input on what kind of approach to this project we should take. Should we use only OpenCV? Only the Kinect (with its SDK or associated software packages)? Or should we use both to create our product? Should we use multiple files or cram it all into one? An outside perspective would be most helpful for using OpenCV and interfacing with a Kinect. 


**Agenda for Technical Review Session** 

We will start by creating a function that will connect the Kinect to python then finding a way to activate the infrared tracking of the the Kinect through the code. From there, we will likely start configuring the joints of the skeletal tracking and assigning images or points on to them.


**Feedback Form**

Create a Google form that folks in the review will use to provide you with feedback or answers to various questions you pose to your audience. Since, at least for the first review, the time you have to present will be very short you should expect most of the feedback you get to come from this form rather than thoughts expressed orally during your session. Please submit a link to your Google form using this other Google form! (you must have this submitted no less than 2 hours before class so we have time to post a link on the course website).

**Link:**
https://goo.gl/forms/vDuMoEarPwt6DqkL2 
