# -*- coding: utf-8 -*-
"""
Created on Fri May  4 09:19:54 2018

@author: Philipe Leal
"""

import netCDF4 as nc4
import numpy as np

f = nc4.Dataset(r'C:\Users\Philipe Leal\Downloads\sample.nc','w', format='NETCDF4')

tempgrp = f.createGroup('Temp_data')

lon = np.arange(45,101,2)
lat = np.arange(-30,25,2.5)
z = np.arange(0,200,10)
x = np.random.randint(10,25, size=(len(lon), len(lat), len(z)))

temp_data = x * np.random.randn(len(lon), len(lat), len(z))

from datetime import datetime
today = datetime.today()
time_num = today.toordinal()


# criando dimensoes dentro do grupo:

tempgrp.createDimension('lon', len(lon))
tempgrp.createDimension('lat', len(lat))
tempgrp.createDimension('z', len(z))
tempgrp.createDimension('time', None)

# criando variaveis dentro do grupo:

    # 1° termo: nome da var
    # 2° termo: tipo de variavel
    # 3° termo: dimensoes da var conforme predimensionada no passo anterior:

longitude = tempgrp.createVariable('Longitude', 'f4', 'lon')
latitude = tempgrp.createVariable('Latitude', 'f4', 'lat')  
levels = tempgrp.createVariable('Levels', 'i4', 'z')
temp = tempgrp.createVariable('Temperature', 'f4', ('time', 'lon', 'lat', 'z'))
time = tempgrp.createVariable('Time', 'i4', 'time')

print(f)
print(f.groups['Temp_data'])

# atribuindo dado ah variavel:

longitude[:] = lon
latitude[:] = lat
levels[:] = z
temp[0,:,:,:] = temp_data
time[0] = time_num

# atribuindo meta-dados (atributos globais) ao netcdf:

#Add global attributes
f.description = "Example dataset containing one group"
f.history = "Created " + today.strftime("%d/%m/%y")

#Add local attributes to variable instances
longitude.units = 'degrees east'
latitude.units = 'degrees north'
time.units = 'days since Jan 01, 0001'
temp.units = 'Kelvin'
levels.units = 'meters'
temp.warning = 'This data is not real!'

# fechando e salvando o netcdf:
f.close()