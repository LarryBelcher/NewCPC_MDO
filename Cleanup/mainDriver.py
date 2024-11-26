#!python


import os, datetime, sys, subprocess

isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
#isz = ['620']
yrs = ['2015','2016']
mons = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


for y in xrange(len(yrs)):
	for i in xrange(len(mons)):
		for j in xrange(len(isz)):
			cmd = 'python anomtavgDriver.py '+yrs[y]+mons[i]+' '+isz[j]
			subprocess.call(cmd, shell=True)

for y in xrange(len(yrs)):		
	for i in xrange(len(mons)):
		for j in xrange(len(isz)):
			cmd = 'python anomprecipDriver.py '+yrs[y]+mons[i]+' '+isz[j]
			subprocess.call(cmd, shell=True)