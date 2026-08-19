# THE COTTON LINE — Does a 150-Year-Old Colonial Land-Tenure Boundary Still Register as a Measurable Spatial Signature in Present-Day Vidarbha?

**Testing whether the 1853 Berar/Central Provinces land-tenure split — abolished in 1956 — still shows up as a spatial-discontinuity signature in cotton-crop phenology, agrarian labor structure, and land-surface temperature today.**

## What This Project Is

In 1853 the British annexed the province of Berar — the five districts that are today Amravati, Akola, Buldhana, Washim, and Yavatmal — directly into colonial administration, settled it under a **Ryotwari** land-tenure system, and pushed it hard into cotton monoculture once the American Civil War cut off Lancashire's usual supply. The six districts to its east — Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli — were instead the core of the **Central Provinces**, settled under the very different **Malguzari** system.

That administrative line was erased at Independence, but it runs almost exactly along the modern Amravati Division / Nagpur Division boundary. This project builds that modern boundary from present-day taluka shapefiles, verifies it against the actual historical district lineage, and tests — via a spatial-discontinuity design, not a before/after or synthetic-control one — whether cotton-signature NDVI, agrarian labor structure, land use, and land-surface temperature still jump at that line today.

## Core Question

Does the historical Berar (Ryotwari) / Central Provinces (Malguzari) boundary still register as a spatial discontinuity in present-day cotton-signature NDVI, agrarian labor structure, and land-surface temperature — once distance-to-boundary, rainfall, and elevation are controlled for?

## Why This Approach

Every other project in this portfolio tests a specific policy or event with a causal-inference design — difference-in-differences, event studies, synthetic control. This one is deliberately a different kind of question: not "did X intervention cause Y effect," but "does a 150-year-old administrative geography still leave a fingerprint on the land." That's a spatial-discontinuity / boundary-persistence problem, closer to landscape pattern analysis and historical GIS than to treatment-effect estimation.

## Core Finding, So Far

No sharp jump in level shows up right at the historical line — but a real east-west gradient does, confirmed independently in two full annual NDVI cycles and echoed in the land-surface-temperature signal: both decline differently with distance from the boundary depending on which side you're on. That's a different, more honest shape of result than a clean discontinuity would have been, and it's reported as such in the dashboard's Spatial Discontinuity Regression page, including where the corridor and full-footprint models genuinely disagree by scale.

The historical district-lineage boundary verification and the FRA compilation supporting the institutional side of this are on the Historical & Institutional Context page.

## Study Design

- Modern boundary built by dissolving 120 talukas into the two divisions and extracting the shared edge — 384.7 km long, from the Akola/Amravati/Wardha corner to the Yavatmal/Chandrapur corner
- 25 km buffer corridor split by division — a 32-taluka near-boundary sample (the actual discontinuity test) and a 68-taluka full-regional-footprint sample, checked as two independent models
- `outcome ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m` — an OLS spatial-discontinuity model, run on both samples, with climate and terrain as controls
- Kharif-to-rabi NDVI decline (the cotton-monoculture-vs-mixed-cropping signature) confirmed across two independent NDVI years, not a single-season read
- Jackknife robustness check — each district dropped and the model re-run, to confirm no single district is driving the result

Full methodology, every data source, the Landsat DN=0 fix, and the corridor-vs-full-footprint scope decision are documented in the dashboard's Methodology & Data page and in `CL_Development_Log.md`.

## Repository Structure

```text
THE_COTTON_LINE/
├── 01_Project _Journal/            # Project roadmap
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

The Development Log (`CL_Development_Log.md`) and Research Paper (`CL_Research_Paper.md`) are both current. The Karanja Ghadge / Sawardoh ground-truth check is still outstanding, and the Project Report and Executive Summary get written once that's complete.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under CC BY 4.0 — you are free to share and adapt this work for any purpose, including commercially, with attribution.

---

*This project's full development process — including every decision, data-pipeline bug, and design pivot — is documented in `CL_Development_Log.md` for full transparency and reproducibility.*
