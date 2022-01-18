#! /usr/bin/python

import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='PTS 04 WSAT Steady State Verification Plots')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

SSRound = 360

filename = 'test04_main.csv'
plt.rc('font', size=8)

wsat_data = pd.read_csv(filename, sep = ';', header=0)

ss_df = wsat_data.loc[wsat_data['Round'].isin([SSRound - 120,
                                               SSRound - 90,
                                               SSRound - 60,
                                               SSRound - 30,
                                               SSRound])]

av_ss = ss_df['IOPS'].mean()
x = ss_df['Round'].tolist()
y = ss_df['IOPS'].tolist()
coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)


ss_df.plot(kind='scatter', x='Round', y='IOPS', color='tab:red')
plt.plot(x, poly1d_fn(x), color='k', linestyle='dotted')
plt.axhline(y=av_ss * 1.1, color='tab:green', linestyle='dashed')
plt.axhline(y=av_ss, color='tab:blue', linestyle='dashed')
plt.axhline(y=av_ss * 0.9, color='tab:purple', linestyle='dashed')
plt.xticks(x, ss_df['Round'].tolist())

plt.savefig(str(args.device_name) + '_iops_ss_verify.svg', format='svg', transparent=True)
plt.savefig(str(args.device_name) + '_iops_ss_verify.pdf', format='pdf')