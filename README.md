# THE COTTON LINE — Does a 150-Year-Old Colonial Land-Tenure Boundary Still Register as a Measurable Spatial Signature in Present-Day Vidarbha?

**Testing whether the 1853 Berar/Central Provinces land-tenure split — abolished in 1956 — still shows up as a spatial-discontinuity signature in cotton-crop phenology, agrarian labor structure, and land-surface temperature today.**

## What This Project Is

Every other project inside my portfolio tests a specific change or policy using standard causal setups like difference-in-differences, event studies, or synthetic control maps. But I chose to build this specific project around a completely different question: I do not want to see if some recent intervention caused a metric shift, but rather if an old 150-year-old administrative border still leaves a physical mark on the landscape today. This is fundamentally a boundary-persistence and spatial-discontinuity issue that sits closer to historical GIS tracking and pattern analysis than to standard treatment checks.

Back in 1853, the British took over Berar—today's Amravati, Akola, Buldhana, Washim, and Yavatmal districts—and forced it into a direct Ryotwari land tax setup to grab cotton for Lancashire mills. On the east side, the Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli districts ran on a landlord-based Malguzari system. Even though the official line vanished in 1956, it sits right where our modern Amravati Division and Nagpur Division boundary lines sit today.

## Core Question

Does that old historical Berar (Ryotwari) versus Central Provinces (Malguzari) boundary still show up as a clear spatial discontinuity on maps of modern cotton-signature NDVI, farm labor ratios, and ground heat once I control for distance-to-boundary, rainfall, and elevation?

## Why This Approach

I built this project to approach spatial analysis differently than the rest of my portfolio. I skipped standard event-tracking models entirely because I am looking at long-term landscape features. I wanted to verify how deep the colonial footprint goes over generations. This is a study of map survival (not a basic short-term policy check).

## Core Finding, So Far

My statistical models show absolutely no sharp level jump right at the old historical line. Instead, I found a very clear east-to-west gradient that shows up across both independent annual satellite greenness cycles and matches my ground temperature metrics. The metrics drop at completely different rates with distance from the border depending on which side you are looking at.

This is a much more honest and accurate picture of the geography than a fake, perfectly clean discontinuity step-jump would be. I chose to report these results exactly as they came out on the dashboard's Spatial Discontinuity Regression page, including the exact places where the small corridor model and the big full-scene map models actually disagree with each other based on scale.

The historical district-lineage boundary verification and the FRA compilation supporting the institutional side of this are on the Historical & Institutional Context page.

## Study Design

- I built the modern border layer by merging 120 taluka shapefiles together to grab the exact 384.7 km shared boundary edge running from the Akola-Amravati-Wardha corner all the way down to Yavatmal and Chandrapur.
- I split my data into two distinct test groups: a tight 32-taluka near-boundary corridor dataset (which acts as my primary discontinuity test within a ±25 km buffer zone) and a much wider 68-taluka regional footprint dataset that I ran as a separate robustness check, not a replacement for the corridor result.
- `outcome ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m` — I ran this OLS spatial-discontinuity regression model across both of my data samples while using terrain maps and rain logs as environmental control variables.
- I tracked the regular drop from the green kharif monsoon peak down to the dry winter rabi point across two full, separate annual Landsat satellite cycles to make sure I am catching actual farming habits rather than just single-year weather fluctuations.
- I set up a complete jackknife test routine that drops out one corridor taluka at a time and reruns my regressions to confirm that no single taluka is swinging the final output numbers.

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

I have fully cleaned up and finalized my running log file (`CL_Development_Log.md`), my main paper draft (`CL_Research_Paper.md`), and my Executive Summary (`CL_Executive_Summary.md`). I also finished my physical ground-truth check comparing Karanja Ghadge and Sawardoh (you can read all those field details on the dashboard's Ground Truth page or check Section 6.6 of my final research paper). The project no longer has a separate Project Report — its overview paragraph is folded into the start of the Executive Summary instead.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under CC BY 4.0 — you are free to share and adapt this work for any purpose, including commercially, with attribution.

---

*This project's full development process — including every decision, data-pipeline bug, and design pivot — is documented in `CL_Development_Log.md` for full transparency and reproducibility.*
