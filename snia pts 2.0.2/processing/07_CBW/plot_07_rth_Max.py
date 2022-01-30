#! /usr/bin/python

import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

parser = argparse.ArgumentParser(description='PTS 07 LAT RTH')
parser.add_argument('-d','--device', help='Device name', dest='device_name', required=True)
args = parser.parse_args()

plt.rc('font', size=8)

HistNames = ['Min', 'Mid', 'Max']
TCSet = [1, 2, 32]
QDSet = [1, 16, 32]
CSVFileList = []
for i in range(1, 32+1):
  CSVFileList.append('results/test07_Max_RTH_clat.' + str(i) +'.log')
               
rth_data0 = pd.concat((pd.read_csv(f, sep = ',',
                      usecols=[1], names=['Lat']) for f in CSVFileList),
                      ignore_index=True)
rth_data0.Lat = rth_data0.Lat.multiply(0.001)

Lat_mean = rth_data0['Lat'].mean()
Lat_p3n = rth_data0['Lat'].quantile(0.999)
Lat_p4n = rth_data0['Lat'].quantile(0.9999)
Lat_p5n = rth_data0['Lat'].quantile(0.99999)
print('Max-IOPS read latency stats:')
print(f'Mean = {Lat_mean:.2f}, 99.9% = {Lat_p3n:.2f}, \
99.99% = {Lat_p4n:.2f}, 99.999% = {Lat_p5n:.2f}' + '\n')

rth_plot0 = sns.histplot(data=rth_data0, x='Lat', element="poly", log_scale=[True, True])
plt.axvline(x=Lat_mean, label='Mean: ' + str(round(Lat_mean, 2)), linestyle='dotted', color='tab:green')
plt.axvline(x=Lat_p3n, label='99.9%: ' + str(round(Lat_p3n, 2)), linestyle='dashed', color='tab:purple')
plt.axvline(x=Lat_p4n, label='99.99%: ' + str(round(Lat_p4n, 2)), linestyle='dashdot', color='tab:cyan')
plt.axvline(x=Lat_p5n, label='99.999%: ' + str(round(Lat_p5n, 2)), linestyle='solid', color='tab:orange')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
rth_plot0.set(xlabel='Latency, µs')
#rth_plot0.set_xlim(10, 10000)

fig = rth_plot0.get_figure()
fig.set_figwidth(8)
fig.set_figheight(4)

#fig.savefig(str(args.device_name) + '_rth_rw=0.svg', format='svg', transparent=True)
fig.savefig(str(args.device_name) + '_rth_Max.png', format='png', bbox_inches='tight')
fig.savefig(str(args.device_name) + '_rth_Max.pdf', format='pdf', bbox_inches='tight')


