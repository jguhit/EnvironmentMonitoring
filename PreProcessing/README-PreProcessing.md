## Script overview 
The structure below summarizes the pre-processing script for each network interface. 

1. CheckMK: AGLT2 end-system
  - AGLT2_Load.py
  - AGLT2_Util.py
  - AGLT2_DiskIO.py
  - AGLT2_Memory.py

2. CaPerf: R-Bin-SEB Internal Router 
  - RBIN.py

3. AGLT2-CHIC: 600W and 710 N to ESnet (CHIC) 
  - AGLT2_CHI.py

The scripts above ensures that all of the environment metrics from each path have the same start and end times and in five-minute intervals 

