# THE COTTON LINE — Is an Erased Colonial Land-Revenue Boundary Still Visible in Vidarbha?

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14802/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22111298.svg)](https://doi.org/10.5281/zenodo.22111298)

Version 2.1 (October 2026). Berar in western Vidarbha was settled under Ryotwari land revenue, and the Central Provinces to the east under Malguzari. The provincial line was abolished in 1956, but on district lineage it matches today's Amravati/Nagpur Division boundary.

This project asks whether that line is still visible as a break in present-day agriculture, using Landsat satellite indices and the 2011 Census, with spatially robust tests.

**Answer: no step at the line.** Vidarbha's cotton core straddles the old line: the satellite cropping index peaks near it on both sides and falls away in both directions. The index tracks official cotton statistics, and fake boundaries reproduce the slope differences found at the real one.

## Research question and hypotheses

After controlling for rainfall, elevation and distance, is the former Berar/Central Provinces boundary detectable as a spatial discontinuity in present-day satellite and census indicators of agriculture?

- **H1:** a level step at the line.
- **H2:** a change of slope with distance at the line.

## Findings

| | Result |
|---|---|
| H1, step | None in the 32-taluka corridor, the Landsat sample (98 talukas for NDVI, 56 for LST) or local-linear estimates at the line. The one exception, labour structure in the 119-taluka model (+0.96, Holm p = 0.029), is absent in the corridor and in local estimates: a regional difference concentrated in Amravati district. |
| H2, slope | The gradient changes across the line for NDVI decline in both years (Holm p < 0.001): the line sits on the crest of a ridge. LST and labour change slope before correction. Placebo lines inside each side reproduce the NDVI and labour patterns. |
| NDVI by side | 0.255 vs 0.246 (year 1) and 0.319 vs 0.262 (year 2); 0.29 on both sides within 50 km of the line. |
| Validation | District NDVI decline vs cotton share: r = 0.86 (10 districts), 0.77 without paddy districts. Field check on 7 Roots & Reflectance fields: 13 of 14 field-years match the reported winter crop. |
| Tests | 20 tests; 5 have conservative p < 0.05; 3 survive Holm. |

Full write-up: [`CL_Research_Paper.md`](CL_Research_Paper.md) · two-page version: [`CL_Executive_Summary.md`](CL_Executive_Summary.md).

## How it works

1. **Rebuild the line.** 120 Census/LGD talukas are dissolved into the two divisions and the 384.7 km shared edge is extracted. It is checked against district lineage 1903–1956 (district level, not a period-map overlay).
2. **Measure the land.**
   - Landsat 8/9 NDVI for early November and early March in two years, at 30 m over paths 144–146, with cloud, shadow and water masked and only ESA WorldCover cropland kept, on pixels valid on both dates.
   - June land surface temperature.
   - Coverage is counted against each taluka's cropland (NDVI) or polygon (LST); talukas less than half observed are excluded.
3. **Add the people.** Census 2011 village data, aggregated to taluka for all 11 districts.
4. **Test.** Step and slope regression with rainfall and elevation, at three scales. Inference uses the most conservative of HC3 and Conley spatial errors, with Holm correction, local-linear RD, placebo lines, symmetric windows, influence and coverage checks, and power (MDE).

## Reproduce everything

```bash
git clone https://github.com/sakshimaske303-commits/THE-COTTON-LINE.git
cd THE-COTTON-LINE
pip install -r requirements.txt
python 05_Python/run_all.py          # rebuilds every table, result and figure from the repository (about 1 minute)
cd 06_Streamlit && streamlit run app.py
```

The pipeline needs only numpy, pandas, scipy, matplotlib and tifffile; no GDAL is required.

The default run starts from the processed tables in `03_Data_Processed/` (the 30 m taluka NDVI table, Census 2011 taluka statistics, WorldClim rainfall and SRTM elevation) and reproduces every number, figure and interactive page. Steps that read raw data run only when that data is present in `02_Data_Raw/`.

**Rebuild NDVI from raw scenes (optional, about 9 GB):**
1. `python 05_Python/00_download_inputs.py` downloads the 36 Landsat scenes (B4, B5, QA) and ESA WorldCover.
2. `python 05_Python/run_all.py --full` rebuilds the 30 m masked NDVI table, then everything else.

| Step | Script | Output |
|---|---|---|
| 1 | `01_build_taluka_geometry.py` | centroids, signed distance, corridor flag |
| 2 | `02_build_census_stats.py` | Census 2011 taluka statistics, 11 districts |
| 3 | `03_build_eo_climate_stats.py` | LST taluka stats (polygon coverage), WorldClim rainfall |
| 3b | `03b_build_eo_30m_masked.py` | 30 m masked NDVI, paths 144–146 (with `--full`) |
| 3c | `03c_sample_elevation.py` | SRTM elevation, 120 talukas |
| 4 | `04_build_analysis_dataset.py` | `Phase4/analysis_taluka_dataset.csv` |
| 5 | `robustness_checks.py` | `Phase4/results/*.csv`, `key_numbers.json` |
| 6 | `05_make_figures.py` | `07_Outputs/v2_fig*.png` |
| 7 | `06_make_interactive.py` | `outputs/` interactive maps and plots |
| 8 | `08_field_bridge.py` | field check, `Ground_Truth/field_decline_*.csv`, Figure 8 |

Steps 2, 3 (rainfall part) and 3c need raw files that are not in git and not fetched by `00_download_inputs.py`: the POCRA village shapefile zips for the 11 districts (`02_Data_Raw/Population/`), WorldClim 2.1 10-minute monthly precipitation (`02_Data_Raw/Hydrology/`) and SRTM 1 arc-second tiles (`02_Data_Raw/Terrain/`). Without them the pipeline uses the processed tables. `07_export_pdfs.py` rebuilds the three PDFs from the Markdown and is not part of the run.

`fix_lst_pipeline.py`, `fix_vegetation_pipeline.py` and `fix_slope_pipeline.py` are the original DN = 0 / slope fixes that produced the 300 m rasters, kept for the record.

## Repository structure

```text
THE_COTTON_LINE/
├── 02_Data_Raw/            raw downloads (not in git: Landsat, SRTM, WorldClim, Census zips)
├── 03_Data_Processed/      boundary geometry, taluka tables, 300 m NDVI/LST rasters,
│   └── Phase4/             analysis_taluka_dataset.csv and results/
├── 05_Python/              the pipeline (run_all.py) and shared helpers (cl_lib.py)
├── 06_Streamlit/           dashboard: app.py + 9 pages
├── 07_Outputs/             figures (v2_fig1 … v2_fig8)
├── outputs/                interactive maps and plots for the portfolio
├── CL_Research_Paper.md    paper (+ PDF)
├── CL_Executive_Summary.md summary (+ PDF)
└── CL_Development_Log.md   development log (+ PDF)
```

## Data sources

| Dataset | Provider |
|---|---|
| Taluka boundaries | Census 2011 / LGD sub-districts via datta07/INDIAN-SHAPEFILES; IIT Bombay POCRA district shapefiles |
| NDVI, LST | Landsat 8/9 Collection 2 Level-2 (USGS), accessed through Microsoft Planetary Computer |
| Labour, land use | Census of India 2011 village attributes (IIT Bombay POCRA village shapefiles) |
| Rainfall | WorldClim 2.1 monthly normals (Fick & Hijmans, 2017) |
| Elevation | SRTM 1 arc-second (NASA/USGS) |
| District context | Maharashtra APY 2024-25; Economic Survey of Maharashtra 2025-26 |
| Cropland mask | ESA WorldCover 2021 v200 (CC BY 4.0) |

## Limitations

- Gadchiroli and most of Gondiya (Landsat path 143) are not observed; LST uses one scene.
- 2021 cropland mask; neighbouring paths are up to nine days apart.
- Single-date scenes per season.
- 2011 census against 2024–26 imagery.
- Rainfall is a climatology; soil and irrigation are not controlled.
- District-level boundary verification.
- The line is also a pre-colonial frontier, a river and an agro-ecological transition, so nothing here can be attributed to tenure.

The companion field study *Roots & Reflectance* (seven fields, Central Provinces side) is illustrative and does not validate the boundary comparison.

## Author and licence

**Sakshi D. Maske**, Independent Geospatial Researcher. Code: MIT licence. Text, figures and processed data: CC BY 4.0 (see `LICENSE`). Cite with `CITATION.cff`.
