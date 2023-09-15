# Fiji LULC Test Data

To evaluate land use and land cover (LULC) maps an independent and representative test dataset is required. Here, a test dataset was generated via stratified random sampling approach across all areas in Fiji not used to generate [training data](https://github.com/livelihoods-and-landscapes/ccai-data/tree/main/fiji-lulc-training-data) (i.e. all Tikinas which did not contain a training data point were valid for sampling to generate the test dataset). Following equation 13 in [Olofsson et al. (2014)](https://www.sciencedirect.com/science/article/pii/S0034425714000704), the sample size of the test dataset was 834. This was based on a desired standard error of the overall accuracy score of 0.01 and a user's accuracy of 0.75 for all classes. The strata for sampling test samples were the eight LULC classes: water, mangrove, bare soil, urban, agriculture, grassland, shrubland, and trees. 

There are different strategies for allocating samples to strata for evaluating LULC maps, as discussed by [Olofsson et al. (2014)](https://www.sciencedirect.com/science/article/pii/S0034425714000704). Equal allocation of samples to strata ensures coverage of rarely occurring classes and minimise the standard error of estimators of user's accuracy. However, equal allocation does not optimise the standard error of the estimator of overall accuracy. Proportional allocation of samples to strata, based on the proportion of the strata in the overall dataset, can result in rarely occurring classes being underrepresented in the test dataset. Optimal allocation of samples to strata is challenging to implement when there are multiple evaluation objectives. [Olofsson et al. (2014)](https://www.sciencedirect.com/science/article/pii/S0034425714000704) recommend a "simple" allocation procedure where 50 to 100 samples are allocated to rare classes and proportional allocation is used to allocate samples to the remaining majority classes. The number of samples to allocate to rare classes can be determined by iterating over different allocations and computing estimated standard errors for performance metrics. Here, the [2021 all-Fiji LULC map](https://github.com/livelihoods-and-landscapes/ccai-data/tree/main/fiji-lulc-maps), minus the Tikinas used for generating training samples, was used to estimate the proportional areal coverage of each LULC class. The LULC map from 2021 was used to permit comparison with other LULC products with a 2021 layer, notably the ESA WorldCover 10m v200 2021 product. 

The 2021 LULC map was dominated by the tree class (74\% of the area classified) and the remaining classes had less than 10\% coverage each. Therefore, a "simple" allocation of 100 samples to the seven minority classes and an allocation of 133 samples to the tree class was used. This ensured all the minority classes had sufficient coverage in the test set while balancing the requirement to minimise standard errors for the estimate of overall accuracy. The allocated number of test dataset points were randomly sampled within each strata and were manually labelled using 2021 annual median RGB composites from Sentinel-2 and Planet NICFI and high-resolution Google Satellite Basemaps. 

## Data format

The Fiji LULC test data is available in GeoJSON format in the file `fiji-lulc-test-data.geojson`. Each point feature has two attributes: `ref_class` (the LULC class manually labelled and quality checked) and `strata` (the strata the sampled point belongs to derived from the 2021 all-Fiji LULC map). The following integers correspond to the `ref_class` and `strata` labels:

1. water
2. mangrove
3. bare earth / rock
4. urban / impervious
5. agriculture
6. grassland
7. shrubland
8. tree

The dataset can be accessed from this repo or on the [Pacific Data Hub](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-test-dataset).

## Use

When evaluating LULC maps using test data derived from a stratified sample, the nature of the stratified sampling needs to be accounted for when estimating performance metrics such as overall accuracy, user's accuracy, and producer's accuracy. This is particulary so if the strata do not match the map classes (i.e. when comparing different LULC products). [Stehman (2014)](https://www.tandfonline.com/doi/full/10.1080/01431161.2014.930207) provide formulas for estimating performance metrics and their standard errors when using test data with a stratified sampling structure. 

To support LULC accuracy assessment a [Python package](https://pypi.org/project/lulc-validation/0.0.4/) has been developed which provides implementations of [Stehman's (2014)](https://www.tandfonline.com/doi/full/10.1080/01431161.2014.930207) formulas. The package can be installed via:

```
pip install lulc-validation
```

with documentation and examples [here](https://github.com/jmad1v07/lulc-validation/tree/main).

In order to compute performance metrics accounting for the stratified nature of the sample the total number of points / pixels available to be sampled in each strata must be known. For this dataset that is:

1. 1779768,
2. 3549325,
3. 541204,
4. 687659,
5. 14279258,
6. 15115599,
7. 4972515,
8. 116131948
