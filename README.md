# THE COTTON LINE — Does a 150-Year-Old Colonial Land-Tenure Boundary Still Register as a Measurable Spatial Signature in Present-Day Vidarbha?

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22111298.svg)](https://doi.org/10.5281/zenodo.22111298)

The effect of the Berar/Central Provinces land tenure split from 1853 — abolished in 1956 — remains as a spatial discontinuity signature of cotton-crop phenology, in agrarian labor structure, and land surface temperature today.

## What This Project Is

All other projects within my portfolio run an experimental test of a particular change/implementation or policy in a traditional causal fashion: difference-in-differences, event studies, etc. However, the question I chose to pursue in this project was different, I wasn't going to find out if there is a metric shift from any recent action, but whether if a 150-year-old administrative border is still felt as a physical imprint in the landscape. This is a basic problem of boundary persistence and spatial discontinuity, rather than a basic treatment check problem, and is therefore more related to historical GIS tracking and pattern analysis than traditional treatment checks.

In 1853 the British annexed the Berar District (which is now Amravati, Akola, Buldhana, Washim and Yavatmal) and imposed a direct land tax known as 'Ryotwari' and forced the peasants to give their cotton to the Lancashire mills. These districts on the east side of the country--Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli--operated under a landlord system of Malguzari. Though the official line was removed from the map in 1956, it is there where our present Amravati Division and Nagpur Division boundary lines lie.

## Core Question

Is that historical Berar (Ryotwari) and the Central Provinces (Malguzari) boundary still visible as a distinct spatial discontinuity in maps of modern cotton-signature NDVI, ratio of farm workers to total laborers, and temperature of ground after adjusting for distance to boundary, rainfall and elevation?

## Why This Approach

The idea behind this project was to take a different approach to spatial analysis, while not radically departing from the rest of my portfolio. I did not do any event-tracking models because I'm dealing with the longer persisting landscape features. I wished to test the extent of the colonization over the course of generations. This is a study (not a simple policy short-term check) on map survival.

## Core Finding, So Far

There is no abrupt change in my models at the old historical level. In contrast, a very clear east to west gradient was identified that can be discerned from both independent annual satellite greenness cycles and align with my ground temperature metrics. Depending on the side of the border looked at, the rates of decline in the metrics differ widely as a function of distance from the border.

The representation is much more accurate and honest than a fake perfect clean discontinuity step-jump would be of the geography. I will report here the same results as returned by the dashboard's Spatial Discontinuity Regression page and the points where the small corridor model and the big full-scene map model actually differ from each other, on a scale basis.

The boundary for the Historic District (Historical & Institutional Context) is verified via the historical district-lineage boundary verification that is listed on the Historic District page and the district compilation for the FRA (Historical & Institutional Context) is listed on the FRA page.

## Study Design

The modern border layer is created by combining 120 taluka shape files, so that it would capture the actual border edge in between the Akola, Amravati and Wardha corner and the entire boundaries till Yavatmal and Chandrapur.
My primary discontinuity test is a closer dataset on the 32 talukas around the boundary (still not considered a base check, just a different set of data to check robustness from the 25 km buffer) and my regional discontinuity set is on a route with a wider 68 talukas predominantly in the region (which serves only as an extra robustness check, not a substitute for my 25 km buffer).
I've used both of my data samples with this OLS spatial-discontinuity regression model using the terrain maps and the rain logs as env control variables: -outcome ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m
To ensure that I'm not just observing one year's weather, but actual farming practices, I took snaps over the regular cycle between the peak of the green kharif monsoon and the dry winter rabi season over two full Landsat satellite cycles.
I created a full jack-knife test, which was taking each corridor taluka out and running my regressions again and comparing the final output numbers to see that there's no one particular taluka swinging the numbers.

Documents for the methodology, all the data sources, the Landsat DN=0 fix, and the scope decision of corridor vs full-footprint are documented on the Methodology & Data page of the dashboard and in `CL_Development_Log.md`.

## Repository Structure

```text
THE_COTTON_LINE/
├── 03_Data_Processed/              # Cleaned, per-taluka CSVs by theme (Vegetation, Population,
│                                    #   Land_Use, Agriculture, Economics, Climate, Hydrology,
│                                    #   Terrain, Administrative boundary/corridor geometry, Phase4
│                                    #   regression datasets) -- raw satellite/DEM sources excluded,
│                                    #   see .gitignore
├── 05_Python/                      # LST/slope/vegetation processing pipelines (the DN=0 fix)
├── 06_Streamlit/                   # Dashboard -- app.py (Home) + 8 pages
│   ├── app.py
│   ├── pages/                      # Study Design, Theoretical Foundations, Cotton Signature (NDVI),
│   │                                #   Agrarian & Land Structure, Spatial Discontinuity Regression,
│   │                                #   Historical & Institutional Context, Interactive Maps,
│   │                                #   Methodology & Data, Ground Truth
│   ├── utils/
│   │   ├── theme.py                # Shared dashboard styling
│   │   └── data.py                 # Shared data-loading functions
│   └── requirements.txt
├── 07_Outputs/                     # Static figures, maps, and the theory diagram
├── CL_Development_Log.md           # Running development log -- every decision, bug, and pivot
├── download_seasonal_scenes.py     # Landsat scene acquisition (year 1 and year 2)
└── requirements.txt
```

## Tech Stack

Python · Pandas · GeoPandas · Statsmodels · Rasterio · SciPy · Plotly · Streamlit

## Data Sources

| Dataset | Provider |
|---|---|
| Administrative boundaries (taluka-level) | IIT Bombay POCRA Maharashtra Census shapefile portal |
| Vegetation (NDVI) / Climate (LST) | Landsat 8/9 Collection 2 Level-2 (Google Earth Engine) |
| Population, Agriculture | Census / POCRA village-level shapefiles; Maharashtra Economic Survey 2025-26 |
| Land Use | Landsat-derived land-cover classification |
| Hydrology (rainfall) | WorldClim 2.1 monthly precipitation climatology |
| Terrain (elevation) | SRTM 1 arc-second DEM |
| Economics (FRA) | Manually compiled from parliamentary answers, CAG audit reports, district-office notices |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/THE-COTTON-LINE.git
cd THE-COTTON-LINE/06_Streamlit
pip install -r requirements.txt
streamlit run app.py
```

## Project Documentation

I have fully cleaned up and finalized my running log file (`CL_Development_Log.md`), my main paper draft (`CL_Research_Paper.md`), and my Executive Summary (`CL_Executive_Summary.md`). I also finished my physical ground-truth check comparing Karanja Ghadge and Sawardoh (you can read all those field details on the dashboard's Ground Truth page or check Section 6.6 of my final research paper). The project no longer has a separate Project Report — its overview paragraph is folded into the start of the Executive Summary instead.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](./LICENSE) — you are free to share and adapt this work for any purpose, including commercially, with attribution. See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every decision, data-pipeline bug, and design pivot — is documented in `CL_Development_Log.md` for full transparency and reproducibility.*
