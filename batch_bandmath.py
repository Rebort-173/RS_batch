from osgeo import gdal
import os, os.path
import numpy as np

class GRID:


    def read_img(self,filename):
        dataset = gdal.Open(filename)
        
        im_width  = dataset.RasterXSize
        im_height = dataset.RasterYSize

        im_geotrans = dataset.GetGeoTransform()
        im_proj = dataset.GetProjection()
        im_data = dataset.ReadAsArray(0,0,im_width,im_height)

        del dataset
        return im_proj,im_geotrans,im_data


    def write_img(self,filename,im_proj,im_geotrans,im_data):

        # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        # gdal.GDT_Float32, gdal.GDT_Float64

        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32


        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape


        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i+1).WriteArray(im_data[i])

        del dataset

if __name__ == "__main__":
    # os.chdir(r'F:\GeoDatas\L_M_LST\Landsat\Test')
    os.chdir(r'F:\GeoDatas\L_M_LST\MODIS')
    run = GRID()

    # input_path = 'Input2'
    # output_path = 'Output2'
    
    input_path = "MOD11A2_WuHan_2019_UTM_Clip_100m"
    output_path = "MOD11A2_WuHan_2019_UTM_Clip_100m_BandMath"

    os.environ['PROJ_LIB'] = r'C:\Users\LR\.conda\envs\Py37\Library\share\proj'

    files = os.listdir(input_path)
    # files = os.listdir(root_path + os.sep + input_path)
    for f in files:
        if os.path.splitext(f)[1].upper() == ".TIF":
            fileName = f
            print(fileName + '---begin bandmath')
            in_dataset = input_path + os.sep + fileName
            out_dataset = output_path + os.sep + fileName.split('.tif')[0] + '_bandmath' + '.tif'
            print(out_dataset)
            proj,geotrans,data = run.read_img(in_dataset)
            data = data.astype(np.float)
            band_math = data/50
            run.write_img(out_dataset, proj, geotrans, band_math)
            print(fileName + '---finish bandmath')
    print('Finish!')

print('git')
print('git')
print('hello')