#! /usr/bin/env python

#Copied from http://picamera.readthedocs.org/en/release-1.5/recipes2.html#recording-motion-vector-data

import numpy as np
import picamera
import picamera.array 
from PIL import Image
import time
import os


frame = 00
frames = 100 #number of frames
delay_time = 1 #seconds
move_on = False
move_on_again = False


def previewer():
	capture = delay_time
	while capture != 0:
		camera.start_preview()	
		time.sleep(capture)
		camera.stop_preview()
		capture = int(raw_input("How long do you want to live view (sec)??:  "))
	#return capture

with picamera.PiCamera() as camera:
	while move_on == False:
		move_on = previewer()
		#print move_on
	#print "exited loop"

def hold_on():
	move_on_again = "nay"
	while move_on_again != "y":
		move_on_again = raw_input("Do you wish to begin assay?? (y/n): ")
	print "Beginning assay in:"
	print "3"
	time.sleep(1)
	print "2"
	time.sleep(1)
	print "1"
	time.sleep(1)

hold_on()
	

with picamera.PiCamera() as camera:
    with picamera.array.PiMotionArray(camera) as stream:
        camera.resolution = (640, 480)
        camera.framerate = 30 #max is 30
        camera.start_recording('/dev/null', format='h264', motion_output=stream)
        camera.wait_recording(10) #how many seconds worth of recording
        camera.stop_recording()
	np.save('array', stream.array)
print np.load('array.npy')