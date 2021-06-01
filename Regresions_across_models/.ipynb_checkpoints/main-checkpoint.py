#1. abre datos
#1. abre datos
#2. abre indicies
#3. genera regresion y archivos .csv
#4. plotea los mapas de sensibilidad guarda en SST_regressions_across_models
import numpy as np
import pandas as pd
import xarray as xr
import os, fnmatch
import glob
import open_data
import regression
import csv2nc
import plot_sensitivity_maps

#Open data--------------------------------------------
ruta = '/pikachu/datos/julia.mindlin/CMIP6_ensambles/preprocesados' #Dropbox/DATOS_CMIP6' #/historical/mon/tas/past'
var = 'mon/ua'
models = [
    'ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CAMS-CSM1-0',
    'CanESM5', 'CESM2_', 'CESM2-WACCM','CMCC-CM2-SR5','CNRM-CM6-1',
    'CNRM-ESM2-1','EC-Earth3', 'FGOALS-g3', 'HadGEM3-GC31-LL','HadGEM3-GC31-MM',
    'IITM-ESM','INM-CM4-8','INM-CM5-0','KACE-1-0-G',
    'MIROC6','MIROC-ES2L', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR',
    'MRI-ESM2-0', 'NESM3', 'NorESM2-LM', 'NorESM2-MM', 'TaiESM1','UKESM1-0-LL'
    ]

scenarios = ['historical','ssp585']
os.chdir(ruta)
os.getcwd()

#Create dictionary
dato = open_data.cargo_todo(scenarios,models,ruta,var)

#Open indices
gloW  = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/GW_index_all_models.csv')
gw_index = gloW.iloc[:,2].values
TA = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/TA_index_all_models.csv')
VB = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/VB_index_all_models.csv')
SST1 = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/SST_ecuatorial_index.csv')
SST2 = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/SST_tropical_index.csv')
zonal_SST = pd.read_csv('/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices/SST_zonal_sst_index.csv')
TA = TA.iloc[:,2] / gw_index
VB = VB.iloc[:,2]
SST1 = SST1.iloc[:,2]
SST2 = SST2.iloc[:,2]
zonal_SST = zonal_SST.iloc[:,2]

indices = [TA,VB,SST1,SST2] #,zonal_SST]
indices_names = ['TA','VB','SST_ecuatorial','SST_tropical'] #,'zonal_SST']

#indices_path = '/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/indices'
#figure = plot_sensitivity_maps.plot_indices_box(indices,indices_names,indices_path)

#Create regression class
reg = regression.across_models()

#Generate regression data
reg.regression_data(dato,scenarios,models,gw_index)

#Create sensitivity maps
path_maps = '/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/sensitivity_maps/psl/new_indices_2'
reg.perform_regression(indices,indices_names,gw_index,path_maps)
file_list = csv2nc.csv_to_nc(path_maps)

#Create plots
path_maps = '/home/julia.mindlin/Tesis/Capitulo3/scripts/SST_regresions_across_models/sensitivity_maps/psl/new_indices_2'
GlobalWarming = xr.open_dataset(path_maps+'/Aij.nc')
TropicalWarming = xr.open_dataset(path_maps+'/TAij.nc')
VorBreak_GW = xr.open_dataset(path_maps+'/VBij.nc')
SeaSurfaceTemperature = xr.open_dataset(path_maps+'/SST_1ij.nc')
SeaSurfaceTemperature2 = xr.open_dataset(path_maps+'/SST_2ij.nc')
maps = [GlobalWarming, TropicalWarming, VorBreak_GW, SeaSurfaceTemperature,SeaSurfaceTemperature2]

frac_var = xr.open_dataset(path_maps+'/R2ij.nc')

GlobalWarming_pval = xr.open_dataset(path_maps+'/Apij.nc')
TropicalWarming_pval = xr.open_dataset(path_maps+'/TApij.nc')
VorBreak_GW_pval = xr.open_dataset(path_maps+'/VBpij.nc')
SeaSurfaceTemperature_pval = xr.open_dataset(path_maps+'/SST_1pij.nc')
SeaSurfaceTemperature2_pval = xr.open_dataset(path_maps+'/SST_2pij.nc')


maps_pval = [GlobalWarming_pval, TropicalWarming_pval, VorBreak_GW_pval, SeaSurfaceTemperature_pval,SeaSurfaceTemperature2_pval]

path_figs = '/home/julia.mindlin/Tesis/Capitulo3/figures/SST_regressions_across_models/u850/new_indices_2'
figure = plot_sensitivity_maps.plot_sensitivity_ua(maps,maps_pval,frac_var,path_figs)


path_figs = '/home/julia.mindlin/Tesis/Capitulo3/figures/SST_regressions_across_models/pr/new_indices_2'
figure = plot_sensitivity_maps.plot_sensitivity_pr(maps,maps_pval,frac_var,path_figs)


path_figs = '/home/julia.mindlin/Tesis/Capitulo3/figures/SST_regressions_across_models/psl/new_indices_2'
figure = plot_sensitivity_maps.plot_sensitivity_psl(maps,maps_pval,frac_var,path_figs)




