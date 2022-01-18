#! /usr/bin/python

import json
import csv
import os
import errno

Rounds=10
PWRounds = 10
ProcessingName = 'test07_pw_iops'

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
  TestRoundWriter.writerow(['Round', 'PWRound', 'IOPS'])
  for TestPass in range(1, Rounds + 1):
    for TestPassPW in range(1, PWRounds + 1):
      JSONFileName = ('fio_pw_pass=' + str(TestPassPW) +
                      '_test_pass=' + str(TestPass) + '.json')
      full_JSONFilePath = os.path.join(ScriptDir,
                          ResultsPath, JSONFileName)
      with open(full_JSONFilePath, 'r') as JSONFile:
        try:
          JSONData = json.load(JSONFile)
          iops = JSONData['jobs'][0]['write']['iops']
          JSONFile.close()
          TestRoundWriter.writerow([TestPass, TestPassPW, iops])
        except ValueError:
          print("Invalid JSON in " + JSONFileName)
          exit(1)
CSVFile.close()

