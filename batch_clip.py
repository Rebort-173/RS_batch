import arcpy, os, os.path
from arcpy import env
from arcpy.sa import *

env.workspace = "F:\GeoDatas\L_M_LST\MODIS"
root_path = r"F:\GeoDatas\L_M_LST\MODIS"
# input_path = "Input"
# output_path = "Output"
input_path = "modtemp"
output_path = "MOD11A1_WuHan_2019_UTM_Clip_100m_BandMath_Square"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")


files = os.listdir(root_path + os.sep + input_path)

for f in files:
   if os.path.splitext(f)[1].upper() == ".TIF":
      fileName = f
      print(fileName + '---begin clip')
      in_dataset = input_path + os.sep + fileName
      out_dataset = output_path + os.sep + fileName.split('.tif')[0] + '_ClipSquare' + '.tif'
      xy_tolerance = ""

      arcpy.Clip_management(in_dataset, "748866 3324792 848766 3424692", out_dataset, "#", "#", "NONE")
      # arcpy.Clip_management(in_dataset, "748866 3324792 848766 3424692", out_dataset, "#", "#", "NONE")

      print(out_dataset + "---finish clip")

print("Finish!")