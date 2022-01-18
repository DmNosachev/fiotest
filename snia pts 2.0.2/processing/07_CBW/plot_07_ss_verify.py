#! /usr/bin/python

import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='PTS 07 CBW Steady State Verification Plots')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

SSRound = 10

plt.rc('font', size=8)

ss_data = pd.read_csv('test07_main_conv.csv', sep = ';', header=0)

ss_df = ss_data.loc[(ss_data['TC'] == 32) &
                    (ss_data['QD'] == 32) &
                    (ss_data['Round'].isin(range(SSRound - 4, SSRound + 1)))]

IOPS_StdDev = ss_df['IOPS'].std()
av_ss = ss_df['IOPS'].mean()
x = ss_df['Round'].tolist()
y = ss_df['IOPS'].tolist()
coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)
print(f'IOPS std deviation = {IOPS_StdDev:.2f}' + '\n')

ss_df.plot(kind='scatter', x='Round', y='IOPS', color='tab:red')
plt.plot(x, poly1d_fn(x), color='k', linestyle='dotted')
plt.axhline(y=av_ss * 1.1, color='tab:green', linestyle='dashed')
plt.axhline(y=av_ss, color='tab:blue', linestyle='dashed')
plt.axhline(y=av_ss * 0.9, color='tab:purple', linestyle='dashed')
plt.xticks(x, ss_df['Round'].tolist())
plt.savefig(str(args.device_name) + '_cbw_ss_verify.pdf', format='pdf')