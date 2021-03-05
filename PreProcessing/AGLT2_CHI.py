#!/usr/bin/env python
# coding: utf-8

# In[12]:


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


# In[140]:


def AGLT2CHI(directory, file):
    directory = str(directory)
    file = str(file)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2_CHI'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "{}.json".format(file)))
    results = df["results"][0]
    df_results = pd.DataFrame(data=results)
    df_results.columns = ['input','output','intf', 'node']
    intf = df_results['intf'][0]
    node = df_results['node'][0]
    time = []
    inputval = []
    outputval = []
    for i in range(64):
        #print(i, df_results["input"][i][0], df_results["input"][i][1], df_results["output"][i][1])
        time.append(df_results["input"][i][0])
        inputval.append(df_results["input"][i][1])
        outputval.append(df_results["output"][i][1])
        
    list_of_tuples = list(zip(time, inputval, outputval))
    df_finres = pd.DataFrame(data = list_of_tuples,columns=['Timestamp','Input','Output'])
    df_finres['Timestamp'] = pd.to_datetime(df_finres["Timestamp"],unit='s')
    
    if directory == 'Output_20210201_1140':
        totaltime = df_finres["Timestamp"][5:65]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])
  
        input_DATA = df_finres["Input"][5:65]
        output_DATA = df_finres["Output"][5:65]

        input_split = np.array_split(input_DATA,12)
        output_split = np.array_split(output_DATA,12)
        inputtotal = []
        outputtotal = []

        for (inputarr, outputarr) in zip(input_split, output_split):
            inputtotal.append(list(inputarr)[0])
            outputtotal.append(list(outputarr)[0])

        list_data = list(zip(totaltime, inputtotal, outputtotal))
        df_data = pd.DataFrame(data=list_data, columns=['Timestamp', 'Input','Output'])
        cols = df_data.columns.drop('Timestamp')
        df_data[cols] = df_data[cols] *(1.25e-10)
        stats = df_data[['Input', 'Output']].describe()
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2_CHI'.format(directory), "Stats_{}.csv".format(file)),                    index=True)
        ax = df_data.plot(kind='line',x='Timestamp', y=['Input', 'Output'], title = '{} {}'.format(intf,node),figsize=(10,4))
        ax.set_ylabel("GB")
        ax.figure.savefig('{}/PP_Output/{}/Plots/AGLT2_CHI/IO_{}.png'.format(path, directory,file))
        return None
    
    if directory == 'Output_20210201_1338':
        totaltime = df_finres["Timestamp"][2:62]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])
  
        input_DATA = df_finres["Input"][2:62]
        output_DATA = df_finres["Output"][2:62]

        input_split = np.array_split(input_DATA,12)
        output_split = np.array_split(output_DATA,12)
        inputtotal = []
        outputtotal = []

        for (inputarr, outputarr) in zip(input_split, output_split):
            inputtotal.append(list(inputarr)[0])
            outputtotal.append(list(outputarr)[0])

        list_data = list(zip(totaltime, inputtotal, outputtotal))
        df_data = pd.DataFrame(data=list_data, columns=['Timestamp', 'Input','Output'])
        cols = df_data.columns.drop('Timestamp')
        df_data[cols] = df_data[cols] *(1.25e-10)
        stats = df_data[['Input', 'Output']].describe()
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2_CHI'.format(directory), "Stats_{}.csv".format(file)),                    index=True)
        ax = df_data.plot(kind='line',x='Timestamp', y=['Input', 'Output'], title = '{} {}'.format(intf,node),figsize=(10,4))
        ax.set_ylabel("GB")
        ax.figure.savefig('{}/PP_Output/{}/Plots/AGLT2_CHI/IO_{}.png'.format(path, directory,file))
        return None
    
    if directory == 'Output_20210201_1602':
        totaltime = df_finres["Timestamp"][3:63]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])
  
        input_DATA = df_finres["Input"][3:63]
        output_DATA = df_finres["Output"][3:63]

        input_split = np.array_split(input_DATA,12)
        output_split = np.array_split(output_DATA,12)
        inputtotal = []
        outputtotal = []

        for (inputarr, outputarr) in zip(input_split, output_split):
            inputtotal.append(list(inputarr)[0])
            outputtotal.append(list(outputarr)[0])

        list_data = list(zip(totaltime, inputtotal, outputtotal))
        df_data = pd.DataFrame(data=list_data, columns=['Timestamp', 'Input','Output'])
        cols = df_data.columns.drop('Timestamp')
        df_data[cols] = df_data[cols] *(1.25e-10)
        stats = df_data[['Input', 'Output']].describe()
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2_CHI'.format(directory), "Stats_{}.csv".format(file)),                    index=True)
        ax = df_data.plot(kind='line',x='Timestamp', y=['Input', 'Output'], title = '{} {}'.format(intf,node),figsize=(10,4))
        ax.set_ylabel("GB")
        ax.figure.savefig('{}/PP_Output/{}/Plots/AGLT2_CHI/IO_{}.png'.format(path, directory,file))
        return None
    
    if directory == 'Output_20210201_1741':
        totaltime = df_finres["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])
  
        input_DATA = df_finres["Input"][4:64]
        output_DATA = df_finres["Output"][4:64]

        input_split = np.array_split(input_DATA,12)
        output_split = np.array_split(output_DATA,12)
        inputtotal = []
        outputtotal = []

        for (inputarr, outputarr) in zip(input_split, output_split):
            inputtotal.append(list(inputarr)[0])
            outputtotal.append(list(outputarr)[0])

        list_data = list(zip(totaltime, inputtotal, outputtotal))
        df_data = pd.DataFrame(data=list_data, columns=['Timestamp', 'Input','Output'])
        cols = df_data.columns.drop('Timestamp')
        df_data[cols] = df_data[cols] *(1.25e-10)
        stats = df_data[['Input', 'Output']].describe()
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2_CHI'.format(directory), "Stats_{}.csv".format(file)),                    index=True)
        ax = df_data.plot(kind='line',x='Timestamp', y=['Input', 'Output'], title = '{} {}'.format(intf,node),figsize=(10,4))
        ax.set_ylabel("GB")
        ax.figure.savefig('{}/PP_Output/{}/Plots/AGLT2_CHI/IO_{}.png'.format(path, directory,file))
        return None
        
    if directory == 'Output_20210201_1915':
        totaltime = df_finres["Timestamp"][5:65]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])
  
        input_DATA = df_finres["Input"][5:65]
        output_DATA = df_finres["Output"][5:65]

        input_split = np.array_split(input_DATA,12)
        output_split = np.array_split(output_DATA,12)
        inputtotal = []
        outputtotal = []

        for (inputarr, outputarr) in zip(input_split, output_split):
            inputtotal.append(list(inputarr)[0])
            outputtotal.append(list(outputarr)[0])

        list_data = list(zip(totaltime, inputtotal, outputtotal))
        df_data = pd.DataFrame(data=list_data, columns=['Timestamp', 'Input','Output'])
        cols = df_data.columns.drop('Timestamp')
        df_data[cols] = df_data[cols] *(1.25e-10)
        stats = df_data[['Input', 'Output']].describe()
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2_CHI'.format(directory), "Stats_{}.csv".format(file)),                    index=True)
        ax = df_data.plot(kind='line',x='Timestamp', y=['Input', 'Output'], title = '{} {}'.format(intf,node),figsize=(10,4))
        ax.set_ylabel("GB")
        ax.figure.savefig('{}/PP_Output/{}/Plots/AGLT2_CHI/IO_{}.png'.format(path, directory,file))
        return None


