#!/bin/bash
#Shell script to start up web motion-JPEG streaming
#Chen Ye - 6.25.2014


LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /home/pi/FlyLapse/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &
raspistill --nopreview -w 640 -h 480 -q 5 -o /home/pi/FlyLapse/stream/pic.jpg -tl 100 -t 99999999 -th 0:0:0
