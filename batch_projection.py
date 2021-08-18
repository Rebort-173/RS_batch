#-*- coding: utf-8 -*-

import arcpy, os, os.path
 
def projectRaster(rootPath):
    try:
        
        ##arcpy工作目录
        root_path = rootPath
        arcpy.env.workspace = root_path
 
        ##待处理文件所在目录(相对于根目录)
        input_path = "LST_8_WuHan_2016"
        output_path = "LST_8_WuHan_2016_UTM"
 
        ##源坐标系 "CGCS2000_3_Degree_GK_CM_123E" 
        #sourceSR = arcpy.SpatialReference("CGCS2000 3 Degree GK CM 123E")
        ##目标坐标系(WGS 1984 Web Mercator Auxiliary Sphere)
        #targetSR = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
        targetSR = "UTM_WGS84.prj"
        
        ##遍历目录，查找栅格数据
        files = os.listdir(root_path + os.sep + input_path)
        for f in files:
            if os.path.splitext(f)[1].upper() == ".TIF":
                fileName = os.path.splitext(f)[0] + ".tif"
                in_dataset = input_path + os.sep + fileName
                out_dataset = output_path + os.sep + fileName.split('.')[0] + '_UTM' + '.tif'
 
                #print("begin project "+in_dataset+" from: " +sourceSR.name+" to: "+targetSR.name)
                print(fileName + "---begin project")
                #arcpy.ProjectRaster_management(in_dataset, out_dataset, targetSR, "NEAREST", "#", "#", "#",sourceSR)
                arcpy.ProjectRaster_management(in_dataset, out_dataset, targetSR, "NEAREST", "100", "#", "#","#")
                print(fileName + "---project success")
 
        print("Finish")
        
    except arcpy.ExecuteError:
        print("Project Raster example failed.")
        print(arcpy.GetMessages())

################################################
if __name__ == '__main__':

    #指定处理文件根目录
    root_path = r"F:\GeoDatas\L_M_LST\Landsat\WuHan\LST_8_WuHan_2016"
    projectRaster(root_path)