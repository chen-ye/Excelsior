#! /usr/bin/env python

import time
import picamera
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

#def previewer2():
#	capture = "empty_variable"
#	while capture != "True":
#		camera.start_preview()	
#		time.sleep(10)
#		camera.stop_preview()
#		capture = raw_input("Preview = False; Capture = True:  ")
#	return capture

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
	


#File and Folder Naming Variables
time_at_start_HM = time.ctime()[11:16]
time_at_start_HMS = time.ctime()[11:19]

currtime = str(time.time())
folder_name = '/home/pi/Desktop/' + 'TimeLapse_Trial::' + str(time_at_start_HMS)
print "Folder name as: %s" % (folder_name)

os.mkdir(folder_name)
filename = folder_name + '/' + 'image_' + str(time_at_start_HM) + '_' + str(frame%3) + '.jpg'
print "File name as: %s" % (filename)

with picamera.PiCamera() as camera:
	print "exited loop"
#	t0 = str(time.ctime())
	t0 = time.ctime()
	time_initial = time.clock()
	print "Begin time is: %.3f" % (time_initial)
#	ti2 = str(time.clock())
	ti2 = time.clock()
	dt = ti2-time_initial
	for frame in range(0,frames+1):
		if dt<= 1.00:
			ti1 = time.clock()
			dt = time.clock() - time_initial
			#time.sleep(delay_time)
			camera.capture(filename)
			print "Interval time: %.4f" % (time.clock() - time_initial)
			filename = folder_name + '/' + 'image_' + str(time_at_start_HM) + '_' + str(frame) + '.jpg'		
			ti = time.ctime()
			print "Frame number: %i" % (frame) 
			print "File name   : %s" % (filename)
			print '______________' 
			ti2 = time.clock()
			print "Time to initiate process: %.4f" % (float(ti2-ti1))
			frame += 1
			
	#time.clock()-time_initial
	time_final = time.clock()
		
	#camera.stop_preview()
print "begun@: %s" % (t0)
print "end @ : %s" % (time.ctime())
print "total time = %s" % (time_final-time_initial)
print "total frames = %i" % (frame)