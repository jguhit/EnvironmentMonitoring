#!/usr/bin/env python
# coding: utf-8

# In[29]:


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


# In[35]:


def Memory(host,directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_Memory_{}.json".format(host)))
    start = df["meta"]["start"]
    end = df["meta"]["end"]
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "percpu_MIN", "percpu_MAX", "percpu_AVERAGE", "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][4:64]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "percpu_MIN", "percpu_MAX", "percpu_AVERAGE", "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][1:61]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][1:61]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "percpu_MIN", "percpu_MAX", "percpu_AVERAGE", "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][2:62]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][2:62]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None
    
    if directory == 'Output_20210201_1741':
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "percpu_MIN", "percpu_MAX", "percpu_AVERAGE", "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][3:63]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][3:63]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None
    
    if directory == 'Output_20210201_1915':
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "percpu_MIN", "percpu_MAX", "percpu_AVERAGE", "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][4:64]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None


# In[37]:


hosts = ['umfs06','umfs09','umfs19', 'umfs20', 'umfs21', 'umfs22', 'umfs23', 'umfs24',          'umfs25', 'umfs26', 'umfs27', 'umfs28']
Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

#'umfs11', 'umfs16'

for i in Dirs:
    for j in hosts:
        print(i,j)
        Memory('{}'.format(j), '{}'.format(i))


# In[38]:


