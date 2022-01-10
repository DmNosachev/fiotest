#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path

parser = argparse.ArgumentParser(description='PTS 01 IOPS Steady State Convergence Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=12)

filename = 'lat03_2.csv'
sns.set_style("whitegrid")

lat_data = pd.read_csv(filename, sep = ';', header=0)
lat_data_melted = pd.melt(lat_data, id_vars=['TC', 'QD', 'RWMIX', 'IOPS'], value_vars=['AV_LAT', 'P99D99_LAT', 'MAX_LAT'], var_name='Latency type')

lat_plot = sns.relplot(x='IOPS', y='value', style='Latency type', hue='RWMIX', kind='line', data=lat_data_melted, palette=sns.color_palette('cubehelix', 3))

lat_plot.fig.set_figwidth(18)
lat_plot.fig.set_figheight(7)
lat_plot.set(ylabel='Latency, µs')
lat_plot.set(xlabel='IOPS')
lat_plot.set(yscale='log')
#lat_plot.set(xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#lat_plot.set(ylim=(0, None))

lat_plot.savefig(str(args.device_name) + '_lat.svg', format='svg', transparent=True)
lat_plot.savefig(str(args.device_name) + '_lat.png', format='png')