#!/usr/bin/env python3

import json, csv
import os, errno
import pandas as pd

processing_name = 'test03_2_main'
tc_set = [1, 2, 4, 8, 16, 32, 64]
qd_set = [1, 2, 4, 8, 16, 32, 64, 128, 256]
rw_mixes = [100, 70, 0]

script_dir = os.path.dirname(os.path.abspath(__file__))
results_path = "results"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
      raise
      
def Average(lst): 
    return sum(lst) / len(lst)

iops_list = []
average_lat_list = []
perc_99d99_lat_list = []
max_lat_list = []

csv_file_name =  'lat03_2.csv'
silentremove(csv_file_name)
  
with open(csv_file_name, mode='w') as csv_file:
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['TC', 'QD', 'RWMIX', 'IOPS', 'AV_LAT', 'P99D99_LAT', 'MAX_LAT'])           
  for rwmix in rw_mixes:
    for tc in tc_set:
      for qd in qd_set:
        iops_list.clear()
        average_lat_list.clear()
        perc_99d99_lat_list.clear()
        max_lat_list.clear()
        for test_pass in range(6, 10):
          json_file_name = 'fio_pass=' + str(test_pass) + '_QD=' + str(qd) + '_TC=' + str(tc) + '_rw=' + str(rwmix) + '_bs=4096.json'
          full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
          with open(full_json_file_path, 'r') as json_file:
            try:
              json_data = json.load(json_file)
              iops = json_data['jobs'][0]['read']['iops'] + json_data['jobs'][0]['write']['iops']
              average_lat = json_data['jobs'][0]['read']['clat_ns']['mean'] + json_data['jobs'][0]['write']['clat_ns']['mean']
              # Absense of IOs means absense of latency statistics
              if json_data['jobs'][0]['read']['total_ios'] == 0:
                perc_99d99_lat_read = 0
              else:
                perc_99d99_lat_read = json_data['jobs'][0]['read']['clat_ns']['percentile']['99.990000']
              if json_data['jobs'][0]['write']['total_ios'] == 0:
                perc_99d99_lat_write = 0
              else:
                perc_99d99_lat_write = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
              
              perc_99d99_lat = perc_99d99_lat_read + perc_99d99_lat_write
              max_lat = json_data['jobs'][0]['read']['clat_ns']['max'] + json_data['jobs'][0]['write']['clat_ns']['max']
              json_file.close()
            except ValueError:
              print("Invalid JSON in " + json_file_name)
              csv_file.close()
              exit(1)
          iops_list.append(iops)
          average_lat_list.append(average_lat)
          perc_99d99_lat_list.append(perc_99d99_lat)
          max_lat_list.append(max_lat)
          test_round_writer.writerow([tc, qd, rwmix, int(round(Average(iops_list))), round(Average(average_lat_list)/1000,1), round(Average(perc_99d99_lat_list)/1000,1), round(max(max_lat_list)/1000,1)])
csv_file.close()
