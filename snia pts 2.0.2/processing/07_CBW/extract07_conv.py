#! /usr/bin/python

import json
import csv
import os
import errno

Rounds=10
QDSet = [32, 16, 8, 4, 2 , 1]
TCSet = [32, 16, 8, 4, 2 , 1]
ProcessingName = 'test07_main_conv'

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
  TestRoundWriter.writerow(['Round', 'TC', 'QD', 'IOPS', 'LAT'])
  for TestPass in range(1, Rounds + 1):
    for QD in QDSet:
      for TC in TCSet:
        JSONFileName = ('fio_pass=' + str(TestPass) + '_qd=' + str(QD) +
                        '_tc=' + str(TC) + '.json')
        full_JSONFilePath = os.path.join(ScriptDir,
                            ResultsPath, JSONFileName)
        with open(full_JSONFilePath, 'r') as JSONFile:
          try:
            JSONData = json.load(JSONFile)
            iops = (JSONData['jobs'][0]['read']['iops'] +
                   JSONData['jobs'][0]['write']['iops'])
            avlat = (JSONData['jobs'][0]['read']['clat_ns']['mean'] +
                   JSONData['jobs'][0]['write']['clat_ns']['mean'])/1000
            JSONFile.close()
            TestRoundWriter.writerow([TestPass, TC, QD, iops, avlat])
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            exit(1)
CSVFile.close()

