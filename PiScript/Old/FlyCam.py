#! /usr/bin/env python

import time
import picamera
import os
import sys

#Logging classes
class tee :
    def __init__(self, _fd1, _fd2) :
        self.fd1 = _fd1
        self.fd2 = _fd2

    def __del__(self) :
       if self.fd1 != sys.stdout and self.fd1 != sys.stderr :
           self.fd1.close()
       if self.fd2 != sys.stdout and self.fd2 != sys.stderr :
           self.fd2.close()

    def write(self, text) :
        self.fd1.write(text)
        self.fd2.write(text)

    def flush(self) :
        self.fd1.flush()
        self.fd2.flush()

rack = raw_input("this is rack: ")
rep = raw_input("this is rep: ")

#Configuration variables
frame = 00
frames = 234 #number of frames
delay_time = .15 #seconds

#File and Folder Naming Variables
time_at_start_HM = time.ctime()[11:16]
time_at_start_HMS = time.ctime()[11:19]
timeWIN = time.strftime("%H-%M-%S")

currtime = str(time.time())
folder_name = '/home/pi/FlyLapse/images/' + 'Flylapse_Rack' + rack + '_Rep' + rep + '_' + timeWIN
print "Folder name as: %s" % (folder_name)

os.mkdir(folder_name)

stdoutsav= sys.stdout
outputlog = open(folder_name + '/FlyCam.log', "w")
sys.stdout = tee(stdoutsav, outputlog)

with picamera.PiCamera() as camera:
	camera.resolution = (1280, 1024)
	camera.start_preview()
	ok = raw_input("Enter to start")
#	time.sleep(3)
	for filename in camera.capture_continuous(folder_name + '/' + 'img_{timestamp:%H-%M-%S}_{counter:03d}.jpg', use_video_port=True):
		print('captured %s' % filename)
		time.sleep(delay_time)
		frame = frame + 1
		if (frame > frames):
			print "Captured " + str(frame) + " frames of Rack " + rack + " Rep " + rep 
			camera.stop_preview()
			break
