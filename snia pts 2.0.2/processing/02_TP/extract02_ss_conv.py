#! /usr/bin/python

import json
import csv
import os
import errno

Rounds = 10
ProcessingName = 'test02_ss_conv'
RWMixes = [100, 0]

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
  TestRoundWriter.writerow(['Round', 'BW', 'RWMIX'])
  for RWMix in RWMixes:
    for TestPass in range(1, Rounds + 1):
      JSONFileName = ('fio_pass=' + str(TestPass) + 
                     '_rw=' + str(RWMix) + '_bs=1048576.json')
      full_JSONFilePath = os.path.join(ScriptDir,
                          ResultsPath, JSONFileName)
      with open(full_JSONFilePath, 'r') as JSONFile:
        try:
          JSONData = json.load(JSONFile)
          # bw field in JSON contains bandwidth in KiBps
          bw = (JSONData['jobs'][0]['read']['bw'] +
                   JSONData['jobs'][0]['write']['bw'])
          JSONFile.close()
          TestRoundWriter.writerow([TestPass, bw, RWMix])
        except ValueError:
          print("Invalid JSON in " + JSONFileName)
          exit(1)
CSVFile.close()

