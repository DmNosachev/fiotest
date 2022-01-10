#! /usr/bin/python

import json
import csv
import os
import errno

Rounds = 10
ProcessingName = 'test01_ss_conv'
BlockSizes = [512, 4096, 8192, 16384, 32768, 65536, 131072, 1048576]
RWMixes = [100, 65, 0]

ScriptDir = os.path.dirname(os.path.abspath(__file__))
ResultsPath = "results"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise
            

CSVFileName = ProcessingName + '.csv'
silentremove(CSVFileName)
with open(CSVFileName, mode='w') as CSVFile:
  TestRoundWriter = csv.writer(CSVFile, delimiter=';',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  TestRoundWriter.writerow(['Round', 'IOPS', 'BS', 'RWMIX'])
  for RWMix in RWMixes:
    for BS in BlockSizes:
      for TestPass in range(1, Rounds + 1):
        JSONFileName = ('fio_pass=' + str(TestPass) + 
                       '_rw=' + str(RWMix) +
                       '_bs=' + str(BS) + '.json')
        full_JSONFilePath = os.path.join(ScriptDir,
                            ResultsPath, JSONFileName)
        with open(full_JSONFilePath, 'r') as JSONFile:
          try:
            JSONData = json.load(JSONFile)
            iops = (JSONData['jobs'][0]['read']['iops'] +
                   JSONData['jobs'][0]['write']['iops'])
            JSONFile.close()
            TestRoundWriter.writerow([TestPass, iops, BS, RWMix])
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            exit(1)
CSVFile.close()

