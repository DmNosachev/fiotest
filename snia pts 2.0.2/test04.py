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

TestName = '04_WSAT'

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

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--rw=randwrite', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--time_based', '--bs=4k']
          
if args.PTSClMode:
  logging.info('Client mode selected')
  OIO = 16
  TC = 2
  FioArgs.append('--size=' + str(round(ptsu.getDeviceSize(args.Device) * 0.75)))
else:
  OIO = 32
  TC = 4
  
RoundTime = 60
WSATRounds = 360
RTHTime = 1200

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

# There is no preconditioning

# 10.2.2
logging.info('Starting test: ' + TestName)
for TestPass in tqdm(range(1, WSATRounds+1)):
  JSONFileName = ('fio_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RoundTime + 5)
  logging.info('Round ' + str(TestPass) + ' of ' + str(WSATRounds) + ' complete')

# 10.2.4
logging.info('Starting RTH test')

JSONFileName = ('fio_rth.json')
exit_code, output = command_runner('fio --runtime=' + str(RTHTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --write_lat_log=' + TestName + '/results/test04' + 
               ' --log_avg_msec=0.1 --disable_slat=1' +
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RTHTime + 100)
logging.info('Round ' + str(TestPass) + ' of ' + str(WSATRounds) + ' complete')