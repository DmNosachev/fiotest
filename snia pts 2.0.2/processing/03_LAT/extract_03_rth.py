#!/usr/bin/env python3

import json, csv
import os, errno

processing_name = 'test03_rth'

script_dir = os.path.dirname(os.path.abspath(__file__))
results_path = 'results'
json_file_name = 'fio_t3ph2.json'

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
      raise

csv_file_name = processing_name + '.csv'
silentremove(csv_file_name)

full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
with open(csv_file_name, mode='w') as csv_file:
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['BIN', 'LAT'])
  with open(full_json_file_path, 'r') as json_file:
    try:
      json_data = json.load(json_file)
      for lat_bin in json_data['jobs'][0]['write']['clat_ns']['bins']:
        lat_val = json_data['jobs'][0]['write']['clat_ns']['bins'][lat_bin]
        test_round_writer.writerow([lat_bin, lat_val])
      json_file.close()
    except ValueError:
      print("Invalid JSON in " + json_file_name)
      csv_file.close()
      exit(1)
csv_file.close()