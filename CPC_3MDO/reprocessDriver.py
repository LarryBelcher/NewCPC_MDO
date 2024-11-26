#!/usr/bin/python


import os, datetime, sys, subprocess
import numpy as np




yint = list(range(2013,2024))
years = [str(x) for x in yint] 
mons = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#years = ['2024']
#mons = ['01', '02', '03', '04', '05', '06']



for i in range(len(years)):
	
	for j in range(len(mons)):
		
		#sizes = ['small', 'large', 'full_res_zips', 'kml']
		sizes = ['full_res_zips']

		for s in sizes:
			cmd = 'python cpcMontempDriver.py '+years[i]+mons[j]+' 14 '+s
			subprocess.call(cmd, shell=True)
			cmd = 'python cleanup.py'
			subprocess.call(cmd, shell=True)
			cmd = 'rm wget*'
			subprocess.call(cmd, shell=True)
			cmd = 'python cpcMontempDriver.py '+years[i]+mons[j]+' 0 '+s
			subprocess.call(cmd, shell=True)
			cmd = 'python cleanup.py'
			subprocess.call(cmd, shell=True)
			cmd = 'rm wget*'
			subprocess.call(cmd, shell=True)
			

			cmd = 'python cpcMonprecipDriver.py '+years[i]+mons[j]+' 14 '+s
			subprocess.call(cmd, shell=True)
			cmd = 'python cleanup.py'
			subprocess.call(cmd, shell=True)
			cmd = 'rm wget*'
			subprocess.call(cmd, shell=True)
			cmd = 'python cpcMonprecipDriver.py '+years[i]+mons[j]+' 0 '+s
			subprocess.call(cmd, shell=True)
			cmd = 'python cleanup.py'
			subprocess.call(cmd, shell=True)
			cmd = 'rm wget*'
			subprocess.call(cmd, shell=True)
			