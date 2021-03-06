# CVPaint

#### *Software Design 2018 Final Project*

## Description
Inspired by the infamous Microsoft Paint, we wanted to create a fun interactive computer vision program where you can draw a picture using your hand as a cursor. The program has the capabilities of changing the color of your cursor and have and eraser to delete and misguided/unintended strokes. You will have the function to save your creation afterwards! For more information, please visit our [website](https://noahdsouza.github.io/CVPaint/index), watch our [video](https://raw.githubusercontent.com/noahdsouza/CVPaint/master/Final%20Deliverables/DemoVideo.gif), or read our [poster](https://github.com/noahdsouza/CVPaint/blob/master/Final%20Deliverables/Softdesposter.pdf)

### Getting Started
CVPaint was designed on Ubuntu, so we strongly recommend you use Ubuntu to run it.

Make sure the computer you are using has a webcam - we used the built-in webcams in Dell Latitude laptops

Uncover your webcam if you put something over it…We know Zuck is watching but CVPaint needs image input!

### Dependencies
You will need several packages in order to run CVPaint (if you don’t already have them) by running the following commands in your terminal:
 ```
$ sudo apt-get install python-opencv
$ pip install imutils
$ pip install numpy
$ pip install pygame
```

### Usage
Grab the code from our GitHub by running
```
$ git clone https://github.com/noahdsouza/CVPaint.git
```
then use these commands to run the code
```
$ cd CVPaint/code/
$ python3 CVPaint.py
```
note: `CVPaint` is only compatible with python3

### Authors
[Rachel Won](https://github.com/rwon869), [Noah D'Souza](https://github.com/noahdsouza), and [Chase Joyner](https://github.com/ChaseJoy)

### License
This repo is free to use. Go nuts. Edits are welcome if they improve the program.

### Attribution
[Adrian Rosebrock](http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) for Open CV object tracking

[Sid Garimella and Amy Phung](https://github.com/AmyPhung/InteractiveProgramming/blob/master/Hand_Detection/HandDetection.py) for hand tracking
