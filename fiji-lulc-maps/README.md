# Fiji Land Use Land Cover

Land use and land cover (LULC) maps for all-Fiji in 2019, 2020, 2021, and 2022. The LULC map is generated from a year's worth of cloud masked Sentinel-2 surface reflectance data and topographic data from the SRTM using a random forests machine learning workflow. The map has a 10 m spatial resolution and a gap filling routine has been used to provide coverage in cloud affected areas where data permits. For more details on the methodology, please see this [resource](https://pacificdata.org/data/dataset/agu-lulc).

This dataset comprises GeoTIFF files storing land cover data for each Tikina. Tikina's that span the anti-meridian are split into two geometries. Each 10 m x 10 m pixel can take on one of eight classes:

1. water
2. mangrove
3. bare soil / rock
4. urban / impervious
5. cropland / agriculture
6. grassland
7. shrubland
8. trees

The cropland / agriculture class is defined as any location where agricultural activities associated with cropping or livestock management were visible in high-resolution images. Land that is recently fallow, but where evidence of cropping or grazing activities is present, would be labelled as cropland. Grassland is defined as any low vegetation (e.g. below knee height) without a bush, shrub, or woody structure. Shrubland is defined as any vegetation that is below head height, does not form a closed canopy, and has a clearly visible bush, shrub, or woody structure. Trees are defined as any vegetation greater than head height forming a clear canopy.

## Data Access

The data is available to download from the Pacific Data Hub:

* [2019](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-2019)
* [2020](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-2020)
* [2021](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-2021)
* [2022](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-2022)

as Google Earth Engine assets:

```
var lulc2019 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-lulc-2019-processed-v1")
var lulc2020 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-lulc-2020-processed-v1")
var lulc2021 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-lulc-2021-processed-v1")
var lulc2022 = ee.ImageCollection("projects/ccai-fiji-public/assets/fiji-lulc-2022-processed-v1")
```

and, via [web map viewer and data download portal](https://landcover.fijiflood.com).