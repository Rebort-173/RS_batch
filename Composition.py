import os, os.path
import numpy as np
# from numpy.core.defchararray import array, count
# from numpy.lib.function_base import average
from osgeo import gdal
# import osgeo.gdalconst

# Obtain PROJ_LIB, deleted as needed
os.environ['PROJ_LIB'] = r'C:\Users\LR\.conda\envs\Py37\Library\share\proj'

def Write_Operation_Arrary(out_name, ds_arrary, ds_geotrans, ds_projection, data_type=gdal.GDT_Float32, driver_name='GTiff'):
    """
    Write_Operation_Arrary
    """
    driver = gdal.GetDriverByName(driver_name)
    # help(driver.Create)
    ds_width = ds_arrary.shape[0]
    ds_heigth = ds_arrary.shape[1]
    out_ds = driver.Create(out_name, ds_width, ds_heigth, 1, data_type)
    out_ds.SetGeoTransform(ds_geotrans)
    out_ds.SetProjection(ds_projection)
    out_ds.GetRasterBand(1).WriteArray(ds_arrary)
        
os.chdir(r'F:\GeoDatas\L_M_LST\Landsat\WuHan')
input_path = 'LST_8_WuHan_2016\LST_8_WuHan_2016_UTM_Bandmath_ClipSquare'
output_path = 'LST_8_WuHan_2016\LST_8_WuHan_2016_UTM_Bandmath_ClipSquare_Composition\LST_2016_Max'
out_dataset = output_path + os.sep + 'LST_2016_Max_Y' + '.tif'
# obtain image parameters
files = os.listdir(input_path)
for f in files:
     if os.path.splitext(f)[1].upper() == ".TIF":
         example = gdal.Open(input_path +  os.sep + f)
         geotrans = example.GetGeoTransform()
         print(geotrans)
         proj = example.GetProjection()
         out_width = example.RasterXSize
         out_heigth = example.RasterYSize
         break

# Transform images to arrary
ds_arrarys = []
for f in files:
     if os.path.splitext(f)[1].upper() == ".TIF":
        fileName = f
        in_dataset = input_path + os.sep + fileName
        ds_arrary = gdal.Open(in_dataset).ReadAsArray()
        ds_arrarys.append(ds_arrary)

def composition(arrary, value):
    """
    value composition
    """
    pix = []
    out_list = []
    for i in range(0, out_width):
        for j in range(0, out_heigth):
            for k in range(0, len(arrary)):
                pix.append(arrary[k][i, j])
            pix = [pix[m] for m in range(0, len(pix)) if pix[m]!=0]
            if len(pix) == 0:
                pix.append(-999)
           
            if value == 'mean':
                pix = np.mean(pix)
            if value == 'max':
                pix = np.max(pix)
            if value == 'min':
                pix = np.min(pix)
            if value == 'median':
                pix = np.median(pix)
            
            out_list.append(pix)
            pix = []

    out_arrary = np.array(out_list)
    out_arrary = out_arrary.reshape(out_heigth, out_width)
    return out_arrary


array_average = composition(ds_arrarys, 'max')
Write_Operation_Arrary(out_dataset, array_average, geotrans, proj)

print('=' * 50)
print('Finish！')
print('=' * 50)
