#! /usr/bin/python

import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
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

RWMixLabels = ['0/100', '5/95', '35/65', '50/50', '65/35', '95/5', '100/0']
BSLabels = ['512 Б', '4 КиБ', '8 КиБ', '16 КиБ', '32 КиБ', '64 КиБ', '128 КиБ', '1 МиБ']

iops_pvt = iops_data.pivot(index='BS', columns='RWMIX', values='IOPS')

result = iops_pvt.to_numpy()
fig=plt.figure(figsize=(8, 8), dpi=250)
ax1=fig.add_subplot(111, projection='3d')
ax1.set_xlabel('RW Mix', labelpad=10)
ax1.set_ylabel('Block Size', labelpad=10)
ax1.set_zlabel('IOPS')
xlabels = np.array(RWMixLabels)
xpos = np.arange(xlabels.shape[0])
ylabels = np.array(BSLabels)
ypos = np.arange(ylabels.shape[0])

xposM, yposM = np.meshgrid(xpos, ypos, copy=False)

zpos=result
zpos = zpos.ravel()

dx=0.5
dy=0.5
dz=zpos

ax1.w_xaxis.set_ticks(xpos + dx/2.)
ax1.w_xaxis.set_ticklabels(xlabels)

ax1.w_yaxis.set_ticks(ypos + dy/2.)
ax1.w_yaxis.set_ticklabels(ylabels)

values = np.linspace(0.2, 1., xposM.ravel().shape[0])
colors = cm.plasma(values)
ax1.bar3d(xposM.ravel(), yposM.ravel(), dz*0, dx, dy, dz, color=colors)
ax1.view_init(elev=26, azim=133)
#plt.show()
#fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
plt.savefig(str(args.device_name) + '_iops_3d.svg', format='svg', transparent=True)
plt.savefig(str(args.device_name) + '_iops_3d.png', format='png')
#plt.savefig(str(args.device_name) + '_iops_3d.pdf', format='pdf')