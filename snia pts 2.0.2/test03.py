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

TestName = '03_LAT'

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

BlockSizes = [512, 4096, 8192]
RWMixes = [100, 65, 0]
RoundTime = 60

FioArgs = ['--output-format=json+', '--eta=always',
          '--name=job', '--rw=randrw', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--iodepth=1', '--numjobs=1']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')
  
if not args.SkipPrecond:
  ptsu.stdPrecond(str(args.Device))
  logging.info('Preconditioning done')

logging.info('Starting test: ' + TestName)
for TestPass in tqdm(range(1, int(args.MaxRounds)+1)):
  for RWMix in RWMixes:
      for BS in BlockSizes:
        JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix)
                       + '_bs=' + str(BS) + '.json')
        exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                           ' --filename=' + str(args.Device) +
                           ' --bs=' + str(BS) + ' --ioengine=' + str(args.IOEngine) +
                           ' --rwmixread=' + str(RWMix) +
                           ' --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=RoundTime + 5)
  logging.info('Round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')

# 3.3 with added 100%-read test
logging.info('Starting 20 min test')
for RWMix in [100, 0]:
  JSONFileName = ('fio_20min_rw=' + str(RWMix) + '.json')
  exit_code, output = command_runner('fio --runtime=1200 --filename=' + 
                           str(args.Device) + ' --bs=4k --ioengine=' +
                           str(args.IOEngine) + ' --rwmixread=' + str(RWMix) + 
                           ' --write_hist_log=' + TestName + '/results/test03' +
                           str(RWMix) + ' --log_hist_msec=1 --disable_slat=1 \
                           --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=1300)