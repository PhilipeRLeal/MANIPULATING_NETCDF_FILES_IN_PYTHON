# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 11:54:55 2018

@author: Philipe Leal
"""

import xarray as xa
import numpy as np
import pandas as pd
# Combining multiple files


### Merging all .nc files in common directory

Dataset_xa = xa.open_mfdataset(r'F:\Chichikakua\Dados_Mensais\*.nc', 
        								 concat_dim='time')
								#chunks={'time':50})


### Salvando em um unico Netcdf de saida:

Dataset_xa.to_netcdf(r'F:\Chichikakua\Mergidos\chichikakua_xarray_merge.nc')


### Abrindo arquivo salvo

combined = xa.open_dataset(r'F:\Chichikakua\Mergidos\chichikakua_xarray_merge.nc')

### Info do netcdf:

combined.info()


### Obtendo comprimento das dimensoes do netCDF:
Frozen_dims = combined.dims

Lat_length = Frozen_dims.get('lat')

Time_length = Frozen_dims.get('time')


# Criando Datetime para posterior resampling:

Start_date = pd.to_datetime(combined.start_date)


Time = pd.date_range(start=Start_date, periods=Time_length, freq='M')


Stop_date = pd.to_datetime(combined.stop_date)


#combined['timestamp'] = Time


combined['start_date'] = Time.min()
combined['stop_date'] = Time.max()

combined.lat[:]
combined.lon[:]

combined2 = combined

combined2.to_netcdf(r'C:\Doutorado\Chichikakua\Mergidos\chichikakua_xarray_merge2.nc', mode='w')


### Resampling by time:

combined_year_mean = combined2.resample(timestamp='2Y').mean()

### Filtrando:


	## Estilo Numpy:
	
combined2.chlor_a[0, # tempo ==0
				  :, # latitude == All
				  :] # longitude == all
				  
	## Estilo Pandas (por localização exata na série):
	
combined2.chlor_a.loc[0,
						  -90,
						  50]

	## por localizoes inexatas:

	
combined2.sel(lon=-40,
				  lat=50,
				  method='nearest')
	
	
Filtro_pelo_ponto_mais_proximo = combined_year_mean.sel(timestamp='2002-09-05',
                            lon= [-68.35 , -68.479],
                            lat= [-15.93 , -16.36], 
                            method='nearest')  # 3° dimensao: lon


Chlo_a_ponto = Filtro_pelo_ponto_mais_proximo.chlor_a.reduce(np.nansum).values

### Operacoes matematicas:

(combined2.chlor_a **2) + 3.0

np.mean(combined2.chlor_a)


### Agregação (reduction)

combined2.mean(dim='time') ### retorna um 2D array com o valor médio do tempo 

Range_temporal = combined2.max(dim='time') - combined2.min(dim='time')
                 
                 
combined2.max(dim=['lat', 'lon']).values ### Retorna 1D array com valor máximo por instante no tempo


### average by calendar month:

combined2['time'] = Time

combined2.groupby('timestamp.month').mean('time')

### resample to every n days:

combined2.resample('10D', dim='time', how=np.nanmax)

### Convertendo xray -> numpy:

NP_Array = combined2.chlor_a.values	
	

### Convertendo xray -> pandas:

DF = combined2.to_dataframe()

DF.head()

# quando queremos so uma variavel:

DF = combined2.chlor_a.to_dataframe()

	
### pandas -> xray

Xarray = xa.Dataset.from_dataframe(DF)


## Ploting:

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig, axes = plt.subplots(2,2)


axes = axes.ravel()
for i in range(len(axes)):
    
    axes[i].set_aspect('equal')
    combined2.chlor_a[i].plot(ax=axes[i])
    
    combined2.chlor_a[i].plot(ax=axes[i])
    
    
    combined2.chlor_a[i].plot(ax=axes[i])
    
    
    combined2.chlor_a[i].plot(ax=axes[i])

plt.show()
### Testando abertura de arquivo criado

from netCDF4 import Dataset

ds = Dataset(r'C:\Doutorado\Chichikakua\Mergidos\chichikakua_xarray_merge2.nc')
