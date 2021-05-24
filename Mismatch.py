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

#optimize storage capacity with LRE>1
LRE = 1.5
load_sum = LRE * sum(data['load'])
solar_sum = sum(data['solar'])
wind_sum = sum(data['wind'])
load = data['load']
num = 21
storage = np.zeros(shape=(len(load)+1, num))
electricity = np.zeros(shape=(len(load), num))
corr_range = np.linspace(0, 1, num)
i = 0
for corr in corr_range:
    corr_wind = (1-corr)/(wind_sum/load_sum)
    corr_solar = corr/(solar_sum/load_sum)
    wind = corr_wind * data['wind']
    solar = corr_solar * data['solar']
    cap = 30000
    storage_sen = np.zeros(len(load)+1)
    storage_sen[0] = 62000
    storage_sen[len(load)] = storage_sen[0] + cap
    while storage_sen[len(load)]-storage_sen[0] > 50 and cap > 0:
        storage_sen = np.zeros(len(load)+1)
        storage_sen[0] = 62000
        electricity[0, i] = load[0] - wind[0] - solar[0]
        capacity = 62000 + cap
        min_elec = -500
        for j in range(1, (len(load)+1)):
            storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
            electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
        
        min_elec = min_elec + 5
        while storage_sen[len(load)]-storage_sen[0] > 50 and min_elec < -10:
            for j in range(1,(len(load)+1)):
                storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
                electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
            min_elec = min_elec + 5
       
        min_elec = min_elec - 10
        for j in range(1,(len(load)+1)):
           storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
           electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
        storage[:,i] = storage_sen
        cap = cap - 200
    cap = cap + 400
    storage_sen = np.zeros(len(load)+1)
    storage_sen[0] = 62000
    electricity[0, i] = load[0] - wind[0] - solar[0]
    capacity = 62000 + cap
    min_elec = -500
    for j in range(1, (len(load)+1)):
        storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
        electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
        
    min_elec = min_elec + 5
    while storage_sen[len(load)]-storage_sen[0] > 50 and min_elec < -10:
        for j in range(1,(len(load)+1)):
            storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
            electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
        min_elec = min_elec + 5
       
    min_elec = min_elec - 10
    for j in range(1,(len(load)+1)):
          storage_sen[j] = min((storage_sen[j-1]-max((load[j-1]-wind[j-1]-solar[j-1]), min_elec)), capacity)
          electricity[j-1, i] = storage_sen[j-1] - storage_sen[j] 
    storage[:,i] = storage_sen

    i = i + 1

max_electric = np.max(electricity, axis=0)
min_electric = np.min(electricity, axis=0)
min_sto = np.array([np.min(storage, axis=0)])

min_sto = np.repeat(min_sto, len(storage), axis = 0)
storage = storage - min_sto
max_sto = np.max(storage, axis=0)
a = load-wind-solar-electricity[:,0]

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



