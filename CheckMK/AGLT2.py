#!/usr/bin/env python
import json
import requests
import os

hosts = ['umfs06','umfs14', 'umfs20', 'umfs23', 'umfs26', 'umfs09', 'umfs16', 'umfs21', 'umfs24', 'umfs27', 'umfs02', 'umfs11', 'umfs19', 'umfs22', 'umfs25', 'umfs28' ]
servers = ['CPU_load', 'CPU_utilization', 'Disk_IO_SUMMARY', 'Memory']
url = 'http://um-omd.aglt2.org/atlas/pnp4nagios/xport/json'

variables = {}

with open(os.path.join(os.environ["Timepath"], "Time.txt")) as f:
    for line in f:
        name, value = line.split("=")
        variables[name] = float(value)

#new variable that gets the current unix time. 
#another variable which is current unix time - 5 mins
#12:00.05, round off to the closest minute where the seconds field is 0. 

start = variables["start"]
startf = int(start)
end = variables["end"]
endf = int(end)

for i in range(len(servers)):
	for j in range(len(hosts)):
		querystring = {"start":"{}".format(startf),"end":"{}".format(endf),"host":"{}".format(hosts[j]), "srv":"{}".format(servers[i])}
		#querystring = {"start":"1602068400","end":"1602070200","host":"{}".format(hosts[j]), "srv":"{}".format(servers[i])} 
		#print(querystring)
		payload = ""
                headers = {
                    'cookie': "pnp4nagios=81b90oupt9qsjvd1h09unjivn1",
                    'authorization': "Basic b21kYWRtaW46U05ldXRyaW5vOTk="
                    }

                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
                #print(response.text)
	
		todos = json.loads(response.text)
                todos == response.json()
                
                #with open('test/AGLT2_{0}_{1}.json'.format(servers[i],hosts[j]), 'w') as fp:
                with open(os.path.join(os.environ["AGLT2"], "AGLT2_{0}_{1}.json".format(servers[i],hosts[j])),'w') as fp:  
			json.dump(todos, fp, sort_keys=True, indent=4)
	
