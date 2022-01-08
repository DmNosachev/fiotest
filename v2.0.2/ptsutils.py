from shutil import which
import subprocess
import logging
import os
import sys
import shutil
from pathlib import Path

def prepResultsDir(testName):
  dirpath = Path(testName) / 'results'
  if dirpath.exists() and dirpath.is_dir():
      shutil.rmtree(dirpath)
  dirpath.mkdir(parents=True)

def isProg(progName):
  return which(progName) is not None

def devicePurge(devType, devName):
  logging.info('Purging device ' + devName)
  if devType == 'sata':
    if (not isProg('hdparm')):
      sys.exit('hdparm not found!')

    out = subprocess.Popen(['hdparm', '--user-master', 'u', '--security-set-pass', 'PasSWorD', devName],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True)
    (stdout,stderr) = out.communicate()
    if stderr != '':
      logging.error("hdparm --security-set-pass encountered an error: " + stderr)
      raise RuntimeError("hdparm error")

    out = subprocess.Popen(['hdparm', '--user-master', 'u', '--security-erase', 'PasSWorD', devName],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True)
    (stdout,stderr) = out.communicate()
    if stderr != '':
      logging.error("hdparm --security-erase encountered an error: " + stderr)
      raise RuntimeError("hdparm error")
  
  elif devType == 'sas':
    if (not isProg('sg_format')):
      sys.exit('sg_format not found!')
    out = subprocess.Popen(['sg_format', '--format', devName],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
    (stdout,stderr) = out.communicate()
    if stderr != '':
      logging.error("sg_format encountered an error: " + stderr)
      raise RuntimeError("sg_format error")

  elif devType == 'nvme':
    if (not isProg('nvme')):
      sys.exit('nvme not found! Install nvme-cli')
    out = subprocess.Popen(['nvme', 'format', devName],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
    (stdout,stderr) = out.communicate()
    if stderr != '':
      logging.error("NVMe CLI encountered an error: " + stderr)
      raise RuntimeError("nvme cli error")

  else:
    out = subprocess.Popen(['dd', 'if=/dev/zero', 'of=' + devName,
                           'bs=128k'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
    (stdout,stderr) = out.communicate()
    if stderr != '':
      logging.error("dd encountered an error: " + stderr)
      raise RuntimeError("dd error")
    logging.info('Purging done (zeroing with dd)')

def stdPrecond(devName):
  logging.info('Starting preconditioning')
  p = subprocess.Popen(['fio', '--name=precondition', "--eta=always",
                         '--filename=' + devName, '--iodepth=32',
                         '--numjobs=1', '--bs=128k', '--ioengine=libaio',
                         '--rw=write', '--group_reporting', '--direct=1',
                         '--thread', '--refill_buffers', '--loops=2'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True, bufsize=1)
  for line in iter(p.stdout.readline, b''):
    print(line)
  p.stdout.close()
  p.wait()