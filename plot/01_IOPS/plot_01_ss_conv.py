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

plt.rc('font', size=8)

filename = 'test01_ss_conv.csv'
sns.set_style("whitegrid")

ss_conv_data = pd.read_csv(filename, sep = ';', header=0)

ss_conv_data.replace(to_replace={4096 : '4K', 8192 : '8K', 16384 : '16K', 32768 : '32K', 65536 : '64K', 131072 : '128K', 1048576 : '1M'}, inplace=True)

ss_conv_plot = sns.relplot(x='Round', y='IOPS', hue='BS', sort=False, kind='line', marker="o", data=ss_conv_data, palette=sns.color_palette('cubehelix', 7))

ss_conv_plot.fig.set_figwidth(8)
ss_conv_plot.fig.set_figheight(4)
ss_conv_plot.set(ylabel='IOPS')
ss_conv_plot.set(xlabel='Round')
ss_conv_plot.set(xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
ss_conv_plot.set(ylim=(0, None))

ss_conv_plot.savefig(str(args.device_name) + '_iops_ss_conv.svg', format='svg', transparent=True)
ss_conv_plot.savefig(str(args.device_name) + '_iops_ss_conv.png', format='png')