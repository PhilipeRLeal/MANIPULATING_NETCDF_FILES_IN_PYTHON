# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:58:46 2018

@author: Philipe Leal
"""
import netCDF4 as nc

from osgeo import gdal, ogr, osr

import sys, os

import numpy as np

from datetime import datetime
start=datetime.now()


def NETCDF_to_GEOTIF(NETCDF_Path, GEOTIF_directory_target_path=None, abrangencia='Global', GEOTRANSFORM=None):
    """ Esta função converte NETCDF em GEOTIF, e retorna o caminho do arquivo de saida do geotif criado.
    
    Variáveis de entrada:
        NETCDF_Path: caminho do arquivo NETCDF que será convertido em GEOTIF
        
        
        GEOTIF_directory_target_path: caminho da pasta em que o geotif será salvo. Caso não seja atribuido, o geotiff será salvo na mesma pasta que o NETCDF
        
        abrangencia: define a abrangencia espacial do NETCDF. Por padrão é global. Caso diferente de global, o geotransform será adquirido diretamente do NETCDF de entrada.
        
        GEOTRANSFORM: deverá ser inserido, somente quando a "abrangencia" nao for global.
    """
    
    NETCDF_Path = NETCDF_Path
    
    dt_45_2055 = nc.Dataset(NETCDF_Path, mode = 'r'  )
    
    if GEOTIF_directory_target_path==None:
        GEOTIF_directory_target_path = str(os.path.splitext(NETCDF_Path)[0])
        
    else:
        GEOTIF_directory_target_path = GEOTIF_directory_target_path
        
    if abrangencia!='Global':      
        
        geotransform = GEOTRANSFORM
        
    else:
        NETCDF_GDAL_Dataset = gdal.Open(NETCDF_Path)
        geotransform = NETCDF_GDAL_Dataset.GetGeoTransform()
        geotransform = (-179.45, geotransform[1], 0, 90, 0, -geotransform[5])
        
        NETCDF_GDAL_Dataset = None

    for i in dt_45_2055.dimensions:
        print (dt_45_2055.dimensions[i])
        print("")
        
    Lat = dt_45_2055.variables['lat'][:]
    
    Long = dt_45_2055.variables['lon'][:]
  
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
    
    nome_arquivo_saida = str(GEOTIF_directory_target_path) + "to_tif.tif"
    
    print("Saida do arquivo: ", nome_arquivo_saida)
    
    
    try: 
        os.path.isfile(nome_arquivo_saida)
    
        driver = None
        os.remove(nome_arquivo_saida)
        print("Arquivo deletado com sucesso!")
    except:    ## Show an error ##
        print("Error: %s file not found" % nome_arquivo_saida)
    
    
    projecao = osr.SRS_WKT_WGS84   
    
    driver = gdal.GetDriverByName("GTiff") # nome do formato dos arquivos de saida
    xsize = np.size(Long)
    ysize =np.size(Lat)
    nbandas = np.size(vars_list)     
    
    
    File_output = driver.Create(nome_arquivo_saida, xsize, ysize, nbandas, gdal.GDT_Float32)
    
    File_output.SetGeoTransform(geotransform)
    File_output.SetProjection(projecao)
    
    for V in range(len(vars_Peixe_list)):
        print("Pegando variavel: ", str(vars_Peixe_list[V]))
        
        East = dt_45_2055.variables[str(vars_Peixe_list[V])][::-1, 0:180]
    
        West = dt_45_2055.variables[str(vars_Peixe_list[V])][::-1, 180:360]
    
        Global = np.concatenate( (West, East), axis=1)   
        Global = np.array(Global)
        
        
        print("Dimensoes de ", vars_Peixe_list[V], ": ", np.shape(Global))
        File_output.GetRasterBand(V+1).WriteArray(Global)
    
    
    File_output.FlushCache()
    File_output = None
    
    print("Função Terminada com Sucesso!!")
    print("\n"+"Tempo de execução: ", (datetime.now()-start))
    
    return str(nome_arquivo_saida)
    
