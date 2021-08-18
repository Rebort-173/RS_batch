# from osgeo import gdal
# # LC81230392016013LGN02_LST.tif

# options = gdal.TranslateOptions(format='PNG')
# # gdal.TranslateInternal('ttt.png', 'LC81230392016013LGN02_LST.tif.tif', options)
# # help(gdal.TranslateInternal)
# driver = gdal.GetDriverByName('PNG')
# help(gdal.GetDriverByNamever())

from osgeo import gdal
file_path="F:\GeoDatas\L_M_LST\Landsat\WuHan\batch\LC81230392016013LGN02_LST.tif"
ds=gdal.Open(file_path)
driver=gdal.GetDriverByName('PNG')
dst_ds = driver.CreateCopy('F:\GeoDatas\L_M_LST\Landsat\WuHan\batch\LC81230392016013LGN02_LST.png', ds)
dst_ds = None
src_ds = None