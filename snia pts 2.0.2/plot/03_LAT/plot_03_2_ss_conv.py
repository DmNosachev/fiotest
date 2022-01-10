#! /usr/bin/python

import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path
import argparse

parser = argparse.ArgumentParser(description='PTS 01 IOPS Steady State Convergence Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test03_2_ss.csv'
sns.set_style("whitegrid")

lat_data = pd.read_csv(filename, sep = ';', header=0)
lat_data['av_lat'] = lat_data['av_lat'] / 1000

lat_plot = sns.relplot(x='round', y='av_lat', color='tab:red', sort=False, kind='line', data=lat_data)

lat_plot.fig.set_figwidth(18)
lat_plot.fig.set_figheight(7)
lat_plot.set(ylabel='Average Latency, µs')
lat_plot.set(xlabel='Round')
lat_plot.set(ylim=(0, None))

lat_plot.savefig(str(args.device_name) + '_lat_ss.svg', format='svg', transparent=True)
lat_plot.savefig(str(args.device_name) + '_lat_ss.png', format='png')