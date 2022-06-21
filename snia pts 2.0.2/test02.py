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

TestName = '02_TP'

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

RWMixes = [100, 0]  
RoundTime = 60

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--rw=randrw', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--time_based', '--numjobs=1',
          ]

if args.PTSClMode:
  logging.info('Client mode selected')
  FioArgs.append('--size=' + str(round(ptsu.getDeviceSize(args.Device) * 0.75)))
  
ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

BS = '128k'

# 2.2 128K WIPC for 128K test, 1M WIPC for 1M test
if not args.SkipPrecond:
  ptsu.stdPrecond(str(args.Device))
  logging.info(BS + ' preconditioning done')

logging.info('Starting test: ' + TestName + ' (' + BS + ')')
for TestPass in tqdm(range(1, int(args.MaxRounds)+1)):
  for RWMix in RWMixes:
    JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix)
                   + '_bs=' + str(BS) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                       ' --filename=' + str(args.Device) +
                       ' --iodepth=' + str(OIO) +
                       ' --bs=' + BS + ' --ioengine=' + str(args.IOEngine) +
                       ' --rwmixread=' + str(RWMix) +
                       ' --output=' + TestName + '/results/' + JSONFileName +
                       ' ' + ' '.join(FioArgs),
                       timeout=RoundTime + 5)
  logging.info(BS + ' test, round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')
  
BS = '1m'

logging.info('Starting preconditioning' + ' (' + BS + ')')
exit_code, output = command_runner('fio --name=precondition1M \
                         --filename=' + str(args.Device) + ' --iodepth=32 \
                         --numjobs=1 --bs=' + BS + ' --ioengine=libaio \
                         --rw=write --group_reporting --direct=1 \
                         --thread --refill_buffers --loops=2',
                         timeout=14400)
logging.info(BS + ' preconditioning done')
                         
logging.info('Starting test: ' + TestName + ' (' + BS + ')')
for TestPass in tqdm(range(1, int(args.MaxRounds)+1)):
  for RWMix in RWMixes:
    JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix)
                   + '_bs=' + str(BS) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                       ' --filename=' + str(args.Device) +
                       ' --iodepth=' + str(OIO) +
                       ' --bs=' + BS + ' --ioengine=' + str(args.IOEngine) +
                       ' --rwmixread=' + str(RWMix) +
                       ' --output=' + TestName + '/results/' + JSONFileName +
                       ' ' + ' '.join(FioArgs),
                       timeout=RoundTime + 5)
  logging.info(BS + ' test, round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')