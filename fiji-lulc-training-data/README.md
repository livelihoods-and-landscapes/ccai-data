## Overview

A geospatial dataset of point geometries with a land use / land cover label and several remote-sensing derived predictor variables that can be used to train and test a land use / land cover classifier. 

This dataset was generated with support from a <a href="https://www.climatechange.ai" target="_blank">Climate Change AI Innovation Grant</a> and the Australian Centre for International Agricultural Research. 

Each of the point geometries was assigned one of the following class labels:

1. water
2. mangrove
3. bare soil
4. urban / impervious
5. cropland / agriculture
6. grassland
7. shrubland
8. trees

The `class` property associated with each `POINT` feature stores the point's class label.

### Data Availability

* [Pacific Data Hub](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-labels) - GeoJSON file and .qml file for styling in QGIS. 
* [GitHub](https://github.com/livelihoods-and-landscapes/ccai-data/tree/main/fiji-lulc-training-data) - GeoJSON file, .qml for styling in QGIS, and .qgz project for visualising data in QGIS.

### Class definitions

The cropland / agriculture class is defined as any location where agricultural activities associated with cropping or livestock management were visible in high-resolution images. Land that is recently fallow, but where evidence of cropping or grazing activities is present, would be labelled as cropland. Grassland is defined as any low vegetation (e.g. below knee height) without a bush, shrub, or woody structure. Scrubland is defined as any vegetation that is below head height, does not form a closed canopy, and has a clearly visible bush, shrub, or woody structure. Trees are defined as any vegetation greater than head height forming a clear canopy. 

### Methods

Image interpretation and labelling points with a land cover class was undertaken within a custom Google Earth Engine application. Within a region of interest, a year’s worth of Sentinel-2 images was clustered into 15 classes using a k-means algorithm. A stratified random sample of points was generated for manual labelling using clusters as strata. Ground truth datasets ere generated in the Ba, Magodro, Rewa, Sigatoka, RakiRaki, Sigatoka, Suva, Suva (urban), Lautoka (urban), Noco, Vuya, Nadi, and Labasa regions. 

To support image interpretation and labelling a point’s land cover using high-resolution images (Google satellite basemaps), ancillary datasets were used (e.g. Planet and Sentinel-2 images) in conjunction with field verification.

Two quality-checks were applied to the labelled land cover points. First, each point was manually screened and quality checked to ensure consistency in class labels. Second, using Planet NICFI basemaps and Sentinel-2 RGB composites 2019, 2020, and 2021, each of the labelled land cover points was screened for a change in land cover event occurring at any point during those three years. If a change in land cover was observed, the point was dropped from the dataset. 

For each labelled point in 2019, 2020, and 2021 features were extracted comprising annual median cloud free spectral reflectance across Sentinel-2 wavebands, monthly NDVI composites, and annual median NDVI, NDBI, NDWI, and GCVI bands and elevation, slope, and aspect bands. 

This resulted in a dataset of 13,914 labelled points across three years: 2019, 2020, and 2021. The difference in the number of points across years is due to cloud cover preventing features being generated in some years

Feature definitions:

* `B_*` - median annual cloud free spectral reflectance for Sentinel-2 wavebands
* `ndvi` -  median annual cloud free NDVI computed from Sentinel-2 
* `gcvi` - median annual cloud free GCVI computed from Sentinel-2
* `ndwi` - median annual cloud free NDWI computed from Sentinel-2
* `ndbi` - median annual cloud free NDBI computed from Sentinel-2
* `ndvi_*` - median monthly cloud free NDVI computed from Sentinel-2
* `elevation` - elevation computed from SRTM
* `aspect` - aspect computed from SRTM
* `slope` - slope computed from SRTM