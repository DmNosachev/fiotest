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

rth_data100 = pd.read_csv('test03_100_clat.1.log', sep = ',',
                      usecols=[1], names=['Lat'])
rth_data100.Lat = rth_data100.Lat.multiply(0.001)

Lat_100_mean = rth_data100['Lat'].mean()
Lat_100_p3n = rth_data100['Lat'].quantile(0.999)
Lat_100_p4n = rth_data100['Lat'].quantile(0.9999)
Lat_100_p5n = rth_data100['Lat'].quantile(0.99999)
print('100% read latency stats:')
print(f'Mean = {Lat_100_mean:.2f}, 99.9% = {Lat_100_p3n:.2f}, \
99.99% = {Lat_100_p4n:.2f}, 99.999% = {Lat_100_p5n:.2f}' + '\n')

rth_plot100 = sns.histplot(data=rth_data100, x='Lat', element='poly', log_scale=[True, True])
plt.axvline(x=Lat_100_mean, label='Mean: ' + str(round(Lat_100_mean, 2)), linestyle='dotted', color='tab:green')
plt.axvline(x=Lat_100_p3n, label='99.9%: ' + str(round(Lat_100_p3n, 2)), linestyle='dashed', color='tab:purple')
plt.axvline(x=Lat_100_p4n, label='99.99%: ' + str(round(Lat_100_p4n, 2)), linestyle='dashdot', color='tab:cyan')
plt.axvline(x=Lat_100_p5n, label='99.999%: ' + str(round(Lat_100_p5n, 2)), linestyle='solid', color='tab:orange')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
rth_plot100.set(xlabel='Latency, µs')
#rth_plot100.set_xlim(10, 10000)

fig = rth_plot100.get_figure()
fig.set_figwidth(8)
fig.set_figheight(4)

fig.savefig(str(args.device_name) + '_rth_rw=100.svg', format='svg', transparent=True)
fig.savefig(str(args.device_name) + '_rth_rw=100.png', format='png', bbox_inches='tight')
#fig.savefig(str(args.device_name) + '_rth_rw=100.pdf', format='pdf', bbox_inches='tight')

