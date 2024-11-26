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


os.chdir('/work/CPC_Monthly/')

fdate = sys.argv[1]   #expects format like: 201301
yyyy = fdate[0:4]		#NOTE a given date will process data for the following month
mm = fdate[4:]
#ms = int2str(mm)
#labeldate = ms+' '+yyyy


leadtime = sys.argv[2]	#expects 14 or 0

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
		cmd = 'wget https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/monthlyupdate/monthupd_prcp_latest.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o monthupd_prcp_latest.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
		dfile = glob.glob('./Data/lead15_'+mmm+'*_prcp.shp')
	dfile = dfile[0].split('.shp')[0]


dbf = dfile+'.dbf'
table = DBF(dbf, load=True)
idate = str(table.records[0]['Fcst_Date'])
idp = idate.split('-')
idyyyy = idp[0]
fnmm = idp[1]
idmm = int2str(idp[1])[0:3]
iddd = idp[2]
idate = iddd+' '+idmm+' '+idyyyy
actdate = idyyyy+'-'+fnmm+'-'+iddd
labdate = str(table.records[1]['Valid_Seas'])
lmm = str(table.records[1]['Valid_Seas'][0:3])
fm = m2fm(lmm)
labdate = fm+' '+str(table.records[1]['Valid_Seas'][4:])

imgsize = sys.argv[3]   #(expects 620, 1000, DIY, HD, HDSD, or GEO)

figdpi = 72




if not os.path.isdir('./Images'):
	cmd = 'mkdir ./Images'
	subprocess.call(cmd,shell=True)
if not os.path.isdir('./Images/Precipitation/'):
	cmd = 'mkdir ./Images/Precipitation/'
	subprocess.call(cmd,shell=True)
if not os.path.isdir('./Images/Precipitation/'+imgsize.lower()):
	cmd = 'mkdir ./Images/Precipitation/'+imgsize.lower()
	subprocess.call(cmd,shell=True)


p1 = subprocess.Popen("python /work/CPC_Monthly/cpcMonprecipMap.py "+dfile+" "+imgsize, shell=True)
p1.wait()

if(imgsize == '1000'):
	p2 = subprocess.Popen("python cpcMonprecipKML.py "+dfile+" "+actdate+' '+labdate, shell=True)
	p2.wait()



if(imgsize == '620'):
	t4x = 3; t4y = 0
	t5x = 558; t5y = 0

if(imgsize == '1000'):
	t4x = 3; t4y = 0
	t5x = 939; t5y = 0

if(imgsize == 'DIY'):
	t4x = 3; t4y = 100
	t5x = 3; t5y = 150

if(imgsize == '620' or imgsize == '1000'):
	im1 = Image.open("temporary_map.png")
	if(imgsize == '620'): im1 = im1.resize((620, 400), Image.ANTIALIAS)
	if(imgsize == '1000'): im1 = im1.resize((1000, 640), Image.ANTIALIAS)
	im2 = Image.open('precipoutlook-cpc-legend.png')	
	
	if(imgsize == '620'):
		imlegend = Image.new("RGB", size=(620,58), color=(255,255,254))
		imbar = im2.resize((620, 58), Image.ANTIALIAS)
		imlegend.paste(imbar, (0,0))
	if(imgsize == '1000'):
		imlegend = Image.new("RGB", size=(1000,64), color=(255,255,254))
		imbar = im2.resize((620, 60), Image.ANTIALIAS)
		imlegend.paste(imbar, (190,0))
		
				
	draw = ImageDraw.Draw(imlegend)
	font = ImageFont.truetype("./Fonts/Trebuchet_MS.ttf", 11)
	font1 = ImageFont.truetype("./Fonts/Trebuchet_MS_Bold.ttf", 11)
	draw.text((t4x, t4y),"Precipitation Outlook",(141,141,141),font=font)	
	draw.text((t4x, t4y+11),"for "+labdate,(141,141,141),font=font)
	if('N' in labdate): draw.text((t4x+16, t4y+11),labdate[0],(210,210,210),font=font1)
	draw.text((t4x, t4y+23),"Issued "+idate,(141,141,141),font=font)
	
	draw.text((t5x, t5y),"Climate.gov",(141,141,141),font=font)
	draw.text((t5x+4, t5y+11),"Data: CPC",(141,141,141),font=font)
	
	
	im3 = Image.new('RGB', size=(im1.size[0], im1.size[1]+imlegend.size[1]), color=(255,255,254))
	im3.paste(im1, (0,0))
	im3.paste(imlegend, (0,im1.size[1]))
	img_path = './Images/Precipitation/'+imgsize+'/'
	imgw = str(im3.size[0])
	imgh = str(im3.size[1])
	img_name = 'precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
	pngfile = img_path+img_name
	print("Saving "+pngfile)
	im3.save(pngfile)
	

