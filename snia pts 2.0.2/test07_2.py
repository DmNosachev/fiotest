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
                      
TestName = '07_CBW_2'

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

HistNames = ['Min', 'Mid', 'Max']
TCSet = [1, 2, 8]
QDSet = [1, 2, 1]

RoundTime = 60

PrecondRounds = 60

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--random_distribution=zoned:50/5:30/15:20/80',
          '--bssplit=512/4:1024/1:1536/1:2048/1:2560/1:3072/1:3584/1:4k/67:8k/10:16k/7:32k/3:64k/3']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

if not args.SkipPrecond:
  # Special preconditioning
  print('Starting preconditioning')
  for TestPass in tqdm(range(1, PrecondRounds+1)):
    JSONFileName = ('fio_pc_pass=' + str(TestPass) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                             ' --filename=' + str(args.Device) +
                             ' --ioengine=' + str(args.IOEngine) +
                             ' --numjobs=32 --iodepth=32 \
                             --rw=randwrite' +
                             ' --output=' + TestName + '/results/' + JSONFileName +
                             ' ' + ' '.join(FioArgs),
                             timeout=RoundTime + 5)
    logging.info('Preconditioning round ' + str(TestPass) + ' of ' +
                 str(PrecondRounds) + ' complete')

for HistName, TC, QD in zip(HistNames, TCSet, QDSet): 
  print('Starting test: ' + HistName)
      JSONFileName = ('fio_' + HistName + '.json')
      exit_code, output = command_runner('fio --runtime=600 \
                               --filename=' + str(args.Device) +
                               ' --ioengine=' + str(args.IOEngine) +
                               ' --numjobs=' + str(TC) +
                               ' --iodepth=' + str(QD) +
                               '--rw=randwrite' +
                               ' --write_lat_log=' + TestName +
                               '/results/test07_' + HistName +
                               ' --log_avg_msec=0.2 --disable_slat=1 \
                               --output=' + TestName + '/results/' + JSONFileName +
                               ' ' + ' '.join(FioArgs),
                               timeout=RoundTime + 5)
      logging.info(HistName + ' complete')
