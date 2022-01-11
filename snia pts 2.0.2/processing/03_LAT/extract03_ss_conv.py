#! /usr/bin/python

import json
import csv
import os
import errno

Rounds = 10
ProcessingName = 'test03_ss_conv'
BlockSizes = [512, 4096, 8192]

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
  TestRoundWriter.writerow(['Round', 'LAT', 'BS'])
  for BS in BlockSizes:
    for TestPass in range(1, Rounds + 1):
      JSONFileName = ('fio_pass=' + str(TestPass) + 
                      '_rw=0_bs=' + str(BS) + '.json')
      full_JSONFilePath = os.path.join(ScriptDir,
                          ResultsPath, JSONFileName)
      with open(full_JSONFilePath, 'r') as JSONFile:
        try:
          JSONData = json.load(JSONFile)
          AvLat = (JSONData['jobs'][0]['read']['clat_ns']['mean'] +
                   JSONData['jobs'][0]['write']['clat_ns']['mean'])/1000
          JSONFile.close()
          TestRoundWriter.writerow([TestPass, AvLat, BS])
        except ValueError:
          print("Invalid JSON in " + JSONFileName)
          exit(1)
CSVFile.close()

