#! /usr/bin/python

import json, csv
import os, errno

rounds = 10
processing_name = 'test03_2_ss'

# make steady state detect data from 4k write at TC=1 QD=32

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
  test_round_writer.writerow(['round', 'av_lat'])
  for test_pass in range(1, rounds + 1):
    json_file_name = 'fio_pass=' + str(test_pass) + '_QD=32_TC=1_rw=0_bs=4096.json'
    full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
    with open(full_json_file_path, 'r') as json_file:
      try:
        json_data = json.load(json_file)
        average_lat = json_data['jobs'][0]['write']['clat_ns']['mean']
        json_file.close()
        test_round_writer.writerow([test_pass, average_lat])
      except ValueError:
        print("Invalid JSON in " + json_file_name)
        exit(1)
csv_file.close()
  
