# SNIA Solid State Storage (SSS) Performance Test Specification (PTS) implementation.
# See http://www.snia.org/tech_activities/standards/curr_standards/pts for more info.

#!/bin/bash

#Throughtput Test

readonly OIO=8;
readonly THREADS=16;
readonly ROUNDS=10;
readonly FIO="/usr/bin/fio"
readonly TEST_NAME="02_Throughtput_test"
LOG_FILE=${TEST_NAME}/results/test.log
TIMESTAMP=$(date +%Y-%m-%d %H:%M:%S)

usage()
{
	echo "Usage: $0 /dev/<device to test>"
    exit 0
}

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

#/usr/local/sbin/nvme format $1
#sg_format --format $1
#hdparm --user-master u --security-set-pass PasSWorD $1
#hdparm --user-master u --security-erase PasSWorD $1

echo "$TIMESTAMP Purge done" >> $LOG_FILE

echo "OIO/thread = $OIO, Threads = $THREADS" >> $LOG_FILE
$FIO --version >> $LOG_FILE
echo "Test Start time: `date`" >> $LOG_FILE

#Workload independent preconditioning
#Run SEQ Workload Independent Preconditioning - Write 2X User Capacity with 128KiB SEQ writes, writing to the entire ActiveRange without LBA restrictions

#$FIO --name=precondition --filename=$1 --iodepth=16 --numjobs=1 --bs=128k --ioengine=libaio --rw=write --group_reporting --direct=1 --thread --refill_buffers --loops=2
echo "$TIMESTAMP Preconditioning done" >> $LOG_FILE

echo "$TIMESTAMP Starting test $TEST_NAME" >> $LOG_FILE

#Test 
echo "Starting test $TEST_NAME"

for PASS in $(eval echo {1..$ROUNDS});
do
	for RWMIX in 100 0;
    do
		for BS in 131072 1048576;
		do
			$FIO --output-format=json --name=job --filename=$1 --iodepth=$OIO --numjobs=$THREADS --bs=$BS --ioengine=libaio --rw=rw --rwmixread=$RWMIX --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 --norandommap --thread --refill_buffers --output=${TEST_NAME}/results/fio_pass=${PASS}_rw=${RWMIX}_bs=${BS}.json
		done
	done
	clear
    echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $ROUNDS done" >> $LOG_FILE
done

exit 0

