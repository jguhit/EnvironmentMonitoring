#  Environment Monitoring Scripts for NetBASILISK 
This repository contains the initial environment scripts for the NetBASILISK project. Script changes are continually made and uploaded. 

## Grabbing Metrics 
The Scripts are divided into the **CheckMK, CAPerf and Grafana** directories. 

**CheckMK**: Python script for grabbing environment metrics from AGLT2 end-system 

**CAPerf**: Python script for grabbing environment metrics from the R-Bin-SEB internal router (In-Between Path) 

**Grafana**: Python script for grabbing environment metrics from external routers (600 W and 710 N) to ESNET (CHIC)

## Preprocessing Scripts 

The preprocessing scripts in **Preprocessing** directory. These scripts take the output files from the CheckMK, CAPerf, and Grafana as inputs to the preprocessing script. Organizes the metrics gathered for each network path and calculates Statistics. 