if(imgsize == 'DIY'):
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = './Images/Precipitation/'+imgsize.lower()+'/'
	img_name = 'precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
	cmd = 'mv '+im1+' '+img_name
	subprocess.call(cmd,shell=True)
	
	path = './Fonts/Trebuchet_MS.ttf'
	propr = font_manager.FontProperties(fname=path)
	path = './Fonts/Trebuchet_MS_Bold.ttf'
	propb = font_manager.FontProperties(fname=path)


	cbar_image = './cpcCbarP.png'
	cbar_x = 110
	cbar_y = 85
	figxsize = 8.89
	figysize = 2.44
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	t1x = 0.38; t1y = 0.685
	t2x = 0.2; t2y = 0.6
	t3x = 0.05; t3y = 0.82
	t4x = 0.84; t4y = 0.82
	t5x = 0.16; t5y = 0.420
	cbar_name = 'precipoutlook-monthly-cpc--'+yyyy+'-'+fnmm+'-'+iddd+'--colorbar.eps'


	fig = plt.figure(figsize=(figxsize,figysize))

	# create an axes instance, leaving room for colorbar at bottom.
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], facecolor='#F5F5F5')
	ax1.set_frame_on(False)
	ax1.set_xticks([])
	ax1.set_xticklabels([])
	ax1.set_yticks([])
	ax1.set_yticklabels([])


	#Add the colorbar
	cbar_orig = Image.open(cbar_image)
	bbox = (1,1,408,14)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	nsx = int((new_size[0]-old_size[0])/2); nsy = int((new_size[1]-old_size[1])/2)
	cbar_im.paste(cbar_orig, (nsx,nsy))
	cbar_im = np.array(cbar_im).astype(np.float) / 255
	fig.figimage(cbar_im, cbar_x, cbar_y)

	path = './Fonts/Trebuchet_MS.ttf'
	font = font_manager.FontProperties(fname=path)
	font.set_family('Trebuchet MS')
	font.set_style('normal')
	font.set_size(fsiz1)
	font.set_weight('bold')
	plt.text(t1x, t1y, "Probability (percent chance)", fontproperties=font, size=fsiz1, color='#333333')

	subtxt = "drier than normal            equal chances           wetter than normal"
	font.set_style('italic')
	font.set_weight('normal')
	plt.text(t2x, t2y, subtxt, fontproperties=font, color='#333333')

	font.set_style('normal')
	plt.text(t3x, t3y+0.1, 'Precipitation Outlook', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t3x, t3y, 'for '+labdate, fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t3x, t3y-0.1, 'Issued '+idate, fontproperties=propr, size=fsiz2, color='#8D8D8D')

	plt.text(t4x, t4y+0.1, 'Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t4x+0.009, t4y, 'Data: CPC', fontproperties=propr, size=fsiz2, color='#8D8D8D')

	plt.text(t5x+0.005, t5y, "80", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.05, t5y, "70", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.1, t5y, "60", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.15, t5y, "50", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.2, t5y, "40", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.25, t5y, "33", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.395, t5y, "33", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.445, t5y, "40", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.495, t5y, "50", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.545, t5y, "60", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.593, t5y, "70", fontproperties=propr, size=fsiz2, color='#333333')
	plt.text(t5x+0.642, t5y, "80", fontproperties=propr, size=fsiz2, color='#333333')



	plt.savefig(cbar_name, dpi=figdpi, orientation='portrait', bbox_inches='tight', pad_inches=0.0)
	
	cmd1 = 'zip precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'--'+yyyy+'-'+fnmm+'-'+iddd+'.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	subprocess.call(cmd1,shell=True)
	cmd2 = 'mv precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'--'+yyyy+'-'+fnmm+'-'+iddd+'.zip '+img_path
	subprocess.call(cmd2,shell=True)
	cmd3 = 'rm '+img_name+' '+cbar_name
	subprocess.call(cmd3,shell=True)




	
if(imgsize == 'HD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1534,736)
	im1 = im1.crop(bbox)
	old_size = im1.size
	new_size = (old_size[0]+2,old_size[1]+2)
	im1new = Image.new("RGB", new_size)
	nsx = int((new_size[0]-old_size[0])/2); nsy = int((new_size[1]-old_size[1])/2)
	im1new.paste(im1, (nsx,nsy))
		
	hdim.paste(im1new, (192,108))
	
	draw = ImageDraw.Draw(hdim)
	
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fntpathb = './Fonts/Trebuchet_MS_Bold.ttf'

	#Add the colorbar
	cbar_orig = Image.open('precipoutlook-cpc-legend-HD.png')
	bbox = (1,1,1767,229)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	nsx = int((new_size[0]-old_size[0])/2); nsy = int((new_size[1]-old_size[1])/2)
	cbar_im.paste(cbar_orig, (nsx,nsy))
	hdim.paste(cbar_orig, (154,850))

	
	
	if(labdate[0:3] == 'Jan'):
		tx1 = 685
		tx2 = 1010
	if(labdate[0:3] == 'Feb'):
		tx1 = 672
		tx2 = 1006
	if(labdate[0:3] == 'Mar'):
		tx1 = 695
		tx2 = 993
	if(labdate[0:3] == 'Apr'):
		tx1 = 700
		tx2 = 983
	if(labdate[0:3] == 'May'):
		tx1 = 710
		tx2 = 980
	if(labdate[0:3] == 'Jun'):
		tx1 = 698
		tx2 = 980
	if(labdate[0:3] == 'Jul'):
		tx1 = 708
		tx2 = 981
	if(labdate[0:3] == 'Aug'):
		tx1 = 690
		tx2 = 995
	if(labdate[0:3] == 'Sep'):
		tx1 = 655
		tx2 = 1010
	if(labdate[0:3] == 'Oct'):
		tx1 = 685
		tx2 = 1010
	if(labdate[0:3] == 'Nov'):
		tx1 = 664
		tx2 = 1013
	if(labdate[0:3] == 'Dec'):
		tx1 = 664
		tx2 = 1013
	

	fnt4 = ImageFont.truetype(fntpathb, 26)
	text = "Outlook for "+labdate
	draw.text((tx1,855), text, (0,0,0), font=fnt4)
	fnt5 = ImageFont.truetype(fntpath, 26)
	text2 = '(Issued '+idate+')'
	draw.text((tx2,854), text2, (0,0,0), font=fnt5)
	
	
	img_path = './Images/Precipitation/'+imgsize.lower()+'/'
	img_name = 'precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'hd--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
	pngfile = img_path+img_name
	print("Saving "+pngfile)
	hdim.save(pngfile)


if(imgsize == 'HDSD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1150,700)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (384,108))
	
	draw = ImageDraw.Draw(hdim)
	
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fntpathb = './Fonts/Trebuchet_MS_Bold.ttf'

	#Add the colorbar
	cbar_orig = Image.open('precipoutlook-cpc-legend-HD.png')
	bbox = (1,1,1767,229)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_orig, (154,810))

	
	
	if(labdate[0:3] == 'Jan'):
		tx1 = 685
		tx2 = 1010
	if(labdate[0:3] == 'Feb'):
		tx1 = 672
		tx2 = 1006
	if(labdate[0:3] == 'Mar'):
		tx1 = 695
		tx2 = 993
	if(labdate[0:3] == 'Apr'):
		tx1 = 700
		tx2 = 983
	if(labdate[0:3] == 'May'):
		tx1 = 710
		tx2 = 980
	if(labdate[0:3] == 'Jun'):
		tx1 = 698
		tx2 = 980
	if(labdate[0:3] == 'Jul'):
		tx1 = 708
		tx2 = 981
	if(labdate[0:3] == 'Aug'):
		tx1 = 690
		tx2 = 995
	if(labdate[0:3] == 'Sep'):
		tx1 = 655
		tx2 = 1010
	if(labdate[0:3] == 'Oct'):
		tx1 = 685
		tx2 = 1010
	if(labdate[0:3] == 'Nov'):
		tx1 = 664
		tx2 = 1013
	if(labdate[0:3] == 'Dec'):
		tx1 = 664
		tx2 = 1013
	
	

	fnt4 = ImageFont.truetype(fntpathb, 26)
	text = "Outlook for "+labdate
	draw.text((tx1,815), text, (0,0,0), font=fnt4)
	fnt5 = ImageFont.truetype(fntpath, 26)
	text2 = '(Issued '+idate+')'
	draw.text((tx2,814), text2, (0,0,0), font=fnt5)
	
	
	img_path = './Images/Precipitation/'+imgsize.lower()+'/'
	img_name = 'precipoutlook-monthly-cpc--'+imgw+'x'+imgh+'hdsd--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
	pngfile = img_path+img_name
	print("Saving "+pngfile)
	hdim.save(pngfile)

'''
cmd = 'rm ./Data/*'
subprocess.call(cmd,shell=True)
'''
cmd = 'rm ./*.zip'
subprocess.call(cmd,shell=True)

