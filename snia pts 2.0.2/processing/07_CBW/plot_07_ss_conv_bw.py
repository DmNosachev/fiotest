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

parser = argparse.ArgumentParser(description='PTS 06 Main Steady State Convergence Plot')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

Rounds = 10
plt.rc('font', size=8)

filename = 'test06_main_conv.csv'
sns.set_style("whitegrid")

ss_conv_data = pd.read_csv(filename, sep = ';', header=0)

ss_df = ss_conv_data.loc[(ss_conv_data['TC'] == 32)]

ss_conv_plot = sns.relplot(data = ss_df, x='Round', y='IOPS', sort=False, style='QD', kind='line', color='black')

ss_conv_plot.fig.set_figwidth(8)
ss_conv_plot.fig.set_figheight(4)
ss_conv_plot.set(ylabel='IOPS')
ss_conv_plot.set(xlabel='Round')
ss_conv_plot.set(xticks=np.linspace(1, Rounds, Rounds))
#ss_conv_plot.set(ylim=(0, None))

ss_conv_plot.savefig(str(args.device_name) + '_cbw_ss_conv_bw.pdf', format='pdf')
