#!/usr/bin/python

import pyproj, glob, shapefile, sys, os, subprocess
from matplotlib.patches import Polygon
from matplotlib.patches import Path, PathPatch
from pyproj import Proj, transform
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from simplekml import (Kml, OverlayXY, ScreenXY, Units, RotationXY, AltitudeMode, Camera)
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
            'description', 'Climate.gov Monthly Drought Outlook; Data: CPC')
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

def add1(mc):
    if(mc == '01'): mm = '02'
    if(mc == '02'): mm = '03'
    if(mc == '03'): mm = '04'
    if(mc == '04'): mm = '05'
    if(mc == '05'): mm = '06'
    if(mc == '06'): mm = '07'
    if(mc == '07'): mm = '08'
    if(mc == '08'): mm = '09'
    if(mc == '09'): mm = '10'
    if(mc == '10'): mm = '11'
    if(mc == '11'): mm = '12'
    if(mc == '12'): mm = '01'
    return mm


if __name__ == "__main__":

    dfile = sys.argv[1]
    
    cmd = 'stat /work/NewCPC_MDO/Data/DO_Merge_Clip.dbf | grep Modify'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
    output = proc.communicate()[0]; output = str(output)
    
    fdate = output.split(' ')[1]
    yyyy = fdate.split('-')[0]
    mtime = fdate.split('-')[1]
    mday = fdate.split('-')[2]
    mm = add1(mtime)
    dd = '00'
    if(mm == '01'): yyyy = str(int(yyyy)+1)
    mmm = mm
    ms = int2str(mmm)
   
    
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

