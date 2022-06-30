#!/usr/bin/python
import argparse
import subprocess
import os
import sys
import logging
from pathlib import Path
import shutil
import ptsutils as ptsu
from tqdm import tqdm
from command_runner import command_runner
import time

TestName = '05_HIR'

try:
    os.remove(TestName + '.log')
except OSError:
    pass
    
logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=TestName + '.log', encoding='utf-8',
                    level=logging.INFO)

parser = ptsu.createCommonParser()
args = parser.parse_args()

if (not ptsu.isProg('fio')):
  sys.exit('fio not found! https://github.com/axboe/fio')

if args.PTSClMode:
  OIO = 16
  TC = 2
else:
  OIO = 32
  TC = 4
  
RoundTime = 60
PCRounds = 36
StateRounds = 360

SleepIntervals = [5, 10, 15, 25, 50]
WLTime = 5

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--rw=randwrite', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--bs=4k', '--rw=randwrite']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

#Special preconditioning
logging.info('Starting preconditioning')
for TestPass in tqdm(range(1, PCRounds+1)):
  JSONFileName = ('fio_pc_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                     ' --filename=' + str(args.Device) +
                     ' --ioengine=' + str(args.IOEngine) +
                     ' --numjobs=' + str(TC) +
                     ' --iodepth=' + str(OIO) +
                     ' --output=' + TestName + '/results/' + JSONFileName +
                     ' ' + ' '.join(FioArgs),
                     timeout=RoundTime + 5)
  logging.info('Preconditioning: round ' + str(TestPass) +
               ' of ' + str(PCRounds) + ' complete')

logging.info('Starting test: ' + TestName)
for SleepTime in SleepIntervals:
# Main segment with pause (Access A + Access B)
  for TestPass in range(1, StateRounds+1):
    JSONFileName = ('fio_st=' + str(SleepTime) + '_AB_pass=' + str(TestPass) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(WLTime) +
                     ' --filename=' + str(args.Device) +
                     ' --ioengine=' + str(args.IOEngine) +
                     ' --numjobs=' + str(TC) +
                     ' --iodepth=' + str(OIO) +
                     ' --output=' + TestName + '/results/' + JSONFileName +
                     ' ' + ' '.join(FioArgs),
                     timeout=WLTime + SleepTime + 5)
    time.sleep(SleepTime)
    logging.info('State ' + str(SleepTime) + 'Access A+B: round ' + str(TestPass) +
                 ' of ' + str(StateRounds) + ' complete')
# Return to baseline (Access C)                 
  for TestPass in range(1, StateRounds+1):
    JSONFileName = ('fio_st=' + str(SleepTime) + '_C_pass=' + str(TestPass) + '.json')
    exit_code, output = command_runner('fio --runtime=5' +
                     ' --filename=' + str(args.Device) +
                     ' --ioengine=' + str(args.IOEngine) +
                     ' --numjobs=' + str(TC) +
                     ' --iodepth=' + str(OIO) +
                     ' --output=' + TestName + '/results/' + JSONFileName +
                     ' ' + ' '.join(FioArgs),
                     timeout=5 + 5)
    logging.info('State ' + str(SleepTime) + 'Access C: round ' + str(TestPass) +
                 ' of ' + str(StateRounds) + ' complete')                     