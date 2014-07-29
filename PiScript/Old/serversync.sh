#!/bin/bash
#Shell script to transfer files from a directory to a server using scp, 
#then move the files from the local directory to some other directory
#Chen Ye - 6.25.2014


#Variables
QUEUEDIR="TransferQueue/"
DONEDIR="Transferred/"
SERVERDIR="root@yeesus.com:~/FlyLapse/images"
LOGFILE="serversync.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

#Copy the files to the server
echo "$TIMESTAMP : Initiating transfer from $QUEUEDIR to $SERVERDIR" | tee -a $LOGFILE
scp -r $QUEUEDIR* $SERVERDIR
#Check if everything worked out
OUT=$?

#Success!
if [ "$OUT" -eq 0 ];then
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : Files copied!" | tee -a $LOGFILE
    #Move files from the queue directory to the transferred directory
    mv $QUEUEDIR* $DONEDIR
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    #Did the move work?
    MOVEOUT=$?
    if [ "$MOVEOUT" -eq 1 ];then
        echo "$TIMESTAMP : Some files not moved! $(ls QUEUEDIR) remains." | tee -a $LOGFILE
    else
        echo "$TIMESTAMP : Files moved from queue!  Exiting..." | tee -a $LOGFILE
    fi
elif [ "$OUT" -eq 1 ];then
#Nothing to move here
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : No files to transfer!  Exiting..." | tee -a $LOGFILE
#Whoops failure
else
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP : File copy failed!  Exiting..." | tee -a $LOGFILE
fi