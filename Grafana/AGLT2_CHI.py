#!/usr/bin/env python 

import requests
import os
import json
url = "https://snapp-portal.omnipop.btaa.org/grafana/api/datasources/proxy/54/query.cgi"
#url = "https://snapp-portal.omnipop.btaa.org/grafana/api/datasources/proxy/52/query.cgi"

identifier = ['d516dc0906bff35d6f5c2c9aae5dea21effaa46f96b00d9e0f28e81492c19853','183b07e6d13fa2c442ce7c7573550d4780be61d1f45fcab948102550a48cd977', 'f6e1d5da2b240f0df1be1209674215b55719235203b1d828e9494a3fa3f7e8c1','50912a45ce1a3d51ead67d63735b3e3563c0939aad10c1b6a166579a0524c6ed','d3947c64aa4ebd202cff06fb9c5e6badf51296db72ab3ba8ff01f35811d423ae', 'a45cf7de85707efbf8a4fb7b07af5b405c192682ddfcd165b5c9ad855b202d80']

variables = {}

with open(os.path.join(os.environ["Timepath"],"Time.txt")) as f:
    for line in f:
        name, value = line.split("=")
        variables[name] = float(value)

start = variables["start"]
startf = int(start)
end = variables["end"]
endf = int(end)


#for i in identifier:
for index, line in enumerate(identifier):
	query = "method=query;query=get%20intf%2C%20node%2C%20aggregate(values.input%2C%2060%2C%20average)%2C%20aggregate(values.output%2C%2060%2C%20average)%20between%20({}%2C%20{})%20by%20intf%2Cnode%20from%20interface%20where%20((identifier%20%3D%20%22{}%22))%20ordered%20by%20node".format(startf,endf,line)
	#query = "method=query;query=get%20intf%2C%20node%2C%20aggregate(values.input%2C%2060%2C%20average)%2C%20aggregate(values.output%2C%2060%2C%20average)%20between%20(1606341600%2C%201606950000)%20by%20intf%2Cnode%20from%20interface%20where%20((identifier%20%3D%20%22{}%22))%20ordered%20by%20node".format(line)
	#print(query)
	response = requests.request("POST", url,data=query)
	#print(response.text)
	todos = json.loads(response.text)
	todos == response.json()

	#with open('testAGLT2CHI/AGLT2_CHI_{}.json'.format(index), 'a') as fp:
	with open(os.path.join(os.environ["AGLT2CHI"],"AGLT2_CHI_{}.json".format(index) ),'w') as fp:
		json.dump(todos, fp, sort_keys=True, indent=4)
	
