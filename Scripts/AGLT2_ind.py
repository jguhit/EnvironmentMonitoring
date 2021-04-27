#!/usr/bin/env python

import json
import requests
import os
import time
import datetime
import pandas as pd
import numpy as np
from Timing import roundups, rounddos

current = datetime.datetime.now()
current_5 = current - datetime.timedelta(minutes=5)
start = rounddos(current_5)
start_final = time.mktime(start.timetuple())
end = rounddos(current)
end_final = time.mktime(end.timetuple())

######==CHECK 1==######
print("start orig: ", current_5, " ", "start rounded: ", start, " ", "start unix: ", start_final)
print("end orig: ", current, " ", "end rounded: ", end, " ", "end unix: ", end_final)

hosts = ['umfs06', 'umfs20', 'umfs23', 'umfs26', 'umfs09', 'umfs16', 'umfs21', 'umfs24', 'umfs27', 'umfs11', 'umfs19', 'umfs22', 'umfs25', 'umfs28']
#hosts = ['umfs06', 'umfs20']
servers = ['CPU_load', 'CPU_utilization', 'Disk_IO_SUMMARY', 'Memory']
#servers = ['CPU_load']
url = 'https://um-omd.aglt2.org/atlas/pnp4nagios/xport/json'

aglt2path = os.environ["aglt2"]
if os.path.isdir(aglt2path):
	print("Path exists: ", aglt2path)
else: 
	print("Path does not exist")

