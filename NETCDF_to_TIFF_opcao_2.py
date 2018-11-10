# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import netCDF4 as nc

from osgeo import gdal, ogr, osr

import sys, os

import numpy as np

dt_45_2055 = nc.Dataset(r'C:\Doutorado\2_Trimestre\Disciplinas\Climatologia\Anomalia_simples\Full_Year\2006_to_2055\RCP4.5_Primary_Productivity_Average_of_all_models_Anomaly_Entire_Year_2055_Global.nc', mode = 'r'  )

for i in dt_45_2055.dimensions:
    print (dt_45_2055.dimensions[i])
    print("")
    
Lat = dt_45_2055.variables['lat'][:]

Long = dt_45_2055.variables['lon'][:]

Lat_min = np.min(Lat)

Lat_max = np.max(Lat)

Long_min = np.min(Long)

Long_max = np.max(Long)

Resolution_Y = abs(Lat[0] - Lat[1])

Resolution_X = abs(Long[0] - Long[1])
# plotando array:



vars = dt_45_2055.variables
vars_list = [] # é um dicionário ordenado
dims = dt_45_2055.dimensions #dims é um dicionário ordenado

print ("Tipo de Objeto dims: {0}.\n".format(type(dims)))

for Uma_variavel in vars:
    print ("")
    print ('--------------- variable: ['+Uma_variavel+']---------------')
    
    print("shape = "+str(vars[Uma_variavel].shape)) #as dimensões das variáveis;
    vars_list.append(Uma_variavel)
    vdims = vars[Uma_variavel].dimensions
    print (vdims)
    print(type(vdims))
    print(len(vdims))
    print("*******")
    
# vdims é uma tupla contendo as dimensoes de cada vars 
           
    for vd in vdims:
        print("dimension["+vd+"]="+str(len(dims[vd])))   
# vai printar o comprimento
        
East = dt_45_2055.variables['anomaly'][::-1, 0:180]

West = dt_45_2055.variables['anomaly'][::-1, 180:360]

Global = np.concatenate( (West, East), axis=1)        
        


vars_Peixe_list = []

for i in vars_list:
    if i =='lat' or i=='lon':
        continue
    else:
        vars_Peixe_list.append(i)
        
        
# Criação de Geotiff de saida:
        
        # Geotransform:
        
#        geotransform[0] = top left x
#        geotransform[1] = w-e pixel resolution
#        geotransform[2] = 0
#        geotransform[3] = top left y
#        geotransform[4] = 0
#        geotransform[5] = n-s pixel resolution (negative value)
        
geotransform = (Long_min, Resolution_X, 0, Lat_max, 0, -Resolution_Y)

    # projecao:
    
    
projecao = osr.SRS_WKT_WGS84   

driver = gdal.GetDriverByName ("GTiff") # nome do formato dos arquivos de saida
xsize = np.size(Long)
ysize =np.size(Lat)
nbandas = np.size(vars_list)     

nome_arquivo_saida = r"C:\Users\Philipe Leal\Desktop\Temporario\teste_anomalia_peixe_netcdf_to_tiff.tif"

if os.path.isfile(nome_arquivo_saida):
    File_output_Max = None
    driver = None
    os.remove(nome_arquivo_saida)
    
else:    ## Show an error ##
    print("Error: %s file not found" % nome_arquivo_saida)

driver = gdal.GetDriverByName ("GTiff")
File_output = driver.Create(nome_arquivo_saida, xsize, ysize, nbandas, gdal.GDT_Float32)

File_output.SetGeoTransform(geotransform)
File_output.SetProjection(projecao)


import matplotlib.pyplot as plt



for V in range(len(vars_Peixe_list)):
    print("Pegando variavel: ", str(vars_Peixe_list[V]))
    
    East = dt_45_2055.variables[str(vars_Peixe_list[V])][::-1, 0:180]

    West = dt_45_2055.variables[str(vars_Peixe_list[V])][::-1, 180:360]

    Global = np.concatenate( (West, East), axis=1)
    
    Global = Global[::-1]
    
    plt.figure()
    plt.pcolor(Long, Lat, Global,cmap='rainbow')
    plt.colorbar()
    plt.show()
    
    print("Dimensoes de ", vars_Peixe_list[V], ": ", np.shape(Global))
    File_output.GetRasterBand(V+1).WriteArray(Global)




