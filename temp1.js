var table = ee.FeatureCollection("users/boyxiaozheng/feature/beijing");
function cal_ndvi(image){
  var mask=ee.Algorithms.Landsat.simpleCloudScore(image).select(['cloud']).lte(20);
  var ndvi=image.normalizedDifference(['B5', 'B4']).updateMask(mask).rename('NDVI');
  return image.addBands(ndvi);
}
​
var ndvi_image= ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
  .filterBounds(table.geometry())
 // .filter(ee.Filter.lt('CLOUD_COVER',10))
  .filterDate('2017-06-01','2017-10-01')
  .map(cal_ndvi);
​
​
var img_list=ndvi_image.toList(20);
​
var et_list=[];
​
for (var i=0;i<20;i++){
  var img=img_list.get(i);
  var s_t=ee.Date(ee.Image(img).get('DATE_ACQUIRED'));
  var ndvi=ee.Image(img).select('NDVI');
  var era5=ee.ImageCollection("ECMWF/ERA5/DAILY")
                              .filterDate(s_t,ee.Date(s_t).advance(1,'day'))
                              .mean();
​
  var gldas=ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H")
                              .filterDate(s_t,ee.Date(s_t).advance(1,'day'))
                              .mean();
  var cons1=ee.Image.constant(0.1440);
  var cons2=ee.Image.constant(0.6495);
  var cons3=ee.Image.constant(0.009);
  var cons4=ee.Image.constant(0.0163);
  var l_rn=gldas.select('Lwnet_tavg').resample('bicubic');
  var s_rn=gldas.select('Swnet_tavg').resample('bicubic');
  var max_ta=era5.select('maximum_2m_air_temperature').subtract(ee.Image.constant(273.15)).resample('bicubic');
  var min_ta=era5.select('minimum_2m_air_temperature').subtract(ee.Image.constant(273.15)).resample('bicubic');
  var mean_ta=era5.select('mean_2m_air_temperature').subtract(ee.Image.constant(273.15)).resample('bicubic');
  var et_wang=l_rn.add(s_rn).multiply(cons1.add(cons2.multiply(ndvi).add(cons3.multiply(mean_ta).add(cons4.multiply(max_ta.subtract(min_ta)))))).rename('wang_LE');
​
  et_list.push(et_wang);
}
​
var et_list2=ee.List(et_list)
​
var et_year=ee.ImageCollection.fromImages(et_list2).mean().clip(table.geometry());
​
var visparam = {
  min: 0,
  max: 200,
  palette:  'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
   '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
​
Map.centerObject(et_year,10);
Map.addLayer(et_year,visparam)