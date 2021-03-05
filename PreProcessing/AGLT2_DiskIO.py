#!/usr/bin/env python
# coding: utf-8

# In[35]:


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


# In[36]:


def DiskIO(host,directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_Disk_IO_SUMMARY_{}.json".format(host)))
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
        df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
        
        #slicing the dataframe
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        diskutil_DATA = new["disk_utilization_MIN"][4:64]
        diskutil_split = np.array_split(diskutil_DATA,12)

        diskutil_min = []
        diskutil_max = []
        diskutil_ave = []
        
        for diskutil_array in diskutil_split:
            diskutil_min.append(min(diskutil_array))
            diskutil_max.append(max(diskutil_array))
            diskutil_ave.append(np.mean(diskutil_array))
            
        list_diskutil = list(zip(totaltime, diskutil_min, diskutil_max, diskutil_ave))
        df_util = pd.DataFrame(data=list_diskutil, columns=['Timestamp', 'disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        stats_util = df_util[['disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE']].describe()
        util = pd.DataFrame(stats_util)
        util.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/DiskIO/dCache'.format(directory), "Stats_DiskIO_{}.csv".format(host)), index=True)
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
        df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
        
        #slicing the dataframe
        totaltime = new["Timestamp"][1:61]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        diskutil_DATA = new["disk_utilization_MIN"][1:61]
        diskutil_split = np.array_split(diskutil_DATA,12)

        diskutil_min = []
        diskutil_max = []
        diskutil_ave = []
        
        for diskutil_array in diskutil_split:
            diskutil_min.append(min(diskutil_array))
            diskutil_max.append(max(diskutil_array))
            diskutil_ave.append(np.mean(diskutil_array))
            
        list_diskutil = list(zip(totaltime, diskutil_min, diskutil_max, diskutil_ave))
        df_util = pd.DataFrame(data=list_diskutil, columns=['Timestamp', 'disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        stats_util = df_util[['disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE']].describe()
        util = pd.DataFrame(stats_util)
        util.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/DiskIO/dCache'.format(directory), "Stats_DiskIO_{}.csv".format(host)), index=True)
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
        df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
        
        #slicing the dataframe
        totaltime = new["Timestamp"][2:62]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        diskutil_DATA = new["disk_utilization_MIN"][2:62]
        diskutil_split = np.array_split(diskutil_DATA,12)

        diskutil_min = []
        diskutil_max = []
        diskutil_ave = []
        
        for diskutil_array in diskutil_split:
            diskutil_min.append(min(diskutil_array))
            diskutil_max.append(max(diskutil_array))
            diskutil_ave.append(np.mean(diskutil_array))
            
        list_diskutil = list(zip(totaltime, diskutil_min, diskutil_max, diskutil_ave))
        df_util = pd.DataFrame(data=list_diskutil, columns=['Timestamp', 'disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        stats_util = df_util[['disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE']].describe()
        util = pd.DataFrame(stats_util)
        util.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/DiskIO/dCache'.format(directory), "Stats_DiskIO_{}.csv".format(host)), index=True)
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
        df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
        
        #slicing the dataframe
        totaltime = new["Timestamp"][3:63]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        diskutil_DATA = new["disk_utilization_MIN"][3:63]
        diskutil_split = np.array_split(diskutil_DATA,12)

        diskutil_min = []
        diskutil_max = []
        diskutil_ave = []
        
        for diskutil_array in diskutil_split:
            diskutil_min.append(min(diskutil_array))
            diskutil_max.append(max(diskutil_array))
            diskutil_ave.append(np.mean(diskutil_array))
            
        list_diskutil = list(zip(totaltime, diskutil_min, diskutil_max, diskutil_ave))
        df_util = pd.DataFrame(data=list_diskutil, columns=['Timestamp', 'disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        stats_util = df_util[['disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE']].describe()
        util = pd.DataFrame(stats_util)
        util.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/DiskIO/dCache'.format(directory), "Stats_DiskIO_{}.csv".format(host)), index=True)
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
        df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
        
        #slicing the dataframe
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            #print(list(times))
            totaltime.append(list(times)[0])

        diskutil_DATA = new["disk_utilization_MIN"][3:63]
        diskutil_split = np.array_split(diskutil_DATA,12)

        diskutil_min = []
        diskutil_max = []
        diskutil_ave = []
        
        for diskutil_array in diskutil_split:
            diskutil_min.append(min(diskutil_array))
            diskutil_max.append(max(diskutil_array))
            diskutil_ave.append(np.mean(diskutil_array))
            
        list_diskutil = list(zip(totaltime, diskutil_min, diskutil_max, diskutil_ave))
        df_util = pd.DataFrame(data=list_diskutil, columns=['Timestamp', 'disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'])
        df_util['Timestamp'] = pd.to_datetime(df_util["Timestamp"],unit='s')
        stats_util = df_util[['disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE']].describe()
        util = pd.DataFrame(stats_util)
        util.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/DiskIO/dCache'.format(directory), "Stats_DiskIO_{}.csv".format(host)), index=True)
        return None


# In[37]:


hosts = ['umfs06','umfs09', 'umfs11', 'umfs16', 'umfs19', 'umfs20', 'umfs21', 'umfs22', 'umfs23', 'umfs24',          'umfs25', 'umfs26', 'umfs27', 'umfs28']
Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

for i in Dirs:
    for j in hosts:
        print(i,j)
        DiskIO('{}'.format(j), '{}'.format(i))


# In[10]:


'''
Output_20210201_1140
start 1612197600
end 1612201500
rows: 65

Output_20210201_1338
start 1612204680
end 1612209180
rows: 75

Output_20210201_1602
start 1612213320
end 1612217820
rows: 75

Output_20210201_1741
start 1612219260
end 1612223760
rows: 75

Output_20210201_1915
start 1612224900
end 1612228980
rows: 68
'''


# In[30]:


def DiskIO(host,directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_Disk_IO_SUMMARY_{}.json".format(host)))
    start = df["meta"]["start"]
    end = df["meta"]["end"]
    #print('start', start)
    #print('end', end)
    LEG = df["meta"]["legend"]
    DATA = df["data"]["row"]
    DATA = pd.DataFrame(data = DATA)
    LEG = pd.DataFrame(data = LEG)
    
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
    df_values.columns = ["disk_utilization_MIN","disk_utilization_MAX","disk_utilization_AVERAGE","disk_read_throughput_MIN",         "disk_read_throughput_MAX", "disk_read_throughput_AVERAGE","disk_write_throughput_MIN",         "disk_write_throughput_MAX","disk_write_throughput_AVERAGE","disk_average_wait_MIN","disk_average_wait_MAX",         "disk_average_wait_AVERAGE","disk_average_read_wait_MIN","disk_average_read_wait_MAX",         "disk_average_read_wait_AVERAGE","disk_average_write_wait_MIN","disk_average_write_wait_MAX",         "disk_average_write_wait_AVERAGE","disk_latency_MIN","disk_latency_MAX","disk_latency_AVERAGE","disk_queue_length_MIN",        "disk_queue_length_MAX","disk_queue_length_AVERAGE","disk_read_ios_MIN","disk_read_ios_MAX",         "disk_read_ios_AVERAGE","disk_write_ios_MIN","disk_write_ios_MAX","disk_write_ios_AVERAGE",         "disk_average_read_request_size_MIN","disk_average_read_request_size_MAX",         "disk_average_read_request_size_AVERAGE","disk_average_request_size_MIN", "disk_average_request_size_MAX",         "disk_average_request_size_AVERAGE","disk_average_write_request_size_MIN",         "disk_average_write_request_size_MAX","disk_average_write_request_size_AVERAGE"]
    df_values.insert(0, "Timestamp", timestamps, True) 
    cols = df_values.columns.drop('Timestamp')
    df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
    new = df_values.filter(['Timestamp','disk_utilization_MIN','disk_utilization_MAX', 'disk_utilization_AVERAGE'], axis=1)
    print(new["Timestamp"])


# In[31]:


DiskIO('umfs11','Output_20210201_1140')


# In[ ]:




