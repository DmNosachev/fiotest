import subprocess
import logging
import os
import sys
import shutil
from pathlib import Path
from command_runner import command_runner
import argparse

FioCommonArgs = ['--output-format=json',
                 '--eta=always',
                 '--name=job',
                 '--direct=1',
                 '--norandommap',
                 '--refill_buffers', 
                 '--thread',
                 '--group_reporting',
                 '--random_generator=tausworthe64',
                 '--time_based']
          
def createCommonParser():
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
  return parser

def prepResultsDir(testName):
  dirpath = Path(testName) / 'results'
  if dirpath.exists() and dirpath.is_dir():
      shutil.rmtree(dirpath)
  dirpath.mkdir(parents=True)
  
  try:
    os.remove(testName + '.log')
  except OSError:
    pass

def isProg(progName):
  return shutil.which(progName) is not None

# Get the file size by seeking at end. Taken from SO: https://stackoverflow.com/questions/2773604/query-size-of-block-device-file-in-python

def getDeviceSize(devName):
    fd=os.open(devName, os.O_RDONLY)
    try:
        return os.lseek(fd, 0, os.SEEK_END)
    finally:
        os.close(fd)
        
def devicePurge(devType, devName):
  logging.info('Purging device ' + devName)
  if devType == 'sata':
    if (not isProg('hdparm')):
      sys.exit('hdparm not found!')

    exit_code, output = command_runner('hdparm --user-master u --security-set-pass PasSWorD ' + devName,
                                       shell=True, live_output=True)
    exit_code, output = command_runner('hdparm --user-master u --security-erase PasSWorD ' + devName,
                                       shell=True, live_output=True)
  
  elif devType == 'sas':
    if (not isProg('sg_format')):
      sys.exit('sg_format not found! Install sg3_utils package')
    
    exit_code, output = command_runner('sg_format --format ' + devName,
                                       shell=True, live_output=True)

  elif devType == 'nvme':
    if (not isProg('nvme')):
      sys.exit('nvme not found! Install nvme-cli package')
    
    exit_code, output = command_runner('nvme format' + devName,
                                      shell=True, live_output=True)

  else:
    exit_code, output = command_runner('dd bs=128k if=/dev/zero of=' + devName,
                                       shell=True, live_output=True)
    logging.info('Purging done (zeroing with dd)')

def stdPrecond(devName):
  logging.info('Starting preconditioning')
  exit_code, output = command_runner('fio --name=precondition \
                         --filename=' + devName + ' --iodepth=32 \
                         --numjobs=1 --bs=128k --ioengine=libaio \
                         --rw=write --group_reporting --direct=1 \
                         --thread --refill_buffers --loops=2',
                         timeout=14400)