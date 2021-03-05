#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[9]:


#RBIN
#0: et-8/0/0
#1: et-8/2/0
def Collation_RBIN(metric, directory):
    metric = str(metric)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    mycsvdir = '{}/PP_Output/{}/Stats/{}/dCache'.format(path, directory, metric)
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
    csvfiles = sorted(csvfiles)
    print("Check the order of the files")
    print(csvfiles)
    dataframes = []  # a list to hold all the individual pandas DataFrames
    for csvfile in csvfiles:
        df = pd.read_csv(csvfile)
        dataframes.append(df)
        
    result = pd.concat(dataframes, ignore_index=True)
    DATA = pd.DataFrame(data = result)
    DATA = DATA.round(3)
    #print(DATA)
    df_count = DATA[DATA.index % 8 == 0]
    df_mean = DATA[DATA.index % 8 == 1]
    df_std = DATA[DATA.index % 8 == 2]
    df_min = DATA[DATA.index % 8 == 3]
    df_pt_25 =  DATA[DATA.index % 8 == 4]
    df_pt_50 =  DATA[DATA.index % 8 == 5]
    df_pt_75 =  DATA[DATA.index % 8 == 6]
    df_max =  DATA[DATA.index % 8 == 7]
    
    dfs = [df_count, df_mean, df_std, df_min, df_pt_25, df_pt_50, df_pt_75, df_max]
    for df in dfs:
        df.rename(columns={'Unnamed: 0':'Metric'}, inplace=True)
        
    def transpose(index, dataframe):
        df = dataframe.T
        df.columns = ['et-8/0/0', 'et-8/2/0']
        df.drop('Metric', axis=0, inplace=True)
        df.to_csv('{}/PP_Output/{}/Stats/{}/Metrics/{}_{}.csv'.format(path, directory,metric,metric,index), index=True)
        print(df)
    
    for index, df in enumerate(dfs):
        transpose(index,df)

#Legend for index:
#0 = count, 1 = mean, 2 = std, 3 = min, 4 = pt_25, 5 = pt_50, 6 = pt_75, 7 = max 


# In[10]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
for i in Dirs:
    print(i)
    Collation_RBIN('RBIN', '{}'.format(i))


# In[2]:


#AGLT2_CHI
#0: et-0/3/0 sw2.star.omnipop.btaa.org
#1: et-3/1/0 sw2.star.omnipop.btaa.org
#2: et-1/3/0 sw2.600wchicag.omnipop.btaa.org
#3: et-5/0/0 sw2.600wchicag.omnipop.btaa.org
#4: et-0/1/0 sw2.600wchicag.omnipop.btaa.org
#5: et-2/1/0 sw2.600wchicag.omnipop.btaa.org

def Collation_AGLT2CHI(metric, directory):
    metric = str(metric)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    mycsvdir = '{}/PP_Output/{}/Stats/{}/dCache'.format(path, directory, metric)
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
    csvfiles = sorted(csvfiles)
    print("Check the order of the files")
    print(csvfiles)
    
    #loop through the files and read them in with pandas
    dataframes = []  # a list to hold all the individual pandas DataFrames
    for csvfile in csvfiles:
        df = pd.read_csv(csvfile)
        dataframes.append(df)
        
    result = pd.concat(dataframes, ignore_index=True)
    DATA = pd.DataFrame(data = result)
    DATA = DATA.round(3)
    #print(DATA)
    df_count = DATA[DATA.index % 8 == 0]
    df_mean = DATA[DATA.index % 8 == 1]
    df_std = DATA[DATA.index % 8 == 2]
    df_min = DATA[DATA.index % 8 == 3]
    df_pt_25 =  DATA[DATA.index % 8 == 4]
    df_pt_50 =  DATA[DATA.index % 8 == 5]
    df_pt_75 =  DATA[DATA.index % 8 == 6]
    df_max =  DATA[DATA.index % 8 == 7]
    
    dfs = [df_count, df_mean, df_std, df_min, df_pt_25, df_pt_50, df_pt_75, df_max]
    for df in dfs:
        df.rename(columns={'Unnamed: 0':'Metric'}, inplace=True)

    def transpose(index, dataframe):
        df = dataframe.T
        df.columns = ['et-0/3/0', 'et-3/1/0', 'et-1/3/0', 'et-5/0/0', 'et-0/1/0', 'et-2/1/0']
        df.drop('Metric', axis=0, inplace=True)
        df.to_csv('{}/PP_Output/{}/Stats/{}/Metrics/{}_{}.csv'.format(path, directory,metric,metric,index), index=True)
        #print(df)
    
    for index, df in enumerate(dfs):
        transpose(index,df)
        
