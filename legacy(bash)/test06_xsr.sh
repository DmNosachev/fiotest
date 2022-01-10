# SNIA Solid State Storage (SSS) Performance Test Specification (PTS) implementation.
# See http://www.snia.org/tech_activities/standards/curr_standards/pts for more info.

#!/bin/bash


usage()
{
	echo "Usage: $0 /dev/<device to test>"
    exit 0
}

readonly OIO=32;
readonly THREADS=4;
readonly AG1_ROUNDS=480;
readonly AG2_ROUNDS=360;
FIO="/usr/bin/fio"
readonly TEST_NAME="06_XSR"
LOG_FILE=${TEST_NAME}/results/test.log
TIMESTAMP=$(date +%Y-%m-%d %H:%M:%S)

if [ $# -lt 1 ] ; then
	usage
fi

if [ ! -e $1 ] ; then
	usage
fi

hash $FIO 2>/dev/null || { echo >&2 "This script requires fio (http://git.kernel.dk/?p=fio.git) but it's not installed."; exit 1; }

#The output from a test run is placed in the ./results folder.
#This folder is recreated after every run.

rm -rf ${TEST_NAME}/results > /dev/null
mkdir -p ${TEST_NAME}/results

# Test and device information
echo "$TIMESTAMP Running ${TEST_NAME} on device: $1" >> $LOG_FILE


echo "Device information:" >> $LOG_FILE
smartctl -i $1 >> $LOG_FILE

#purge the device

#hdparm --user-master u --security-set-pass PasSWorD $1
#hdparm --user-master u --security-erase PasSWorD $1

nvme format $1

echo "$TIMESTAMP Purge done" >> $LOG_FILE

echo "OIO/thread = $OIO, Threads = $THREADS" >> $LOG_FILE
$FIO --version >> $LOG_FILE
echo "Test Start time: `date`" >> $LOG_FILE

echo "$TIMESTAMP Starting test $TEST_NAME" >> $LOG_FILE

for PASS in $(eval echo {1..$AG1_ROUNDS});
do
	$FIO --output-format=json --name=job --filename=$1 --iodepth=32 --numjobs=1 --bs=1M --ioengine=libaio --rw=write --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 --norandommap --thread --refill_buffers --output=${TEST_NAME}/results/fio_ag1_pass=${PASS}.json
	clear
    echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $AG1_ROUNDS AG1 done" >> $LOG_FILE
done

echo "$TIMESTAMP AG1 done" >> $LOG_FILE

for PASS in $(eval echo {1..$AG2_ROUNDS});
do
	$FIO --output-format=json --name=job --filename=$1 --iodepth=32 --numjobs=8 --bs=8k --ioengine=libaio --rw=randwrite --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 --norandommap --thread --refill_buffers --random_generator=tausworthe64 --output=${TEST_NAME}/results/fio_ag2_pass=${PASS}.json
	clear
    echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $AG2_ROUNDS AG2 done" >> $LOG_FILE
done

echo "$TIMESTAMP AG2 done" >> $LOG_FILE

for PASS in $(eval echo {1..$AG1_ROUNDS});
do
	$FIO --output-format=json --name=job --filename=$1 --iodepth=32 --numjobs=1 --bs=1M --ioengine=libaio --rw=write --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 --norandommap --thread --refill_buffers --output=${TEST_NAME}/results/fio_ag3_pass=${PASS}.json
	clear
    echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $AG1_ROUNDS AG3 done" >> $LOG_FILE
done

echo "$TIMESTAMP AG1 done" >> $LOG_FILE

exit 0

