#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import shutil
import csv
import os.path

parser = argparse.ArgumentParser(description='PTS 01 IOPS 2D Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

filename = 'test01_main.csv'
sns.set_style("whitegrid")

iops_data = pd.read_csv(filename, sep = ';', header=0)

iops_data.replace(to_replace={100 : '100/0', 95 : '95/5', 65 : '65/35', 50 : '50/50', 35 : '35/65', 5 : '5/95', 0 : '0/100'}, inplace=True)

iops_data.replace(to_replace={4096 : '4K', 8192 : '8K', 16384 : '16K', 32768 : '32K', 65536 : '64K', 131072 : '128K', 1048576 : '1M'}, inplace=True)

iops_plot = sns.relplot(x='BS', y='IOPS', hue='RWMIX', sort=False, kind='line', marker="o", data=iops_data, palette=sns.color_palette('cubehelix', 7))

iops_plot.fig.set_figwidth(8)
iops_plot.fig.set_figheight(4)
iops_plot.set(ylabel='IOPS')
iops_plot.set(xlabel='RW mix')
iops_plot.set(yscale='log')
iops_plot.set(yticks=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 300000, 400000, 500000, 600000])
#iops_plot.set(ylim=(0, None))

iops_plot.savefig(str(args.device_name) + '_iops2d.svg', format='svg', transparent=True)
iops_plot.savefig(str(args.device_name) + '_iops2d.png', format='png')