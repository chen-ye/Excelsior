#! /usr/bin/env python

import time
import picamera
from datetime import datetime, timedelta


fps = int(raw_input("How many frames per second?? (integer) "))
print fps
	
assay_length = int(raw_input("How long is the assay?? (sec) "))
print assay_length
	
	#next_frame = (datetime.now() + timedelta(microseconds=fps/1000))
	#print next_frame
	
	#delay = (next_frame - datetime.now()).microseconds
	#print delay
	
	#time.sleep(delay)

def previewer():
	capture = 2
	while capture != 0:
		camera.start_preview()	
		time.sleep(capture)
		camera.stop_preview()
		capture = int(raw_input("How long do you want to live view (sec)??:  "))
	#return capture




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

with picamera.PiCamera() as camera:
	while move_on == False:
		move_on = previewer()
		#print move_on
	#print "exited loop"

hold_on()

with picamera.PiCamera() as camera:
	previewer()
	
	for image in 
	for filename in camera.capture_continuous('image_{timestamp:%Y-%m-%d-%H-%M}_' + image + '.jpg'):
		print('Captured %s' % filename)
		