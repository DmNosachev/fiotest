#! /usr/bin/python

import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import shutil
import csv
import os.path

plt.rc('font', size=8)

filename = 'test03read_clat.1.log'
processed_filename = 'test03_read.csv'
device_name = 'CD6-V'

fields = ['time_ms', 'clat_ns', 'data_direction', 'block_size', 'prio']

if not os.path.isfile(processed_filename):
  with open(filename, 'r') as csvfile, open(processed_filename, 'w') as processed_file:
    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.writer(processed_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
    for row in reader:
      clat_ms = int(row['clat_ns']) / 1000
      writer.writerow([clat_ms])
  processed_file.close()
  csvfile.close()
  
clat = pd.read_csv(processed_filename, names = ['clat_mus'])

data_mean = clat['clat_mus'].mean()
data_p3n = clat['clat_mus'].quantile(0.999)
data_p4n = clat['clat_mus'].quantile(0.9999)
data_p5n = clat['clat_mus'].quantile(0.99999)

print('Mean:', data_mean)
print('99.9%:', data_p3n)
print('99.99%:', data_p4n)
print('99.999%:', data_p5n)
          
sns_plot = sns.displot(clat, x='clat_mus', bins=1000)

plt.axvline(x=data_mean, label='Mean: ' + str(round(data_mean, 2)), color='tab:green')
plt.axvline(x=data_p3n, label='99.9%: ' + str(round(data_p3n, 2)), color='tab:purple')
plt.axvline(x=data_p4n, label='99.99%: ' + str(round(data_p4n, 2)), color='tab:cyan')
plt.axvline(x=data_p5n, label='99.999%: ' + str(round(data_p5n, 2)), color='tab:orange')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
plt.xlim(left=80, right=110)
plt.title(device_name + ' 4k read QD=1 latency histogram')

sns_plot.fig.set_figwidth(6)
sns_plot.fig.set_figheight(3)
sns_plot.set(xlabel='latency, µs')

sns_plot.savefig(device_name + '_clat_read.svg', format='svg', transparent=True)
sns_plot.savefig(device_name + '_clat_read.png', format='png')