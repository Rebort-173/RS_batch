import os, os.path
import numpy as np
from numpy.lib.function_base import median
from osgeo import gdal

os.environ['PROJ_LIB'] = r'C:\Users\LR\.conda\envs\Py37\Library\share\proj'

os.chdir(r'F:\GeoDatas\L_M_LST\Landsat\WuHan')
input_path = 'LST_8_WuHan_2017\LST_8_WuHan_2017_UTM_Bandmath_ClipSquare_Composition\LST_2017_Max'
output_path = 'Ouput'

# Transform images to arrary
i = 0
files = os.listdir(input_path)
for f in files:
     if os.path.splitext(f)[1].upper() == ".TIF":
        fileName = f
        print(fileName)
        in_dataset = input_path + os.sep + fileName
        ds_arrarys = gdal.Open(in_dataset).ReadAsArray()
        ds_arrary = [element for element in ds_arrarys.flat if element!=-999]
        nodata = [element for element in ds_arrarys.flat if element==-999]
        total_nodata = len(nodata)
        min = np.min(ds_arrary)
        max = np.max(ds_arrary)
        mean = np.mean(ds_arrary)
        med = np.median(ds_arrary)
        std = np.std(ds_arrary)
        i += 1
        # print('No.  fileName  Min  Max  Mean  StdDev')
        # print(i, fileName, min, max, mean, med, std, sep=' ')
        print(min, max, mean, med, std, total_nodata, sep=' ')
