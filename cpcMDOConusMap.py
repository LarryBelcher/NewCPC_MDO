#!/usr/bin/python

import pyproj
import glob
import shapefile
import sys
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
    dbf = dfile + '.dbf'
    table = DBF(dbf, load=True)
    idate = str(table.records[0]['Fcst_Date'])
    idp = idate.split('/')
    idyyyy = idp[2]
    mm = idp[0]


imgsize = sys.argv[2]  # (expects small, large)


path = './Fonts/SourceSansPro-Italic.ttf'
propi = font_manager.FontProperties(fname=path)


if(imgsize == 'small'):
    figxsize = 8.62
    figysize = 5.56
    figdpi = 72
    lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
    logo_image = './noaa_logo_42.png'
    logo_x = 566
    logo_y = 4
    framestat = 'False'
    base_img = './CONUS_620_BaseLayer.png'
    line_img = './CONUS_620_stateLines.png'
    bgcol = '#F5F5F5'
    cmask = "./Custom_mask.png"
    outpng = "conus_map-small.png"

if(imgsize == 'large'):
    figxsize = 13.89
    figysize = 8.89
    figdpi = 72
    lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
    logo_image = './noaa_logo_42.png'
    logo_x = 946
    logo_y = 4
    framestat = 'False'
    base_img = './CONUS_1000_BaseLayer.png'
    line_img = './CONUS_1000_stateLines.png'
    bgcol = '#F5F5F5'
    cmask = "./Custom_mask.png"
    outpng = "conus_map-large.png"

if(imgsize == 'DIY'):
    # Switch everything to 'GEO', but only output a png
    imgsize = 'GEO'
    '''
	figxsize = 13.655
	figysize = 8.745
	figdpi = 300
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_DIY_BaseLayer.png'
	line_img = './CONUS_DIY_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"
	'''

if(imgsize == 'HD'):
    figxsize = 21.33
    figysize = 10.25
    figdpi = 72
    lllon, lllat, urlon, urlat = [-126.95182, 19.66787, -52.88712, 46.33016]
    logo_image = './noaa_logo_100.png'
    logo_x = 1421
    logo_y = 35
    framestat = 'True'
    base_img = './CONUS_HD_BaseLayer.png'
    line_img = './CONUS_HD_stateLines.png'
    framestat = 'False'
    bgcol = '#F5F5F5'
    cmask = "./Custom_HD_mask.png"

if(imgsize == 'HDSD'):
    figxsize = 16
    figysize = 9.75
    figdpi = 72
    lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
    logo_image = './noaa_logo_100.png'
    logo_x = 1037
    logo_y = 35
    framestat = 'True'
    base_img = './CONUS_HDSD_BaseLayer.png'
    line_img = './CONUS_HDSD_stateLines.png'
    framestat = 'False'
    bgcol = '#F5F5F5'
    cmask = "./Custom_HDSD_mask.png"


if(imgsize == 'GEO'):
    figxsize = 13.655
    figysize = 8.745
    figdpi = 300
    # lllon, lllat, urlon, urlat = [-179.9853516, 14.9853516, -59.9853516,
    # 74.9853516]
    lllon, lllat, urlon, urlat = [-179.9999, 15.0, -60.0, 75.0]
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

# Set up the base map for everything except the geotif
if(imgsize != 'GEO'):
    # Create Map and Projection Coordinates
    kwargs = {'epsg': '5070',
              'resolution': 'i',
              'llcrnrlon': lllon,
              'llcrnrlat': lllat,
              'urcrnrlon': urlon,
              'urcrnrlat': urlat,
              'lon_0': -96.,
              'lat_0': 23.,
              'lat_1': 29.5,
              'lat_2': 45.5,
                      'area_thresh': 15000,
                      'ax': ax1,
                      'fix_aspect': False
              }


# Set up the base map for the geotif
if(imgsize == 'GEO'):
    # Create Map and Projection Coordinates
    kwargs = {'epsg': '4326',
              'resolution': 'i',
              'llcrnrlon': lllon,
              'llcrnrlat': lllat,
              'urcrnrlon': urlon,
              'urcrnrlat': urlat,
              'lon_0': -119.9853516,
              'lat_0': 44.9853516,
                      'area_thresh': 15000,
                      'ax': ax1,
                      'fix_aspect': False
              }


# Set up the Basemap
m = Basemap(**kwargs)

if(imgsize == 'small'):
    plt.figtext(0.00433, 0.0125, 'AK and HI not to scale',
                size=11, style='italic', color='#8D8D8D')
if(imgsize == 'large'):
    plt.figtext(0.00433, 0.0125, 'AK and HI not to scale',
                size=18, style='italic', color='#8D8D8D')


# Add the BaseLayer image 1st pass
outline_im = Image.open(base_img)
m.imshow(outline_im, origin='upper', aspect='auto')

if(dfile != 'ND'):
    # Now read in the CPC Shapes and fill the basemap
    r = shapefile.Reader(dfile)
    shapes = r.shapes()
    records = r.records()
    fields = r.fields[1:]
    # print(fields)

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
        
        if(int(idyyyy) < 2024):
            eastings, northings = zip(*shape.points)
            orgproj = pyproj.Proj(init='esri:102003')
            wgs84 = pyproj.Proj(init='epsg:4326')
            lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            data = np.array(m(lons, lats)).T
        
        if(int(idyyyy) >= 2024):
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
        
        if(int(int(idyyyy) >= 2024)):
            col = dict1[record.Outlook]
            edgcol = dict1[record.Outlook]
        if(int(idyyyy) < 2024):
            col = '#ffffff'
            edgcol = '#ffffff'
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


# Add the custom mask
omask_im = Image.open(cmask)
m.imshow(omask_im, origin='upper', alpha=10., zorder=1,
         aspect='auto', interpolation='nearest')
# Add the Line image
outline_im = Image.open(line_img)
m.imshow(outline_im, origin='upper', alpha=1.0, zorder=10, aspect='auto')


if(imgsize == 'GEO'):
    m.drawlsmask(land_color='#b2b2b2', ocean_color='#f5f5f5')
    shp_info = m.readshapefile('Shapefiles/cb_2017_us_state_500k',
                               'states', drawbounds=True, color='#767676', zorder=10)
    statenames = []
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        statenames.append(statename)


# Add the NOAA logo (except for DIY)
if(imgsize == 'small' or imgsize == 'large' or imgsize == 'HD' or imgsize == 'HDSD'):
    logo_im = Image.open(logo_image)
    height = logo_im.size[1]
    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255 for the logo
    logo_im = np.array(logo_im).astype(np.float) / 255
    fig.figimage(logo_im, logo_x, logo_y, zorder=10)


plt.savefig(outpng, dpi=figdpi, orientation='landscape',
            transparent='false', bbox_inches='tight', pad_inches=0.00)
