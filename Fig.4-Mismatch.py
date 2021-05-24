# -*- coding: utf-8 -*-
"""

@author: Qi Chen
"""

import numpy as np
import pandas as pd 

data = pd.read_csv('C:/2020_data.csv',index_col=0)

#mismatch with different LRE and Psolar
LRE = 1
load_sum = LRE * sum(data['load'])
load = data['load']
solar_sum = sum(data['solar'])
wind_sum = sum(data['wind'])
num = 21
mismatch = np.zeros(num)
i = 0
corr_range = np.linspace(0, 1, num)

for corr in corr_range:
    corr_wind = (1-corr)/(wind_sum/load_sum)
    corr_solar = corr/(solar_sum/load_sum)
    wind = corr_wind * data['wind']
    solar = corr_solar * data['solar']
    match = solar + wind - load
    match_sum = 0
    for j in range(1,len(load)+1):
        if match[j-1] > 0:
            match_sum = match_sum + match[j-1]
    mismatch[i] = match_sum/sum(data['load'])
    i = i + 1
