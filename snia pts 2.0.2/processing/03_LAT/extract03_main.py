#!/usr/bin/python

import json
import csv
import os
import errno

ProcessingName = 'test03_main'
BlockSizes = [512, 4096, 8192]
RWMixes = [100, 65, 0]
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
LatList = []
LatP4nList = []
LatMaxList = []

CSVFileName = ProcessingName + '.csv'
silentremove(CSVFileName )

with open(CSVFileName , mode='w') as CSVFile:
  TestRoundWriter = csv.writer(CSVFile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL, dialect='unix')
  TestRoundWriter.writerow(['BS', 'RWMIX', 'IOPS', 'LAT', 'LAT99.99', 'Max_LAT'])           
  for RWMix in RWMixes:
    for BS in BlockSizes:
      IOPSList.clear()
      LatList.clear()
      LatP4nList.clear()
      LatMaxList.clear()
      for TestPass in range(SSRound - 4, SSRound + 1):
        JSONFileName = ('fio_pass=' + str(TestPass) + '_rw=' + str(RWMix) + \
                       '_bs=' + str(BS) + '.json')
        FullJSONFilePath = os.path.join(ScriptDir,
                           ResultsPath, JSONFileName)
        with open(FullJSONFilePath, 'r') as JSONFile:
          try:
            JSONData = json.load(JSONFile)
            IOPS = JSONData['jobs'][0]['read']['iops'] + JSONData['jobs'][0]['write']['iops']
            average_lat = JSONData['jobs'][0]['read']['clat_ns']['mean'] + JSONData['jobs'][0]['write']['clat_ns']['mean']
              # Absense of IOs means absense of latency statistics
            if JSONData['jobs'][0]['read']['total_ios'] == 0:
                perc_99d99_lat_read = 0
            else:
                perc_99d99_lat_read = JSONData['jobs'][0]['read']['clat_ns']['percentile']['99.990000']
            if JSONData['jobs'][0]['write']['total_ios'] == 0:
                perc_99d99_lat_write = 0
            else:
                perc_99d99_lat_write = JSONData['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
              
            LatP4n = (perc_99d99_lat_read + perc_99d99_lat_write)/1000
            LatMax = (JSONData['jobs'][0]['read']['clat_ns']['max'] + JSONData['jobs'][0]['write']['clat_ns']['max'])/1000
            Lat = (JSONData['jobs'][0]['read']['clat_ns']['mean'] + JSONData['jobs'][0]['write']['clat_ns']['mean'])/1000
            JSONFile.close()
          except ValueError:
            print("Invalid JSON in " + JSONFileName)
            CSVFile.close()
            exit(1)
        IOPSList.append(IOPS)
        LatList.append(Lat)
        LatP4nList.append(LatP4n)
        LatMaxList.append(LatMax)
      TestRoundWriter.writerow([BS, RWMix, int(round(Average(IOPSList))),
                               round(Average(LatList),2),
                               round(Average(LatP4nList),2),
                               round(max(LatMaxList),2)])
  CSVFile.close()
