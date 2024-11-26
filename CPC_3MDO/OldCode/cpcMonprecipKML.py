#!/usr/bin/python

import pyproj
import glob
import shapefile
import sys
import os
import subprocess
from matplotlib.patches import Polygon
from matplotlib.patches import Path, PathPatch
from pyproj import Proj, transform
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from simplekml import (Kml, OverlayXY, ScreenXY, Units,
                       RotationXY, AltitudeMode, Camera)
import matplotlib.font_manager as font_manager
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
# from dbfread import DBF

mpl.rcParams['savefig.pad_inches'] = 0


def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):

    kml = Kml()
    altitude = kw.pop('altitude', 2e7)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=np.mean([urcrnrlat, llcrnrlat]),
                    longitude=np.mean([urcrnrlon, llcrnrlon]),
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', 'overlay')
        ground.color = kw.pop('color', '9effffff')
        ground.latlonbox.rotation = kw.pop('rotation', 0)
        ground.description = kw.pop(
            'description', 'Climate.gov Monthly Precipitation Outlook; Data: CPC')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToSeaFloor')
        ground.icon.href = fig
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.015, y=0.075,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    filename = figs[0].split('.png')[0]+'.kmz'
    kmzfile = kw.pop('kmzfile', figs[0])
    kml.savekmz(kmzfile)


