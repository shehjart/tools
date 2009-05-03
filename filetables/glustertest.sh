#!/bin/sh

FDCOUNT_START=100
FDCOUNT_END=100010
FDCOUNT_INCR=100
FDCOUNTS=$(seq  --separator=" " $FDCOUNT_START $FDCOUNT_INCR $FDCOUNT_END)

VMP="/testmount"
TESTDIR="testdir"
VIRTUAL_TESTPATH=$VMP"/"$TESTDIR
MOUNTPOINT="/test/cmount"
MOUNTED_TESTPATH=$MOUNTPOINT"/"$TESTDIR

ulimit -n $FDCOUNT_END

SRV_VOLFILE="/home/shehjart/docs/volfiles/localdisk-iot.vol"
CLIENT_VOLFILE="/home/shehjart/docs/volfiles/localdiskiotclient.vol"
GLUSTERFSD="/usr/local/sbin/glusterfsd"
SRVLOG="/test/srvlog"
TEST_CLIENTLOG="/tmp/fdtable.clog"
MOUNTED_CLIENTLOG="/test/clog2"
VOLNAME="localdiskthreads"
LOGLEVEL="DEBUG"
GLUSTERFS="/usr/local/sbin/glusterfs"
OUTPUT="/home/shehjart/code/tools-git/filetables/gluster-new.dat"


#clean the logs
rm -f $SRVLOG
rm -f $TEST_CLIENTLOG
rm -f $MOUNTED_CLIENTLOG

umount $MOUNTPOINT
killall glusterfs
killall glusterfsd

#start the server
$GLUSTERFSD -f $SRV_VOLFILE -L $LOGLEVEL -l $SRVLOG

for fd in $FDCOUNTS;
do
        echo "FD Count: " $fd
        #mount the fuse mount point
        $GLUSTERFS -f $CLIENT_VOLFILE -l $MOUNTED_CLIENTLOG -L $LOGLEVEL $MOUNTPOINT
        #clean the test directory through the fuse mount point
        rm -rf $MOUNTED_TESTPATH
        mkdir $MOUNTED_TESTPATH

        sleep 2    
        ./glfiletable --silent --glusterfstest --test-path $VIRTUAL_TESTPATH --vmp $VMP -l $TEST_CLIENTLOG -L $LOGLEVEL -f $CLIENT_VOLFILE -v $VOLNAME --fd-count $fd --output $OUTPUT
       
        umount $MOUNTPOINT
done

