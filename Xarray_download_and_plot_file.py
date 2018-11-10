# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 14:48:14 2018

@author: Philipe Leal
"""

import xarray as xr

remote_data = xr.open_dataset('http://iridl.ldeo.columbia.edu/SOURCES/.OSU/.PRISM/.monthly/dods',
                              decode_times=False)
 
# nothing is loaded over the network until we look at particular values:
remote_data

tmax = remote_data['tmax'][:2, # 1°dimensão: tempo -- primeiros dois instantes
                   ::3, # 2°dimensão: latitude -- de 3 em 3 unidades 
                   ::3] # 3°dimensão: longitude -- de 3 em 3 unidades 


# the data is downloaded automatically when we make the plot
tmax[0].plot()

### Some servers require authentication before we can access the data

# Para autenticação simples (Basic authentication protocol):

import requests

session = requests.Session()
session.auth = ('username', 'password')

store = xr.backends.PydapDataStore.open('http://example.com/data',
                                        session=session)
ds = xr.open_dataset(store)


# Para authentication mais complexa (ex: NASA):
from pydata.cas.urs import setup_session

ds_url = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/hyrax/example.nc'

session = setup_session('username', 'password', check_url=ds_url)
store = xr.backends.PydapDataStore.open(ds_url, session=session)

ds = xr.open_dataset(store)