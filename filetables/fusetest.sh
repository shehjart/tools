#!/bin/sh

FDCOUNT_START=100
FDCOUNT_END=100010
FDCOUNT_INCR=100
FDCOUNTS=$(seq  --separator=" " $FDCOUNT_START $FDCOUNT_INCR $FDCOUNT_END)

VMP="/testmount"
TESTDIR=$VMP
VIRTUAL_TESTPATH=$VMP
MOUNTPOINT="/test/cmount"
MOUNTED_TESTPATH=$MOUNTPOINT

ulimit -n $FDCOUNT_END

SRV_VOLFILE="/home/shehjart/docs/volfiles/localdisk-iot.vol"
CLIENT_VOLFILE="/home/shehjart/docs/volfiles/disk.vol"
GLUSTERFSD="/usr/local/sbin/glusterfsd"
SRVLOG="/test/srvlog"
TEST_CLIENTLOG="/tmp/fdtable.clog"
MOUNTED_CLIENTLOG="/test/clog2"
VOLNAME="localdiskthreads"
LOGLEVEL="NONE"
GLUSTERFS="/usr/local/sbin/glusterfs"
OUTPUT="/home/shehjart/tests/diskopentest/fuse-o1.dat"


#clean the logs
rm -f $SRVLOG
rm -f $TEST_CLIENTLOG
rm -f $MOUNTED_CLIENTLOG

umount $MOUNTPOINT
killall glusterfs
killall glusterfsd

#start the server
#$GLUSTERFSD -f $SRV_VOLFILE -L $LOGLEVEL -l $SRVLOG

for fd in $FDCOUNTS;
do
        echo "FD Count: " $fd
        #mount the fuse mount point
        $GLUSTERFS -f $CLIENT_VOLFILE -l $MOUNTED_CLIENTLOG -L $LOGLEVEL $MOUNTPOINT

        echo "Sleeping.."
        sleep 2    
        ./glfiletable --silent --posixtest --test-path $MOUNTPOINT --fd-count $fd --output $OUTPUT

        echo "Sleeping.."
        sleep 2
        umount $MOUNTPOINT
        
done

