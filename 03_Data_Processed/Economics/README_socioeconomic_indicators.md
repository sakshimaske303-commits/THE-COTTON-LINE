# Vidarbha socio-economic indicators (MITRA, extracted August 2026)

**Source:** Maharashtra Institution for Transformation (MITRA), Office of the Chief Economic Advisor
to the CM, Department of Planning, GoM, "Socio-Economic Analytics" district explorer:
https://mahaniti.mahamitra.org/resources/socio-economic-analytics/explorer

The portal's underlying data are the district annexures of the **Maharashtra Economic Survey 2024-25**.
It has no bulk download or API, so I recorded the 45-indicator panel for each of the 11 districts by hand.

## Files

- `vidarbha_socioeconomic_indicators.csv`: indicators as rows, districts as columns.
- `vidarbha_socioeconomic_indicators_wide.csv`: districts as rows, indicators as columns, for joins
  in QGIS or pandas. Includes four "(actual)" columns with area and population converted to real units.

## Units

Some indicators are in thousands or lakhs:

- **Geographical Area (sq km) [2011]**: thousand sq km (Nagpur `9.9` = 9,900 sq km).
- **Population, Total Households, Projected Population (lakh)**: lakhs (Nagpur `46.5` = 4,650,000).
- All other indicators are in their stated units.

Each indicator carries a `[year]` tag: mostly 2011 Census for demographics, 2023-24 for economic and
social indicators, 2021-22 for factories, 2015-16 for landholdings, 2013 (6th Economic Census) for
establishments.

## Use in this project

- **Net sown area, foodgrain area and output, cropping intensity, holding size, MGNREGA days:**
  district-level cross-check of the taluka census aggregates.
- **Annual rainfall, forest area:** cross-check of the raster and census values.
- **Per capita income, credit-deposit ratio, banking access, priority-sector credit:** background
  for the discussion.
- **SC/ST share, literacy, underweight children, schools:** regional profile in the introduction.

District-level only (11 rows).
