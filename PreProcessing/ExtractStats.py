#!/usr/bin/env python
# coding: utf-8

# In[127]:


import json
import matplotlib.dates as md
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import datetime as dt
import time
from datetime import datetime
import itertools 
import glob
import os


# In[119]:


def Extract(directory, interface, metric, stat):
    directory = str(directory)
    interface = str(interface)
    metric = str(metric)
    stat = str(stat)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '{}/PP_Output/{}/Stats/{}/{}/Metrics'.format(path,directory,interface,metric)
    df = pd.read_csv(os.path.join(path2, "DiskIO_{}.csv".format(stat)))
    df = df.drop([0,1,2])
    df = df.drop('Unnamed: 0', axis = 1)
    df = df.T
    df['Servers'] = ['umfs06', 'umfs09', 'umfs11', 'umfs16', 'umfs19', 'umfs20', 'umfs21',
       'umfs22', 'umfs23', 'umfs24', 'umfs25', 'umfs26', 'umfs27', 'umfs28']
    df = df.rename(columns={3: "disk_utilization_average"})
    df = pd.Series(df.disk_utilization_average.values,index=df.Servers).to_dict()
    print(df)


# In[120]:


ind = [1,2,3,7]
stat = ['mean', 'std', 'min', 'max']
zipped = list(zip(ind,stat))
for i,j in zipped:
    print(j)
    Extract('Output_20210201_1140', 'AGLT2', 'DiskIO', '{}'.format(i))


# In[140]:


def Extract_AGLT2CHI(directory, interface, stat):
    directory = str(directory)
    interface = str(interface)
    stat = str(stat)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '{}/PP_Output/{}/Stats/{}/Metrics'.format(path,directory,interface)
    
    if interface == 'AGLT2_CHI':
        df = pd.read_csv(os.path.join(path2, "AGLT2_CHI_{}.csv".format(stat)))
        df = df.rename(columns={"Unnamed: 0": "Metrics"})
        df = df.drop('Metrics', axis = 1)
        df = df.T
        df = df.rename(columns={0: "Input", 1: "Output"})
        df = df.round(5)
        df = df.to_dict(orient='Index')
        print(df)
        
    if interface == 'RBIN':
        df = pd.read_csv(os.path.join(path2, "RBIN_{}.csv".format(stat)))
        df = df.rename(columns={"Unnamed: 0": "Metrics"})
        df = df.drop('Metrics', axis = 1)
        df = df.T
        df = df.rename(columns={0: "GBIn", 1: "GBOut", 2: "GBPerSecIn", 3: "GBPerSecOut", 4: "UtilIn", 5: "UtilOut"})
        df = df.round(5)
        df = df.to_dict(orient='Index')
        print(df)


# In[141]:


Extract_AGLT2CHI('Output_20210201_1140', 'AGLT2_CHI', '1')


# In[142]:


Extract_AGLT2CHI('Output_20210201_1140', 'RBIN', '1')


# In[ ]:




