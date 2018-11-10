# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:11:19 2018

@author: Philipe Leal
"""

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import xarray as xr

airtemps = xr.tutorial.load_dataset('air_temperature')

# Convert to celsius

air = airtemps.air - 273.15

# copy attributes to get nice figure labels and change Kelvin to Celsius
air.attrs = airtemps.air.attrs

air.attrs['units'] = 'deg C'

# plotando series de uma localização no espaço:

    # por posicao sequencial no array:
    
    
air1d = air.isel(lat=10, # posicao 10
                 lon=10) # posicao 10

air1d[:200].plot.line('b-^') # plotando os 200 primeiros instantes

# plotando toda a series temporal no dado ponto:

fig, axes = plt.subplots(ncols=2)
ax = air1d.plot(ax=axes[0])
air1d.plot.hist(ax=axes[1])
plt.tight_layout()

plt.show()

    # por posicao espacial (pode ser uma lista de pontos):
        # neste caso: 3 pontos distintos, de mesma longitude
    
fig, axes = plt.subplots(ncols=2)
air.isel(lon=10, lat=[19,21,22]).plot.line(ax=axes[0], 
                                            x='time' # a dimensao para ser usada pelos pontos
                                            ) 

    # ou, gerando mesma imagem:
    
air.isel(lon=10, lat=[19,21,22]).plot.line(ax=axes[0], 
                                            hue='lat' # the dimension to be represented by multiple lines.
                                            ) 
plt.tight_layout()

plt.show()

## Plotando ao longo do eixo y (latitude):

air.isel(time=10, lon=[10, 11]).plot(y='lat', hue='lon')


# alterando direção dos axis:

air.isel(time=10, lon=[10, 11]).plot.line(y='lat', hue='lon', xincrease=False, yincrease=False)

# plotting com 2 dimensoes:

air2d = air.isel(time=500)

fig, axes = plt.subplots()
axes.set_aspect('equal')
air2d.plot(ax=axes)