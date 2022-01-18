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

parser = argparse.ArgumentParser(description='PTS 07 PW IOPS Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

Rounds=10

plt.rc('font', size=8)

filename = 'test07_pw_iops.csv'
sns.set_style("whitegrid")

pw_data = pd.read_csv(filename, sep = ';', header=0)

pw_iops_plot = sns.catplot(data=pw_data, x='Round', y='IOPS', edgecolor=None, rasterized=True, palette=sns.color_palette('plasma', 1))

pw_iops_plot.fig.set_figwidth(8)
pw_iops_plot.fig.set_figheight(4)
pw_iops_plot.set(ylabel='IOPS')
pw_iops_plot.set(xlabel='Round')
pw_iops_plot.set(xticks=np.linspace(1, Rounds, Rounds))

pw_iops_plot.savefig(str(args.device_name) + '_cbw_pw_iops.svg', format='svg', transparent=True)
pw_iops_plot.savefig(str(args.device_name) + '_cbw_pw_iops.png', format='png')
pw_iops_plot.savefig(str(args.device_name) + '_cbw_pw_iops.pdf', format='pdf')
