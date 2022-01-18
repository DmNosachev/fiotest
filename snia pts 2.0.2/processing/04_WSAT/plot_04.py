#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path

parser = argparse.ArgumentParser(description='PTS 04 WSAT Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test04_main.csv'
sns.set_style("whitegrid")

wsat_data = pd.read_csv(filename, sep = ';', header=0)
wsat_data_lat_melted = pd.melt(wsat_data, id_vars=['Round', 'TGib', 'TDF'],
                           value_vars=['Average', '99%', '99.9%', '99.99%', 'Maximum'],
                           var_name='Latency type')

wsat_plot = sns.relplot(x='TDF', y='value', hue='Latency type',
                        kind='line', data=wsat_data_lat_melted,
                        palette=sns.color_palette('plasma', 5))

sns.move_legend(
    wsat_plot, "lower center",
    bbox_to_anchor=(0.5, -.1),
    ncol=3,
    title=None,
    frameon=False,
)

wsat_plot.fig.set_figwidth(8)
wsat_plot.fig.set_figheight(4)
wsat_plot.set(ylabel='Latency, µs')
wsat_plot.set(xlabel='Drive fills')
wsat_plot.set(yscale='log')
wsat_plot.set(xlim=(0, None))

wsat_plot.savefig(str(args.device_name) + '_wsat_latency.svg', format='svg', transparent=True)
wsat_plot.savefig(str(args.device_name) + '_wsat_latency.pdf', format='pdf')

wsat_iops_plot = sns.relplot(x='TDF', y='IOPS', kind='line', data=wsat_data)

wsat_iops_plot.fig.set_figwidth(8)
wsat_iops_plot.fig.set_figheight(4)
wsat_iops_plot.set(ylabel='IOPS')
wsat_iops_plot.set(xlabel='Drive fills')
wsat_iops_plot.set(xlim=(0, None))

wsat_iops_plot.savefig(str(args.device_name) + '_wsat_iops.svg', format='svg', transparent=True)
wsat_iops_plot.savefig(str(args.device_name) + '_wsat_iops.png', format='png')
wsat_iops_plot.savefig(str(args.device_name) + '_wsat_iops.pdf', format='pdf')