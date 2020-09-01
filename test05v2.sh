# SNIA Solid State Storage (SSS) Performance Test Specification (PTS) implementation.
# See http://www.snia.org/tech_activities/standards/curr_standards/pts for more info.

#!/bin/bash
readonly OIO=16;
readonly THREADS=16;
readonly FIO="/usr/bin/fio"
readonly TEST_NAME="06_Host_Idle_Recovery_Modified"
ROUNDS=360;
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

#hash $FIO 2>/dev/null || { echo >&2 "This script requires fio (http://git.kernel.dk/?p=fio.git) but it's not installed."; exit 1; }

#The output from a test run is placed in the ./results folder.
#This folder is recreated after every run.

rm -rf ${TEST_NAME}/results > /dev/null
mkdir -p ${TEST_NAME}/results

# Test and device information
echo "$TIMESTAMP Running ${TEST_NAME} on device: $1" >> $LOG_FILE


#echo "Device information:" >> $LOG_FILE
#smartctl -i $1 >> $LOG_FILE

#purge the device

#/opt/HGST/hdm/bin/hdm secure-erase --force --type user --path /dev/nvme0
#sg_format --format $1
#hdparm --user-master u --security-set-pass PasSWorD $1
#hdparm --user-master u --security-erase PasSWorD $1
/usr/sbin/nvme format $1

echo "$TIMESTAMP Purge done" >> $LOG_FILE

echo "OIO/thread = $OIO, Threads = $THREADS" >> $LOG_FILE
$FIO --version >> $LOG_FILE
echo "Test Start time: $TIMESTAMP" >> $LOG_FILE

echo "11.2.3: preconditioning"

for PASS in {1..780};
	do
		$FIO --output-format=json --name=job --filename=$1 --iodepth=$OIO --numjobs=$THREADS --bs=4096 --ioengine=libaio --rw=randwrite --group_reporting --runtime=60 --time_based --direct=1 --randrepeat=0 --norandommap --thread --refill_buffers --output=${TEST_NAME}/results/fio_precond_pass=${PASS}.json
		clear
		echo -e "`date` ${TEST_NAME} preconditioning pass $PASS of 780 done" >> $LOG_FILE
	done
echo "$TIMESTAMP Preconditioning done" >> $LOG_FILE

declare -a SUBTEST_LIST=("State_1_AB" "State_2_AB" "State_3_AB" "State_5_AB" "State_10_AB")
for SUBTEST_NAME in "${SUBTEST_LIST[@]}"
do
	case "$SUBTEST_NAME" in
		"State_1_AB")
			SLEEP_TIME=5
			;;
		"State_2_AB")
			SLEEP_TIME=10
			;;
		"State_3_AB")
			SLEEP_TIME=15
			;;
		"State_5_AB")
			SLEEP_TIME=25
			;;
		"State_10_AB")
			SLEEP_TIME=50
			;;
	esac
		
	for PASS in $(eval echo {1..$ROUNDS})
	do
		$FIO --output-format=json --output=${TEST_NAME}/results/fio_${SUBTEST_NAME}_access-AB_pass=${PASS}.json --name=job --filename=$1 --iodepth=$OIO --numjobs=$THREADS --bs=4096 --ioengine=libaio --rw=randwrite --group_reporting --runtime=5 --direct=1 --norandommap --refill_buffers --thread
		sleep $SLEEP_TIME
		echo -e "$TIMESTAMP ${TEST_NAME} ${SUBTEST_NAME} pass $PASS of $ROUNDS done" >> $LOG_FILE
	done
	for PASS in $(eval echo {1..$ROUNDS})
	do
		$FIO --output-format=json --output=${TEST_NAME}/results/fio_${SUBTEST_NAME}_access-C_pass=${PASS}.json --name=job --filename=$1 --iodepth=$OIO --numjobs=$THREADS --bs=4096 --ioengine=libaio --rw=randwrite --group_reporting --runtime=5 --direct=1 --norandommap --refill_buffers --thread
		echo -e "$TIMESTAMP ${TEST_NAME} ${SUBTEST_NAME} Access C pass $PASS of $ROUNDS done" >> $LOG_FILE
	done
done

exit 0