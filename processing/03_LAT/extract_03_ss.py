#! /usr/bin/python

import json, csv
import os, errno

rounds = 15
processing_name = 'test03_ss'
block_sizes = [512, 4096, 8192]

script_dir = os.path.dirname(__file__)
results_path = "results/"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
      raise
            
for bs in block_sizes:
  csv_file_name = processing_name + '_bs=' + str(bs) + '.csv'
  silentremove(csv_file_name)
  with open(csv_file_name, mode='w') as csv_file:
    test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
    test_round_writer.writerow(['round', 'av_lat'])
    for test_pass in range(1, rounds + 1):
      json_file_name = 'fio_pass=' + str(test_pass) + '_rw=0' + '_bs=' + str(bs) + '.json'
      full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
      with open(full_json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        average_lat = json_data['jobs'][0]['write']['clat_ns']['mean']
        json_file.close()
        test_round_writer.writerow([test_pass, average_lat])
  csv_file.close()
