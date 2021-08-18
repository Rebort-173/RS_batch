from osgeo import gdal
import os, os.path
import numpy as np

os.environ['PROJ_LIB'] = r'C:\Users\LR\.conda\envs\Py37\Library\share\proj'

os.chdir(r'E:\Research\Program\Fusion\Rebuild\test data')
filename = "Coleanbally_15images_simulated_cloudy_tif.tif"
dataset = gdal.Open(filename)

# nb = dataset.RasterCount
# print(nb)

print(f'投影信息：{dataset.GetProjection()}')
print(f'栅格波段数：{dataset.RasterCount}')
print(f'栅格列数（宽度）：{dataset.RasterXSize}')
print(f'栅格行数（高度）：{dataset.RasterYSize}')

n_nl = 3
n_ns = 3
patch_long = 500
ind_patch = np.zeros((n_nl * n_ns, 4), dtype=np.int)

for i_ns in range(0, n_ns):
    for i_nl in range(0, n_nl):
        ind_patch[n_ns * i_nl + i_ns, 0] = i_ns * patch_long
        ind_patch[n_ns * i_nl + i_ns, 1] = np.min([ns - 1, (i_ns + 1) * patch_long - 1])
        ind_patch[n_ns * i_nl + i_ns, 2] = i_nl * patch_long
        ind_patch[n_ns * i_nl + i_ns, 3] = np.min([nl - 1, (i_nl + 1) * patch_long - 1])
print(ind_patch)

ns = 2000
nl = 2000
n_nl = 3
n_ns = 3
patch_long = 500


ind_patch1 = np.zeros((n_nl * n_ns, 4), dtype=np.int)
ind_patch = np.zeros((n_nl * n_ns, 4), dtype=np.int)
location = np.zeros((n_nl * n_ns, 4), dtype=np.int)

for i_ns in range(0, n_ns):
    for i_nl in range(0, n_nl):
        ind_patch1[n_ns * i_nl + i_ns, 0] = i_ns * patch_long
        ind_patch[n_ns * i_nl + i_ns, 0] = np.max([0, ind_patch1[n_ns * i_nl + i_ns, 0] - 10])
        location[n_ns * i_nl + i_ns, 0] = ind_patch1[n_ns * i_nl + i_ns, 0] - ind_patch[n_ns * i_nl + i_ns, 0]

        ind_patch1[n_ns * i_nl + i_ns, 1] = np.min([ns - 1, (i_ns + 1) * patch_long - 1])
        ind_patch[n_ns * i_nl + i_ns, 1] = np.min([ns - 1, ind_patch1[n_ns * i_nl + i_ns, 1] + 10])
        location[n_ns * i_nl + i_ns, 1] = ind_patch1[n_ns * i_nl + i_ns, 1] - ind_patch1[n_ns * i_nl + i_ns, 0] + location[n_ns * i_nl + i_ns, 0]

        ind_patch1[n_ns * i_nl + i_ns, 2] = i_nl * patch_long
        ind_patch[n_ns * i_nl + i_ns, 2] = np.max([0, ind_patch1[n_ns * i_nl + i_ns, 2] - 10])
        location[n_ns * i_nl + i_ns, 2] = ind_patch1[n_ns * i_nl + i_ns, 2] - ind_patch[n_ns * i_nl + i_ns, 2]

        ind_patch1[n_ns * i_nl + i_ns, 3] = np.min([nl - 1, (i_nl + 1) * patch_long - 1])
        ind_patch[n_ns * i_nl + i_ns, 3] = np.min([nl - 1, ind_patch1[n_ns * i_nl + i_ns, 3] + 10])
        location[n_ns * i_nl + i_ns, 3] = ind_patch1[n_ns * i_nl + i_ns, 3] - ind_patch1[ n_ns * i_nl + i_ns, 2] + location[n_ns * i_nl + i_ns, 2]
print(ind_patch1)
print(ind_patch)
print(location)