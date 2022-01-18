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

parser = argparse.ArgumentParser(description='PTS 07 CBW Demand Variation Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test07_main_averaged.csv'
sns.set_style("whitegrid")

dv_data = pd.read_csv(filename, sep = ';', header=0)
dv_data.sort_values('QD', inplace=True, ascending=True)
dv_data.QD = dv_data.QD.astype(str)

dv_plot = sns.relplot(data=dv_data, x='QD', y='IOPS', hue='TC', sort=False, kind='line', palette=sns.color_palette('plasma', 6))

sns.move_legend(
    dv_plot, "lower center",
    bbox_to_anchor=(0.5, -.15),
    ncol=3,
    title='TC',
    frameon=False,
)

dv_plot.fig.set_figwidth(8)
dv_plot.fig.set_figheight(4)
dv_plot.set(ylabel='IOPS')
dv_plot.set(xlabel='Queue depth')

dv_plot.savefig(str(args.device_name) + '_cbw_dv.svg', format='svg', transparent=True)
dv_plot.savefig(str(args.device_name) + '_cbw_dv.pdf', format='pdf')
