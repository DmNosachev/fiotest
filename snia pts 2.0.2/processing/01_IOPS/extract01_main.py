#!/usr/bin/python

import json
import csv
import os
import errno
import pandas as pd

ProcessingName = 'test01_main'
BlockSizes = [512, 4096, 8192, 16384, 32768, 65536, 131072, 1048576]
RWMixes = [100, 95, 65, 50, 35, 5, 0]
SSRound = 10

ScriptDir = os.path.dirname(os.path.abspath(__file__))
ResultsPath = "results"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise
      
def Average(lst): 
    return sum(lst) / len(lst)

IOPSList = []

CSVFileName = ProcessingName + '.csv'
silentremove(CSVFileName )

with open(CSVFileName , mode='w') as CSVFile:
  TestRoundWriter = csv.writer(CSVFile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL, dialect='unix')
  TestRoundWriter.writerow(['BS', 'RWMIX', 'IOPS'])           
  for RWMix in RWMixes:
    for BS in BlockSizes:
      IOPSList.clear()
      for TestPass in range(SSRound - 4, SSRound + 1):
        JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix) + \
                       '_bs=' + str(BS) + '.json')
        FullJSONFilePath = os.path.join(ScriptDir,
                           ResultsPath, JSONFileName)
        with open(FullJSONFilePath, 'r') as JSONFile:
          try:
            JSONData = json.load(JSONFile)
            iops = (JSONData['jobs'][0]['read']['iops'] +
                   JSONData['jobs'][0]['write']['iops'])
            JSONFile.close()
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            CSVFile.close()
            exit(1)
        IOPSList.append(iops)
      TestRoundWriter.writerow([BS, RWMix, int(round(Average(IOPSList)))])
  CSVFile.close()

iops_data = pd.read_csv(CSVFileName, sep = ';', header=0)
iops_pvt = iops_data.pivot(index='BS', columns='RWMIX', values='IOPS')
iops_pvt.to_csv(ProcessingName + '_pivot.csv', sep = ';')