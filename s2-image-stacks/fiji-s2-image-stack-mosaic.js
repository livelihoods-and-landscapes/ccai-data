/**
 * Fiji Sentinel-2 ImageStack mosaic examples.
 */ 

var fijiPoint = ee.Geometry.Point([177.94253996291732, -17.81633110801625]);

// get Fiji ImageStack collections
var imageStack2019 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2019-s2cloudless");
var imageStack2020 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2020-s2cloudless");
var imageStack2021 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2021-s2cloudless");
var imageStack2022 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2022-s2cloudless");


// all Fiji mosaic
var fijiImage2019 = imageStack2019.mosaic();
var fijiImage2020 = imageStack2020.mosaic();
var fijiImage2021 = imageStack2021.mosaic();
var fijiImage2022 = imageStack2022.mosaic();

// create Fiji RGB composite image using annual median spectral reflectance
var rgbVisParam = {
  "opacity":1,
  "bands":["B4","B3","B2"],
  "min":0.017,
  "max":0.149,
  "gamma":1
};
Map.centerObject(fijiPoint, 8);
Map.addLayer(fijiImage2019, rgbVisParam, "Fiji RGB 2019");
Map.addLayer(fijiImage2020, rgbVisParam, "Fiji RGB 2020");
Map.addLayer(fijiImage2021, rgbVisParam, "Fiji RGB 2021");
Map.addLayer(fijiImage2022, rgbVisParam, "Fiji RGB 2022");

