# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 12:22:50 2018

@author: Philipe_Leal
"""


#!/usr/bin/env python
'''
Convert a bunch of GDAL readable grids to a NetCDF Time Series.
Here we read a bunch of files that have names like:
/usgs/data0/prism/1890-1899/us_tmin_1895.01
/usgs/data0/prism/1890-1899/us_tmin_1895.02
...
/usgs/data0/prism/1890-1899/us_tmin_1895.12
'''

import numpy as np
import datetime as dt
import os
import gdal
import netCDF4
import re

Mother_directory_path = r'C:\Doutorado\1Trimestre\Geoprocessamento\LT_All_sat\MADT_eddies'

File_base_path = r'C:\Doutorado\1Trimestre\Geoprocessamento\LT_All_sat\MADT_eddies\2010\MADT_eddies_dura_10_area_min_2_desv_05_2010_dia063.tif'

ds = gdal.Open(File_base_path)
a = ds.ReadAsArray()
nlat,nlon = np.shape(a)

b = ds.GetGeoTransform() #bbox, interval
lon = np.arange(nlon)*b[1]+b[0]
lat = np.arange(nlat)*b[5]+b[3]


basedate = dt.datetime(2010,1,1,0,0,0)

# create NetCDF file
nco = netCDF4.Dataset(os.path.join(Mother_directory_path, 'time_series.nc'),'w',clobber=True)

# chunking is optional, but can improve access a lot: 
# (see: http://www.unidata.ucar.edu/blogs/developer/entry/chunking_data_choosing_shapes)
chunk_lon=16
chunk_lat=16
chunk_time=12

# create dimensions, variables and attributes:
nco.createDimension('lon',nlon)
nco.createDimension('lat',nlat)
nco.createDimension('time',None)
timeo = nco.createVariable('time','f4',('time'))
timeo.units = 'days since 2000-01-01 00:00:00'
timeo.standard_name = 'time'

lono = nco.createVariable('lon','f4',('lon'))
lono.units = 'degrees_east'
lono.standard_name = 'longitude'

lato = nco.createVariable('lat','f4',('lat'))
lato.units = 'degrees_north'
lato.standard_name = 'latitude'

# create container variable for CRS: lon/lat WGS84 datum
crso = nco.createVariable('crs','i4')
crso.long_name = 'Lon/Lat Coords in WGS84'
crso.grid_mapping_name='latitude_longitude'
crso.longitude_of_prime_meridian = 0.0
crso.semi_major_axis = 6378137.0
crso.inverse_flattening = 298.257223563

# create short integer variable for temperature data, with chunking
tmno = nco.createVariable('tmn', 'i2',  ('time', 'lat', 'lon'), 
   zlib=True,chunksizes=[chunk_time,chunk_lat,chunk_lon],fill_value=-9999)
tmno.units = 'degC'
tmno.scale_factor = 0.01
tmno.add_offset = 0.00
tmno.long_name = 'minimum monthly temperature'
tmno.standard_name = 'air_temperature'
tmno.grid_mapping = 'crs'
tmno.set_auto_maskandscale(False)

nco.Conventions='CF-1.6'

#write lon,lat
lono[:]=lon
lato[:]=lat

pat = re.compile('us_tmin_[0-9]{4}\.[0-9]{2}')
itime=0

#step through data, writing time and data to NetCDF
for root, dirs, files in os.walk(Mother_directory_path):
    dirs.sort()
    files.sort()
    
    for f in files:
        if re.match(pat,f):
            # read the time values by parsing the filename
            year=int(f[8:12])
            mon=int(f[13:15])
            date=dt.datetime(year,mon,1,0,0,0)
            print(date)
            dtime=(date-basedate).total_seconds()/86400.
            timeo[itime]=dtime
            # min temp
            if f.endswith('tif'):
                print('file: ', f)
                tmn_path = os.path.join(root,f)
                print(tmn_path)
                tmn=gdal.Open(tmn_path)
                a=tmn.ReadAsArray()  #data
                tmno[itime,:,:]=a
                itime=itime+1

nco.close()