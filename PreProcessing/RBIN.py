#!/usr/bin/env python
# coding: utf-8

# In[28]:


import json
import matplotlib.dates as md
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import datetime as dt
import time
from datetime import datetime
import itertools 
import os 


# In[29]:


def RBIN(directory, file):
    directory = str(directory)
    file = str(file)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/RBIN'.format(directory)
    #my_path = os.path.abspath(__file__)
    #print(os.path.join(path + path2,"{}.json".format(file)))
    df = pd.read_json(os.path.join(path + path2, "{}.json".format(file)))
    ID, time, BitsIn, BitsOut, BitsSecIn, BitsSecOut, UtilIn, UtilOut = df.columns
    df[time] = pd.to_datetime(df[time],unit='s')
    cols = df.columns.drop([ID,time,UtilIn,UtilOut])
    df[cols] = df[cols]* (1.25e-10)
    df = df[0:12]
    stats = df[[BitsIn, BitsOut,BitsSecIn, BitsSecOut, UtilIn, UtilOut]].describe()
    stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/RBIN'.format(directory), "Stats_{}.csv".format(file)),                index=True)
    if file == 'RBIN_0':
        ax = df.plot(kind='line',x=time, y=[BitsIn, BitsOut], title = 'et-8/0/0 BitsIn_Out',figsize=(10,4))
        ax1 = df.plot(kind='line',x=time, y=[BitsSecIn,BitsSecOut], title = 'et-8/0/0 BitsPerSecondIn_Out' ,figsize=(10,4))
        ax2 = df.plot(kind='line',x=time, y=[UtilIn,UtilOut],title = 'et-8/0/0 Utilization_Out' ,figsize=(10,4))
        ax.set_ylabel("GB")
        ax1.set_ylabel("GB/s")
        ax2.set_ylabel("%")
        ax.figure.savefig('{}/PP_Output/{}/Plots/RBIN/BitsIn_Out_{}.png'.format(path,directory,file))
        ax1.figure.savefig('{}/PP_Output/{}/Plots/RBIN/BitsSecIn_Out_{}.png'.format(path,directory,file))
        ax2.figure.savefig('{}/PP_Output/{}/Plots/RBIN/UtilIn_Out_{}.png'.format(path,directory,file))

        
    else:
        ax = df.plot(kind='line',x=time, y=[BitsIn, BitsOut], title = 'et-8/2/0 BitsIn_Out',figsize=(10,4))
        ax1 = df.plot(kind='line',x=time, y=[BitsSecIn,BitsSecOut], title = 'et-8/2/0 BitsPerSecondIn_Out' ,figsize=(10,4))
        ax2 = df.plot(kind='line',x=time, y=[UtilIn,UtilOut],title = 'et-8/2/0 Utilization_Out' ,figsize=(10,4))    
        ax.set_ylabel("GB")
        ax1.set_ylabel("GB/s")
        ax2.set_ylabel("%")
        ax.figure.savefig('{}/PP_Output/{}/Plots/RBIN/BitsIn_Out_{}.png'.format(path,directory,file))
        ax1.figure.savefig('{}/PP_Output/{}/Plots/RBIN/BitsSecIn_Out_{}.png'.format(path,directory,file))
        ax2.figure.savefig('{}/PP_Output/{}/Plots/RBIN/UtilIn_Out_{}.png'.format(path,directory,file))
       
    return stats


# In[30]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
Files = ['RBIN_0', 'RBIN_1']
for i in Dirs:
    for j in Files: 
        RBIN('{}'.format(i), '{}'.format(j))


# In[26]:


def RBINtimes(directory, file):
    directory = str(directory)
    file = str(file)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/RBIN'.format(directory)
    #my_path = os.path.abspath(__file__)
    #print(os.path.join(path + path2,"{}.json".format(file)))
    df = pd.read_json(os.path.join(path + path2, "{}.json".format(file)))
    ID, time, BitsIn, BitsOut, BitsSecIn, BitsSecOut, UtilIn, UtilOut = df.columns
    df[time] = pd.to_datetime(df[time],unit='s')
    cols = df.columns.drop([ID,time,UtilIn,UtilOut])
    df[cols] = df[cols]* (1.25e-10)
    df = df[0:12]
    print(df)


# In[27]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
Files = ['RBIN_0', 'RBIN_1']
for i in Dirs:
    for j in Files: 
        print(i,j)
        RBINtimes('{}'.format(i), '{}'.format(j))


# In[ ]:





# In[ ]:




