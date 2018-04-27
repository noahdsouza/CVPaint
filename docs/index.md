### Inspired by the infamous Microsoft Paint, we wanted to create a fun interactive computer vision program where you can draw a picture using your hand as a cursor. The program has the capabilities of changing the color of your cursor and have and eraser to delete and misguided/unintended strokes. You will have the function to save your creation afterwards!

![](https://raw.githubusercontent.com/noahdsouza/CVPaint/master/docs/images/sideBySide.gif)

# Getting Started
* `CVPaint` was designed on Ubuntu, so we strongly recommend you use Ubuntu to run it.
* Make sure the computer you are using has a webcam - we used the built-in webcams in Dell Latitude laptops 
* Uncover your webcam if you put something over it...We know Zuck is watching but `CVPaint` needs image input!

# Prerequisites
You will need several packages in order to run `CVPaint` (if you don't already have them):
* OpenCV
  * `$ pip install opencv-python`
* iMutils
  * `$ pip install imutils`

# Getting the Code
Now that you have the required dependencies, you can go ahead a grab the code from our GitHub by running
``` bash
$ git clone https://github.com/noahdsouza/CVPaint.git
```
You should now have a local repository named `CVPaint`.

# Running CVPaint
`CVPaint` has several files and functions, but to run the main one, follow these steps!
1. Open a terminal
1. Enter the `CVPaint` code directory by entering `cd CVPaint/code/` into the command line
1. Run `CVPaint` by entering `python CVPaint.py` into the command line
1. Go absolutely nuts with our project!
  1. To pause the paintbrush, hit the space bar
  1. To quit and save your art into the `images` subfolder

# Project Evolution
`CVPaint` wasn't always a painting program!

Way back when, `CVPaint` was a Software Design project called `CVPuppets` which was supposed to take collect depth information from a Microsoft Kinect and mimic human movements with a 3D model.

Turns out, that's really difficult, which normally wouldn't be a problem. Unfortunately, due to time constraints, we felt we should pivot to something more feasible. From that, we came up with `CVPaint`!

Let's talk some more about `CVPuppets`.

* First we acquired a Microsoft Kinect from Chase's house and used it to collect depth information
* We used the Point Cloud Library interpret the data (using RANSAC and the pinhole camera model) mathematically into information for mapping movements
* Then we realized that actually mapping movements was far out of the scope of our project, making us decide to do an ankle-breaking pivot to `CVPaint`
