set MRT_DATA_DIR=D:\Tools\MRT\bin

for %%i in (*.hdf) do D:\Tools\MRT\bin\resample.exe -p F:\GeoDatas\L_M_LST\MODIS\MOD11A1_WuHan_2019\MOD11A1_Clip.prm -i %%i -o %%iout.tif

pause