#!/usr/bin/python

'''*************************************************************************************************
Program: anomMaindriver.py

Usage: ./anomMaindriver.py [args]

Synopsis:
This script will check for updated CMB climate division monthly data. If new data exist, the 
most recent monthly maps will be created. The user has the option to pass arguments in the form of
year and month to force the script to generate maps for a specific month (year). Otherwise, the
script will attempt to process the "previous" month's maps.

*************************************************************************************************'''

import datetime, subprocess, sys
from dateutil.relativedelta import *


if __name__ == '__main__':

	#First, clear out the old data
	cmd = 'rm ./Data/climdiv-*'
	subprocess.call(cmd, shell=True)
	
	cmd = 'curl ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/ | grep climdiv-tmpcdv'
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	serverfilename = out.split()[8]
	fileurl = 'ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/'+serverfilename
	cmd = 'wget '+fileurl
	subprocess.call(cmd, shell=True)
	cmd = 'mv '+serverfilename+' ./Data/'
	subprocess.call(cmd, shell=True)
	
	cmd = 'curl ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/ | grep climdiv-pcpndv'
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	serverfilename = out.split()[8]
	fileurl = 'ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/'+serverfilename
	cmd = 'wget '+fileurl
	subprocess.call(cmd, shell=True)
	cmd = 'mv '+serverfilename+' ./Data/'
	subprocess.call(cmd, shell=True)
	
	
	if(len(sys.argv) != 3):
		date_last_month = datetime.datetime.now() - relativedelta(months=1)
		yyyy = date_last_month.year
		mm = date_last_month.month
		stryyyy = str(yyyy)
		if(mm < 10): strmm = '0'+str(mm)
		if(mm > 9): strmm = str(mm)
	
	serverfilename = './Data/'+serverfilename
	lines = tuple(open(serverfilename, 'r'))
	#Obtain the data value on the last line for the month preceding the
	#current month(i.e., 2015 data for the last division in the data file)
	dchk = lines[len(lines)-1].split()[mm]
	

	#If the value of "dchk" is not "missing", proceed to produce the maps for the 
	#previous month
	if(dchk != '-99.90'):	
		isz = ['620', '1000', 'DIY', 'GEO', 'HD', 'HDSD']
		for i in xrange(len(isz)):
			cmd = 'python anomtavgDriver.py '+stryyyy+strmm+' '+isz[i]
			subprocess.call(cmd, shell=True)
		
		for j in xrange(len(isz)):
			cmd = 'python anomprecipDriver.py '+stryyyy+strmm+' '+isz[j]
			subprocess.call(cmd, shell=True)
		cmd = './UploadCMBanomImages.csh'
		subprocess.call(cmd, shell=True)

	
	
		