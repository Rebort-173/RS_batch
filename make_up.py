import os, os.path
import numpy as np
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
input_L = 'Landsat\L_2020_12_02.tif'
input_M = 'MODIS\MODIS_100\M100_2020_12_02.tif'
output = 'Landsat_Makeup'
out_dataset = output + os.sep + 'L_all_2020_12_02' + '.tif'

L_Xsize, L_Ysize, L_proj, L_geotrans, L_arrary = read_img(input_L)
M_Xsize, M_Ysize, M_proj, M_geotrans, M_arrary = read_img(input_M)

print('L_arrary_shape = ' + str(L_arrary.shape))
print('M_arrary_shape = ' + str(M_arrary.shape))
print(L_geotrans)
print(M_geotrans)

if L_Xsize != M_Xsize:
    print('The Xsize of two images is not equal')
if L_Ysize != M_Ysize:
    print('The Ysize of two images is not equal')

print('L_arrary_nan = ' + str(len(L_arrary[np.isnan(L_arrary)])))
print('M_arrary_nan = ' + str(len(M_arrary[np.isnan(M_arrary)])))
for i in range(0, L_Ysize):
    for j in range(0, L_Xsize):
        if np.isnan(L_arrary[i, j]):
            L_arrary[i, j] = M_arrary[i, j]
out_arrary = np.array(L_arrary).reshape(L_Ysize, L_Xsize)
print('out_arrary =' + str(out_arrary.shape))
Write_Operation_Arrary(out_dataset, out_arrary, L_geotrans, L_proj)
print('Finish')
