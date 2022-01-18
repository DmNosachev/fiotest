#! /usr/bin/python

import json
import csv
import os
import errno
import argparse

parser = argparse.ArgumentParser(description='PTS 04 WSAT Plot')
parser.add_argument('-c','--capacity-bytes', help='Device capacity in bytes',
                    type=int, dest='device_cap_bytes', required=True)
args = parser.parse_args()

rounds = 360
processing_name = 'test04_main'

DriveCapacityGiB = args.device_cap_bytes / 1073741824

script_dir = os.path.dirname(os.path.abspath(__file__))
results_path = "results"

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise
            
csv_file_name = processing_name + '.csv'
silentremove(csv_file_name)
with open(csv_file_name, mode='w') as csv_file:
  TotalGib = 0
  TotalDriveFills = 0
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"',
                      quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['Round', 'IOPS', 'Average', '99%',
                              '99.9%', '99.99%', 'Maximum',
                              'TGib', 'TDF'])
  for test_pass in range(1, rounds + 1):
    json_file_name = 'fio_pass=' + str(test_pass) + '.json'
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
        TotalGib += json_data['jobs'][0]['write']['io_kbytes']/1024/1024
        TotalDriveFills = TotalGib/DriveCapacityGiB
        json_file.close()
        test_round_writer.writerow([test_pass, iops, lat_av/1000, lat_p99/1000, lat_p999/1000, lat_p9999/1000, lat_max/1000, TotalGib, TotalDriveFills])
      except ValueError:
        print("Invalid JSON in " + json_file_name)
        exit(1)
csv_file.close()
  
