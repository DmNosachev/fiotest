#! /usr/bin/python

import json, csv
import os, errno

processing_name = 'test05'

hir_states = ['State_1_AB', 'State_2_AB', 'State_3_AB', 'State_5_AB', 'State_10_AB']
access_states = ['AB', 'C']
rounds = 360

script_dir = os.path.dirname(os.path.abspath(__file__))
results_path = "results"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
      raise
            
csv_file_name = processing_name + '.csv'
silentremove(csv_file_name)
with open(csv_file_name, mode='w') as csv_file:
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['Round', 'IOPS', 'AVLAT', 'P99_LAT', 'P99D9_LAT', 'P99D99_LAT', 'MAX_LAT', 'STATE'])
  total_round = 0
  for state_name in hir_states:
    for access_name in access_states:
      for test_pass in range(1, rounds + 1):
        total_round += 1
        json_file_name = 'fio_' + state_name + '_access-' + access_name + '_pass=' + str(test_pass) + '.json'
        full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
        with open(full_json_file_path, 'r') as json_file:
          try:
            json_data = json.load(json_file)
            iops = json_data['jobs'][0]['write']['iops']
            lat_av = json_data['jobs'][0]['write']['clat_ns']['mean']
            lat_p99 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.000000']
            lat_p999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.900000']
            lat_p9999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
            lat_max = json_data['jobs'][0]['write']['clat_ns']['max']
            json_file.close()
            
            state = state_name
            if access_name == 'C': state = 'pause'
            
            test_round_writer.writerow([total_round, iops, lat_av/1000, lat_p99/1000, lat_p999/1000, lat_p9999/1000, lat_max/1000, state])
          except ValueError:
            print("Invalid JSON in " + json_file_name)
            exit(1)
csv_file.close()
  