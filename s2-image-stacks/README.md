# Fiji Sentinel-2 and Topography ImageStacks

Multiband raster images were created for each Tikina in Fiji using Sentinel-2 L2A surface reflectance remote sensing data, the S2Cloudless cloud masking product, and SRTM topography data. 

For each Tikina in Fiji, for each year since 2019, all [Sentinel-2 L2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED?hl=en) scenes were obtained and were cloud masked using the [S2Cloudless](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_CLOUD_PROBABILITY) product and the QA60 Sentinel-2 band. For all cloud free pixels, the following spectral indices were computed: normalised difference vegetation index (NDVI), normalised difference built index (NDBI), normalised difference water index (NDWI), and the green chlorophyll vegetation index (GCVI). Then annual median composites were generated from all cloud free pixels for visible, near infrared, shortwave infrared, and spectral indices bands. To capture seasonal vegetation dynamics and phenology, a monthly NDVI band was generated using a greennest pixel composite with linear interpolation for gap filling of months with cloudy images. Finally, topography related bands of elevation, slope, and aspect were generated from the [SRTM product](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003). 

## Data Access

ImageStacks for Fiji for 2019, 2020, 2021, and 2022 are available as public `ImageCollection`s on Google Earth Engine with the following asset IDs:

```
var imageStack2019 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2019-s2cloudless")
var imageStack2020 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2020-s2cloudless")
var imageStack2021 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2021-s2cloudless")
var imageStack2022 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-s2-image-stack-2022-s2cloudless")
```

Please see the Google Earth Engine JavaScript examples in this directory for generating all-Fiji mosaic `Image`s from each year's ImageStack and visualising and exploring ImageStack bands from 2019.

* `fiji-s2-image-stack-mosaic.js`
* `fiji-s2-image-stack-2019-visualisation.js`

## Data Format

Each `ImageCollection` corresponds to a year (one of 2019, 2020, 2021, or 2022 currently) and is comprised of multiband `Image` objects. Each `Image` object corresponds to a Tikina (an administrative unit in Fiji). The `ImageCollection` can be mosaiced to provide an all-Fiji `Image`. 