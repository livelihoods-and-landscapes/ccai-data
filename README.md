# CCAI Fiji Land Cover and Flood Data

Overview of data and software outputs from a Climate Change AI Innovation Grant project focusing on flood detection and land cover mapping in Fiji.

## Fiji LULC Training Data

##  Tropical and Sub-Tropical Flood Masks

A dataset of 513 flood and water mask layers, generated as GeoTIFF files with a 10 m spatial resolution. Each of these layers corresponds to a flood event and date (there can be many flood mask layers per-event which represent flooding on different days as the event evolves). Flood and water masks were generated for 65 flood events since 2018 in 26 countries spanning the tropics and sub-tropics.

The worfklow and source code to generate this dataset can be found in `/tropical-subtropical-flood-masks`. This is based on the `TST-Floods` repo, to keep this repo in sync run:

```
cd tropical-subtropical-flood-masks
git submodule update --remote TST-Floods
```

The metadata for the flood and water mask files can be found in `/metadata/metadata.csv'.

The data is available for download from the [Pacific Data Hub](pacificdata.org/data/dataset/tropical-and-sub-tropical-flood-and-water-masks).
