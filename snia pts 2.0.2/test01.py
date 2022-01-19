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

TestName = '01_WSAT'

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
  
BlockSizes = [512, 4096, 8192, 16384, 32768, 65536, 131072, 1048576]
RWMixes = [100, 95, 65, 50, 35, 5, 0]
RoundTime = 10

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--rw=randrw', '--direct=1',
          '--norandommap', '--refill_buffers',
          '--time_based',
          '--thread', '--group_reporting']

if args.PTSClMode:
  logging.info('Client mode selected')
  TC = 2
  FioArgs.append('--size=' + str(ptsu.getDeviceSize(str(round(args.Device * 0.75)))))
else:
  TC = 4
  
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
                           ' --iodepth=' + str(OIO) + ' --numjobs=' + str(TC) +
                           ' --bs=' + str(BS) + ' --ioengine=' + str(args.IOEngine) +
                           ' --rwmixread=' + str(RWMix) +
                           ' --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=RoundTime + 5)
  logging.info('Round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')