# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 22:39:00 2018

@author: Philipe_Leal
"""
from netCDF4 import Dataset
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


Path_nc = r'Downloads\Water_body_phosphate_combined.nc'

Dataset_nc = Dataset(Path_nc)

Lista_vars = list(Dataset_nc.variables.keys())


latbounds = [ 40 , 43 ]
lonbounds = [ 30 , 36 ] # degrees east 
lats = Dataset_nc.variables['lat'][:] 
lons = Dataset_nc.variables['lon'][:]

# latitude lower and upper index
latli = np.argmin( np.abs( lats - latbounds[0] ) ) # retorna a posição do valor mínimo da lat (e a subtração é em módulo)
latui = np.argmin( np.abs( lats - latbounds[1] ) ) # retorna a posição do valor mínimo

# longitude lower and upper index
lonli = np.argmin( np.abs( lons - lonbounds[0] ) )
lonui = np.argmin( np.abs( lons - lonbounds[1] ) )  


# subset the data:

Water_body_phosphate_L2_Subset = Dataset_nc.variables['Water_body_phosphate_L2'][ : , :, latli:latui , lonli:lonui ] 