#Legend for index:
#0 = count, 1 = mean, 2 = std, 3 = min, 4 = pt_25, 5 = pt_50, 6 = pt_75, 7 = max 


# In[15]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
for i in Dirs:
    print(i)
    Collation_AGLT2CHI('AGLT2_CHI', '{}'.format(i))


# In[3]:


def Collation_AGLT2(metric, directory):
    metric = str(metric)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    mycsvdir = '{}/PP_Output/{}/Stats/AGLT2/{}/dCache'.format(path, directory, metric)
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
    csvfiles = sorted(csvfiles)
    print("Check the order of the files")
    print(csvfiles)
    #loop through the files and read them in with pandas
    dataframes = []  # a list to hold all the individual pandas DataFrames
    for csvfile in csvfiles:
        df = pd.read_csv(csvfile)
        dataframes.append(df)
            
    result = pd.concat(dataframes, ignore_index=True)
    DATA = pd.DataFrame(data = result)
    DATA = DATA.round(3)
    #print(DATA)
    #extracting the first column of the DATA dataframe into these smaller dataframes
    df_count = DATA[DATA.index % 8 == 0]
    df_mean = DATA[DATA.index % 8 == 1]
    df_std = DATA[DATA.index % 8 == 2]
    df_min = DATA[DATA.index % 8 == 3]
    df_pt_25 =  DATA[DATA.index % 8 == 4]
    df_pt_50 =  DATA[DATA.index % 8 == 5]
    df_pt_75 =  DATA[DATA.index % 8 == 6]
    df_max =  DATA[DATA.index % 8 == 7]
    
    dfs = [df_count, df_mean, df_std, df_min, df_pt_25, df_pt_50, df_pt_75, df_max]
    for df in dfs:
    #df.round(3)
        df.rename(columns={'Unnamed: 0':'Metric'}, inplace=True)
    #print(df_count)
    
    def transpose(index, dataframe):
        df = dataframe.T
        df.columns = ['umfs06','umfs09', 'umfs11', 'umfs16', 'umfs19', 'umfs20', 'umfs21', 'umfs22',                      'umfs23', 'umfs24', 'umfs25','umfs26', 'umfs27', 'umfs28']
        #df.columns = ['umfs06', 'umfs09', 'umfs19', 'umfs20',  'umfs21', 'umfs22', 'umfs23', 'umfs24', \
                      #'umfs26', 'umfs27', 'umfs28']
        #df.drop('Host', axis=0)
        df.to_csv('{}/PP_Output/{}/Stats/AGLT2/{}/Metrics/{}_{}.csv'.format(path,directory,metric,metric,index), index=True)
    
    for index, df in enumerate(dfs):
        transpose(index,df)


# In[24]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs: 
    Collation_AGLT2('CPU_load', '{}'.format(i))


# In[3]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs: 
    Collation_AGLT2('CPU_utilization', '{}'.format(i))


# In[4]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs: 
    Collation_AGLT2('DiskIO', '{}'.format(i))


# In[7]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs: 
    Collation_AGLT2('Memory', '{}'.format(i))


# In[ ]:




