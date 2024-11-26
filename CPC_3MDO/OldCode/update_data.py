#!/usr/bin/python


import os, sys, time, subprocess
import datetime


if __name__ == '__main__':

	os.chdir("/work/CPC_Monthly")

 	today = datetime.date.today()
 	first = today.replace(day=1)
 	lastMonth = first - datetime.timedelta(days=1)
 
	
	###Check the avg temp file
	cmd = 'curl http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/ | grep '+lastMonth.strftime("%Y%m")
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	if(len(out) != 0):
		precipfile = 'http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/monthupd'+out.split('monthupd')[1].split('"')[0]
		temperaturefile = 'http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/monthupd'+out.split('monthupd')[3].split('"')[0]
		os.chdir("/work/CPC_Monthly/Data")
		cmd = 'wget '+precipfile
		subprocess.call(cmd,shell=True)
		cmd = 'wget '+temperaturefile
		subprocess.call(cmd,shell=True)
		cmd = 'unzip ./monthupd'+out.split('monthupd')[1].split('"')[0]
		subprocess.call(cmd,shell=True)
		cmd = 'unzip ./monthupd'+out.split('monthupd')[3].split('"')[0]
		subprocess.call(cmd,shell=True)
		cmd = 'rm *.zip'
		subprocess.call(cmd,shell=True)

