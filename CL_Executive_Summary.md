# The Cotton Line — Executive Summary

**Sakshi D. Maske**
Independent Geospatial Researcher · Version 2.1, October 2026

---

## The question

In the nineteenth century, western Vidarbha (Berar: Amravati, Akola, Buldhana, Washim, Yavatmal) was settled under the Ryotwari land-revenue system, and the Nagpur region to the east under Malguzari. The provincial line was abolished in 1956. On district lineage it matches today's boundary between Amravati and Nagpur Divisions.

**Is that line still visible as a break in present-day agriculture, measured from satellites and the census, once rainfall, elevation and distance are accounted for?**

Two hypotheses: the outcomes **step** at the line (H1), or their **slope** with distance changes at the line (H2).

## Data and method

- **Boundary.** A 384.7 km line rebuilt from 120 talukas. Distances from each taluka centroid in UTM 44N.
- **Outcomes.**
  - Landsat 8/9 NDVI decline from early November to early March, in two years: a cropping-intensity index, computed at 30 m on cropland only, with cloud and shadow masked.
  - Landsat land surface temperature on 20 June 2026.
  - The 2011 Census ratio of agricultural labourers to cultivators.
  - The 2011 Census net sown area.
- **Samples.** 32 talukas within 25 km of the line; 98 talukas with at least half their cropland observed by Landsat (all 56 Berar talukas and 42 on the Central Provinces side; 56 for LST); all 119 census talukas.
- **Model.** Spatial-discontinuity regression with rainfall and elevation controls.
- **Inference.** The most conservative of HC3 and Conley spatial standard errors; Holm correction over 20 tests.
- **Robustness.** Local-linear estimates at the line, symmetric windows, placebo lines, influence, coverage thresholds and statistical power.

## Findings

1. **No step at the line.** No outcome jumps at the boundary in the corridor, in the Landsat sample, or in local estimates at the line. The larger samples could detect a step of about one standard deviation.
2. **The NDVI pattern is a ridge across the line.** The decline is highest within 50 km of the line on both sides (0.29) and falls towards Buldhana in the west (0.21) and the paddy districts in the east (0.13). The side averages are close: 0.255 against 0.246 in year 1, 0.319 against 0.262 in year 2.
3. **Labour structure differs regionally, not at the line.** Across all 119 talukas Berar has 0.96 more labourers per cultivator at the line (Holm p = 0.029). The difference is absent in the corridor and in local estimates. It is concentrated in Amravati district.
4. **Slopes differ, but fake lines do the same.** The gradient changes across the line for NDVI in both years (Holm p < 0.001), because the line sits on the crest of the ridge, and, before correction, for LST and labour. Placebo lines inside each side reproduce this for NDVI and labour. Only the LST pattern passes the placebo test, and it is one pre-monsoon date that most likely reflects soil.
5. **The satellite index measures something real.** District NDVI decline tracks official cotton share (r = 0.86 for 10 districts; 0.77 without the paddy districts). Washim, a soybean district, is the outlier: the index measures single-season cropping, not cotton alone. On seven farm fields from the companion study, 13 of 14 field-years match the farmers' winter-crop record: the chickpea field has the smallest decline, the fallow-winter fields large ones.

## What it means

Vidarbha's cotton core straddles the old Berar/Central Provinces line, and the line itself leaves no measurable break. With only one Landsat path, an earlier version saw a west-to-east gradient; observing all of Berar showed that the pattern falls away on both sides. The boundary also coincides with an older political frontier, the Wardha river and a soil and rainfall transition, so nothing here can be attributed to land tenure.

## Limitations

- Gadchiroli and most of Gondiya (Landsat path 143) are not observed; LST uses one scene.
- The cropland mask is from 2021; neighbouring paths are observed up to nine days apart.
- Single-date scenes per season.
- 2011 census data against 2024–26 imagery.
- Rainfall is a long-term climatology, and soil and irrigation are not controlled.
- The historical line is verified at district level only.

A companion field study (*Roots & Reflectance*, seven fields on the Central Provinces side) explains why the satellite measurement uses November and March scenes: no field was observable for 65–75 days of the monsoon.

Full paper: `CL_Research_Paper.md`. Every number is reproduced by `python 05_Python/run_all.py`.
