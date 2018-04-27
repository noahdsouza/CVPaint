# Project Evolution
`CVPaint` wasn't always a painting program!

Way back when, `CVPaint` was a Software Design project called `CVPuppets` which was supposed to take collect depth information from a Microsoft Kinect and mimic human movements with a 3D model.

Turns out, that's really difficult, which normally wouldn't be a problem. Unfortunately, due to time constraints, we felt we should pivot to something more feasible. From that, we came up with `CVPaint`!

Let's talk some more about `CVPuppets`.

* First we acquired a Microsoft Kinect from Chase's house and used it to collect depth information
* We used the Point Cloud Library interpret the data (using RANSAC and the pinhole camera model) mathematically into information for mapping movements
* Then we realized that actually mapping movements was far out of the scope of our project, making us decide to do an ankle-breaking pivot to `CVPaint`
