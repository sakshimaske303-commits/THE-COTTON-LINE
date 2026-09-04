# Vidarbha Socio-Economic Indicators — MITRA (extracted Aug 2026)

**Source:** Maharashtra Institution for Transformation (MITRA), Office of the Chief Economic
Advisor to the Hon'ble CM, Dept. of Planning, GoM — "Socio-Economic Analytics" district explorer:
https://mahaniti.mahamitra.org/resources/socio-economic-analytics/explorer

Data underlying this portal is the **Maharashtra Economic Survey 2024-25** (district-wise annexures).

This was extracted by clicking each of the 11 Vidarbha districts one at a time in the live map
explorer and capturing the full 45-indicator "Feature detail" panel for each (there is no bulk
download/API on the site — it only renders per-district on click).

## Files

- `vidarbha_socioeconomic_indicators.csv` — indicators as rows, districts as columns. Good for
  scanning/comparing one indicator across all 11 districts at a glance.
- `vidarbha_socioeconomic_indicators_wide.csv` — districts as rows, indicators as columns
  (standard "long table" shape). This is the one to use if you want to join it to your district
  shapefiles/attribute tables in QGIS, or load into pandas for analysis. It also includes 4 extra
  "(actual)" columns with area/population converted out of thousands/lakhs into real units.
- `README.md` — this file.

## Units — read this before using the numbers

The portal reports several indicators in **thousands** or **lakhs**, not raw units. Watch for:

- **Geographical Area (sq km) [2011]** — in **thousand sq km**. E.g. Nagpur shows `9.9` = 9,900 sq km.
- **Population (lakh) [2011]**, **Total Households (lakh) [2011]**, **Projected Population (lakh)
  [Mar 2025]** — in **lakhs** (1 lakh = 100,000). E.g. Nagpur Population `46.5` = 4,650,000 people.
- Everything else (rates, percentages, per-lakh-population ratios, per-capita income in Rs, etc.)
  is already in its stated real unit.

The wide CSV includes pre-computed "(actual)" columns for area/population/households/projected
population so you don't have to do this conversion by hand.

Each indicator also carries a `[year]` tag in its column/row name showing which year/round of data
it's from (mostly 2011 Census for demographics, 2023-24 for most economic/social indicators,
2021-22 for factory data, 2015-16 for landholding size, 2013 for establishments/employment from
the 6th Economic Census).

## Relevance to THE COTTON LINE

- **Net Sown Area %, Foodgrain Area %, Foodgrain Production per capita, Cropping Intensity,
  Avg Operational Holding size, MGNREGA employment days** → Section 4.2 (Agrarian Labor Structure,
  Land Use, and Cotton Dependency) — district-level cross-check against this project's own
  taluka-level Census aggregates.
- **Annual Rainfall, Forest Area %** → Section 3.5 (rainfall control variable) and Section 4.2
  (forest-cover comparison) — district-level cross-check against this project's raster/Census-
  derived numbers.
- **Per Capita Income, Credit-Deposit Ratio, Banking Offices/ATMs per lakh, Priority Sector
  Credit %** → background context for the Discussion's agrarian-distress-governance framing.
- **SC/ST %, Literacy, Underweight Children %, Schools per lakh** → general socio-economic profile
  referenced in the Introduction.

## What this does NOT cover

This is **district-level** data only (11 rows). It does not solve the taluka-level shapefile
completeness gap identified separately in the shapefile QA — that needs a different source (see
the main sourcing report).
