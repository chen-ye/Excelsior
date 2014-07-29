#! /usr/bin/env python

# Script for recording climbing assays.  
# Chen Ye 2014

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
seconds = 28 #number of seconds

#File and Folder Naming Variables
timeWIN = time.strftime("%H-%M-%S")

currtime = str(time.time())
folder_name = '/home/pi/FlyLapse/images/' + 'VFlylapse_Rack' + rack + '_Rep' + rep + '_' + timeWIN
print "Folder name as: %s" % (folder_name)

os.mkdir(folder_name)

stdoutsav= sys.stdout
outputlog = open(folder_name + '/FlyCam.log', "w")
sys.stdout = tee(stdoutsav, outputlog)

with picamera.PiCamera() as camera:
	camera.resolution = (1500, 1200)
	camera.framerate = 15
	camera.start_preview()
	ok = raw_input("enter to start")
	print "Starting..."
	camera.start_recording(folder_name+'/video_'+rack+rep+'.h264',format='h264',quality=10,bitrate=19000000)
	camera.wait_recording(seconds)
	camera.stop_recording()
	camera.stop_preview()
	print "Captured " + str(seconds) + " seconds of Rack " + rack + " Rep " + rep 
