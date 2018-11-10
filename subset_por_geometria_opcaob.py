# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 00:27:44 2018

@author: Philipe_Leal
"""

import numpy as np
import netCDF4
from math import pi
from numpy import cos, sin
from scipy.spatial import cKDTree
from netCDF4 import Dataset
filename = r'Downloads/rtofs_glo_3dz_f006_6hrly_reg3.nc'
ncDataset = netCDF4.Dataset(filename, 'r')
print(ncDataset)                # shows global attributes, dimensions, and variables
ncvars = ncDataset.variables   # a dictionary of variables
# print information about specific variables, including type, shape, and attributes
for varname in ['temperature', 'salinity', 'Latitude', 'Longitude']:
    print(ncvars[varname])


class Kdtree_fast(object):
    def __init__(self, ncfile, latvarname, lonvarname):
        self.ncfile = ncfile
        self.latvar = self.ncfile.variables[latvarname]
        self.lonvar = self.ncfile.variables[lonvarname]        
        # Read latitude and longitude from file into numpy arrays
        rad_factor = pi/180.0 # for trigonometry, need angles in radians
        self.latvals = self.latvar[:] * rad_factor
        self.lonvals = self.lonvar[:] * rad_factor
        self.shape = self.latvals.shape
        clat,clon = cos(self.latvals),cos(self.lonvals)
        slat,slon = sin(self.latvals),sin(self.lonvals)
        triples = list(zip(np.ravel(clat*clon), np.ravel(clat*slon), np.ravel(slat)))
        self.kdt = cKDTree(triples)

    def query(self,lat0,lon0):
        rad_factor = pi/180.0 
        lat0_rad = lat0 * rad_factor
        lon0_rad = lon0 * rad_factor
        clat0,clon0 = cos(lat0_rad),cos(lon0_rad)
        slat0,slon0 = sin(lat0_rad),sin(lon0_rad)
        dist_sq_min, minindex_1d = self.kdt.query([clat0*clon0,clat0*slon0,slat0])
        iy_min, ix_min = np.unravel_index(minindex_1d, self.shape)
        return iy_min,ix_min

ncDataset = Dataset(filename, 'r')

ns = Kdtree_fast(ncDataset,'Latitude','Longitude')
iy,ix = ns.query(50.0, -140.0)
print('Closest lat lon:', ns.latvar[iy,ix], ns.lonvar[iy,ix])
