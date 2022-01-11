#!/usr/bin/python

import json
import csv
import os
import errno

ProcessingName = 'test02_main'
BlockSizes = [131072, 1048576]
RWMixes = [100, 0]
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

BWList = []

CSVFileName = ProcessingName + '.csv'
silentremove(CSVFileName )

with open(CSVFileName , mode='w') as CSVFile:
  TestRoundWriter = csv.writer(CSVFile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL, dialect='unix')
  TestRoundWriter.writerow(['BS', 'RWMIX', 'BW'])           
  for RWMix in RWMixes:
    for BS in BlockSizes:
      BWList.clear()
      for TestPass in range(SSRound - 4, SSRound + 1):
        JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix) + \
                       '_bs=' + str(BS) + '.json')
        FullJSONFilePath = os.path.join(ScriptDir,
                           ResultsPath, JSONFileName)
        with open(FullJSONFilePath, 'r') as JSONFile:
          try:
            JSONData = json.load(JSONFile)
            bw = (JSONData['jobs'][0]['read']['bw'] +
                   JSONData['jobs'][0]['write']['bw'])
            JSONFile.close()
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            CSVFile.close()
            exit(1)
        BWList.append(bw)
      TestRoundWriter.writerow([BS, RWMix, int(round(Average(BWList)))])
  CSVFile.close()
