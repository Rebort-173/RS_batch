//创建一个函数用来掩膜，保留观测次数大于0的像元。
//num_observations_1km表示观测次数
var maskEmptyPixels = function(image) {
    var withObs = image.select('num_observations_1km').gt(0)
    return image.updateMask(withObs)
  }
  // 创建一个函数用来去除有云的像元
  var maskClouds = function(image) {
    // 选择质量评估波段
    var QA = image.select('state_1km')
    // 1<<10表示二进制第10位，第10位表示有云
    var bitMask = 1 << 10;
    // 使得检测出含云像元置为0，进行掩膜去除含云
    return image.updateMask(QA.bitwiseAnd(bitMask).eq(0))
  }
  
  //选择MODIS地表反射率数据，并去除观测数为0的数据
  var collection = ee.ImageCollection('MODIS/006/MOD09GA')
          .filterDate('2010-04-01', '2010-05-01')
          .map(maskEmptyPixels)
  
  // 获取在时间内像元观测值的数，以单个像元为单位
  var totalObsCount = collection
          .select('num_observations_1km')
          .count()
  
  //去云处理.
  var collectionCloudMasked = collection.map(maskClouds)
  //获取该时间间隔内非多云像素的观测值总数
  var clearObsCount = collectionCloudMasked
          .select('num_observations_1km')
          .count()
          .unmask(0)
  //计算影像数据集中值，并进行真彩色合成
  Map.addLayer(
      collectionCloudMasked.median(),
      {bands: ['sur_refl_b01', 'sur_refl_b04', 'sur_refl_b03'],
       gain: 0.07,
       gamma: 1.4
      },
      'median of masked collection'
    )
    //显示像元观测次数
  Map.addLayer(
      totalObsCount,
      {min: 84, max: 92},
      'count of total observations',
      false
    )
    //无云像元数据
  Map.addLayer(
      clearObsCount,
      {min: 0, max: 90},
      'count of clear observations',
      false
    )
    //显示无云像元占中像元比例
  Map.addLayer(
      clearObsCount.toFloat().divide(totalObsCount),
      {min: 0, max: 1},
      'ratio of clear to total observations'
    )  