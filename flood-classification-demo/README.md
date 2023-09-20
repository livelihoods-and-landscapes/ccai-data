# Flood classification

**NOTE - DEVELOPMENT MODEL USED HERE**

Example application of segmenting an image into flood, permanent water, and land classes using remotely sensed derived inputs. 

The example here uses pre- and post-flood event synthetic Sentinel-2 like NDVI and NDWI images with topographic variables as predictors. The synthetic Sentinel-2 like NDVI and NDWI images are generated using the STARFM algorithm using Sentinel-2 and MODIS data as inputs. 

The segmentation model is a UNet style model trained on a large dataset of tropical and sub-tropical flood events. 

* `00_get_images_gee.ipynb` - for a target flood event and area of interest, download required remote sensing images from Google Earth Engine.
* `01_prepare_images_for_fusion.ipynb` - search through pairs of MODIS and Sentinel-2 images downloaded from Google Earth Engine to find candidate pair for image fusion with STARFM.
* `02_image_fusion.ipynb` - STARFM image fusion implementation to generate pre- and post-flood event synthetic Sentinel-2 like NDVI and NDWI images.
* `03_prepare_image_stacks.ipynb` - convert geospatial data into NumPy arrays for running through a UNet model for flood, water, and land classifications. 
* `04_predict_flooding.ipynb` - generate predictions of flood, water, and land for a target image. 