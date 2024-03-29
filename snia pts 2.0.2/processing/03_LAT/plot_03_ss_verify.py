#! /usr/bin/python

import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='PTS 03 LAT Steady State Verification Plots')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

SSRound = 10

plt.rc('font', size=8)

iops_ss_data = pd.read_csv('test03_ss_conv.csv', sep = ';', header=0)


ss_df = iops_ss_data.loc[(iops_ss_data['BS'] == 4096) &
               (iops_ss_data['Round'].isin(range(SSRound - 4, SSRound + 1)))]

av_ss = ss_df['LAT'].mean()
x = ss_df['Round'].tolist()
y = ss_df['LAT'].tolist()
coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)

ss_df.plot(kind='scatter', x='Round', y='LAT', color='tab:red')
plt.plot(x, poly1d_fn(x), color='k', linestyle='dotted')
plt.axhline(y=av_ss * 1.1, color='tab:green', linestyle='dashed')
plt.axhline(y=av_ss, color='tab:blue', linestyle='dashed')
plt.axhline(y=av_ss * 0.9, color='tab:purple', linestyle='dashed')
plt.xticks(x, ss_df['Round'].tolist())

plt.savefig(str(args.device_name) + '_lat_ss_verify.pdf', format='pdf')