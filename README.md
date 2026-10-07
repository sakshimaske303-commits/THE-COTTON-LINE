# THE COTTON LINE — Does a Nineteenth-Century Colonial Land-Tenure Boundary Still Register in Present-Day Vidarbha?

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14802/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22111298.svg)](https://doi.org/10.5281/zenodo.22111298)

This project tests whether the boundary between Berar (Ryotwari land-revenue settlement) and the Central Provinces (Malguzari settlement), abolished as a provincial border in 1956, is still detectable in cotton-related crop phenology, agrarian labour structure, and land surface temperature. It finds no boundary-specific step in most outcomes. It finds a regional gradient that partly coincides with the old line, but the evidence is exploratory and does not identify a tenure effect.

## What This Project Is

Most of my other projects estimate the effect of a specific policy or event using difference-in-differences or event-study designs. This one is different. It asks whether an old administrative border is still visible in the landscape, which makes it a boundary-persistence and spatial-discontinuity problem, closer to historical GIS and spatial pattern analysis than to treatment-effect estimation.

Historical background: Berar (today's Amravati, Akola, Buldhana, Washim and Yavatmal districts) was assigned to the East India Company by a treaty with the Nizam of Hyderabad in 1853, was administered under the Ryotwari system, and was merged with the Central Provinces in 1903. The districts to the east (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli) were settled under Malguzari. Nagpur itself was annexed by the Company in 1853 under the doctrine of lapse, so 1853 is not a Berar-only date. The provincial boundary was abolished in 1956; at district level it corresponds to the present Amravati Division / Nagpur Division line.

## Core Question

After controlling for distance to the boundary, rainfall and elevation, is the Berar/Central Provinces boundary still detectable as a spatial discontinuity in kharif-to-rabi NDVI decline (a cropping-intensity index), agrarian labour structure (agricultural labourers relative to cultivators), land use, and land surface temperature?

## Findings So Far

- No boundary-specific level jump is found for NDVI decline, land surface temperature or net cultivated area, at either scale.
- The raw NDVI decline is larger on the Berar side (0.325 vs 0.255 in year one; 0.316 vs 0.241 in year two), but the gap is close to zero near the line and the boundary term is about zero once distance is controlled. This is a regional gradient.
- On the full footprint the side-by-distance interaction is significant for NDVI decline (p = 0.035) and land surface temperature (p = 0.011). Only the temperature result is robust to alternative standard errors and symmetric distance windows.
- The labour ratio shows a corridor slope difference (p = 0.036) that depends on one urban taluka, and a full-footprint level difference (p = 0.014) that is absent in the corridor.
- Sixteen coefficients were tested, four are significant at 5%, and none survives a Holm correction. Treat all results as exploratory.

The full account, including robustness checks and limitations, is in `CL_Research_Paper.md` (Sections 4.4 and 6).

## Study Design

The modern boundary is built by dissolving 120 taluka polygons into their two historical divisions and extracting the shared edge (384.7 km). I checked it against district administrative lineage from 1903 to 1956; this is district-level evidence, not a geometric overlay of a period map.

Two samples are used. The 32-taluka corridor contains the talukas intersecting a 25 km buffer of the line (12 of them have centroids more than 25 km away). The 68-taluka footprint is the set covered by Landsat WRS-2 path 144, rows 045/046. Both use the same OLS model:

`outcome ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m`

NDVI decline is measured from a November scene to a March scene, in two separate years using the same footprint and method. A leave-one-out jackknife over the 32 corridor talukas and the additional checks in `05_Python/robustness_checks.py` (HC3 and clustered errors, multiple-testing correction, symmetric windows, placebo cutoffs, influence, coverage) test stability. Census labour and land-use data cover 8 of 11 districts; Akola, Buldhana and Washim are not in those analyses.

Methodology, data sources, the Landsat DN = 0 fix and the scope decisions are documented on the Methodology & Data page of the dashboard and in `CL_Development_Log.md`.

## Repository Structure

```text
THE_COTTON_LINE/
├── 03_Data_Processed/              # Cleaned per-taluka CSVs by theme, boundary/corridor geometry,
│                                   #   Phase 4 regression datasets, robustness outputs
│                                   #   (raw satellite/DEM sources excluded, see .gitignore)
├── 05_Python/                      # LST/slope/vegetation processing (the DN=0 fix) and
│   └── robustness_checks.py        #   robustness_checks.py, which reproduces the regressions
├── 06_Streamlit/                   # Dashboard: app.py (Home) + 9 pages
│   ├── app.py
│   ├── pages/                      # Study Design, Theoretical Foundations, Cotton Signature (NDVI),
│   │                               #   Agrarian & Land Structure, Spatial Discontinuity Regression,
│   │                               #   Historical & Institutional Context, Interactive Maps,
│   │                               #   Methodology & Data, Ground Truth
│   ├── utils/
│   └── requirements.txt
├── 07_Outputs/                     # Static figures and maps
├── CL_Research_Paper.md            # Main paper
├── CL_Executive_Summary.md         # Two-page summary
├── CL_Development_Log.md           # Running development log: decisions, bugs, pivots
├── download_seasonal_scenes.py     # Landsat scene acquisition (year 1 and year 2)
└── requirements.txt
```

The scripts that assemble the Phase 4 datasets (NDVI aggregation, distance calculation, dataset merge) are not yet in the repository; `05_Python/main.py` and `config.py` are placeholders that say so. The regression results can be reproduced from the shipped Phase 4 CSVs with `05_Python/robustness_checks.py`.

## Tech Stack

Python · Pandas · GeoPandas · Statsmodels · Rasterio · SciPy · Plotly · Streamlit

## Data Sources

| Dataset | Provider |
|---|---|
| Administrative boundaries (taluka-level) | IIT Bombay POCRA Maharashtra Census shapefile portal |
| Vegetation (NDVI) / Climate (LST) | Landsat 8/9 Collection 2 Level-2 (Microsoft Planetary Computer STAC) |
| Population, Agriculture | Census (2011) village-level shapefiles; Maharashtra Economic Survey 2025-26 |
| Land Use | Census village land-use attributes |
| Hydrology (rainfall) | WorldClim 2.1 precipitation climatology (~18.5 km grid) |
| Terrain (elevation) | SRTM 1 arc-second DEM |
| Economics (FRA) | Compiled from state reports and secondary reporting (context only) |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/THE-COTTON-LINE.git
cd THE-COTTON-LINE
pip install -r requirements.txt
python 05_Python/robustness_checks.py     # reproduces the regressions and robustness tables
cd 06_Streamlit
streamlit run app.py                      # dashboard
```

## Limitations to Keep in Mind

The line is also an older political frontier and river line, so any gradient cannot be attributed to tenure alone. Spatial autocorrelation is not fully modelled, scenes are single-date and lack a QA_PIXEL cloud mask, census data (2011) are compared with 2024–26 imagery, and the Berar-side census sample is two districts. The Karanja Ghadge / Sawardoh field check covers the Central Provinces side only and is illustrative. See Section 6 of the paper.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](./LICENSE). You are free to share and adapt this work for any purpose, including commercially, with attribution. See `CITATION.cff` for citation metadata.

---

*The full development process, including decisions, data-pipeline bugs and design pivots, is documented in `CL_Development_Log.md`.*
