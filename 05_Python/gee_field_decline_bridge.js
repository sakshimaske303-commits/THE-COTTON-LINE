// Field-level Nov-to-Mar NDVI decline on the 7 Roots & Reflectance fields, both years,
// Landsat 8/9 and Sentinel-2. Pixel centres inside each field; clouds and shadow masked.
// Earth Engine Code Editor -> Run -> Tasks. Export lands in Drive/ROOTS_REFLECTANCE;
// save it as 03_Data_Processed/Ground_Truth/field_decline_bridge.csv.

// ---- 1. Field geometries (copied from Roots & Reflectance src/gee_extract_indices.js) ----
var fields = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Polygon([[[78.3501074, 21.2230902], [78.3501135, 21.2233177], [78.3511170, 21.2230808], [78.3510103, 21.2229295], [78.3501074, 21.2230902]]]), {zone: 'sawardoh', field_num: 1, field_id: 'BACD', name: 'Cotton & Pigeon Pea (Tur)', area_ha: 0.2215, sown: '2026-06-22', crops: 'cotton,tur'}),
  ee.Feature(ee.Geometry.Polygon([[[78.3501074, 21.2230902], [78.3510103, 21.2229295], [78.3508953, 21.2221869], [78.3498298, 21.2223510], [78.3501074, 21.2230902]]]), {zone: 'sawardoh', field_num: 2, field_id: 'BDHG', name: 'Orange, Cotton & Pigeon Pea (Tur)', area_ha: 0.8792, sown: '2026-06-22', crops: 'cotton,tur,orange'}),
  ee.Feature(ee.Geometry.Polygon([[[78.3498298, 21.2223510], [78.3508953, 21.2221869], [78.3503374, 21.2213256], [78.3496810, 21.2219894], [78.3498298, 21.2223510]]]), {zone: 'sawardoh', field_num: 3, field_id: 'GHLJ', name: 'Cotton', area_ha: 0.7771, sown: '2026-06-22', crops: 'cotton'}),
  ee.Feature(ee.Geometry.Polygon([[[78.3511170, 21.2230808], [78.3508953, 21.2221869], [78.3517567, 21.2220694], [78.3519297, 21.2226489], [78.3518717, 21.2227811], [78.3511170, 21.2230808]]]), {zone: 'sawardoh', field_num: 4, field_id: 'CHIFE', name: 'Orange, Cotton, Pigeon Pea (Tur) & Turmeric', area_ha: 0.8226, sown: '2026-06-22', crops: 'cotton,tur,orange,turmeric'}),
  ee.Feature(ee.Geometry.Polygon([[[78.3496267, 21.2218309], [78.3492049, 21.2211202], [78.3501095, 21.2207714], [78.3503190, 21.2210368], [78.3496267, 21.2218309]]]), {zone: 'sawardoh', field_num: 5, field_id: 'KMON', name: 'Cotton', area_ha: 0.6585, sown: '2026-06-22', crops: 'cotton'}),
  ee.Feature(ee.Geometry.Polygon([[[78.4009879, 21.1595884], [78.4018892, 21.1592801], [78.4016370, 21.1586170], [78.4007550, 21.1588820], [78.4009879, 21.1595884]]]), {zone: 'karanja', field_num: 1, field_id: 'BAEF', name: 'Soyabean & Pigeon Pea (Tur)', area_ha: 0.786, sown: '2026-06-27', crops: 'soyabean,tur'}),
  ee.Feature(ee.Geometry.Polygon([[[78.4016370, 21.1586170], [78.4007550, 21.1588820], [78.4004545, 21.1579731], [78.4012324, 21.1577139], [78.4016370, 21.1586170]]]), {zone: 'karanja', field_num: 2, field_id: 'EFCD', name: 'Soyabean', area_ha: 0.9758, sown: '2026-06-27', crops: 'soyabean'})
]);

// ---- 2. Windows (same seasons as the Landsat scenes in the paper) ----
var windows = [
  {year: 'y1', season: 'nov', start: '2025-10-25', end: '2025-11-20'},
  {year: 'y1', season: 'mar', start: '2026-02-25', end: '2026-03-20'},
  {year: 'y2', season: 'nov', start: '2024-10-25', end: '2024-11-20'},
  {year: 'y2', season: 'mar', start: '2025-02-25', end: '2025-03-20'}
];

// ---- 3. Landsat 8/9 C2 L2: QA_PIXEL mask, scaled reflectance, NDVI ----
function landsatNdvi(img) {
  var qa = img.select('QA_PIXEL');
  var bad = qa.bitwiseAnd(1 << 1).or(qa.bitwiseAnd(1 << 2)).or(qa.bitwiseAnd(1 << 3))
              .or(qa.bitwiseAnd(1 << 4)).or(qa.bitwiseAnd(1 << 7)).neq(0);
  var sr = img.select(['SR_B4', 'SR_B5']).multiply(0.0000275).add(-0.2);
  return sr.normalizedDifference(['SR_B5', 'SR_B4']).rename('ndvi').updateMask(bad.not())
           .copyProperties(img, ['system:time_start']);
}
var landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'))
  .filterBounds(fields).map(landsatNdvi);

// ---- 4. Sentinel-2 SR harmonized + Cloud Score+ ----
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(fields)
  .linkCollection(csPlus, ['cs_cdf'])
  .map(function(img) {
    return img.normalizedDifference(['B8', 'B4']).rename('ndvi')
              .updateMask(img.select('cs_cdf').gte(0.60))
              .copyProperties(img, ['system:time_start']);
  });

// ---- 5. Window medians per field (pixel centres inside the field) ----
var rows = ee.FeatureCollection(windows.map(function(w) {
  return ee.FeatureCollection([['landsat', landsat, 30], ['sentinel2', s2, 10]].map(function(s) {
    var col = ee.ImageCollection(s[1]).filterDate(w.start, w.end);
    var med = col.median();
    return med.reduceRegions({collection: fields, reducer: ee.Reducer.mean().combine(ee.Reducer.count(), '', true),
                               scale: s[2]})
      .map(function(f) {
        return f.set({sensor: s[0], year: w.year, season: w.season, n_scenes: col.size(),
                       window: w.start + '/' + w.end});
      });
  })).flatten();
})).flatten();

print(rows.limit(10));
Export.table.toDrive({collection: rows, description: 'COTTON_LINE_field_decline', folder: 'ROOTS_REFLECTANCE',
  fileFormat: 'CSV', selectors: ['zone', 'field_num', 'field_id', 'name', 'crops', 'area_ha', 'sensor', 'year',
  'season', 'mean', 'count', 'n_scenes', 'window']});
