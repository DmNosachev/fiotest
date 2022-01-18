#! /usr/bin/python

import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

parser = argparse.ArgumentParser(description='PTS 03 LAT RTH')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)


rth_data0 = pd.read_csv('test030_clat.1.log', sep = ',',
                      usecols=[1], names=['Lat'])
rth_data0.Lat = rth_data0.Lat.multiply(0.001)

cdf_plot0 = sns.ecdfplot(data=rth_data0, x='Lat', log_scale=[True, True])
cdf_plot0.set(xlabel='Latency, µs')
#rth_plot0.set_xlim(10, 10000)

fig = cdf_plot0.get_figure()
fig.set_figwidth(8)
fig.set_figheight(4)

#fig.savefig(str(args.device_name) + '_rth_rw=0.svg', format='svg', transparent=True)
fig.savefig(str(args.device_name) + '_cdf_rw=0.png', format='png', bbox_inches='tight')
fig.savefig(str(args.device_name) + '_cdf_rw=0.pdf', format='pdf', bbox_inches='tight')


