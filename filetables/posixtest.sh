#!/bin/sh

FDCOUNT_START=100
FDCOUNT_END=100010
FDCOUNT_INCR=100
FDCOUNTS=$(seq  --separator=" " $FDCOUNT_START $FDCOUNT_INCR $FDCOUNT_END)
OUTPUT="/home/shehjart/tests/opentest/posix.dat"
TESTPATH="/test/disk1"

ulimit -n $FDCOUNT_END

for fd in $FDCOUNTS;
do
        echo "FD Count: " $fd
        ./glfiletable --silent --posixtest --test-path $TESTPATH --fd-count $fd --output $OUTPUT
done

