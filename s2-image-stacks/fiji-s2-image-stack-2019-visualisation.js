/**
 * Fiji Sentinel-2 ImageStack 2019 visualisations.
 */ 

var fijiPoint = ee.Geometry.Point([177.94253996291732, -17.81633110801625]);

// get Fiji 2019 ImageStack collection
var imageStack2019 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2019-s2cloudless");

// get data for a single Tikina (e.g. Ba)
var ba = ee.Image("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2019-s2cloudless/Ba_2019");
print("Ba ImageStack:", ba);

// all Fiji mosaic
var fijiImage2019 = imageStack2019.mosaic();

// create Fiji RGB composite image using annual median spectral reflectance
var rgbVisParam = {
  "opacity":1,
  "bands":["B4","B3","B2"],
  "min":0.017,
  "max":0.149,
  "gamma":1
};
Map.centerObject(fijiPoint, 8);
Map.addLayer(fijiImage2019, rgbVisParam, "Fiji RGB");

// annual median NDVI
var ndviVisParam = {
  "opacity":1,
  "bands":["ndvi"],
  "palette": ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
  "min":0,
  "max":0.914
};
Map.addLayer(fijiImage2019.select("ndvi"), ndviVisParam, "Fiji annual NDVI", false);