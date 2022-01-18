#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path
import numpy as np

parser = argparse.ArgumentParser(description='PTS 07 CBW Demand Intensity Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test07_main_averaged.csv'
sns.set_style("whitegrid")

di_data = pd.read_csv(filename, sep = ';', header=0)

di_plot = sns.relplot(data=di_data, x='IOPS', y='LAT', hue='TC', style="QD", kind='scatter', palette=sns.color_palette('tab10', 6))

IOPS_min = di_data['IOPS'].min()
# Потом вычислять автоматически
IOPS_max = 42290
IOPS_mid = IOPS_min + (IOPS_max - IOPS_min) / 2
print('IOPS stats:')
print(f'Mid = {IOPS_mid:.2f}, Min = {IOPS_min:.2f}, \
Max = {IOPS_max:.2f}' + '\n')

plt.axvline(x=IOPS_mid, label='Mean: ' + str(round(IOPS_mid)), linestyle='dashed', color='tab:gray')
plt.axvline(x=IOPS_min, label='Min: ' + str(round(IOPS_min)), linestyle='dashed', color='tab:gray')
plt.axvline(x=IOPS_max, label='Max: ' + str(round(IOPS_max)), linestyle='dashed', color='tab:gray')
plt.axhline(y=5000, label='Lat limit: 5 ms', linestyle='dashed', color='tab:red')

di_plot.fig.set_figwidth(8)
di_plot.fig.set_figheight(4)
di_plot.set(yscale="log")
di_plot.set(ylabel='Latency, µs')
di_plot.set(xlabel='IOPS')

di_plot.savefig(str(args.device_name) + '_cbw_di.svg', format='svg', transparent=True)
di_plot.savefig(str(args.device_name) + '_cbw_di.pdf', format='pdf')
