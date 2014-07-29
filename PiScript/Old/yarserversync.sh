#!/bin/bash
#Shell script to transfer files from a directory to a server using rsync
#Chen Ye - 6.26.2014


#Variables
XFERDIR="/home/pi/FlyLapse/images/"
SERVERDIR="root@yeesus.com:~/FlyLapse/images"
LOGFILE="/home/pi/FlyLapse/rserversync.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

#Copy the files to the server
echo "$TIMESTAMP : Initiating transfer from $XFERDIR to $SERVERDIR" | tee -a $LOGFILE
rsync -Cavz $XFERDIR* $SERVERDIR | tee -a $LOGFILE
#Check if everything worked out
OUT=$?

#Success!
if [ "$OUT" -eq 0 ];then
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : Files copied!" | tee -a $LOGFILE
elif [ "$OUT" -eq 1 ];then
#Nothing to move here
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : No files to transfer!  Exiting..." | tee -a $LOGFILE
#Whoops failure
else
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : File copy failed!  Exiting..." | tee -a $LOGFILE
fi

