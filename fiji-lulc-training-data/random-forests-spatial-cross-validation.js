var samples = ee.FeatureCollection("projects/ccai-fiji-public/assets/ground-truth-samples-s2cloudless-cluster-v1");

/**
 * Spatial cross validation and hyperparameter tuning of LULC random forests classifer for Fiji.
 * 
 * For more information on the training data generation please see:
 * https://github.com/livelihoods-and-landscapes/ccai-data/tree/main/fiji-lulc-training-data
 * 
 * The training data consists of 13,914 points with a land use and land cover label.
 * For each point, a series of predictor variables have been generated from Sentinel-2 and SRTM data.
 * 
 * The training data has a `cluster` property. This represents a spatial cluster within a Tikina (Fijian administrative unit).
 * This `cluster` property is used to implement spatial cross validation for hyperparameter tuning. 
 * 
 */

// seed
var seed = 123;

// ntrees
var ntrees = [50, 150, 250];

// min n in leaf node
var minNLeaf = [1, 5, 10];

// Splits
var cluster = [0, 1, 2, 3, 4];

// Input properties
var inputs = [
  'B2',
  'B3',
  'B4',
  'B5',
  'B6',
  'B7',
  'B8',
  'B8A',
  'B11',
  'B12',
  'aspect',
  'elevation',
  'slope',
  'ndvi',
  'ndwi',
  'ndbi',
  'gcvi',
  'ndvi_1',
  'ndvi_2',
  'ndvi_3',
  'ndvi_4',
  'ndvi_5',
  'ndvi_6',
  'ndvi_7',
  'ndvi_8',
  'ndvi_9',
  'ndvi_10',
  'ndvi_11',
  'ndvi_12'
  ];

samples = samples.remap([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [1, 2, 3, 4, 5, 6, 6, 7, 2, 2, 2], 'class');

// adapted from: https://courses.spatialthoughts.com/end-to-end-gee-supplement.html#hyperparameter-tuning
function nTreeMap(nt){
  function minNLeafMap(minN) {
    return ee.FeatureCollection(cluster.map(function(k){
      var tmpSamples = samples.randomColumn('id', seed);
      var tmpTest = tmpSamples.filter(ee.Filter.eq('k', k));
      var filter = ee.Filter.equals({
        leftField: 'k',
        rightField: 'k'
      });
      var invertedJoin = ee.Join.inverted();
      var tmpTrain = invertedJoin.apply(tmpSamples, tmpTest, filter);
      var classifier = ee.Classifier.smileRandomForest({
        numberOfTrees: nt,
        seed: seed,
        minLeafPopulation: minN
      })
        .train({ 
          features: tmpTrain, 
          classProperty: 'class',
          inputProperties: inputs
        });
      var accuracy = tmpTest
        .classify(classifier)
        .errorMatrix('class', 'classification')
        .accuracy();
        
      var errorMatrix = tmpTest
        .classify(classifier)
        .errorMatrix('class', 'classification');
        
      return ee.Feature(null, {
        'ntrees': nt, 
        'split': k, 
        'accuracy': accuracy, 
        'error_matrix': errorMatrix,
        'min_n_leaf': minN
      });
    }));
  }
  return ee.FeatureCollection(minNLeaf.map(minNLeafMap));
}

var crossValResults = ntrees.map(nTreeMap);

var ntrees50 = crossValResults[0].flatten();
var ntrees150 = crossValResults[1].flatten();
var ntrees250 = crossValResults[2].flatten();

print(ntrees50);
print(ntrees150);
print(ntrees250);

Export.table.toDrive({
  collection: ntrees50, 
  description: "ntrees50crossval", 
  fileNamePrefix: "ntrees-50-cross-validation-v1-tune", 
  fileFormat: "GeoJSON"
});

Export.table.toDrive({
  collection: ntrees150, 
  description: "ntrees150crossval", 
  fileNamePrefix: "ntrees-150-cross-validation-v1-tune", 
  fileFormat: "GeoJSON"
});

Export.table.toDrive({
  collection: ntrees250, 
  description: "ntrees250crossval", 
  fileNamePrefix: "ntrees-250-cross-validation-v1-tune", 
  fileFormat: "GeoJSON"
});
