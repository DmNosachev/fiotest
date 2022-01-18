#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path

parser = argparse.ArgumentParser(description='PTS 06 XSR Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test06.csv'
sns.set_style("whitegrid")

xsr_data = pd.read_csv(filename, sep = ';', header=0)
xsr_data_lat_melted = pd.melt(xsr_data, id_vars=['Round', 'AG'],
                           value_vars=['Average', '99%', '99.9%', '99.99%', 'Maximum'],
                           var_name='Latency type')

xsr_plot = sns.relplot(x='Round', y='value', hue='Latency type',
                        kind='line', data=xsr_data_lat_melted,
                        palette=sns.color_palette('plasma', 5))

sns.move_legend(
    xsr_plot, "lower center",
    bbox_to_anchor=(0.5, -.1),
    ncol=3,
    title=None,
    frameon=False,
)

xsr_plot.fig.set_figwidth(8)
xsr_plot.fig.set_figheight(4)
xsr_plot.set(ylabel='Latency, µs')
xsr_plot.set(xlabel='Round')
xsr_plot.set(yscale='log')
xsr_plot.set(xlim=(1, None))

xsr_plot.savefig(str(args.device_name) + '_xsr_latency.svg', format='svg', transparent=True)
xsr_plot.savefig(str(args.device_name) + '_xsr_latency.pdf', format='pdf')

xsr_bw_plot = sns.relplot(x='Round', y='BW', hue='AG', kind='line', data=xsr_data,
                        palette=sns.color_palette('tab10', 3))
                        
sns.move_legend(
    xsr_bw_plot, "lower center",
    bbox_to_anchor=(0.5, -.1),
    ncol=3,
    title=None,
    frameon=False,
)

xsr_bw_plot.fig.set_figwidth(8)
xsr_bw_plot.fig.set_figheight(4)
xsr_bw_plot.set(ylabel='BW, MiBps')
xsr_bw_plot.set(xlabel='Round')
xsr_bw_plot.set(xlim=(1, None))

xsr_bw_plot.savefig(str(args.device_name) + '_xsr_bw.svg', format='svg', transparent=True)
xsr_bw_plot.savefig(str(args.device_name) + '_xsr_bw.pdf', format='pdf')