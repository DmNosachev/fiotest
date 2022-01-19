import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def checkSteadyState(testName, ss_df, xSel, ySel, plotName, plotFormats):
  plt.rc('font', size=8)
  
  av_ss = ss_df[ySel].mean()
  x = ss_df[xSel].tolist()
  y = ss_df[ySel].tolist()
  coef = np.polyfit(x, y, 1)
  poly1d_fn = np.poly1d(coef)
  slope_prc = 100*((abs(coef[0])/poly1d_fn(x[4])) / (1/4))
  
  print('Steady state check for ' + testName + ':')
  if ((max(y) - min(y)) >= av_ss*0.2):
    print('Maximum data excursion check failed')
  
  if (slope_prc > 10):
    print('Slope excursion check failed')

  print(f'Average = {av_ss:.2f}')
  print(f'Allowed max data exc = {av_ss*0.2:.2f}')
  print(f'Measured max data exc = {(max(y) - min(y)):.2f}')
  print(f'Linear fit (a * x + b) = {coef[0]:.2f} * x + {coef[1]:.2f}')
  print(f'Slope percent (allowed max 10%) = {slope_prc:.2f}')
  
  ss_df.plot(kind='scatter', x='Round', y='IOPS', color='tab:red')
  plt.plot(x, poly1d_fn(x), color='k', linestyle='dotted')
  plt.axhline(y=av_ss * 1.1, color='tab:green', linestyle='dashed')
  plt.axhline(y=av_ss, color='tab:blue', linestyle='dashed')
  plt.axhline(y=av_ss * 0.9, color='tab:purple', linestyle='dashed')
  plt.xticks(x, ss_df['Round'].tolist())
  
  for FileFmt in plotFormats:
    plt.savefig(plotName + '.' +FileFmt,
                format=FileFmt, transparent=True)