#!/usr/bin/env python3

import json, csv
import os, errno

processing_name = 'test01_main'
block_sizes = [4096, 8192, 16384, 32768, 65536, 131072, 1048576]
rw_mixes = [100, 95, 65, 50, 35, 5, 0]

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

csv_file_name = processing_name + '.csv'
silentremove(csv_file_name)

with open(csv_file_name, mode='w') as csv_file:
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['BS', 'RWMIX', 'IOPS'])           
  for rwmix in rw_mixes:
    for bs in block_sizes:
      iops_list.clear()
      for test_pass in range(6, 10):
        json_file_name = 'fio_pass=' + str(test_pass) + '_rw=' + str(rwmix) + '_bs=' + str(bs) + '.json'
        full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
        with open(full_json_file_path, 'r') as json_file:
          try:
            json_data = json.load(json_file)
            iops = json_data['jobs'][0]['read']['iops'] + json_data['jobs'][0]['write']['iops']
            json_file.close()
          except ValueError:
            print("Invalid JSON in " + json_file_name)
            csv_file.close()
            exit(1)
        iops_list.append(iops)
      test_round_writer.writerow([bs, rwmix, int(round(Average(iops_list)))])
  csv_file.close()
