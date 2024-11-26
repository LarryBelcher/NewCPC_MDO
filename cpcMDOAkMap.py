#!/usr/bin/python

import pyproj
import glob
import shapefile
import sys, subprocess
import os
from matplotlib.patches import Polygon
from matplotlib.patches import Path, PathPatch
from dbfread import DBF
from pyproj import Proj, transform
from PIL import Image
import matplotlib.font_manager as font_manager
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.use('Agg')


dfile = sys.argv[1]
# dfile = glob.glob('./Data/*_temp.prj')
# dfile = dfile[0].split('.prj')[0]

if(dfile == 'ND'):
	labeldate = 'No Data'
	mm = '00'


if(dfile != 'ND'):
	dbf = dfile+'.dbf'
	table = DBF(dbf, load=True)
	idate = str(table.records[0]['Fcst_Date'])
	idp = idate.split('/')
	idyyyy = idp[2]
	mm = idp[0]


imgsize = sys.argv[2]  # (expects small or large)



path = './Fonts/SourceSansPro-Italic.ttf'
propi = font_manager.FontProperties(fname=path)




figxsize = 8.62
figysize = 5.56
figdpi = 72
# lllon, lllat, urlon, urlat = [-179.9853516, 14.9853516, -59.9853516, 74.9853516]
lllon, lllat, urlon, urlat = [-180., 51., -129., 72.]
framestat = 'False'
base_img = './trans.tif'
bgcol = 'none'


fig = plt.figure(figsize=(figxsize, figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=framestat)  # , axisbg=bgcol)
ax1.spines['left'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)


if(imgsize == 'small'):
	m = Basemap(width=3225250,height=2800000, resolution='i',projection='aea', area_thresh = 1500000, fix_aspect = False, lat_1=65.,lat_2=69.,lon_0=-155.5,lat_0=62.)
	#Below is original, but was very distorted
	#m = Basemap(width=4250250,height=2800000, resolution='i',projection='aea', area_thresh = 1500000, fix_aspect = False, lat_1=65.,lat_2=69.,lon_0=-159.,lat_0=62.)
	

if(imgsize == 'large'):
	m = Basemap(width=3225250,height=2800000, resolution='i',projection='aea', area_thresh = 1500000, fix_aspect = False, lat_1=65.,lat_2=69.,lon_0=-155.5,lat_0=62.)
	#Below is original, but HI was very distorted
	#m = Basemap(width=4250250,height=2800000, resolution='i',projection='aea', area_thresh = 1500000, fix_aspect = False, lat_1=65.,lat_2=69.,lon_0=-159.,lat_0=62.)


m.drawmeridians(np.arange(int(-180),int(-179),1), color='#f5f5f5', linewidth=9., dashes=[1,0])
m.fillcontinents(color='#e3e3e3', zorder=9, ax=ax1)

if(dfile != 'ND'):
	# Now read in the CPC Shapes and fill the basemap
	r = shapefile.Reader(dfile)
	shapes = r.shapes()
	records = r.records()





if(mm != '00'):
    
    # Fill States w/ dark grey "No Drought"
    shp_info = m.readshapefile('Shapefiles/cb_2017_us_state_500k',
                               'states', drawbounds=True, color='#767676', zorder=8)
    for nshape, seg in enumerate(m.states):
        poly = Polygon(seg, facecolor='#ffffff',
                       edgecolor='#ffffff', linewidth=0.1, zorder=8)
        ax1.add_patch(poly)
    

# Now fill the ploy's with appropriate color
    dict1 = {'No_Drought': '#ffffff', 'Development': '#ffdd63',
             'Persistence': '#9b634a', 'Improvement': '#ded2bd', 'Removal': '#b3ae69'}

    for record, shape in zip(records, shapes):
        
        if(int(idyyyy) << 2024):
            eastings, northings = zip(*shape.points)
            orgproj = pyproj.Proj(init='esri:102003')
            wgs84 = pyproj.Proj(init='epsg:4326')
            lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            data = np.array(m(lons, lats)).T
        
        if(int(int(idyyyy) >= 2024)):
            lons, lats = zip(*shape.points)
            data = np.array(m(lons, lats)).T

        if len(shape.parts) == 1:
            segs = [data, ]
        else:
            segs = []
            for i in range(1, len(shape.parts)):
                index = shape.parts[i - 1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])

            # assuming that the longest segment is the enclosing
            # line and ordering the segments by length:
            lens = np.array([len(s) for s in segs])
            order = lens.argsort()[::-1]
            segs = [segs[i] for i in order]

        lines = LineCollection(segs, antialiaseds=(1,), zorder=9)
        
        if(int(idyyyy) >= 2024):
            col = dict1[record.Outlook]
            edgcol = dict1[record.Outlook]
        if(int(idyyyy) < 2024):
            col = '#000000'
            edgcol = '#000000'
            vals = [record[0], record[1], record[2], record[5]]
            vtest = [i for i, j in enumerate(vals) if j == max(vals)]
            vtest = vtest[0]
            if(vtest == 3):
                col = '#b3ae69'
                edgcol = '#b3ae69'
            if(vtest == 2):
                col = '#ffdd63'
                edgcol = '#ffdd63'
            if(vtest == 1):
                col = '#9b634a'
                edgcol = '#9b634a'
            if(vtest == 0):
                col = '#ded2bd'
                edgcol = '#ded2bd'

        lines.set_edgecolor(edgcol)
        lines.set_linewidth(1.0)
        lines.set_zorder(9)
        ax1.add_collection(lines)

        # producing a path from the line segments:
        segs_lin = [v for s in segs for v in s]
        codes = [[Path.MOVETO]+[Path.LINETO for p in s[1:]] for s in segs]
        codes_lin = [c for s in codes for c in s]
        path = Path(segs_lin, codes_lin)
        # patch = PathPatch(path, facecolor="#abc0d3", lw=0, zorder = 3)
        patch = PathPatch(path, facecolor=col, lw=0, zorder=9)
        ax1.add_patch(patch)


m.drawlsmask(land_color='#e3e3e3', ocean_color='#f5f5f5')


shp_info = m.readshapefile('Shapefiles/cb_2017_us_state_500k','states', drawbounds=True, color='#525252', zorder=10)
statenames = []
for shapedict in m.states_info:
	statename = shapedict['NAME']
	statenames.append(statename)
for nshape,seg in enumerate(m.states):
	if statenames[nshape] in ['Alaska']:
		poly = Polygon(seg, facecolor='#e3e3e3',edgecolor='#525252', linewidth=0.3, zorder=7)
		ax1.add_patch(poly)




tmppng = "tmpalaska_map.png"

plt.savefig(tmppng, dpi=figdpi, orientation='landscape', transparent='false', bbox_inches='tight', pad_inches=0.00)


#Resize the previous output to match aspect ratio of inset
img = Image.open(tmppng)
img = img.resize((500, 400), Image.ANTIALIAS)
img.save("alaska_map.png")

if(imgsize == 'small'):
	img2 = Image.open("alaska_map.png")
	img2 = img2.resize((184, 147), Image.ANTIALIAS)
	img2.save("ak-inset-small.png")

if(imgsize == 'large'):
	img2 = Image.open("alaska_map.png")
	img2 = img2.resize((297, 237), Image.ANTIALIAS)
	img2.save("ak-inset-large.png")

#cleanup
cmd = 'rm '+tmppng+" alaska_map.png"
subprocess.call(cmd,shell=True) 