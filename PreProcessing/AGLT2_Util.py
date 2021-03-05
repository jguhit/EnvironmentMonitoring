#!/usr/bin/env python
# coding: utf-8

# In[6]:


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


# In[28]:


def Util(host,directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_CPU_utilization_{}.json".format(host)))
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
        df_values.columns = ['user_MIN', 'user_MAX', 'user_AVERAGE','system_MIN', 'system_MAX','system_AVERAGE',                         'wait_MIN', 'wait_MAX','wait_AVERAGE' , 'util_MIN', 'util_MAX', 'util_AVERAGE' ]
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

        user_DATA = df_values["user_MIN"][4:64]
        system_DATA = df_values["system_MIN"][4:64]
        wait_DATA = df_values["wait_MIN"][4:64]
        util_DATA = df_values["util_MIN"][4:64]

        user_split = np.array_split(user_DATA,12)
        system_split = np.array_split(system_DATA,12)
        wait_split = np.array_split(wait_DATA,12)
        util_split = np.array_split(util_DATA,12)

        user_min = []
        user_max = []
        user_ave = []
        system_min = []
        system_max = []
        system_ave = []
        wait_min = []
        wait_max = []
        wait_ave = []
        util_min = []
        util_max = []
        util_ave = []
        
        for (user_array,system_array, wait_array, util_array) in zip(user_split, system_split, wait_split, util_split):
            user_min.append(min(user_array))
            user_max.append(max(user_array))
            user_ave.append(np.mean(user_array))
            system_min.append(min(system_array))
            system_max.append(max(system_array))
            system_ave.append(np.mean(system_array))
            wait_min.append(min(wait_array))
            wait_max.append(max(wait_array))
            wait_ave.append(np.mean(wait_array))
            util_min.append(min(util_array))
            util_max.append(max(util_array))
            util_ave.append(np.mean(util_array))
            
        list_user = list(zip(totaltime, user_min, user_max, user_ave))
        list_system = list(zip(totaltime, system_min, system_max, system_ave))
        list_wait = list(zip(totaltime, wait_min, wait_max, wait_ave))
        list_util = list(zip(totaltime, util_min, util_max, util_ave))
        df_user = pd.DataFrame(data=list_user, columns=['Timestamp', 'user_MIN','user_MAX', 'user_AVERAGE'])
        df_user['Timestamp'] = pd.to_datetime(df_user["Timestamp"],unit='s')
        df_system = pd.DataFrame(data=list_system, columns=['Timestamp', 'system_MIN','system_MAX', 'system_AVERAGE'])
        df_system['Timestamp'] = pd.to_datetime(df_system["Timestamp"],unit='s')
        df_wait = pd.DataFrame(data=list_wait, columns=['Timestamp', 'wait_MIN','wait_MAX', 'wait_AVERAGE'])
        df_wait['Timestamp'] = pd.to_datetime(df_wait["Timestamp"],unit='s')
        df_util = pd.DataFrame(data=list_util, columns=['Timestamp', 'util_MIN','util_MAX', 'util_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        plot_user = df_user.plot(kind='line',x='Timestamp', y=['user_MIN','user_MAX', 'user_AVERAGE'], title = 'User {}'.format(host), figsize=(10,4))
        plot_system = df_system.plot(kind='line',x='Timestamp', y=['system_MIN','system_MAX', 'system_AVERAGE'],title = 'System {}'.format(host), figsize=(10,4))
        plot_wait = df_wait.plot(kind='line',x='Timestamp', y=['wait_MIN','wait_MAX', 'wait_AVERAGE'], title = 'I/O Wait {}'.format(host) , figsize=(10,4))
        plot_util = df_util.plot(kind='line',x='Timestamp', y=['util_MIN','util_MAX', 'util_AVERAGE'], title = 'CPU Utilization {}'.format(host), figsize=(10,4))
        plot_user.set_ylabel("%")
        plot_system.set_ylabel("%")
        plot_wait.set_ylabel("%")
        plot_util.set_ylabel("%")
        stats_user = df_user[['user_MIN','user_MAX', 'user_AVERAGE']].describe()
        stats_system = df_system[['system_MIN','system_MAX', 'system_AVERAGE']].describe()
        stats_wait = df_wait[['wait_MIN','wait_MAX', 'wait_AVERAGE']].describe()
        stats_util = df_util[['util_MIN','util_MAX', 'util_AVERAGE']].describe()
        
        user = pd.DataFrame(stats_user)
        system = pd.DataFrame(stats_system)
        wait = pd.DataFrame(stats_wait)
        util = pd.DataFrame(stats_util)
        stats = pd.concat([user,system, wait, util ], axis=1)
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/CPU_utilization/dCache'.format(directory), "Stats_CPU_utilization_{}.csv".format(host)), index=True)
        
        plot_user.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/User_{}.png'.format(path, directory, host))
        plot_system.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/System_{}.png'.format(path, directory, host))
        plot_wait.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Wait_{}.png'.format(path, directory, host))
        plot_util.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Util_{}.png'.format(path, directory, host))
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
        df_values.columns = ['user_MIN', 'user_MAX', 'user_AVERAGE','system_MIN', 'system_MAX','system_AVERAGE',                         'wait_MIN', 'wait_MAX','wait_AVERAGE' , 'util_MIN', 'util_MAX', 'util_AVERAGE' ]
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

        user_DATA = df_values["user_MIN"][1:61]
        system_DATA = df_values["system_MIN"][1:61]
        wait_DATA = df_values["wait_MIN"][1:61]
        util_DATA = df_values["util_MIN"][1:61]

        user_split = np.array_split(user_DATA,12)
        system_split = np.array_split(system_DATA,12)
        wait_split = np.array_split(wait_DATA,12)
        util_split = np.array_split(util_DATA,12)

        user_min = []
        user_max = []
        user_ave = []
        system_min = []
        system_max = []
        system_ave = []
        wait_min = []
        wait_max = []
        wait_ave = []
        util_min = []
        util_max = []
        util_ave = []
        
        for (user_array,system_array, wait_array, util_array) in zip(user_split, system_split, wait_split, util_split):
            user_min.append(min(user_array))
            user_max.append(max(user_array))
            user_ave.append(np.mean(user_array))
            system_min.append(min(system_array))
            system_max.append(max(system_array))
            system_ave.append(np.mean(system_array))
            wait_min.append(min(wait_array))
            wait_max.append(max(wait_array))
            wait_ave.append(np.mean(wait_array))
            util_min.append(min(util_array))
            util_max.append(max(util_array))
            util_ave.append(np.mean(util_array))
            
        list_user = list(zip(totaltime, user_min, user_max, user_ave))
        list_system = list(zip(totaltime, system_min, system_max, system_ave))
        list_wait = list(zip(totaltime, wait_min, wait_max, wait_ave))
        list_util = list(zip(totaltime, util_min, util_max, util_ave))
        df_user = pd.DataFrame(data=list_user, columns=['Timestamp', 'user_MIN','user_MAX', 'user_AVERAGE'])
        df_user['Timestamp'] = pd.to_datetime(df_user["Timestamp"],unit='s')
        df_system = pd.DataFrame(data=list_system, columns=['Timestamp', 'system_MIN','system_MAX', 'system_AVERAGE'])
        df_system['Timestamp'] = pd.to_datetime(df_system["Timestamp"],unit='s')
        df_wait = pd.DataFrame(data=list_wait, columns=['Timestamp', 'wait_MIN','wait_MAX', 'wait_AVERAGE'])
        df_wait['Timestamp'] = pd.to_datetime(df_wait["Timestamp"],unit='s')
        df_util = pd.DataFrame(data=list_util, columns=['Timestamp', 'util_MIN','util_MAX', 'util_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        plot_user = df_user.plot(kind='line',x='Timestamp', y=['user_MIN','user_MAX', 'user_AVERAGE'], title = 'User {}'.format(host), figsize=(10,4))
        plot_system = df_system.plot(kind='line',x='Timestamp', y=['system_MIN','system_MAX', 'system_AVERAGE'],title = 'System {}'.format(host), figsize=(10,4))
        plot_wait = df_wait.plot(kind='line',x='Timestamp', y=['wait_MIN','wait_MAX', 'wait_AVERAGE'], title = 'I/O Wait {}'.format(host) , figsize=(10,4))
        plot_util = df_util.plot(kind='line',x='Timestamp', y=['util_MIN','util_MAX', 'util_AVERAGE'], title = 'CPU Utilization {}'.format(host), figsize=(10,4))
        plot_user.set_ylabel("%")
        plot_system.set_ylabel("%")
        plot_wait.set_ylabel("%")
        plot_util.set_ylabel("%")
        stats_user = df_user[['user_MIN','user_MAX', 'user_AVERAGE']].describe()
        stats_system = df_system[['system_MIN','system_MAX', 'system_AVERAGE']].describe()
        stats_wait = df_wait[['wait_MIN','wait_MAX', 'wait_AVERAGE']].describe()
        stats_util = df_util[['util_MIN','util_MAX', 'util_AVERAGE']].describe()
        
        user = pd.DataFrame(stats_user)
        system = pd.DataFrame(stats_system)
        wait = pd.DataFrame(stats_wait)
        util = pd.DataFrame(stats_util)
        stats = pd.concat([user,system, wait, util ], axis=1)
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/CPU_utilization/dCache'.format(directory), "Stats_CPU_utilization_{}.csv".format(host)), index=True)
        
        plot_user.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/User_{}.png'.format(path, directory, host))
        plot_system.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/System_{}.png'.format(path, directory, host))
        plot_wait.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Wait_{}.png'.format(path, directory, host))
        plot_util.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Util_{}.png'.format(path, directory, host))
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
        df_values.columns = ['user_MIN', 'user_MAX', 'user_AVERAGE','system_MIN', 'system_MAX','system_AVERAGE',                         'wait_MIN', 'wait_MAX','wait_AVERAGE' , 'util_MIN', 'util_MAX', 'util_AVERAGE' ]
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

        user_DATA = df_values["user_MIN"][2:62]
        system_DATA = df_values["system_MIN"][2:62]
        wait_DATA = df_values["wait_MIN"][2:62]
        util_DATA = df_values["util_MIN"][2:62]

        user_split = np.array_split(user_DATA,12)
        system_split = np.array_split(system_DATA,12)
        wait_split = np.array_split(wait_DATA,12)
        util_split = np.array_split(util_DATA,12)

        user_min = []
        user_max = []
        user_ave = []
        system_min = []
        system_max = []
        system_ave = []
        wait_min = []
        wait_max = []
        wait_ave = []
        util_min = []
        util_max = []
        util_ave = []
        
        for (user_array,system_array, wait_array, util_array) in zip(user_split, system_split, wait_split, util_split):
            user_min.append(min(user_array))
            user_max.append(max(user_array))
            user_ave.append(np.mean(user_array))
            system_min.append(min(system_array))
            system_max.append(max(system_array))
            system_ave.append(np.mean(system_array))
            wait_min.append(min(wait_array))
            wait_max.append(max(wait_array))
            wait_ave.append(np.mean(wait_array))
            util_min.append(min(util_array))
            util_max.append(max(util_array))
            util_ave.append(np.mean(util_array))
            
        list_user = list(zip(totaltime, user_min, user_max, user_ave))
        list_system = list(zip(totaltime, system_min, system_max, system_ave))
        list_wait = list(zip(totaltime, wait_min, wait_max, wait_ave))
        list_util = list(zip(totaltime, util_min, util_max, util_ave))
        df_user = pd.DataFrame(data=list_user, columns=['Timestamp', 'user_MIN','user_MAX', 'user_AVERAGE'])
        df_user['Timestamp'] = pd.to_datetime(df_user["Timestamp"],unit='s')
        df_system = pd.DataFrame(data=list_system, columns=['Timestamp', 'system_MIN','system_MAX', 'system_AVERAGE'])
        df_system['Timestamp'] = pd.to_datetime(df_system["Timestamp"],unit='s')
        df_wait = pd.DataFrame(data=list_wait, columns=['Timestamp', 'wait_MIN','wait_MAX', 'wait_AVERAGE'])
        df_wait['Timestamp'] = pd.to_datetime(df_wait["Timestamp"],unit='s')
        df_util = pd.DataFrame(data=list_util, columns=['Timestamp', 'util_MIN','util_MAX', 'util_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        plot_user = df_user.plot(kind='line',x='Timestamp', y=['user_MIN','user_MAX', 'user_AVERAGE'], title = 'User {}'.format(host), figsize=(10,4))
        plot_system = df_system.plot(kind='line',x='Timestamp', y=['system_MIN','system_MAX', 'system_AVERAGE'],title = 'System {}'.format(host), figsize=(10,4))
        plot_wait = df_wait.plot(kind='line',x='Timestamp', y=['wait_MIN','wait_MAX', 'wait_AVERAGE'], title = 'I/O Wait {}'.format(host) , figsize=(10,4))
        plot_util = df_util.plot(kind='line',x='Timestamp', y=['util_MIN','util_MAX', 'util_AVERAGE'], title = 'CPU Utilization {}'.format(host), figsize=(10,4))
        plot_user.set_ylabel("%")
        plot_system.set_ylabel("%")
        plot_wait.set_ylabel("%")
        plot_util.set_ylabel("%")
        stats_user = df_user[['user_MIN','user_MAX', 'user_AVERAGE']].describe()
        stats_system = df_system[['system_MIN','system_MAX', 'system_AVERAGE']].describe()
        stats_wait = df_wait[['wait_MIN','wait_MAX', 'wait_AVERAGE']].describe()
        stats_util = df_util[['util_MIN','util_MAX', 'util_AVERAGE']].describe()
        
        user = pd.DataFrame(stats_user)
        system = pd.DataFrame(stats_system)
        wait = pd.DataFrame(stats_wait)
        util = pd.DataFrame(stats_util)
        stats = pd.concat([user,system, wait, util ], axis=1)
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/CPU_utilization/dCache'.format(directory), "Stats_CPU_utilization_{}.csv".format(host)), index=True)
        
        plot_user.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/User_{}.png'.format(path, directory, host))
        plot_system.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/System_{}.png'.format(path, directory, host))
        plot_wait.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Wait_{}.png'.format(path, directory, host))
        plot_util.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Util_{}.png'.format(path, directory, host))
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
        df_values.columns = ['user_MIN', 'user_MAX', 'user_AVERAGE','system_MIN', 'system_MAX','system_AVERAGE',                         'wait_MIN', 'wait_MAX','wait_AVERAGE' , 'util_MIN', 'util_MAX', 'util_AVERAGE' ]
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

        user_DATA = df_values["user_MIN"][3:63]
        system_DATA = df_values["system_MIN"][3:63]
        wait_DATA = df_values["wait_MIN"][3:63]
        util_DATA = df_values["util_MIN"][3:63]

        user_split = np.array_split(user_DATA,12)
        system_split = np.array_split(system_DATA,12)
        wait_split = np.array_split(wait_DATA,12)
        util_split = np.array_split(util_DATA,12)

        user_min = []
        user_max = []
        user_ave = []
        system_min = []
        system_max = []
        system_ave = []
        wait_min = []
        wait_max = []
        wait_ave = []
        util_min = []
        util_max = []
        util_ave = []
        
        for (user_array,system_array, wait_array, util_array) in zip(user_split, system_split, wait_split, util_split):
            user_min.append(min(user_array))
            user_max.append(max(user_array))
            user_ave.append(np.mean(user_array))
            system_min.append(min(system_array))
            system_max.append(max(system_array))
            system_ave.append(np.mean(system_array))
            wait_min.append(min(wait_array))
            wait_max.append(max(wait_array))
            wait_ave.append(np.mean(wait_array))
            util_min.append(min(util_array))
            util_max.append(max(util_array))
            util_ave.append(np.mean(util_array))
            
        list_user = list(zip(totaltime, user_min, user_max, user_ave))
        list_system = list(zip(totaltime, system_min, system_max, system_ave))
        list_wait = list(zip(totaltime, wait_min, wait_max, wait_ave))
        list_util = list(zip(totaltime, util_min, util_max, util_ave))
        df_user = pd.DataFrame(data=list_user, columns=['Timestamp', 'user_MIN','user_MAX', 'user_AVERAGE'])
        df_user['Timestamp'] = pd.to_datetime(df_user["Timestamp"],unit='s')
        df_system = pd.DataFrame(data=list_system, columns=['Timestamp', 'system_MIN','system_MAX', 'system_AVERAGE'])
        df_system['Timestamp'] = pd.to_datetime(df_system["Timestamp"],unit='s')
        df_wait = pd.DataFrame(data=list_wait, columns=['Timestamp', 'wait_MIN','wait_MAX', 'wait_AVERAGE'])
        df_wait['Timestamp'] = pd.to_datetime(df_wait["Timestamp"],unit='s')
        df_util = pd.DataFrame(data=list_util, columns=['Timestamp', 'util_MIN','util_MAX', 'util_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        plot_user = df_user.plot(kind='line',x='Timestamp', y=['user_MIN','user_MAX', 'user_AVERAGE'], title = 'User {}'.format(host), figsize=(10,4))
        plot_system = df_system.plot(kind='line',x='Timestamp', y=['system_MIN','system_MAX', 'system_AVERAGE'],title = 'System {}'.format(host), figsize=(10,4))
        plot_wait = df_wait.plot(kind='line',x='Timestamp', y=['wait_MIN','wait_MAX', 'wait_AVERAGE'], title = 'I/O Wait {}'.format(host) , figsize=(10,4))
        plot_util = df_util.plot(kind='line',x='Timestamp', y=['util_MIN','util_MAX', 'util_AVERAGE'], title = 'CPU Utilization {}'.format(host), figsize=(10,4))
        plot_user.set_ylabel("%")
        plot_system.set_ylabel("%")
        plot_wait.set_ylabel("%")
        plot_util.set_ylabel("%")
        stats_user = df_user[['user_MIN','user_MAX', 'user_AVERAGE']].describe()
        stats_system = df_system[['system_MIN','system_MAX', 'system_AVERAGE']].describe()
        stats_wait = df_wait[['wait_MIN','wait_MAX', 'wait_AVERAGE']].describe()
        stats_util = df_util[['util_MIN','util_MAX', 'util_AVERAGE']].describe()
        
        user = pd.DataFrame(stats_user)
        system = pd.DataFrame(stats_system)
        wait = pd.DataFrame(stats_wait)
        util = pd.DataFrame(stats_util)
        stats = pd.concat([user,system, wait, util ], axis=1)
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/CPU_utilization/dCache'.format(directory), "Stats_CPU_utilization_{}.csv".format(host)), index=True)
        
        plot_user.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/User_{}.png'.format(path, directory, host))
        plot_system.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/System_{}.png'.format(path, directory, host))
        plot_wait.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Wait_{}.png'.format(path, directory, host))
        plot_util.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Util_{}.png'.format(path, directory, host))
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
        df_values.columns = ['user_MIN', 'user_MAX', 'user_AVERAGE','system_MIN', 'system_MAX','system_AVERAGE',                         'wait_MIN', 'wait_MAX','wait_AVERAGE' , 'util_MIN', 'util_MAX', 'util_AVERAGE' ]
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

        user_DATA = df_values["user_MIN"][4:64]
        system_DATA = df_values["system_MIN"][4:64]
        wait_DATA = df_values["wait_MIN"][4:64]
        util_DATA = df_values["util_MIN"][4:64]

        user_split = np.array_split(user_DATA,12)
        system_split = np.array_split(system_DATA,12)
        wait_split = np.array_split(wait_DATA,12)
        util_split = np.array_split(util_DATA,12)

        user_min = []
        user_max = []
        user_ave = []
        system_min = []
        system_max = []
        system_ave = []
        wait_min = []
        wait_max = []
        wait_ave = []
        util_min = []
        util_max = []
        util_ave = []
        
        for (user_array,system_array, wait_array, util_array) in zip(user_split, system_split, wait_split, util_split):
            user_min.append(min(user_array))
            user_max.append(max(user_array))
            user_ave.append(np.mean(user_array))
            system_min.append(min(system_array))
            system_max.append(max(system_array))
            system_ave.append(np.mean(system_array))
            wait_min.append(min(wait_array))
            wait_max.append(max(wait_array))
            wait_ave.append(np.mean(wait_array))
            util_min.append(min(util_array))
            util_max.append(max(util_array))
            util_ave.append(np.mean(util_array))
            
        list_user = list(zip(totaltime, user_min, user_max, user_ave))
        list_system = list(zip(totaltime, system_min, system_max, system_ave))
        list_wait = list(zip(totaltime, wait_min, wait_max, wait_ave))
        list_util = list(zip(totaltime, util_min, util_max, util_ave))
        df_user = pd.DataFrame(data=list_user, columns=['Timestamp', 'user_MIN','user_MAX', 'user_AVERAGE'])
        df_user['Timestamp'] = pd.to_datetime(df_user["Timestamp"],unit='s')
        df_system = pd.DataFrame(data=list_system, columns=['Timestamp', 'system_MIN','system_MAX', 'system_AVERAGE'])
        df_system['Timestamp'] = pd.to_datetime(df_system["Timestamp"],unit='s')
        df_wait = pd.DataFrame(data=list_wait, columns=['Timestamp', 'wait_MIN','wait_MAX', 'wait_AVERAGE'])
        df_wait['Timestamp'] = pd.to_datetime(df_wait["Timestamp"],unit='s')
        df_util = pd.DataFrame(data=list_util, columns=['Timestamp', 'util_MIN','util_MAX', 'util_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        plot_user = df_user.plot(kind='line',x='Timestamp', y=['user_MIN','user_MAX', 'user_AVERAGE'], title = 'User {}'.format(host), figsize=(10,4))
        plot_system = df_system.plot(kind='line',x='Timestamp', y=['system_MIN','system_MAX', 'system_AVERAGE'],title = 'System {}'.format(host), figsize=(10,4))
        plot_wait = df_wait.plot(kind='line',x='Timestamp', y=['wait_MIN','wait_MAX', 'wait_AVERAGE'], title = 'I/O Wait {}'.format(host) , figsize=(10,4))
        plot_util = df_util.plot(kind='line',x='Timestamp', y=['util_MIN','util_MAX', 'util_AVERAGE'], title = 'CPU Utilization {}'.format(host), figsize=(10,4))
        plot_user.set_ylabel("%")
        plot_system.set_ylabel("%")
        plot_wait.set_ylabel("%")
        plot_util.set_ylabel("%")
        stats_user = df_user[['user_MIN','user_MAX', 'user_AVERAGE']].describe()
        stats_system = df_system[['system_MIN','system_MAX', 'system_AVERAGE']].describe()
        stats_wait = df_wait[['wait_MIN','wait_MAX', 'wait_AVERAGE']].describe()
        stats_util = df_util[['util_MIN','util_MAX', 'util_AVERAGE']].describe()
        
        user = pd.DataFrame(stats_user)
        system = pd.DataFrame(stats_system)
        wait = pd.DataFrame(stats_wait)
        util = pd.DataFrame(stats_util)
        stats = pd.concat([user,system, wait, util ], axis=1)
        stats.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/CPU_utilization/dCache'.format(directory), "Stats_CPU_utilization_{}.csv".format(host)), index=True)
        
        plot_user.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/User_{}.png'.format(path, directory, host))
        plot_system.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/System_{}.png'.format(path, directory, host))
        plot_wait.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Wait_{}.png'.format(path, directory, host))
        plot_util.figure.savefig('{}/PP_Output/{}/Plots/AGLT2/CPU_utilization/Util_{}.png'.format(path, directory, host))
        return None


# In[29]:


hosts = ['umfs06','umfs09', 'umfs11', 'umfs16', 'umfs19', 'umfs20', 'umfs21', 'umfs22', 'umfs23', 'umfs24',          'umfs25', 'umfs26', 'umfs27', 'umfs28']
Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs:
    for j in hosts:
        print(i,j)
        Util('{}'.format(j), '{}'.format(i))


# In[23]:


def Utiltime(host, directory):
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


# In[24]:


Utiltime('umfs11', 'Output_20210201_1915')


# In[ ]:


#Output_20210201_1140
#start 1612197600
#end 1612201500
#rows: 65

#Output_20210201_1338
#start 1612204680
#end 1612209180
#rows: 75 

#Output_20210201_1602
#start 1612213320
#end 1612217820
#rows 75

#Output_20210201_1741
#start 1612219260
#end 1612223760
#rows 75

#Output_20210201_1915
#start 1612224900
#end 1612228980
#rows: 68

