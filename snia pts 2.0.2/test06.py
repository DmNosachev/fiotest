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

TestName = '06_CBW'

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

QDSet = [32, 16, 8, 4, 2 , 1]
TCSet = [32, 16, 8, 4, 2 , 1]

RWMixes = [100, 65, 0]
RoundTime = 60

PrecondRounds = 36
IRPWRounds = 10

FioArgs = ['--output-format=json+', '--eta=always',
          '--name=job', '--rw=randwrite', '--direct=1',
          '--norandommap', '--refill_buffers', 
          '--thread', '--group_reporting',
          '--random_generator=tausworthe64',
          '--random_distribution=zoned:50/5:30/15:20/80',
          '--bssplit=512/4:1024/1:1536/1:2048/1:2560/1:3072/1:3584/1:4k/67:8k/10:16k/7:32k/3:64k/3']

ptsu.prepResultsDir(TestName)

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

# Special preconditioning
print('Staring preconditioning')
for TestPass in tqdm(range(1, PrecondRounds+1)):
  JSONFileName = ('fio_pc_pass=' + str(TestPass) + '.json')
  exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                           ' --filename=' + str(args.Device) +
                           ' --ioengine=' + str(args.IOEngine) +
                           ' --numjobs=32 --iodepth=32' +
                           ' --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=RoundTime + 5)
  logging.info('Preconditioning round ' + str(TestPass) + ' of ' +
               str(PrecondRounds) + ' complete')

print('Staring main test')
logging.info('Starting test: ' + TestName)
for TestPass in tqdm(range(1, args.MaxRounds+1)):
  for IRPWPass in range(1, IRPWRounds+1):
    JSONFileNamePW = ('fio_pw_pass=' + str(IRPWPass) + '_test_pass=' + 
                      str(args.MaxRounds) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                             ' --filename=' + str(args.Device) +
                             ' --ioengine=' + str(args.IOEngine) +
                             ' --numjobs=32 --iodepth=32' +
                             ' --output=' + TestName + '/results/' + JSONFileNamePW +
                             ' ' + ' '.join(FioArgs),
                             timeout=RoundTime + 5)
    logging.info('IRPW' + str(TestPass) + ' round ' +
                 str(IRPWPass) + ' of ' + str(args.MaxRounds) +
                 ' / ' +  str(IRPWRounds) + ' complete')
  for QD in QDSet:
      for TC in TCSet:
        JSONFileName = ('fio_pass=' + str(TestPass) + '_qd=' + str(QD) +
                        '_tc=' + str(TC) + '.json')
        exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                           ' --filename=' + str(args.Device) +
                           ' --ioengine=' + str(args.IOEngine) +
                           ' --numjobs=' + str(QD) +
                           ' --iodepth=32' + str(TC) +
                           ' --output=' + TestName + '/results/' + JSONFileName +
                           ' ' + ' '.join(FioArgs),
                           timeout=RoundTime + 5)
  logging.info('Round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')