# In[141]:


Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
Files = ['AGLT2_CHI_0', 'AGLT2_CHI_1', 'AGLT2_CHI_2', 'AGLT2_CHI_3', 'AGLT2_CHI_4', 'AGLT2_CHI_5']
for i in Dirs:
    for j in Files: 
        AGLT2CHI('{}'.format(i), '{}'.format(j))


# In[113]:


AGLT2CHI('Output_20210201_1140', 'AGLT2_CHI_0')


# In[138]:


def AGLT2CHItime(directory, file):
    directory = str(directory)
    file = str(file)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2_CHI'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "{}.json".format(file)))
    results = df["results"][0]
    df_results = pd.DataFrame(data=results)
    df_results.columns = ['input','output','intf', 'node']
    intf = df_results['intf'][0]
    node = df_results['node'][0]
    time = []
    inputval = []
    outputval = []
    for i in range(64):
        #print(i, df_results["input"][i][0], df_results["input"][i][1], df_results["output"][i][1])
        time.append(df_results["input"][i][0])
        inputval.append(df_results["input"][i][1])
        outputval.append(df_results["output"][i][1])
    
    list_of_tuples = list(zip(time, inputval, outputval))
    df_finres = pd.DataFrame(data = list_of_tuples,columns=['Timestamp','Input','Output'])
    #df_finres['Timestamp'] = pd.to_datetime(df_finres["Timestamp"],unit='s')
    
    #totaltime = df_finres["Timestamp"][5:65]
    #totaltime = df_finres["Timestamp"][2:62]
    #totaltime = df_finres["Timestamp"][3:63]
    #totaltime = df_finres["Timestamp"][4:64]
    #totaltime = df_finres["Timestamp"][5:65]
    timesplit = np.array_split(totaltime,12)
    totaltime = []
    for times in timesplit:
        print(list(times))


# In[139]:


#Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
Dirs = ['Output_20210201_1915']
Files = ['AGLT2_CHI_0']
for i in Dirs:
    for j in Files: 
        print(i,j)
        AGLT2CHItime('{}'.format(i), '{}'.format(j))


# In[ ]:





# In[ ]:




