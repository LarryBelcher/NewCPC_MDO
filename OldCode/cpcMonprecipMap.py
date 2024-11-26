#!/usr/bin/python

import glob
import shapefile
import sys
import os
from matplotlib.patches import Polygon
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


dbf = dfile+'.dbf'
table = DBF(dbf, load=True)
idate = str(table.records[0]['Fcst_Date'])
idp = idate.split('-')
idyyyy = idp[0]
mm = idp[1]


imgsize = sys.argv[2]  # (expects 620, 1000, DIY, HD, or HDSD)


path = './Fonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = './Fonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
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

if(imgsize == '1000'):
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

if(imgsize == 'DIY'):
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


# Add the BaseLayer image 1st pass
outline_im = Image.open(base_img)
m.imshow(outline_im, origin='upper', aspect='auto')


# Now read in the CPC Shapes and fill the basemap
r = shapefile.Reader(dfile)
shapes = r.shapes()
records = r.records()


# First fill all poly's with white
if(mm != '00'):
    for record, shape in zip(records, shapes):
        lons, lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T

        if len(shape.parts) == 1:
            segs = [data, ]
        else:
            segs = []
            for i in range(1, len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])

        lines = LineCollection(segs, antialiaseds=(1,))

        col = '#ffffff'
        lines.set_facecolors(col)
        lines.set_edgecolors(col)
        lines.set_linewidth(1.0)
        lines.set_zorder(10)
        ax1.add_collection(lines)


# Now fill the above/below ploy's with appropriate color
if(mm != '00'):
    for record, shape in zip(records, shapes):
        lons, lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T

        if len(shape.parts) == 1:
            segs = [data, ]
        else:
            segs = []
            for i in range(1, len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])

        lines = LineCollection(segs, antialiaseds=(1,))
        # Now obtain the data in a given poly and assign a color to the value
        dval = int(float(record[2]))

        col = '#ffffff'
        if(record[3] == 'Above'):
            if(dval >= 70):
                col = '#005953'
            if(dval == 60):
                col = '#05877f'
            if(dval == 50):
                col = '#11ab94'
            if(dval == 40):
                col = '#78ccb0'
            if(dval == 33):
                col = '#b1e0d1'
            lines.set_facecolors(col)
            lines.set_edgecolors(col)
            lines.set_linewidth(1.0)
            lines.set_zorder(10)
            ax1.add_collection(lines)

        if(record[3] == 'Below'):
            if(dval >= 70):
                col = '#803621'
            if(dval == 60):
                col = '#994c37'
            if(dval == 50):
                col = '#ba6a3f'
            if(dval == 40):
                col = '#d9a55d'
            if(dval == 33):
                col = '#f0d49c'

            lines.set_facecolors(col)
            lines.set_edgecolors(col)
            lines.set_linewidth(1.0)
            lines.set_zorder(10)
            ax1.add_collection(lines)

            if(record[3] == 'EC'):
                col = '#ffffff'
                lines.set_facecolors(col)
                lines.set_edgecolors(col)
                lines.set_linewidth(1.0)
                lines.set_zorder(10)
                ax1.add_collection(lines)


if(imgsize != 'GEO'):
    # Add the custom mask
    omask_im = Image.open(cmask)
    m.imshow(omask_im, origin='upper', alpha=1., zorder=10,
             aspect='auto', interpolation='nearest')

    # Add the Line image
    outline_im = Image.open(line_img)
    #m.imshow(outline_im, origin='upper', alpha=1.0, zorder=10, aspect='auto')
    m.imshow(outline_im, origin='upper', alpha=1.0, zorder=10)


if(imgsize == 'GEO'):
    m.drawlsmask(land_color='#e3e3e3', ocean_color='#f5f5f5')
    shp_info = m.readshapefile('Shapefiles/cb_2017_us_state_500k',
                               'states', drawbounds=True, color='#525252', zorder=10)
    statenames = []
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        statenames.append(statename)
    for nshape, seg in enumerate(m.states):
        if statenames[nshape] in ['Hawaii']:
            poly = Polygon(seg, facecolor='#e3e3e3',
                           edgecolor='#525252', linewidth=0.3, zorder=10)
            ax1.add_patch(poly)

# Add the NOAA logo (except for DIY)
if(imgsize == '620' or imgsize == '1000' or imgsize == 'HD' or imgsize == 'HDSD'):
    logo_im = Image.open(logo_image)
    height = logo_im.size[1]
    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255 for the logo
    logo_im = np.array(logo_im).astype(np.float) / 255
    fig.figimage(logo_im, logo_x, logo_y, zorder=10)


outpng = "temporary_map.png"
outtif = "temporary_map.tif"

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
    plt.savefig(outpng, dpi=figdpi, orientation='landscape',
                bbox_inches='tight', pad_inches=0.00)

if(imgsize == 'HD' or imgsize == 'HDSD'):
    # , bbox_inches='tight', pad_inches=0.01)
    plt.savefig(outpng, dpi=figdpi, orientation='landscape')

if(imgsize == 'GEO'):
    plt.savefig(outpng, dpi=figdpi, orientation='landscape',
                transparent='true', bbox_inches='tight', pad_inches=0.00)
