# -*- coding: utf-8 -*-
"""
@author: Qi Chen
"""

import numpy as np
import pandas as pd 

data = pd.read_csv('C:/2020_data.csv',index_col=0)

#storage with additional and controllable energy
day = 366
num = 1
storage = np.zeros(len(data)+1)
electricity = np.zeros(len(data)+1)
electricity_addition = np.zeros(len(data)+1)
storage[0] = 6000
LRE = 1
t = 0
#day
load_sum = LRE * sum(data['load'])
load_or = data['load']
solar_sum = sum(data['solar'])
wind_sum = sum(data['wind'])
corr = 0.8
corr_wind = (1-corr)/(wind_sum/load_sum)
corr_solar = corr/(solar_sum/load_sum)
wind_or = corr_wind * data['wind']
solar_or = corr_solar * data['solar']
    
for d in range(0, day):
    load = load_or[24*d: 24*(d+1)]
    wind = wind_or[24*d: 24*(d+1)]
    solar = solar_or[24*d: 24*(d+1)]
    if sum(load)>sum(wind)+sum(solar):
        sto = (sum(load) - sum(wind) - sum(solar))/24
    for j in range(0, 24):
        electricity_addition[(24*d+j)] = sto
        electricity[(24*d+j)] = load[(24*d+j)] - solar[(24*d+j)] - wind[(24*d+j)] - electricity_addition[(24*d+j)]
        storage[(24*d+j+1)] = storage[(24*d+j)] - electricity[(24*d+j)]
    else:
        coe_solar = (sum(load)-sum(wind))/sum(solar)
        solar = coe_solar * solar
    for j in range(0, 24):
        electricity[(24*d+j)] = load[(24*d+j)] - solar[(24*d+j)] - wind[(24*d+j)]
        storage[(24*d+j+1)] = storage[(24*d+j)] - electricity[(24*d+j)]
               
min_sto = np.array([np.min(storage, axis=0)])
min_sto = np.repeat(min_sto, len(storage), axis = 0)
storage = storage - min_sto


