#! /usr/bin/python

import json
import csv
import os
import errno

SSRound=10
QDSet = [32, 16, 8, 4, 2, 1]
TCSet = [32, 16, 8, 4, 2, 1]
ProcessingName = 'test07_main_averaged'

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
LatList = []

CSVFileName = ProcessingName + '.csv'
silentremove(CSVFileName)
with open(CSVFileName, mode='w') as CSVFile:
  TestRoundWriter = csv.writer(CSVFile, delimiter=';',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  TestRoundWriter.writerow(['TC', 'QD', 'IOPS', 'LAT'])
  for QD in QDSet:
    for TC in TCSet:
      IOPSList.clear()
      LatList.clear()
      for TestPass in range(SSRound - 4, SSRound + 1):
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
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            exit(1)
        IOPSList.append(iops)
        LatList.append(avlat)
      TestRoundWriter.writerow([TC, QD, int(round(Average(IOPSList))),
                                round(Average(LatList),2)])
CSVFile.close()

