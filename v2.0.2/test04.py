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



if args.PTSClMode:
  OIO = 16
  TC = 2
else:
  OIO = 32
  TC = 4
  
BlockSizes = [512, 4096, 8192]
RWMixes = [100, 65, 0]
RoundTime = 60

WSATRounds = 360

FioArgs = ['--output-format=json+', '--eta=always',
          '--name=job', '--rw=randwrite', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--numjobs=1 --bs=4k']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

logging.info('Starting test: ' + TestName)
for TestPass in tqdm(range(1, WSATRounds+1)):
  for RWMix in RWMixes:
      for BS in BlockSizes:
        JSONFileName = ('fio_pass=' + str(TestPass) + '.json')
        exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                           ' --filename=' + str(args.Device) +
                           ' --ioengine=' + str(args.IOEngine) +
                           ' --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=RoundTime + 5)
  logging.info('Round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')

# 10.2.4
logging.info('Starting 20 min test')

exit_code, output = command_runner('fio --name=20min --filename=' +
                         str(args.Device) + ' --iodepth=' + str(OIO) +
                         ' --output-format=json+ --numjobs=' + str(TC) +
                         ' --bs=4k --ramp_time=10 --runtime=1200 \
                         --time_based --ioengine=libaio \
                         --write_hist_log=test04' +
                         ' --log_hist_msec=1 --disable_slat=1 \
                         --rw=randwrite --group_reporting --direct=1 \
                         --thread --refill_buffers --random_generator=tausworthe64',
                         timeout=RoundTime + 5)