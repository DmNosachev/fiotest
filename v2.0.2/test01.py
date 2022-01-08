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

parser = argparse.ArgumentParser(description='SNIA PTS 2.0.2 IOPS Test')
parser.add_argument('-d','--device', help='Block level device to test',
                    dest='Device', required=True)
parser.add_argument('-t','--device-type', default='sata', const='sata',
                    nargs='?', dest='DevType',
                    choices=['sata', 'sas', 'nvme', 'other'],
                    help='Device type (sata/sas/nvme/other) \
                    (default: %(default)s)',
                    required=False)
parser.add_argument('-e','--engine', default='libaio', const='libaio',
                    nargs='?', dest='IOEngine',
                    choices=['libaio', 'windowsaio', 'io_uring', 'sg',
                            'null', 'libiscsi'],
                    help='Fio IO engine (libaio/windowsaio/io_uring/sg/ \
                          null/libiscsi) \
                    (default: %(default)s)',
                    required=False)
parser.add_argument('-c','--pts-c', action='store_true', dest='PTSClMode',
                    default=False, help='Use PTS Client settings',
                    required=False)
parser.add_argument('-sp','--skip-precondition', action='store_true',
                    dest='SkipPrecond', default=False,
                    help='Skip preconditioning', required=False)
parser.add_argument('-se','--skip-erase', action='store_true',
                    dest='SkipErase', default=False, help='Skip purge',
                    required=False)
parser.add_argument('-r','--rounds', help='Maximum rounds in main test',
                    dest='MaxRounds', default='10', type=int,
                    choices=range(5, 25), required=False)
args = parser.parse_args()

if (not ptsu.isProg('fio')):
  sys.exit('fio not found! https://github.com/axboe/fio')

OIO = 32

if args.PTSClMode:
  TC = 2
else:
  TC = 4
  
BlockSizes = [512, 4096, 8192, 16384, 32768, 65536, 131072, 1048576]
RWMixes = [100, 95, 65, 50, 35, 5, 0]
RoundTime = 60

FioArgs = ['--output-format=json', '--eta=always',
          '--name=job', '--rw=randrw', '--direct=1',
          '--norandommap', '--refill_buffers']

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
                           shell=True, live_output=True, timeout=RoundTime)
  logging.info('Round ' + str(TestPass) + ' of ' + str(args.MaxRounds) + ' complete')