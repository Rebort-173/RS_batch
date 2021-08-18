import os, os.path
import numpy as np
from numpy.core.fromnumeric import mean
from osgeo import gdal

os.environ['PROJ_LIB'] = r'C:\Users\LR\.conda\envs\Py37\Library\share\proj'

def read_img(filename):
    dataset = gdal.Open(filename)
    
    Xsize  = dataset.RasterXSize
    Ysize = dataset.RasterYSize
    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_arrary = dataset.ReadAsArray(0,0,Xsize,Ysize)
    del dataset
    return Xsize, Ysize, im_proj, im_geotrans, im_arrary

def Write_Operation_Arrary(out_name, ds_arrary, ds_geotrans, ds_projection, data_type = gdal.GDT_Float32, driver_name='GTiff'):
    """
    Write_Operation_Arrary
    """
    driver = gdal.GetDriverByName(driver_name)
    # help(driver.Create)
    ds_Xsize = ds_arrary.shape[1]
    ds_Ysize = ds_arrary.shape[0]
    out_ds = driver.Create(out_name, ds_Xsize, ds_Ysize, 1, data_type)
    out_ds.SetGeoTransform(ds_geotrans)
    out_ds.SetProjection(ds_projection)
    out_ds.GetRasterBand(1).WriteArray(ds_arrary)

os.chdir(r'F:\GeoDatas\HuBei_Composition\2_Resize')
input_L = 'Landsat_Makeup\L_all_2020_12_02.tif'
input_M = 'MODIS\M_2020_12_02.tif'
output = 'Landsat_normalization'
out_dataset = output + os.sep + 'L_normal_2020_12_02' + '.tif'

L_Xsize, L_Ysize, L_proj, L_geotrans, L_arrary = read_img(input_L)
M_Xsize, M_Ysize, M_proj, M_geotrans, M_arrary = read_img(input_M)

print('L_arrary_shape = ' + str(L_arrary.shape))
print('M_arrary_shape = ' + str(M_arrary.shape))

print('L_arrary_nan = ' + str(len(L_arrary[np.isnan(L_arrary)])))
print('M_arrary_nan = ' + str(len(M_arrary[np.isnan(M_arrary)])))
if len(L_arrary[np.isnan(L_arrary)]) or len(M_arrary[np.isnan(M_arrary)]):
    print('Nan is exist')

ratio = 10
for i in range(0, M_Ysize):
    for j in range(0, M_Xsize):
        L_mean = np.mean(L_arrary[i*10:i*10+10, j*10:j*10+10])
        residual = L_mean - M_arrary[i, j]
        for m in range(i*10, i*10+10):
            for n in range(j*10, j*10+10):
                L_arrary[m, n] = L_arrary[m, n] - residual

out_arrary = L_arrary
# out_arrary = np.array(L_arrary).reshape(L_Ysize, L_Xsize)
print('out_arrary =' + str(out_arrary.shape))
Write_Operation_Arrary(out_dataset, out_arrary, L_geotrans, L_proj)
print('Finish')
