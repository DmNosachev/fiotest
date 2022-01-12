#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path

parser = argparse.ArgumentParser(description='PTS 05 HIR Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=12)

filename = 'test05.csv'
sns.set_style("whitegrid")

hir_data = pd.read_csv(filename, sep = ';', header=0)
hir_data_melted = pd.melt(hir_data, id_vars=['Round', 'IOPS', 'STATE'], value_vars=['AVLAT', 'P99_LAT', 'P99D9_LAT', 'P99D99_LAT', 'MAX_LAT'], var_name='Latency type')

avlat_data = hir_data_melted.loc[hir_data_melted['Latency type'] == 'AVLAT']

hir_plot = sns.relplot(x='Round', y='value', hue='STATE', kind='line', data=avlat_data, palette=sns.color_palette('cubehelix', 6))

hir_plot.fig.set_figwidth(15)
hir_plot.fig.set_figheight(7)
hir_plot.set(ylabel='Latency, µs')
hir_plot.set(xlabel='Time, min')
hir_plot.set(yscale='log')
hir_plot.set(rasterized=True)

hir_plot.savefig(str(args.device_name) + '_hir_latency.svg', format='svg', transparent=True)
hir_plot.savefig(str(args.device_name) + '_hir_latency.png', format='png')

p99d99_data = hir_data_melted.loc[hir_data_melted['Latency type'] == 'P99D99_LAT']

p99d99_plot = sns.relplot(x='Round', y='value', hue='STATE', kind='line', data=p99d99_data, palette=sns.color_palette('cubehelix', 6))

p99d99_plot.fig.set_figwidth(15)
p99d99_plot.fig.set_figheight(7)
p99d99_plot.set(ylabel='Latency, µs')
p99d99_plot.set(xlabel='Time, min')
p99d99_plot.set(yscale='log')
p99d99_plot.set(rasterized=True)

p99d99_plot.savefig(str(args.device_name) + '_hir_latency_p99d99.svg', format='svg', transparent=True)
p99d99_plot.savefig(str(args.device_name) + '_hir_latency_p99d99.png', format='png')

hir_iops_plot = sns.relplot(x='Round', y='IOPS', hue='STATE', kind='line', data=hir_data, palette=sns.color_palette('cubehelix', 6))

hir_iops_plot.fig.set_figwidth(15)
hir_iops_plot.fig.set_figheight(7)
hir_iops_plot.set(ylabel='IOPS')
hir_iops_plot.set(xlabel='Time, min')

hir_iops_plot.savefig(str(args.device_name) + '_hir_iops.svg', format='svg', transparent=True)
hir_iops_plot.savefig(str(args.device_name) + '_hir_iops.png', format='png')