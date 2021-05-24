# -*- coding: utf-8 -*-
"""
@author: Qi Chen
"""
import numpy as np
import pandas as pd 

data = pd.read_csv('C:/2020_data.csv',index_col=0)

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
