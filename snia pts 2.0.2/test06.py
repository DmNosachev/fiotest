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

TestName = '06_XSR'

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

OIO = 32
TC = 1
  
RoundTime = 60
SeqRounds = 360
RndRounds = 480

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--rw=randwrite']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

# There is no preconditioning

logging.info('Starting test: ' + TestName)
logging.info('Starting AG1')
for TestPass in tqdm(range(1, SeqRounds+1)):
  JSONFileName = ('fio_ag1_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --rw=write --bs=1m'
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RoundTime + 5)
  logging.info('AG1: round ' + str(TestPass) + ' of ' + str(SeqRounds) + ' complete')

logging.info('Starting AG2')
for TestPass in tqdm(range(1, RndRounds+1)):
  JSONFileName = ('fio_ag2_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --rw=randwrite --bs=8k'
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RoundTime + 5)
  logging.info('AG2: round ' + str(TestPass) + ' of ' + str(RndRounds) + ' complete')
  
logging.info('Starting AG3')
for TestPass in tqdm(range(1, SeqRounds+1)):
  JSONFileName = ('fio_ag3_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --rw=write --bs=1m'
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RoundTime + 5)
  logging.info('AG3: round ' + str(TestPass) + ' of ' + str(SeqRounds) + ' complete')