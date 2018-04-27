# Project Evolution
`CVPaint` wasn't always a painting program!

Way back when, `CVPaint` was a Software Design project called `CVPuppets` which was supposed to take collect depth information from a Microsoft Kinect and mimic human movements with a 3D model.

Turns out, that's really difficult, which normally wouldn't be a problem. Unfortunately, due to time constraints, we felt we should pivot to something more feasible. From that, we came up with `CVPaint`!

Let's talk some more about `CVPuppets`.

* First we acquired a Microsoft Kinect from Chase's house and used it to collect depth information
* We used the Point Cloud Library interpret the data (using RANSAC and the pinhole camera model) mathematically into information for mapping movements
* Then we realized that actually mapping movements was far out of the scope of our project, making us decide to do an ankle-breaking pivot to `CVPaint`
![](https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/Beforepivot.gif)
("Don't worry CVPuppets is not dead (yet)! I have been spending countless hours burning my retinas trying to make this a reality. This will happen!!  -Chase)

The code works like so:
Opening the Kinects camera and utilizes it main and infrared camera. The camera can be used for OpenCV to collect the data using the depth image.