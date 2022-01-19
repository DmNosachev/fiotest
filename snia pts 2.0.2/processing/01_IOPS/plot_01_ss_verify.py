#! /usr/bin/python

import argparse
import pandas as pd
import csv
import ptsproc

parser = argparse.ArgumentParser(description='PTS 01 IOPS Steady State Verification Plots')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
parser.add_argument('-ssr','--ss-round', help='Final round for steady state verification',
                      dest='SSRound', default='10', type=int,
                      choices=range(5, 25), required=False)
args = parser.parse_args()

FileFormats = ['svg', 'pdf']

BlockSizes = [4096, 65536, 1048576]
RWMixes = [0, 65, 100]

iops_ss_data = pd.read_csv('test01_ss_conv.csv', sep = ';', header=0)

for BS, RWMix in zip(BlockSizes, RWMixes):
  ss_df = iops_ss_data.loc[(iops_ss_data['RWMIX'] == RWMix) & 
                 (iops_ss_data['BS'] == BS) & 
                 (iops_ss_data['Round'].isin(range(args.SSRound - 4, args.SSRound + 1)))]
  
  ptsproc.checkSteadyState(str(BS), ss_df, 'Round', 'IOPS',
                           args.device_name + '_iops_ss_verify_' +
                           str(BS), FileFormats)