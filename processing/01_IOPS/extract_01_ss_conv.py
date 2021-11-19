#! /usr/bin/python

# 7.3.3 Steady State Convergence Report

import json, csv
import os, errno

rounds = 10
processing_name = 'test01_ss_conv'
block_sizes = [4096, 8192, 16384, 32768, 65536, 131072, 1048576]

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
  test_round_writer.writerow(['round', 'iops', 'bs'])
  for bs in block_sizes:
    for test_pass in range(1, rounds + 1):
      json_file_name = 'fio_pass=' + str(test_pass) + '_rw=0' + '_bs=' + str(bs) + '.json'
      full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
      with open(full_json_file_path, 'r') as json_file:
        try:
          json_data = json.load(json_file)
          iops = json_data['jobs'][0]['write']['iops']
          json_file.close()
          test_round_writer.writerow([test_pass, iops, bs])
        except ValueError:
          print("Invalid JSON in " + json_file_name)
          exit(1)
csv_file.close()

