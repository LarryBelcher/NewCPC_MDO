#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, sys, subprocess, glob, calendar
from dbfread import DBF
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np


def int2str(mmi):
	if(mmi == '00'): ms = 'No Data'
	if(mmi == '01'): ms = 'January'
	if(mmi == '02'): ms = 'February'
	if(mmi == '03'): ms = 'March'
	if(mmi == '04'): ms = 'April'
	if(mmi == '05'): ms = 'May'
	if(mmi == '06'): ms = 'June'
	if(mmi == '07'): ms = 'July'
	if(mmi == '08'): ms = 'August'
	if(mmi == '09'): ms = 'September'
	if(mmi == '10'): ms = 'October'
	if(mmi == '11'): ms = 'November'
	if(mmi == '12'): ms = 'December'
	return ms

def m2fm(mmm):
	if(mmm == 'Jan'): fmm = 'January'
	if(mmm == 'Feb'): fmm = 'February'
	if(mmm == 'Mar'): fmm = 'March'
	if(mmm == 'Apr'): fmm = 'April'
	if(mmm == 'May'): fmm = 'May'
	if(mmm == 'Jun'): fmm = 'June'
	if(mmm == 'Jul'): fmm = 'July'
	if(mmm == 'Aug'): fmm = 'August'
	if(mmm == 'Sep'): fmm = 'September'
	if(mmm == 'Oct'): fmm = 'October'
	if(mmm == 'Nov'): fmm = 'November'
	if(mmm == 'Dec'): fmm = 'December'
	return fmm


#-----------------------------------------------------------------------------------------
### SET THE PATH TO THE CODE/DATA 
### !!! This is the only machine dependent variable and MUST be changed to be consistent
### !!! with the computer you are running this on
workdir = '/work/CPC_Monthly'
os.chdir(workdir)
#-----------------------------------------------------------------------------------------


fdate = sys.argv[1]   #expects format like: 201301
leadtime = sys.argv[2]	#expects 14 or 0

yyyy = fdate[0:4]		#NOTE a given date will process data for the following month
mm = fdate[4:]




if(leadtime == '14'):
	pmm = int(mm)+1
	if(pmm == 13): pmm = 1
	mmm = calendar.month_name[pmm][0:3]
	dfile = glob.glob('./Data/lead14_'+mmm+'*_temp.shp')
	if(len(dfile) == 0):
		cmd = 'wget http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/seastemp_'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o seastemp_'+fdate+'.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
		cmd = 'rm seastemp_'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		dfile = glob.glob('./Data/lead14_'+mmm+'*_temp.shp')
	dfile = dfile[0].split('.shp')[0]


if(leadtime == '0'):
	pmm = int(mm)+1
	if(pmm == 13): pmm = 1
	mmm = calendar.month_name[pmm][0:3]
	dfile = glob.glob('./Data/lead15_'+mmm+'*_temp.shp')
	if(len(dfile) == 0):
		cmd = 'wget http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/monthupd_temp'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o monthupd_temp'+fdate+'.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
		cmd = 'rm monthupd_temp'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		dfile = glob.glob('./Data/lead15_'+mmm+'*_temp.shp')
	dfile = dfile[0].split('.shp')[0]


dbf = dfile+'.dbf'
table = DBF(dbf, load=True)
idate = str(table.records[0]['Fcst_Date'])
idp = idate.split('-')
idyyyy = idp[0]
fnmm = idp[1]
iddd = idp[2]
idate = idyyyy+'-'+fnmm+'-'+iddd
labdate = str(table.records[1]['Valid_Seas'])
lmm = str(table.records[1]['Valid_Seas'][0:3])
fm = m2fm(lmm)
labdate = fm+' '+str(table.records[1]['Valid_Seas'][4:])


p1 = subprocess.Popen("python cpcMontempKML.py "+dfile+" "+idate+' '+labdate, shell=True)
p1.wait()

p2 = subprocess.Popen("python cleanup.py "+dfile, shell=True)
p2.wait()


if(leadtime == '14'):
	pmm = int(mm)+1
	if(pmm == 13): pmm = 1
	mmm = calendar.month_name[pmm][0:3]
	dfile = glob.glob('./Data/lead14_'+mmm+'*_prcp.shp')
	if(len(dfile) == 0):
		cmd = 'wget http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/seasprcp_'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o seasprcp_'+fdate+'.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
		dfile = glob.glob('./Data/lead14_'+mmm+'*_prcp.shp')
	dfile = dfile[0].split('.shp')[0]


if(leadtime == '0'):
	pmm = int(mm)+1
	if(pmm == 13): pmm = 1
	mmm = calendar.month_name[pmm][0:3]
	dfile = glob.glob('./Data/lead15_'+mmm+'*_prcp.shp')
	if(len(dfile) == 0):
		cmd = 'wget http://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/monthupd_prcp'+fdate+'.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o monthupd_prcp'+fdate+'.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
		dfile = glob.glob('./Data/lead15_'+mmm+'*_prcp.shp')
	dfile = dfile[0].split('.shp')[0]


dbf = dfile+'.dbf'
table = DBF(dbf, load=True)
idate = str(table.records[0]['Fcst_Date'])
idp = idate.split('-')
idyyyy = idp[0]
fnmm = idp[1]
iddd = idp[2]
idate = idyyyy+'-'+fnmm+'-'+iddd
labdate = str(table.records[1]['Valid_Seas'])
lmm = str(table.records[1]['Valid_Seas'][0:3])
fm = m2fm(lmm)
labdate = fm+' '+str(table.records[1]['Valid_Seas'][4:])


p1 = subprocess.Popen("python cpcMonprecipKML.py "+dfile+" "+idate+' '+labdate, shell=True)
p1.wait()

p2 = subprocess.Popen("python cleanup.py "+dfile, shell=True)
p2.wait()