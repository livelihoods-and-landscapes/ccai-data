# CCAI Fiji Land Cover and Flood Data

Overview of data and software outputs from a Climate Change AI Innovation Grant project focusing on flood detection and land cover mapping in Fiji.

## Fiji ImageStacks

Multiband raster images for each Tikina in Fiji using Sentinel-2 L2A surface reflectance remote sensing data, the S2Cloudless cloud masking product, and SRTM topography data. This processed remote sensing data can be used for various applications such as land use and land cover (LULC) mapping, change detection, and vegetation condition monitoring. 

This dataset is available on Google Earth Engine. 

Resources to access this data and examples for use can be found in `/s2-image-stacks`. 


## Fiji LULC Maps

Annual land use and land cover (LULC) maps for all-Fiji at a 10 m spatial resolution for 2019, 2020, 2021, and 2022. The maps are generated using a machine learning workflow applied to Sentinel-2 L2A surface reflectance data and SRTM topography data. 

This dataset is available on the Pacific Data Hub, Google Earth Engine, and a custom web map viewer and download portal.

Resources to access this data and examples for use can be found in `/fiji-lulc-maps`. 


## Fiji LULC Training Data

A dataset of 13,914 points across Fiji with a land use land cover (LULC) label and several predictor variables derived from Sentinel-2 L2A surface reflectance data and SRTM topography data. 

This dataset is available on the Pacific Data Hub, Google Earth Engine, and as GeoJSON file in this repository. 

Resources to access this data and examples for use can be found in `/fiji-lulc-training-data`. 

##  Tropical and Sub-Tropical Flood Masks

A dataset of 513 flood and water mask layers, generated as GeoTIFF files with a 10 m spatial resolution. Each of these layers corresponds to a flood event and date (there can be many flood mask layers per-event which represent flooding on different days as the event evolves). Flood and water masks were generated for 65 flood events since 2018 in 26 countries spanning the tropics and sub-tropics.

The worfklow and source code to generate this dataset can be found in `/tropical-subtropical-flood-masks`. This is based on the `TST-Floods` repo, to keep this repo in sync run:

```
cd tropical-subtropical-flood-masks
git submodule update --remote TST-Floods
```

The metadata for the flood and water mask files can be found in `/metadata/metadata.csv'.

The data is available for download from the [Pacific Data Hub](pacificdata.org/data/dataset/tropical-and-sub-tropical-flood-and-water-masks).
