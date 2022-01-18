#! /usr/bin/python

import json
import csv
import os
import errno
import argparse

SeqRounds = 60
RndRounds = 80
processing_name = 'test06'

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
  test_round_writer = csv.writer(csv_file, delimiter=';', quotechar='"',
                      quoting=csv.QUOTE_MINIMAL, dialect='unix')
  test_round_writer.writerow(['AG', 'Round', 'IOPS', 'BW', 'Average', '99%',
                              '99.9%', '99.99%', 'Maximum'])
  for test_pass in range(1, SeqRounds + 1):
    json_file_name = 'fio_ag1_pass=' + str(test_pass) + '.json'
    full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
    with open(full_json_file_path, 'r') as json_file:
      try:
        json_data = json.load(json_file)
        iops = json_data['jobs'][0]['write']['iops_mean']
        bw_mib = json_data['jobs'][0]['write']['bw_mean']/1024
        lat_av = json_data['jobs'][0]['write']['clat_ns']['mean']
        lat_p99 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.000000']
        lat_p999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.900000']
        lat_p9999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
        lat_max = json_data['jobs'][0]['write']['clat_ns']['max']
        json_file.close()
        test_round_writer.writerow(['AG1', test_pass, iops, bw_mib, lat_av/1000, lat_p99/1000, lat_p999/1000, lat_p9999/1000, lat_max/1000])
      except ValueError:
        print("Invalid JSON in " + json_file_name)
        exit(1)
        
  for test_pass in range(1, RndRounds + 1):
    json_file_name = 'fio_ag2_pass=' + str(test_pass) + '.json'
    full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
    with open(full_json_file_path, 'r') as json_file:
      try:
        json_data = json.load(json_file)
        iops = json_data['jobs'][0]['write']['iops_mean']
        bw_mib = json_data['jobs'][0]['write']['bw_mean']/1024
        lat_av = json_data['jobs'][0]['write']['clat_ns']['mean']
        lat_p99 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.000000']
        lat_p999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.900000']
        lat_p9999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
        lat_max = json_data['jobs'][0]['write']['clat_ns']['max']
        json_file.close()
        test_round_writer.writerow(['AG2', test_pass+SeqRounds, iops, bw_mib, lat_av/1000, lat_p99/1000, lat_p999/1000, lat_p9999/1000, lat_max/1000])
      except ValueError:
        print("Invalid JSON in " + json_file_name)
        exit(1)
        
  for test_pass in range(1, SeqRounds + 1):
    json_file_name = 'fio_ag3_pass=' + str(test_pass) + '.json'
    full_json_file_path = os.path.join(script_dir, results_path, json_file_name)
    with open(full_json_file_path, 'r') as json_file:
      try:
        json_data = json.load(json_file)
        iops = json_data['jobs'][0]['write']['iops_mean']
        bw_mib = json_data['jobs'][0]['write']['bw_mean']/1024
        lat_av = json_data['jobs'][0]['write']['clat_ns']['mean']
        lat_p99 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.000000']
        lat_p999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.900000']
        lat_p9999 = json_data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']
        lat_max = json_data['jobs'][0]['write']['clat_ns']['max']
        json_file.close()
        test_round_writer.writerow(['AG3', test_pass+SeqRounds+RndRounds, iops, bw_mib, lat_av/1000, lat_p99/1000, lat_p999/1000, lat_p9999/1000, lat_max/1000])
      except ValueError:
        print("Invalid JSON in " + json_file_name)
        exit(1)
csv_file.close()
  