def Memory2(host,directory):
    host = str(host)
    directory = str(directory)
    path = '/Users/jemguhit/Documents/University_of_Michigan/Research/NetBasilisk/PreProcessing'
    path2 = '/Benchmark_Results/{}/environment/AGLT2'.format(directory)
    df = pd.read_json(os.path.join(path + path2, "AGLT2_Memory_{}.json".format(host)))
    start = df["meta"]["start"]
    end = df["meta"]["end"]
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][4:64]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][1:61]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][1:61]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][2:62]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][2:62]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None
    
    if directory == 'Output_20210201_1741':
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][3:63]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][3:63]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None
    
    if directory == 'Output_20210201_1915':
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
        df_values.columns = ["active_MIN", "active_MAX", "active_AVERAGE", "active_anon_MIN", "active_anon_MAX", "active_anon_AVERAGE",         "active_file_MIN", "active_file_MAX", "active_file_AVERAGE", "anon_huge_pages_MIN", "anon_huge_pages_MAX",         "anon_huge_pages_AVERAGE", "anon_pages_MIN", "anon_pages_MAX", "anon_pages_AVERAGE", "bounce_MIN", "bounce_MAX",         "bounce_AVERAGE", "buffers_MIN", "buffers_MAX", "buffers_AVERAGE", "cached_MIN", "cached_MAX", "cached_AVERAGE",         "caches_MIN", "caches_MAX", "caches_AVERAGE",  "cma_free_MIN",  "cma_free_MAX",  "cma_free_AVERAGE",         "cma_total_MIN", "cma_total_MAX", "cma_total_AVERAGE", "commit_limit_MIN", "commit_limit_MAX",         "commit_limit_AVERAGE", "committed_as_MIN", "committed_as_MAX", "committed_as_AVERAGE", "dirty_MIN", "dirty_MAX",         "dirty_AVERAGE", "hardware_corrupted_MIN", "hardware_corrupted_MAX", "hardware_corrupted_AVERAGE",         "huge_pages_free_MIN", "huge_pages_free_MAX", "huge_pages_free_AVERAGE", "huge_pages_rsvd_MIN",         "huge_pages_rsvd_MAX", "huge_pages_rsvd_AVERAGE", "huge_pages_surp_MIN", "huge_pages_surp_MAX",         "huge_pages_surp_AVERAGE", "huge_pages_total_MIN", "huge_pages_total_MAX", "huge_pages_total_AVERAGE",         "inactive_MIN", "inactive_MAX", "inactive_AVERAGE", "inactive_anon_MIN", "inactive_anon_MAX",         "inactive_anon_AVERAGE", "inactive_file_MIN", "inactive_file_MAX", "inactive_file_AVERAGE", "kernel_stack_MIN",         "kernel_stack_MAX", "kernel_stack_AVERAGE", "mapped_MIN", "mapped_MAX", "mapped_AVERAGE", "mem_available_MIN",         "mem_available_MAX", "mem_available_AVERAGE", "mem_free_MIN", "mem_free_MAX", "mem_free_AVERAGE",         "mem_total_MIN", "mem_total_MAX", "mem_total_AVERAGE", "mem_used_MIN", "mem_used_MAX", "mem_used_AVERAGE",         "mlocked_MIN", "mlocked_MAX", "mlocked_AVERAGE", "nfs_unstable_MIN", "nfs_unstable_MAX", "nfs_unstable_AVERAGE",         "page_tables_MIN", "page_tables_MAX", "page_tables_AVERAGE", "pending_MIN", "pending_MAX", "pending_AVERAGE",         "sreclaimable_MIN", "sreclaimable_MAX", "sreclaimable_AVERAGE",         "sunreclaim_MIN", "sunreclaim_MAX", "sunreclaim_AVERAGE", "shmem_MIN", "shmem_MAX", "shmem_AVERAGE", "slab_MIN",         "slab_MAX", "slab_AVERAGE", "swap_cached_MIN", "swap_cached_MAX", "swap_cached_AVERAGE", "swap_free_MIN",         "swap_free_MAX",  "swap_free_AVERAGE", "swap_total_MIN", "swap_total_MAX",  "swap_total_AVERAGE",         "swap_used_MIN", "swap_used_MAX",  "swap_used_AVERAGE", "total_total_MIN",  "total_total_MAX",         "total_total_AVERAGE", "total_used_MIN", "total_used_MAX",  "total_used_AVERAGE",  "unevictable_MIN",         "unevictable_MAX", "unevictable_AVERAGE", "writeback_MIN", "writeback_MAX",  "writeback_AVERAGE",         "writeback_tmp_MIN", "writeback_tmp_MAX", "writeback_tmp_AVERAGE"]
        df_values.insert(0, "Timestamp", timestamps, True) 
        cols = df_values.columns.drop('Timestamp')
        df_values[cols] = df_values[cols].apply(pd.to_numeric, errors='coerce')
        df_values[cols] = df_values[cols] *(1.25e-10)
        new = df_values.filter(['Timestamp','mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'], axis=1)
        
        totaltime = new["Timestamp"][4:64]
        timesplit = np.array_split(totaltime,12)
        totaltime = []
        for times in timesplit:
            totaltime.append(list(times)[0])
        
    
        mem_available_DATA = new['mem_available_MIN'][4:64]
        mem_available_split = np.array_split(mem_available_DATA,12)
    
        mem_available_min = []
        mem_available_max = []
        mem_available_ave = []
    
        for mem_available_array in mem_available_split:
        
            mem_available_min.append(min(mem_available_array))
            mem_available_max.append(max(mem_available_array))
            mem_available_ave.append(np.mean(mem_available_array))

        list_mem_available = list(zip(totaltime, mem_available_min, mem_available_max, mem_available_ave))
    
        df_mem_available = pd.DataFrame(data=list_mem_available, columns=['Timestamp', 'mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE'])
        df_mem_available['Timestamp'] = pd.to_datetime(df_mem_available['Timestamp'],unit='s')
        
        stats_mem_available = df_mem_available[['mem_available_MIN','mem_available_MAX', 'mem_available_AVERAGE']].describe()
        mem_available = pd.DataFrame(stats_mem_available)

        mem_available.to_csv(os.path.join(path + '/PP_Output/{}/Stats/AGLT2/Memory/dCache'.format(directory), "Stats_Memory_{}.csv".format(host)), index=True)
        return None


# In[39]:


hosts = ['umfs11', 'umfs16']
Dirs = ['Output_20210201_1140', 'Output_20210201_1338', 'Output_20210201_1602', 'Output_20210201_1741',         'Output_20210201_1915']

#'umfs11', 'umfs16'

for i in Dirs:
    for j in hosts:
        print(i,j)
        Memory2('{}'.format(j), '{}'.format(i))


# In[ ]:




