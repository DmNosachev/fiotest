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

RoundTime = 60
WSATRounds = 360
RTHTime = 1200

logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=TestName + '.log', encoding='utf-8',
                    level=logging.INFO)
                    
ptsu.prepResultsDir(TestName)

scriptDir = os.path.dirname(os.path.abspath(__file__))
mainTestCSVName = TestName + '.csv'
DriveCapacityGiB = ptsu.getDeviceSize(args.Device)/1024/1024/1024
    
parser = ptsu.createCommonParser()
args = parser.parse_args()

if (not ptsu.isProg('fio')):
  sys.exit('fio not found! https://github.com/axboe/fio')

FioArgs = ['--bs=4k']
FioArgs.extend(ptsu.FioCommonArgs)
          
if args.PTSClMode:
  logging.info('Client mode selected')
  OIO = 16
  TC = 2
  FioArgs.append('--size=' + str(round(ptsu.getDeviceSize(args.Device) * 0.75)))
else:
  OIO = 32
  TC = 4

if not args.SkipErase:
  ptsu.devicePurge(str(args.DevType), str(args.Device))
  logging.info('Purge done')

# There is no preconditioning

# Total GiB written to device
TotalGib = 0

# 10.2.2
logging.info('Starting test: ' + TestName)
with open(mainTestCSVName, mode='w') as mainTestCSV:
  testRoundWriter = csv.writer(mainTestCSV, delimiter=';', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL, dialect='unix')
  testRoundWriter.writerow(['Round', 'IOPS', 'Average latency',
                            '99.9% latency', '99.999%  latency',
                            'Maximum  latency', 'TGib', 'TDF'])
  for TestPass in tqdm(range(1, WSATRounds+1)):
    JSONFileName = ('fio_pass=' + str(TestPass) + '.json')
    exit_code, output = command_runner('fio --runtime=' + str(RoundTime) +
                 ' --filename=' + str(args.Device) +
                 ' --ioengine=' + str(args.IOEngine) +
                 ' --numjobs=' + str(TC) +
                 ' --iodepth=' + str(OIO) +
                 ' --write_lat_log=' + TestName + '/results/test04_pass=' + str(TestPass) +
                 ' --disable_slat=1 --output=' + TestName + '/results/' + JSONFileName +
                 ' ' + ' '.join(FioArgs),
                 timeout=RoundTime + 5)
  # Fio writes only 99.99 latency in JSON, but we need 99.999. Solution is to log every IO latency and calculate our own stats
    for i in range(1, TC+1):
      LogFileList.append(TestName + '/results/test04_pass=' + str(TestPass) + '_clat.' + i +'.log')
    rth_data = pd.concat((pd.read_csv(f, sep = ',',
                        usecols=[1], names=['Lat']) for f in LogFileList),
                        ignore_index=True)
    rth_data.Lat = rth_data.Lat.multiply(0.001)
    Lat_mean = rth_data['Lat'].mean()
    Lat_max = rth_data['Lat'].max()
    Lat_p3n = rth_data['Lat'].quantile(0.999)
    Lat_p4n = rth_data['Lat'].quantile(0.9999)
    Lat_p5n = rth_data['Lat'].quantile(0.99999)
    # TODO: Удалить логи, в т.ч. lat и slat
    
    fullJSONFilePath = os.path.join(scriptDir, 'results', JSONFileName)
    with open(fullJSONFilePath, 'r') as JSONFile:
      try:
        JSONData = json.load(JSONFile)
        IOPS = json_data['jobs'][0]['write']['iops_mean']
        TotalGib += json_data['jobs'][0]['write']['io_kbytes']/1024/1024
        TotalDriveFills = TotalGib/DriveCapacityGiB
        JSONFile.close()
        testRoundWriter.writerow([TestPass, IOPS, Lat_mean/1000, Lat_p3n/1000, Lat_p4n/1000, Lat_p5n/1000, Lat_max/1000, TotalGib, TotalDriveFills])
      except ValueError:
        print("Invalid JSON in " + JSONFileName)
        exit(1)
    logging.info('Round ' + str(TestPass) + ' of ' + str(WSATRounds) + ' complete')
csv_file.close()

# 10.2.4
logging.info('Starting RTH test')

JSONFileName = ('fio_rth.json')
exit_code, output = command_runner('fio --runtime=' + str(RTHTime) +
               ' --filename=' + str(args.Device) +
               ' --ioengine=' + str(args.IOEngine) +
               ' --numjobs=' + str(TC) +
               ' --iodepth=' + str(OIO) +
               ' --write_lat_log=' + TestName + '/results/test04_2' + 
               ' --log_avg_msec=0.1 --disable_slat=1' +
               ' --output=' + TestName + '/results/' + JSONFileName +
               ' ' + ' '.join(FioArgs),
               timeout=RTHTime + 100)
logging.info('Round ' + str(TestPass) + ' of ' + str(WSATRounds) + ' complete')