def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi/180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.

    fig = plt.figure(figsize=figsize, frameon=False, dpi=pixels//10)

    # KML friendly image.  If using basemap try: `fix_aspect=False`.
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    ax.axis('off')
    return fig, ax


def int2str(mmi):
    if(mmi == '00'):
        ms = 'No Data'
    if(mmi == '01'):
        ms = 'January'
    if(mmi == '02'):
        ms = 'February'
    if(mmi == '03'):
        ms = 'March'
    if(mmi == '04'):
        ms = 'April'
    if(mmi == '05'):
        ms = 'May'
    if(mmi == '06'):
        ms = 'June'
    if(mmi == '07'):
        ms = 'July'
    if(mmi == '08'):
        ms = 'August'
    if(mmi == '09'):
        ms = 'September'
    if(mmi == '10'):
        ms = 'October'
    if(mmi == '11'):
        ms = 'November'
    if(mmi == '12'):
        ms = 'December'
    return ms


def add1(mc):
    if(mc == '01'):
        mm = '02'
    if(mc == '02'):
        mm = '03'
    if(mc == '03'):
        mm = '04'
    if(mc == '04'):
        mm = '05'
    if(mc == '05'):
        mm = '06'
    if(mc == '06'):
        mm = '07'
    if(mc == '07'):
        mm = '08'
    if(mc == '08'):
        mm = '09'
    if(mc == '09'):
        mm = '10'
    if(mc == '10'):
        mm = '11'
    if(mc == '11'):
        mm = '12'
    if(mc == '12'):
        mm = '01'
    return mm


if __name__ == "__main__":

    dfile = sys.argv[1]
    idate = sys.argv[2]
    labdate = sys.argv[3]
    yyyy = idate[:4]
    mm = idate[5:7]

    path = './Fonts/Trebuchet_MS.ttf'
    propr = font_manager.FontProperties(fname=path)
    path = './Fonts/Trebuchet_MS_Bold.ttf'
    propb = font_manager.FontProperties(fname=path)

    pixels = 1024 * 10

    lllon, lllat, urlon, urlat = [-179.9999, 15.0, -60.0, 75.0]

    fig, ax = gearth_fig(llcrnrlon=lllon,
                         llcrnrlat=lllat,
                         urcrnrlon=urlon,
                         urcrnrlat=urlat,
                         pixels=pixels)

    fig1, ax1 = gearth_fig(llcrnrlon=lllon,
                           llcrnrlat=lllat,
                           urcrnrlon=urlon,
                           urcrnrlat=urlat,
                           pixels=pixels)

    kwargs = {'epsg': '4326',
              'resolution': 'i',
              'llcrnrlon': lllon,
              'llcrnrlat': lllat,
              'urcrnrlon': urlon,
              'urcrnrlat': urlat,
              'lon_0': -119.9853516,
              'lat_0': 44.9853516,
              'area_thresh': 15000,
                      'ax': ax,
                      'fix_aspect': False
              }

# Make the transparent version of the map
    # Set up the Basemap
    m1 = Basemap(**kwargs)

    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()
    
    

    # Now fill the above/below ploy's with appropriate color
    if(mm != '00'):
        for record, shape in zip(records, shapes):
            lons, lats = zip(*shape.points)
            data = np.array(m1(lons, lats)).T

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
            col = (1.0, 1.0, 1.0, 0.8)

            if(record[3] == 'EC'):
                col = (1.0, 1.0, 1.0, 0.8)
                col1 = (1.0, 1.0, 1.0, 0.8)
                lines.set_facecolors(col)
                lines.set_edgecolors(col1)
                lines.set_linewidth(0.05)
                lines.set_zorder(9)
                ax1.add_collection(lines)
            
            
            if(record[3] == 'Above'):
                if(dval >= 70): col = (0.0, 0.34901960784313724, 0.3254901960784314, 0.5)
                if(dval == 60): col = (0.0196078431372549, 0.5294117647058824, 0.4980392156862745, 0.5)
                if(dval == 50): col = (0.06666666666666667, 0.6705882352941176, 0.5803921568627451, 0.5)
                if(dval == 40): col = (0.47058823529411764, 0.8, 0.6901960784313725, 0.5)
                if(dval == 33): col = (0.6941176470588235, 0.8784313725490196, 0.8196078431372549, 0.5)
                lines.set_facecolors(col)
                lines.set_edgecolors(col)
                lines.set_linewidth(0.05)
                lines.set_zorder(10)
                ax1.add_collection(lines)
            
            
            if(record[3] == 'Below'):
                if(dval >= 70): col = (0.5019607843137255, 0.21176470588235294, 0.12941176470588237, 0.5)
                if(dval == 60): col = (0.6, 0.2980392156862745, 0.21568627450980393, 0.5)
                if(dval == 50): col = (0.7294117647058823, 0.41568627450980394, 0.24705882352941178, 0.5)
                if(dval == 40): col = (0.8509803921568627, 0.6470588235294118, 0.36470588235294116, 0.5)
                if(dval == 33): col = (0.9411764705882353, 0.8313725490196079, 0.611764705882353, 0.5)
                lines.set_facecolors(col)
                lines.set_edgecolors(col)
                lines.set_linewidth(0.05)
                lines.set_zorder(10)
                ax1.add_collection(lines)
        
        
        

    ofile = 'Precipitation--Monthly--Outlook--US--'+idate+'_'
    altfile = 'Outlook--Monthly--Precipitation--US--'+idate+'_'

    fig1.savefig(ofile+'transparent.png', transparent='True')
    fig1.savefig(altfile+'transparent.png', transparent='True')


    # Set up the Basemap
    m = Basemap(**kwargs)

    # Make the opaque version of the map
    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()


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

            if(record[3] == 'EC'):
                col = '#ffffff'
                lines.set_facecolors(col)
                lines.set_edgecolors(col)
                lines.set_linewidth(1.0)
                lines.set_zorder(10)
                ax.add_collection(lines)

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
                ax.add_collection(lines)

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
                ax.add_collection(lines)


    ofile = 'Precipitation--Monthly--Outlook--US--'+idate+'_'
    altfile = 'Outlook--Monthly--Precipitation--US--'+idate+'_'

    fig.savefig(ofile+'opaque.png', transparent='False')
    fig.savefig(altfile+'opaque.png', transparent='False')


    # Now make the kmz's
    # Create "Temperature"... version
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'],
             kmzfile=ofile+'transparent.kmz', name='Monthly Precipitation Outlook for '+labdate+' '+yyyy)

    cmd = "unzip "+ofile+"transparent.kmz 'doc.kml' > "+ofile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'opaque.png'],
             kmzfile=ofile+'opaque.kmz', name='Monthly Precipitation Outlook for '+labdate+' '+yyyy)

    cmd = "unzip "+ofile+"opaque.kmz 'doc.kml'> "+ofile+"opaque.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+ofile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'cp precipoutlook-cpc-kml-legend.png '+ofile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+ofile+'KML-assets.zip '+ofile+'transparent.kml '+ofile+'opaque.kml '+ofile+'legend.png files/Precipitation--Monthly--Outlook*'
    subprocess.call(cmd, shell=True)

    cmd = 'rm -rf files/'
    subprocess.call(cmd, shell=True)

    # Create Outlook... version
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[altfile+'transparent.png'],
             kmzfile=altfile+'transparent.kmz', name='Monthly Precipitation Outlook for '+labdate+' '+yyyy)

    cmd = "unzip "+altfile+"transparent.kmz 'doc.kml' > "+altfile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+altfile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[altfile+'opaque.png'],
             kmzfile=altfile+'opaque.kmz', name='Monthly Precipitation Outlook for '+labdate+' '+yyyy)

    cmd = "unzip "+altfile+"opaque.kmz 'doc.kml'> "+altfile+"opaque.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+altfile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+altfile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'cp precipoutlook-cpc-kml-legend.png '+altfile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+altfile+'KML-assets.zip '+altfile+'transparent.kml '+altfile +'opaque.kml '+altfile+'legend.png files/Outlook--Monthly--Precipitation*'
    subprocess.call(cmd, shell=True)

    cmd = 'rm -rf files/'
    subprocess.call(cmd, shell=True)

    
    
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Precipitation--Monthly--Outlook*KML-assets.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Precipitation--Monthly--Outlook--US/05-kml/'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Outlook*KML-assets.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Outlook--Monthly--Precipitation--US/05-kml/'
    subprocess.call(cmd, shell=True)

    # Cleanup
    cmd = 'rm *.zip'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kml'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kmz'
    subprocess.call(cmd, shell=True)
    cmd = 'rm -rf files/'
    subprocess.call(cmd, shell=True)
    cmd = 'rm Precipitation--Monthly--Outlook*.png'
    subprocess.call(cmd, shell=True)
    cmd = 'rm Outlook--Monthly--Precipitation*.png'
    subprocess.call(cmd, shell=True)
    
    
    
