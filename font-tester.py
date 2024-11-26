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




imgsize = 'full_res_zips'


if(imgsize == 'full_res_zips'):
	
	cbar_image = './cpcMonTempLegend.png'
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
	cbar_name = 'Temperature--Monthly--Average--CONUS--'+yyyy+'-'+fnmm+'-'+iddd+'--colorbar.eps'


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
	bbox = (1,1,407,13)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	nsx = int((new_size[0]-old_size[0])/2); nsy = int((new_size[1]-old_size[1])/2)
	cbar_im.paste(cbar_orig, (nsx,nsy))
	cbar_im = np.array(cbar_im).astype(np.float) / 255
	fig.figimage(cbar_im, cbar_x, cbar_y)

	path = './Fonts/SourceSansPro-Regular.ttf'
	font = font_manager.FontProperties(fname=path)
	font.set_family('Trebuchet MS')
	font.set_style('normal')
	font.set_size(fsiz1)
	font.set_weight('bold')
	plt.text(t1x, t1y, "Probability (percent chance)", fontproperties=font, size=fsiz1, color='#333333')

	subtxt = "cooler than normal            equal chances           warmer than normal"
	font.set_style('italic')
	font.set_weight('normal')
	plt.text(t2x, t2y, subtxt, fontproperties=font, color='#333333')

	font.set_style('normal')
	plt.text(t3x, t3y+0.1, 'Temperature Outlook', fontproperties=propr, size=fsiz2, color='#8D8D8D')
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
	
	cmd1 = 'zip tempoutlook-monthly-cpc--'+imgw+'x2623--'+yyyy+'-'+fnmm+'-'+iddd+'.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	subprocess.call(cmd1,shell=True)
	cmd2 = 'mv tempoutlook-monthly-cpc--'+imgw+'x2623--'+yyyy+'-'+fnmm+'-'+iddd+'.zip '+img_path
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
	cbar_orig = Image.open('tempoutlook-cpc-legend-HD.png')
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
	
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'tempoutlook-monthly-cpc--'+imgw+'x'+imgh+'hd--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
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
	cbar_orig = Image.open('tempoutlook-cpc-legend-HD.png')
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
	
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'tempoutlook-monthly-cpc--'+imgw+'x'+imgh+'hdsd--'+yyyy+'-'+fnmm+'-'+iddd+'.png'
	pngfile = img_path+img_name
	print("Saving "+pngfile)
	hdim.save(pngfile)


#cmd = 'rm ./Data/*'
#subprocess.call(cmd,shell=True)
cmd = 'rm /work/CPC_Monthly/*.zip'
subprocess.call(cmd,shell=True)

