# SNIA Solid State Storage (SSS) Performance Test Specification (PTS) implementation.
# See http://www.snia.org/tech_activities/standards/curr_standards/pts for more info.

#!/bin/bash

readonly PRECOND_ROUNDS=25;
readonly IRPW_ROUNDS=5;
readonly ROUNDS=10;
readonly FIO="/usr/bin/fio"
readonly TEST_NAME="07_ECW"
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

#echo "Device information:" >> $LOG_FILE
#smartctl -i $1 >> $LOG_FILE

#purge the device

#sleep 30
#sg_format --format $1
#hdparm --user-master u --security-set-pass PasSWorD $1
#hdparm --user-master u --security-erase PasSWorD $1

nvme format $1

echo "$TIMESTAMP Purge done" >> $LOG_FILE

echo "OIO/thread = $OIO, Threads = $THREADS" >> $LOG_FILE
$FIO --version >> $LOG_FILE
echo "Test Start time: `date`" >> $LOG_FILE

#Pre-conditioning using the Access Pattern, but with R/W Mix=0% (100% Write)
for PASS in $(eval echo {1..$PRECOND_ROUNDS});
do
  $FIO --output-format=json --name=job --filename=$1 --iodepth=32 --numjobs=32 '--bssplit=512/4:1024/1:1536/1:2048/1:2560/1:3072/1:3584/1:4k/67:8k/10:16k/7:32k/3:64k/3' --ioengine=libaio --rw=randrw --rwmixread=0 --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 '--random_distribution=zoned:50/5:30/15:20/80' --norandommap --thread --refill_buffers --random_generator=tausworthe64 --output=${TEST_NAME}/results/fio_precond_pass=${PASS}_QD=${OIO}_TC=${THREADS}.json
  echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $PRECOND_ROUNDS preconditioning done" >> $LOG_FILE
done

echo "$TIMESTAMP Preconditioning done" >> $LOG_FILE

echo "$TIMESTAMP Starting test $TEST_NAME" >> $LOG_FILE

#Test 
echo "Starting test $TEST_NAME"

for PASS in $(eval echo {1..$ROUNDS});
do
  #4.2 Apply Inter-Round Pre-Write
  for PASS in $(eval echo {1..$IRPW_ROUNDS});
  do
    $FIO --output-format=json --name=job --filename=$1 --iodepth=32 --numjobs=32 '--bssplit=512/4:1024/1:1536/1:2048/1:2560/1:3072/1:3584/1:4k/67:8k/10:16k/7:32k/3:64k/3' --ioengine=libaio --rw=randrw --rwmixread=0 --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 '--random_distribution=zoned:50/5:30/15:20/80' --norandommap --thread --refill_buffers --random_generator=tausworthe64 --output=${TEST_NAME}/results/fio_irpw_pass=${PASS}_QD=${OIO}_TC=${THREADS}.json
  done
	for THREADS in 32 16 8 6 4 2 1;
		do
		for OIO in 32 16 8 6 4 2 1;
		do
			$FIO --output-format=json --name=job --filename=$1 --iodepth=$OIO --numjobs=$THREADS '--bssplit=512/4:1024/1:1536/1:2048/1:2560/1:3072/1:3584/1:4k/67:8k/10:16k/7:32k/3:64k/3' --ioengine=libaio --rw=randrw --rwmixread=40 --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 '--random_distribution=zoned:50/5:30/15:20/80' --norandommap --thread --refill_buffers --random_generator=tausworthe64 --output=${TEST_NAME}/results/fio_pass=${PASS}_QD=${OIO}_TC=${THREADS}.json
		done
	done
	clear
    echo -e "$TIMESTAMP ${TEST_NAME} pass $PASS of $ROUNDS done" >> $LOG_FILE
done

exit 0


