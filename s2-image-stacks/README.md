# Fiji Sentinel-2 and Topography ImageStacks

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