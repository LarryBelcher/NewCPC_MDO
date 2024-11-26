#!/usr/bin/python


import os



if __name__ == '__main__':
	
	
	#yyyy = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
	yyyy = ['2020', '2021']
	mm = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	
	for i in range(len(yyyy)):
		for j in range(len(mm)):
			cmd = 'python /work/CPC_Monthly/kmlReprocessDriver.py '+yyyy[i]+mm[j]+' 0'
			os.system(cmd)
			cmd = 'python /work/CPC_Monthly/kmlReprocessDriver.py '+yyyy[i]+mm[j]+' 14'
			os.system(cmd)
