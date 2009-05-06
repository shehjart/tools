#!/bin/sh

FDCOUNT_START=100
FDCOUNT_END=50010
FDCOUNT_INCR=100
FDCOUNTS=$(seq  --separator=" " $FDCOUNT_START $FDCOUNT_INCR $FDCOUNT_END)

VMP="/testmount"
VIRTUAL_TESTPATH=$VMP

ulimit -n $FDCOUNT_END

SRV_VOLFILE="/home/shehjart/docs/volfiles/localdisk-iot.vol"
CLIENT_VOLFILE="/home/shehjart/docs/volfiles/localdiskiotclient.vol"
GLUSTERFSD="/usr/local/sbin/glusterfsd"
SRVLOG="/test/srvlog"
TEST_CLIENTLOG="/tmp/fdtable.clog"
VOLNAME="localdiskthreads"
LOGLEVEL="NONE"
OUTPUT="/home/shehjart/tests/opentest-o1fd/libgfclient.dat"


#clean the logs
rm -f $SRVLOG
rm -f $TEST_CLIENTLOG

killall glusterfs
killall glusterfsd

#start the server
$GLUSTERFSD -f $SRV_VOLFILE -L $LOGLEVEL -l $SRVLOG

for fd in $FDCOUNTS;
do
        echo "FD Count: " $fd
        ./glfiletable --silent --glusterfstest --test-path $VIRTUAL_TESTPATH --vmp $VMP -l $TEST_CLIENTLOG -L $LOGLEVEL -f $CLIENT_VOLFILE -v $VOLNAME --fd-count $fd --output $OUTPUT
done

