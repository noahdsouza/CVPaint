[Home](index)  |  [Project Details](project_details)  |  [Project Evolution](evolution)  |  [About Us](about)

# Project Evolution
`CVPaint` wasn't always a painting program!

Way back when, `CVPaint` was a Software Design project called `CVPuppets` which was supposed to take collect depth information from a Microsoft Kinect and mimic human movements with a 3D model.

Turns out, that's really difficult, which normally wouldn't be a problem. Unfortunately, due to time constraints, we felt we should pivot to something more feasible. From that, we came up with `CVPaint`!

Let's talk some more about `CVPuppets`.

* First we acquired a Microsoft Kinect from Chase's house and used it to collect depth information
* We used the Point Cloud Library interpret the data, using RANSAC and the pinhole camera model, mathematically into information for mapping movements
* RANSAC is an algorithm which randomly chooses two points in a data set (in this case, our point cloud), draws a straight line connecting the points, and determines how many other points lie within a defined distance away, called inliers. It runs for n number of iterations, and returns a line of best fit by maximizing the number of inliers. We attempted to use RANSAC for skeleton tracking. 
* The pinhole camera model was a way to map the depth information from the Kinect to our screen, using similar triangles. 
* Then we realized that actually mapping movements was far out of the scope of our project, making us decide to do an ankle-breaking pivot to `CVPaint`
![](https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/Beforepivot.gif)


The code works like so:
Opening the Kinects camera and utilizes it main and infrared camera. The camera can be used for OpenCV to collect the data using the depth image.

However, we eventually realized that in fact, concepts/parts of `CVPuppets` could be salvaged. With more time, we would have liked to fully integrate the Kinect motion tracking into our `CVPaint` code so the user could use their fingers to control the paint cursor and used the depth map to manipulate the thickness of the lines being drawn.