for j in range(len(hosts)):
	print("===host===", hosts[j])
	for i in range(len(servers)):
		#print("===host===", hosts[j])
		#print(servers[i], hosts[j])
		#find a way to query for multiple hosts either one hosts all metadata, or all hosts per metadata 
		#"host": "umfs06", "host": [""]
		querystring = {"host":"{}".format(hosts[j]), "srv":"{}".format(servers[i]), "start":"{}".format(int(start_final)), "end":"{}".format(int(end_final))}
		payload = ""
		#headers = {'cookie':"pnp4nagios=81b90oupt9qsjvd1h09unjivn1", 'authorization': "Basic b21kYWRtaW46U05ldXRyaW5vOTk="}
		headers = {"cookie": "pnp4nagios=v7gj225tqflmgal5c1ji54rqj1", "Cookie": "__utma=37526576.779950651.1585936035.1585936035.1585936035.1; pnp4nagios=hru4rg9ch6imsi34khjc747jg3; auth_atlas=omdadmin:1618406441.45:d4e6cb1629f078fa89b59d2429785d00","Authorization": "Basic b21kYWRtaW46U05ldXRyaW5vOTk="}
		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
		todos = json.loads(response.text)
		todos == response.json()
		#time.sleep(60)
		df = pd.DataFrame(todos)
		#print(df)
		start = df["meta"]["start"]
		end = df["meta"]["end"]
		LEG = df["meta"]["legend"]
		DATA = df["data"]["row"]
		DATA = pd.DataFrame(data = DATA)
		LEG = pd.DataFrame(data = LEG)
		row, col = DATA.shape

		timestamps = []
		for k in range(row):
			start = int(start)
			start = start + 60
			timestamps.append(start)

		#print(DATA.iloc[0,0])
		#print("\n")
		#print(DATA.iloc[1,0])
		#print("\n")
		#print("row", row)
		values = []
		for l in range(row):
			datum = DATA.iloc[l,0]
			values.append(datum)
	        
		#print(values)	
		if i == 0:
			var_ave = []
			for i in range(len(values)):
				var_ave.append(values[i][5])
			#index = 5 only collects load5 ave 
			tuples = list(zip(timestamps, var_ave))
			#print(tuples)
			df_values = pd.DataFrame(data = tuples, columns = ['Timestamp', 'load5_AVERAGE'], dtype = float)
			df_values["load5_AVERAGE"] = df_values["load5_AVERAGE"].replace(np.nan,0)
			df_values["Timestamp"] = pd.to_datetime(df_values["Timestamp"],unit='s')
			df_values = df_values.set_index(["Timestamp"])
			df_values = df_values.resample("5T").agg(['min','max','mean','std'], axis="columns").round(5)			
			df_values = df_values[:1]
			df_values = df_values.reset_index()
			df_values = df_values.drop('Timestamp', axis=1)
			df_values = df_values.T
			print(df_values)
			df_values = df_values.to_csv(os.path.join(aglt2path, "AGLT2_CPU_load_{}.csv".format(hosts[j])), index=True)
			checkpath = os.path.join(aglt2path, "AGLT2_CPU_load_{}.csv".format(hosts[j]))
			if os.path.exists(checkpath): 
				print("Path and file exists", checkpath)
			else:
				print("Path and file does not exist")

			print("AGLT2 CPU Load Done")	
			#df_values = df_values.to_csv("../Output/Raw/AGLT2/AGLT2_CPU_load_{}.csv".format(hosts[j]), index=True)
		
		if i == 1:
			var_ave = []
			#util_ave = '11''
			for i in range(len(values)):  
				var_ave.append(values[i][11]) #values[i][util_ave]

			tuples = list(zip(timestamps, var_ave))
			df_values = pd.DataFrame(data = tuples, columns = ['Timestamp', 'util_AVERAGE'], dtype = float) 
			df_values["util_AVERAGE"] = df_values["util_AVERAGE"].replace(np.nan,0)
			df_values["Timestamp"] = pd.to_datetime(df_values["Timestamp"], unit='s')
			df_values = df_values.set_index(["Timestamp"])
			#df_values = df_values.resample("5T").mean()
			df_values = df_values.resample("5T").agg(['min','max','mean','std'], axis="columns").round(5)
			df_values = df_values[:1]
			df_values = df_values.reset_index()
			df_values = df_values.drop('Timestamp', axis=1)
			df_values = df_values.T
			print(df_values)
			df_values = df_values.to_csv(os.path.join(aglt2path, "AGLT2_CPU_utilization_{}.csv".format(hosts[j])), index=True)
			checkpath = os.path.join(aglt2path, "AGLT2_CPU_utilization_{}.csv".format(hosts[j]))
			if os.path.exists(checkpath):
				print("Path and file exists", checkpath)
			else:
				print("Path and file does not exist")
			print("AGLT2 CPU Utilization done")
			#df_values = df_values.to_csv("../Output/Raw/AGLT2/AGLT2_CPU_utilization_{}.csv".format(hosts[j]), index=True)

		if i == 2:
			var_ave = []
			for i in range(len(values)): 
				var_ave.append(values[i][2])
			tuples = list(zip(timestamps, var_ave))
			df_values = pd.DataFrame(data = tuples, columns = ['Timestamp', 'disk_utilization_AVERAGE'], dtype = float)
			df_values["disk_utilization_AVERAGE"] = df_values["disk_utilization_AVERAGE"].replace(np.nan,0)
			df_values["Timestamp"] = pd.to_datetime(df_values["Timestamp"], unit='s')
			df_values = df_values.set_index(["Timestamp"])
			#df_values = df_values.resample("5T").mean()
			df_values = df_values.resample("5T").agg(['min','max','mean','std'], axis="columns").round(5) 
			df_values = df_values[:1] 
			df_values = df_values.reset_index()
			df_values = df_values.drop('Timestamp', axis=1)
			df_values = df_values.T
			print(df_values)
			df_values = df_values.to_csv(os.path.join(aglt2path,"AGLT2_Disk_IO_SUMMARY_{}.csv".format(hosts[j])), index=True)
			checkpath = os.path.join(aglt2path, "AGLT2_Disk_IO_SUMMARY_{}.csv".format(hosts[j]))
			if os.path.exists(checkpath):
				print("Path and file exists", checkpath)
			else:
				print("Path and file does not exist")
			print("AGLT2 Disk IO Summary done")
			#df_values = df_values.to_csv("../Output/Raw/AGLT2/AGLT2_Disk_IO_SUMMARY_{}.csv".format(hosts[j]), index=True)

		if i == 3:
			var_ave = []
			for i in range(len(values)): 
				var_ave.append(values[i][74])
			tuples = list(zip(timestamps, var_ave))
			#print(tuples)
			df_values = pd.DataFrame(data = tuples, columns = ['Timestamp', 'mem_available_AVERAGE'], dtype = float)
			df_values["mem_available_AVERAGE"] = df_values["mem_available_AVERAGE"].replace(np.nan, 0)
			df_values["Timestamp"] = pd.to_datetime(df_values["Timestamp"], unit='s')
			df_values = df_values.set_index(["Timestamp"])
			df_values = df_values.resample("5T").agg(['min','max','mean', 'std'], axis="columns").round(5)
			#df_values = df_values.resample("5T").mean() 
			cols = df_values.columns
			df_values[cols] = df_values[cols] *(1.25e-10)
			df_values = df_values[:1]
			df_values = df_values.reset_index()
			df_values = df_values.drop('Timestamp', axis=1)
			df_values = df_values.T
			print(df_values)
			df_values = df_values.to_csv(os.path.join(aglt2path, "AGLT2_Memory_{}.csv".format(hosts[j])), index=True)
			checkpath = os.path.join(aglt2path, "AGLT2_Memory_{}.csv".format(hosts[j]))
			if os.path.exists(checkpath):
				print("Path and file exists", checkpath)
			else:
				print("Path and file does not exist")

			print("AGLT2 Memory done")
			#df_values = df_values.to_csv("../Output/Raw/AGLT2/AGLT2_Memory_{}.csv".format(hosts[j]), index=True)