#Make the transparent version of the map
    # Set up the Basemap
    m1 = Basemap(**kwargs)
    
    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()
    
    if(mm != '00'):
        
        # Fill States w/ white "No Drought"
        shp_info = m1.readshapefile('/work/CPC_MDO/Shapefiles/cb_2017_us_state_500k', 'states', drawbounds=True, color=(1.0,1.0,1.0,0.8), zorder=8)
        for nshape, seg in enumerate(m1.states):
            poly = Polygon(seg, facecolor=(1.0,1.0,1.0,0.8), edgecolor=(1.0,1.0,1.0,0.8), linewidth=0.1, zorder=8)
            ax1.add_patch(poly)


        # Now fill the ploy's with appropriate color
        for record, shape in zip(records, shapes):
            #eastings, northings = zip(*shape.points)
            #orgproj = pyproj.Proj(init='esri:102003')
            #wgs84 = pyproj.Proj(init='epsg:4326')
            #lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            
            #data = np.array(m1(lons, lats)).T

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

               # assuming that the longest segment is the enclosing
                # line and ordering the segments by length:
                lens = np.array([len(s) for s in segs])
                order = lens.argsort()[::-1]
                segs = [segs[i] for i in order]
            
            lines = LineCollection(segs, antialiaseds=(1,), zorder=9)
            # Now obtain the data in a given poly and assign a color to the value

            '''
            col = (1.0,1.0,1.0,0.8)
            vals = [record[0], record[1], record[2], record[5]]
            vtest = [i for i, j in enumerate(vals) if j == max(vals)]
            vtest = vtest[0]
            if(vtest == 3):
               col = (0.7019607843137254,0.6823529411764706,0.4117647058823529,0.8)
               edgcol = (0.7019607843137254,0.6823529411764706,0.4117647058823529,0.)
            if(vtest == 2):
                col = (1.0,0.8666666666666667,0.38823529411764707,0.8)
                edgcol = (1.0,0.8666666666666667,0.38823529411764707,0.)
            if(vtest == 1):
                col = (0.6078431372549019,0.38823529411764707,0.2901960784313726,0.8)
                edgcol = (0.6078431372549019,0.38823529411764707,0.2901960784313726,0.)
            if(vtest == 0):
                col = (0.8705882352941177,0.8235294117647058,0.7411764705882353,0.8)
                edgcol = (0.8705882352941177,0.8235294117647058,0.7411764705882353,0.)
            '''
            col0 = (1.0,1.0,1.0,0.8)
            col1 = (1.0,0.8666666666666667,0.38823529411764707,0.8)
            col2 = (0.6078431372549019,0.38823529411764707,0.2901960784313726,0.8)
            col3 = (0.8705882352941177,0.8235294117647058,0.7411764705882353,0.8)
            col4 = (0.7019607843137254,0.6823529411764706,0.4117647058823529,0.8)
            
            dict1={'No_Drought': col0, 'Development': col1, 'Persistence': col2, 'Improvement': col3, 'Removal': col4}
            col = dict1[record.Outlook]
            edgcol = dict1[record.Outlook]

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
        

    ofile = 'Drought--Monthly--Drought-Outlook--US--'+yyyy+'-'+mm+'-'+dd+'_'
    altfile = 'Outlook--Monthly--Drought--US--'+yyyy+'-'+mm+'-'+dd+'_'
    

    fig1.savefig(ofile+'transparent.png', transparent='True')    
    fig1.savefig(altfile+'transparent.png', transparent='True')

    
    # Set up the Basemap
    m = Basemap(**kwargs)

    #Make the opaque version of the map
    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()

    if(mm != '00'):
        # Fill States w/ white "No Drought"
        shp_info = m.readshapefile('/work/CPC_MDO/Shapefiles/cb_2017_us_state_500k', 'states', drawbounds=True, color='#767676', zorder=8)
        for nshape, seg in enumerate(m.states):
            poly = Polygon(seg, facecolor='#ffffff', edgecolor='#ffffff', linewidth=0.1, zorder=8)
            ax.add_patch(poly)
        
        # Now fill the ploy's with appropriate color
        for record, shape in zip(records, shapes):
            #eastings, northings = zip(*shape.points)
            #orgproj = pyproj.Proj(init='esri:102003')
            #wgs84 = pyproj.Proj(init='epsg:4326')
            #lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            
            #data = np.array(m(lons, lats)).T
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

               # assuming that the longest segment is the enclosing
                # line and ordering the segments by length:
                lens = np.array([len(s) for s in segs])
                order = lens.argsort()[::-1]
                segs = [segs[i] for i in order]
            
            lines = LineCollection(segs, antialiaseds=(1,), zorder=9)
            # Now obtain the data in a given poly and assign a color to the value

            dict1={'No_Drought': '#ffffff', 'Development': '#ffdd63', 'Persistence': '#9b634a', 'Improvement': '#ded2bd', 'Removal': '#b3ae69'}

            col = dict1[record.Outlook]
            edgcol = dict1[record.Outlook]

            lines.set_edgecolor(edgcol)
            lines.set_linewidth(1.0)
            lines.set_zorder(9)
            ax.add_collection(lines)
            
            # producing a path from the line segments:
            segs_lin = [v for s in segs for v in s]
            codes = [[Path.MOVETO]+[Path.LINETO for p in s[1:]] for s in segs]
            codes_lin = [c for s in codes for c in s]
            path = Path(segs_lin, codes_lin)
            # patch = PathPatch(path, facecolor="#abc0d3", lw=0, zorder = 3)
            patch = PathPatch(path, facecolor=col, lw=0, zorder=9)
            ax.add_patch(patch)



    fig.savefig(ofile+'opaque.png', transparent='False')  
    fig.savefig(altfile+'opaque.png', transparent='False')


        
    

    #Now make the kmz's
    ###Create Drought... version
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'], 
                kmzfile=ofile+'transparent.kmz', name='Monthly Drought Outlook for '+ms+', '+yyyy)

    
    cmd = "unzip "+ofile+"transparent.kmz 'doc.kml' > "+ofile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'opaque.png'], 
                kmzfile=ofile+'opaque.kmz', name='Monthly Drought Outlook for '+ms+', '+yyyy)
    
    cmd = "unzip "+ofile+"opaque.kmz 'doc.kml'> "+ofile+"opaque.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+ofile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'cp mdo-kml-legend.png '+ofile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+ofile+'KML-assets.zip '+ofile+'transparent.kml '+ofile+'opaque.kml '+ofile+'legend.png files/Drought*'
    subprocess.call(cmd, shell=True)


    #Create Outlook... version
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[altfile+'transparent.png'], 
                kmzfile=altfile+'transparent.kmz', name='Monthly Drought Outlook for '+ms+', '+yyyy)

    
    cmd = "unzip "+altfile+"transparent.kmz 'doc.kml' > "+altfile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+altfile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[altfile+'opaque.png'], 
                kmzfile=altfile+'opaque.kmz', name='Monthly Drought Outlook for '+ms+', '+yyyy)
    
    cmd = "unzip "+altfile+"opaque.kmz 'doc.kml'> "+altfile+"opaque.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+altfile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+altfile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'cp mdo-kml-legend.png '+altfile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+altfile+'KML-assets.zip '+altfile+'transparent.kml '+altfile+'opaque.kml '+altfile+'legend.png files/Outlook*'
    subprocess.call(cmd, shell=True)

    
'''
    
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Drought*KML-assets.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Drought--Monthly--Drought-Outlook--US/05-kml/'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Outlook*KML-assets.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Outlook--Monthly--Drought--US/05-kml/'
    subprocess.call(cmd, shell=True)


    #Cleanup
    cmd = 'rm *.zip'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kml'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kmz'
    subprocess.call(cmd, shell=True)
    cmd = 'rm -rf files/'
    subprocess.call(cmd, shell=True)
    cmd = 'rm Drought--Monthly--Drought-Outlook--US*.png'
    subprocess.call(cmd, shell=True)
    cmd = 'rm Outlook--Monthly--Drought--US*.png'
    subprocess.call(cmd, shell=True)
    
'''