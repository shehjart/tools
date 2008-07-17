FILESIZE=2147483648
WRBLKSIZE=65536
FALLOCBLKSIZE=1048576
STARTOFF=0
TESTFILE=/data/testfile
RUNS=1
FMODE=keepsize
MISCOPTIONS="--verbose"

./writefallocate --filesize $FILESIZE --wrblksize $WRBLKSIZE --fallocate $FALLOCBLKSIZE --startoff $STARTOFF --filename $TESTFILE --runcount $RUNS --fallocmode=$FMODE $MISCOPTIONS 
