#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[41]:


def Load(host, directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_CPU_load_{}.json".format(host)))
    start = df["meta"]["start"]
    end = df["meta"]["end"]
    #print('start', start)
    #print('end', end)
    LEG = df["meta"]["legend"]
    DATA = df["data"]["row"]
    DATA = pd.DataFrame(data = DATA)
    LEG = pd.DataFrame(data = LEG)
    
    if directory == 'Output_20210201_1140':
        timestamps = []
        for i in range(64):
            start = int(start)
            start = start + 60
            timestamps.append(start)

        timestamps = np.array(timestamps)
        values = []
        for i in range(64):
            #print(DATA.iloc[i,0])
            values.append(DATA.iloc[i,0])
        values = np.array(values)
        df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
        df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                             'load15_MIN','load15_MAX','load15_AVERAGE']
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')

        #slicing the dataframe
        totaltime = df_values["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        load1_DATA = df_values["load1_MIN"][4:64]
        load5_DATA = df_values["load5_MIN"][4:64]
        load15_DATA = df_values["load15_MIN"][4:64]

        load1_split = np.array_split(load1_DATA,12)
        load5_split = np.array_split(load5_DATA,12)
        load15_split = np.array_split(load15_DATA,12)

        load1_min = []
        load1_max = []
        load1_ave = []
        load5_min = []
        load5_max = []
        load5_ave = []
        load15_min = []
        load15_max = []
        load15_ave = []

        for (load1_array,load5_array, load15_array) in zip(load1_split, load5_split, load15_split):
            load1_min.append(min(load1_array))
            load1_max.append(max(load1_array))
            load1_ave.append(np.mean(load1_array))
            load5_min.append(min(load5_array))
            load5_max.append(max(load5_array))
            load5_ave.append(np.mean(load5_array))
            load15_min.append(min(load15_array))
            load15_max.append(max(load15_array))
            load15_ave.append(np.mean(load15_array))

        list_load1 = list(zip(totaltime, load1_min, load1_max, load1_ave))
        list_load5 = list(zip(totaltime, load5_min, load5_max, load5_ave))
        list_load15 = list(zip(totaltime, load15_min, load15_max, load15_ave))

        df_load1 = pd.DataFrame(data=list_load1, columns=['Timestamp', 'load1_MIN','load1_MAX', 'load1_AVERAGE'])
        print(df_load1)
        df_load1['Timestamp'] = pd.to_datetime(df_load1["Timestamp"],unit='s')
        df_load5 = pd.DataFrame(data=list_load5, columns=['Timestamp', 'load5_MIN','load5_MAX', 'load5_AVERAGE'])
        df_load5['Timestamp'] = pd.to_datetime(df_load5["Timestamp"],unit='s')
        df_load15 = pd.DataFrame(data=list_load15, columns=['Timestamp', 'load15_MIN','load15_MAX', 'load15_AVERAGE'])
        df_load15['Timestamp'] = pd.to_datetime(df_load15["Timestamp"],unit='s')

        plot_load1 = df_load1.plot(kind='line',x='Timestamp', y=['load1_MIN','load1_MAX', 'load1_AVERAGE'],                                   title = 'Load1 {}'.format(host), figsize=(10,4))
        plot_load5 = df_load5.plot(kind='line',x='Timestamp', y=['load5_MIN','load5_MAX', 'load5_AVERAGE'],                                    title = 'Load5 {}'.format(host), figsize=(10,4))
        plot_load15 = df_load15.plot(kind='line',x='Timestamp', y=['load15_MIN','load15_MAX', 'load15_AVERAGE'],                                      title = 'Load15 {}'.format(host) , figsize=(10,4))

        stats_load1 = df_load1[['load1_MIN','load1_MAX', 'load1_AVERAGE']].describe()
        stats_load5 = df_load5[['load5_MIN','load5_MAX', 'load5_AVERAGE']].describe()
        stats_load15 = df_load15[['load15_MIN','load15_MAX', 'load15_AVERAGE']].describe()


        load1 = pd.DataFrame(stats_load1)
        load5 = pd.DataFrame(stats_load5)
        load15 = pd.DataFrame(stats_load15)

        stats = pd.concat([load1, load5, load15], axis=1)

        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2'.format(directory), "Stats_CPU_load_{}.csv".format(host)), index=True)

        plot_load1.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load1_{}.png'.format(path, directory, host))
        plot_load5.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load5_{}.png'.format(path, directory, host))
        plot_load15.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load15_{}.png'.format(path, directory, host))
        return None
    
    if directory == 'Output_20210201_1338':
        timestamps = []
        for i in range(75):
            start = int(start)
            start = start + 60
            timestamps.append(start)

        timestamps = np.array(timestamps)
        values = []
        for i in range(75):
            #print(DATA.iloc[i,0])
            values.append(DATA.iloc[i,0])
        values = np.array(values)
        df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
        df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                             'load15_MIN','load15_MAX','load15_AVERAGE']
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')

        #slicing the dataframe
        totaltime = df_values["Timestamp"][1:61]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        load1_DATA = df_values["load1_MIN"][1:61]
        load5_DATA = df_values["load5_MIN"][1:61]
        load15_DATA = df_values["load15_MIN"][1:61]

        load1_split = np.array_split(load1_DATA,12)
        load5_split = np.array_split(load5_DATA,12)
        load15_split = np.array_split(load15_DATA,12)

        load1_min = []
        load1_max = []
        load1_ave = []
        load5_min = []
        load5_max = []
        load5_ave = []
        load15_min = []
        load15_max = []
        load15_ave = []

        for (load1_array,load5_array, load15_array) in zip(load1_split, load5_split, load15_split):
            load1_min.append(min(load1_array))
            load1_max.append(max(load1_array))
            load1_ave.append(np.mean(load1_array))
            load5_min.append(min(load5_array))
            load5_max.append(max(load5_array))
            load5_ave.append(np.mean(load5_array))
            load15_min.append(min(load15_array))
            load15_max.append(max(load15_array))
            load15_ave.append(np.mean(load15_array))

        list_load1 = list(zip(totaltime, load1_min, load1_max, load1_ave))
        list_load5 = list(zip(totaltime, load5_min, load5_max, load5_ave))
        list_load15 = list(zip(totaltime, load15_min, load15_max, load15_ave))

        df_load1 = pd.DataFrame(data=list_load1, columns=['Timestamp', 'load1_MIN','load1_MAX', 'load1_AVERAGE'])
        df_load1['Timestamp'] = pd.to_datetime(df_load1["Timestamp"],unit='s')
        df_load5 = pd.DataFrame(data=list_load5, columns=['Timestamp', 'load5_MIN','load5_MAX', 'load5_AVERAGE'])
        df_load5['Timestamp'] = pd.to_datetime(df_load5["Timestamp"],unit='s')
        df_load15 = pd.DataFrame(data=list_load15, columns=['Timestamp', 'load15_MIN','load15_MAX', 'load15_AVERAGE'])
        df_load15['Timestamp'] = pd.to_datetime(df_load15["Timestamp"],unit='s')

        plot_load1 = df_load1.plot(kind='line',x='Timestamp', y=['load1_MIN','load1_MAX', 'load1_AVERAGE'],                                   title = 'Load1 {}'.format(host), figsize=(10,4))
        plot_load5 = df_load5.plot(kind='line',x='Timestamp', y=['load5_MIN','load5_MAX', 'load5_AVERAGE'],                                    title = 'Load5 {}'.format(host), figsize=(10,4))
        plot_load15 = df_load15.plot(kind='line',x='Timestamp', y=['load15_MIN','load15_MAX', 'load15_AVERAGE'],                                      title = 'Load15 {}'.format(host) , figsize=(10,4))

        stats_load1 = df_load1[['load1_MIN','load1_MAX', 'load1_AVERAGE']].describe()
        stats_load5 = df_load5[['load5_MIN','load5_MAX', 'load5_AVERAGE']].describe()
        stats_load15 = df_load15[['load15_MIN','load15_MAX', 'load15_AVERAGE']].describe()


        load1 = pd.DataFrame(stats_load1)
        load5 = pd.DataFrame(stats_load5)
        load15 = pd.DataFrame(stats_load15)

        stats = pd.concat([load1, load5, load15], axis=1)

        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2'.format(directory), "Stats_CPU_load_{}.csv".format(host)), index=True)

        plot_load1.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load1_{}.png'.format(path, directory, host))
        plot_load5.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load5_{}.png'.format(path, directory, host))
        plot_load15.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load15_{}.png'.format(path, directory, host))
        return None
    
    if directory == 'Output_20210201_1602':
        timestamps = []
        for i in range(75):
            start = int(start)
            start = start + 60
            timestamps.append(start)

        timestamps = np.array(timestamps)
        values = []
        for i in range(75):
            #print(DATA.iloc[i,0])
            values.append(DATA.iloc[i,0])
        values = np.array(values)
        df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
        df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                             'load15_MIN','load15_MAX','load15_AVERAGE']
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')

        #slicing the dataframe
        totaltime = df_values["Timestamp"][2:62]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        load1_DATA = df_values["load1_MIN"][2:62]
        load5_DATA = df_values["load5_MIN"][2:62]
        load15_DATA = df_values["load15_MIN"][2:62]

        load1_split = np.array_split(load1_DATA,12)
        load5_split = np.array_split(load5_DATA,12)
        load15_split = np.array_split(load15_DATA,12)

        load1_min = []
        load1_max = []
        load1_ave = []
        load5_min = []
        load5_max = []
        load5_ave = []
        load15_min = []
        load15_max = []
        load15_ave = []

        for (load1_array,load5_array, load15_array) in zip(load1_split, load5_split, load15_split):
            load1_min.append(min(load1_array))
            load1_max.append(max(load1_array))
            load1_ave.append(np.mean(load1_array))
            load5_min.append(min(load5_array))
            load5_max.append(max(load5_array))
            load5_ave.append(np.mean(load5_array))
            load15_min.append(min(load15_array))
            load15_max.append(max(load15_array))
            load15_ave.append(np.mean(load15_array))

        list_load1 = list(zip(totaltime, load1_min, load1_max, load1_ave))
        list_load5 = list(zip(totaltime, load5_min, load5_max, load5_ave))
        list_load15 = list(zip(totaltime, load15_min, load15_max, load15_ave))

        df_load1 = pd.DataFrame(data=list_load1, columns=['Timestamp', 'load1_MIN','load1_MAX', 'load1_AVERAGE'])
        df_load1['Timestamp'] = pd.to_datetime(df_load1["Timestamp"],unit='s')
        df_load5 = pd.DataFrame(data=list_load5, columns=['Timestamp', 'load5_MIN','load5_MAX', 'load5_AVERAGE'])
        df_load5['Timestamp'] = pd.to_datetime(df_load5["Timestamp"],unit='s')
        df_load15 = pd.DataFrame(data=list_load15, columns=['Timestamp', 'load15_MIN','load15_MAX', 'load15_AVERAGE'])
        df_load15['Timestamp'] = pd.to_datetime(df_load15["Timestamp"],unit='s')

        plot_load1 = df_load1.plot(kind='line',x='Timestamp', y=['load1_MIN','load1_MAX', 'load1_AVERAGE'],                                   title = 'Load1 {}'.format(host), figsize=(10,4))
        plot_load5 = df_load5.plot(kind='line',x='Timestamp', y=['load5_MIN','load5_MAX', 'load5_AVERAGE'],                                    title = 'Load5 {}'.format(host), figsize=(10,4))
        plot_load15 = df_load15.plot(kind='line',x='Timestamp', y=['load15_MIN','load15_MAX', 'load15_AVERAGE'],                                      title = 'Load15 {}'.format(host) , figsize=(10,4))

        stats_load1 = df_load1[['load1_MIN','load1_MAX', 'load1_AVERAGE']].describe()
        stats_load5 = df_load5[['load5_MIN','load5_MAX', 'load5_AVERAGE']].describe()
        stats_load15 = df_load15[['load15_MIN','load15_MAX', 'load15_AVERAGE']].describe()


        load1 = pd.DataFrame(stats_load1)
        load5 = pd.DataFrame(stats_load5)
        load15 = pd.DataFrame(stats_load15)

        stats = pd.concat([load1, load5, load15], axis=1)

        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2'.format(directory), "Stats_CPU_load_{}.csv".format(host)), index=True)

        plot_load1.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load1_{}.png'.format(path, directory, host))
        plot_load5.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load5_{}.png'.format(path, directory, host))
        plot_load15.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load15_{}.png'.format(path, directory, host))
        return None
    
    if directory == 'Output_20210201_1741':
        timestamps = []
        for i in range(75):
            start = int(start)
            start = start + 60
            timestamps.append(start)

        timestamps = np.array(timestamps)
        values = []
        for i in range(75):
            #print(DATA.iloc[i,0])
            values.append(DATA.iloc[i,0])
        values = np.array(values)
        df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
        df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                             'load15_MIN','load15_MAX','load15_AVERAGE']
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')

        #slicing the dataframe
        totaltime = df_values["Timestamp"][3:63]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        load1_DATA = df_values["load1_MIN"][3:63]
        load5_DATA = df_values["load5_MIN"][3:63]
        load15_DATA = df_values["load15_MIN"][3:63]

        load1_split = np.array_split(load1_DATA,12)
        load5_split = np.array_split(load5_DATA,12)
        load15_split = np.array_split(load15_DATA,12)

        load1_min = []
        load1_max = []
        load1_ave = []
        load5_min = []
        load5_max = []
        load5_ave = []
        load15_min = []
        load15_max = []
        load15_ave = []

        for (load1_array,load5_array, load15_array) in zip(load1_split, load5_split, load15_split):
            load1_min.append(min(load1_array))
            load1_max.append(max(load1_array))
            load1_ave.append(np.mean(load1_array))
            load5_min.append(min(load5_array))
            load5_max.append(max(load5_array))
            load5_ave.append(np.mean(load5_array))
            load15_min.append(min(load15_array))
            load15_max.append(max(load15_array))
            load15_ave.append(np.mean(load15_array))

        list_load1 = list(zip(totaltime, load1_min, load1_max, load1_ave))
        list_load5 = list(zip(totaltime, load5_min, load5_max, load5_ave))
        list_load15 = list(zip(totaltime, load15_min, load15_max, load15_ave))

        df_load1 = pd.DataFrame(data=list_load1, columns=['Timestamp', 'load1_MIN','load1_MAX', 'load1_AVERAGE'])
        df_load1['Timestamp'] = pd.to_datetime(df_load1["Timestamp"],unit='s')
        df_load5 = pd.DataFrame(data=list_load5, columns=['Timestamp', 'load5_MIN','load5_MAX', 'load5_AVERAGE'])
        df_load5['Timestamp'] = pd.to_datetime(df_load5["Timestamp"],unit='s')
        df_load15 = pd.DataFrame(data=list_load15, columns=['Timestamp', 'load15_MIN','load15_MAX', 'load15_AVERAGE'])
        df_load15['Timestamp'] = pd.to_datetime(df_load15["Timestamp"],unit='s')

        plot_load1 = df_load1.plot(kind='line',x='Timestamp', y=['load1_MIN','load1_MAX', 'load1_AVERAGE'],                                   title = 'Load1 {}'.format(host), figsize=(10,4))
        plot_load5 = df_load5.plot(kind='line',x='Timestamp', y=['load5_MIN','load5_MAX', 'load5_AVERAGE'],                                    title = 'Load5 {}'.format(host), figsize=(10,4))
        plot_load15 = df_load15.plot(kind='line',x='Timestamp', y=['load15_MIN','load15_MAX', 'load15_AVERAGE'],                                      title = 'Load15 {}'.format(host) , figsize=(10,4))

        stats_load1 = df_load1[['load1_MIN','load1_MAX', 'load1_AVERAGE']].describe()
        stats_load5 = df_load5[['load5_MIN','load5_MAX', 'load5_AVERAGE']].describe()
        stats_load15 = df_load15[['load15_MIN','load15_MAX', 'load15_AVERAGE']].describe()


        load1 = pd.DataFrame(stats_load1)
        load5 = pd.DataFrame(stats_load5)
        load15 = pd.DataFrame(stats_load15)

        stats = pd.concat([load1, load5, load15], axis=1)

        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2'.format(directory), "Stats_CPU_load_{}.csv".format(host)), index=True)

        plot_load1.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load1_{}.png'.format(path, directory, host))
        plot_load5.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load5_{}.png'.format(path, directory, host))
        plot_load15.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load15_{}.png'.format(path, directory, host))
        return None
    
    if directory == 'Output_20210201_1915':
        timestamps = []
        for i in range(68):
            start = int(start)
            start = start + 60
            timestamps.append(start)

        timestamps = np.array(timestamps)
        values = []
        for i in range(68):
            #print(DATA.iloc[i,0])
            values.append(DATA.iloc[i,0])
        values = np.array(values)
        df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
        df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                             'load15_MIN','load15_MAX','load15_AVERAGE']
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')

        #slicing the dataframe
        totaltime = df_values["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        load1_DATA = df_values["load1_MIN"][4:64]
        load5_DATA = df_values["load5_MIN"][4:64]
        load15_DATA = df_values["load15_MIN"][4:64]

        load1_split = np.array_split(load1_DATA,12)
        load5_split = np.array_split(load5_DATA,12)
        load15_split = np.array_split(load15_DATA,12)

        load1_min = []
        load1_max = []
        load1_ave = []
        load5_min = []
        load5_max = []
        load5_ave = []
        load15_min = []
        load15_max = []
        load15_ave = []

        for (load1_array,load5_array, load15_array) in zip(load1_split, load5_split, load15_split):
            load1_min.append(min(load1_array))
            load1_max.append(max(load1_array))
            load1_ave.append(np.mean(load1_array))
            load5_min.append(min(load5_array))
            load5_max.append(max(load5_array))
            load5_ave.append(np.mean(load5_array))
            load15_min.append(min(load15_array))
            load15_max.append(max(load15_array))
            load15_ave.append(np.mean(load15_array))

        list_load1 = list(zip(totaltime, load1_min, load1_max, load1_ave))
        list_load5 = list(zip(totaltime, load5_min, load5_max, load5_ave))
        list_load15 = list(zip(totaltime, load15_min, load15_max, load15_ave))

        df_load1 = pd.DataFrame(data=list_load1, columns=['Timestamp', 'load1_MIN','load1_MAX', 'load1_AVERAGE'])
        df_load1['Timestamp'] = pd.to_datetime(df_load1["Timestamp"],unit='s')
        df_load5 = pd.DataFrame(data=list_load5, columns=['Timestamp', 'load5_MIN','load5_MAX', 'load5_AVERAGE'])
        df_load5['Timestamp'] = pd.to_datetime(df_load5["Timestamp"],unit='s')
        df_load15 = pd.DataFrame(data=list_load15, columns=['Timestamp', 'load15_MIN','load15_MAX', 'load15_AVERAGE'])
        df_load15['Timestamp'] = pd.to_datetime(df_load15["Timestamp"],unit='s')

        plot_load1 = df_load1.plot(kind='line',x='Timestamp', y=['load1_MIN','load1_MAX', 'load1_AVERAGE'],                                   title = 'Load1 {}'.format(host), figsize=(10,4))
        plot_load5 = df_load5.plot(kind='line',x='Timestamp', y=['load5_MIN','load5_MAX', 'load5_AVERAGE'],                                    title = 'Load5 {}'.format(host), figsize=(10,4))
        plot_load15 = df_load15.plot(kind='line',x='Timestamp', y=['load15_MIN','load15_MAX', 'load15_AVERAGE'],                                      title = 'Load15 {}'.format(host) , figsize=(10,4))

        stats_load1 = df_load1[['load1_MIN','load1_MAX', 'load1_AVERAGE']].describe()
        stats_load5 = df_load5[['load5_MIN','load5_MAX', 'load5_AVERAGE']].describe()
        stats_load15 = df_load15[['load15_MIN','load15_MAX', 'load15_AVERAGE']].describe()


        load1 = pd.DataFrame(stats_load1)
        load5 = pd.DataFrame(stats_load5)
        load15 = pd.DataFrame(stats_load15)

        stats = pd.concat([load1, load5, load15], axis=1)

        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2'.format(directory), "Stats_CPU_load_{}.csv".format(host)), index=True)

        plot_load1.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load1_{}.png'.format(path, directory, host))
        plot_load5.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load5_{}.png'.format(path, directory, host))
        plot_load15.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_load/load15_{}.png'.format(path, directory, host))
        return None


# In[42]:


hosts = ['umfs06','umfs09', 'umfs11', 'umfs16', 'umfs19', 'umfs20', 'umfs21', 'umfs22', 'umfs23', 'umfs24',          'umfs25', 'umfs26', 'umfs27', 'umfs28']
Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs:
    for j in hosts:
        print(i,j)
        Load('{}'.format(j), '{}'.format(i))


# In[ ]:


#Util, DISK IO, Memory 


# In[99]:


#Output_20210201_1140
#start 1612197600
#end 1612201500
#rows: 65 
#[4:60] --> [4:64]

#Output_20210201_1338
#start 1612204680
#end 1612209180
#rows: 75
#[1:57] --> [1:61]

#Output_20210201_1602
#start 1612213320
#end 1612217820
#rows: 75 
#[2:58] --> [2:62]

#Output_20210201_1741
#start 1612219260
#end 1612223760
#rows: 75
#[3:59] --> [3:63]

#Output_20210201_1915
#start 1612224900
#end 1612228980
#rows: 68
#[4:60] --> [4:64]


# In[95]:


def Loadtime(host, directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_CPU_load_{}.json".format(host)))
    start = df["meta"]["start"]
    end = df["meta"]["end"]
    #print('start', start)
    #print('end', end)
    LEG = df["meta"]["legend"]
    DATA = df["data"]["row"]
    DATA = pd.DataFrame(data = DATA)
    LEG = pd.DataFrame(data = LEG)
    timestamps = []
    for i in range(68):
        start = int(start)
        start = start + 60
        #print(i, start)
        timestamps.append(start)
    
    timestamps = np.array(timestamps)
    values = []
    for i in range(68):
        #print(DATA.iloc[i,0])
        values.append(DATA.iloc[i,0])
    values = np.array(values)
    df_values = pd.DataFrame(np.array(values), columns=np.array(LEG))
    df_values.columns = ['load1_MIN','load1_MAX','load1_AVERAGE', 'load5_MIN','load5_MAX','load5_AVERAGE',                         'load15_MIN','load15_MAX','load15_AVERAGE']
    df_values.insert(0, "Timestamp", timestamps, True) 
    cols = df_values.columns.drop('Timestamp')
    df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
    
    #slicing the dataframe
    totaltime = df_values["Timestamp"][4:64]
    timesplit = np.array_split(totaltime,12)
    totaltime = []
    for times in timesplit:
        print(list(times))


# In[96]:


#Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741', 'Output_20210201_1915']
#for i in Dirs:
#    print(i)
Loadtime('umfs06', 'Output_20210201_1915')


# In[ ]:





# In[39]:


def Load_trial(host, directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_CPU_load_{}.json".format(host)))
    #print(df.head())
    start = df["meta"]["start"]
    end = df["meta"]["end"]
    LEG = df["meta"]["legend"]
    DATA = df["data"]["row"]
    DATA = pd.DataFrame(data = DATA)
    LEG = pd.DataFrame(data = LEG)
    #print(DATA)
    
    timestamps = []
    for i in range(64):
        start = int(start)
        start = start + 60
        timestamps.append(start)

    timestamps = np.array(timestamps)
    
    print(start,end)
    print(timestamps)


# In[40]:


Load_trial('umfs06', 'Output_20210201_1140')


# In[ ]:




