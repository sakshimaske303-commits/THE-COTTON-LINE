# THE COTTON LINE — Project Roadmap

## Research Question

Does the historical Berar (Ryotwari, cotton-monoculture) / Central Provinces (Malguzari, mixed-tenure) administrative boundary — abolished at Independence — still register as a measurable spatial discontinuity in present-day cotton dependency, drought vulnerability, and agrarian stress across Vidarbha's 11 districts?

## Phase 1 — Data Foundation (in progress)

- [x] Administrative boundaries — all 11 districts, taluka-level
- [x] Climate — Landsat thermal (LST), merged regional mosaic
- [x] Agriculture — APY 2024-25, cotton MSP procurement, Economic Survey
- [x] Hydrology — WorldClim precipitation climatology
- [x] Infrastructure — roads, railways (OSM)
- [x] Terrain — SRTM DEM, derived slope
- [x] Vegetation — Landsat red/NIR bands for NDVI
- [x] Population — village-level Census attributes, all 11 districts
- [x] Land use / land cover — census-derived breakdown (forest/net-sown/fallow/etc.), not satellite LULC; a real independent classification, satellite cross-check still a nice-to-have
- [x] Economics — covered by the APY 2024-25 + Economic Survey District Indicators already pulled in for the agrarian-stress proxy, no separate sourcing needed
- [x] FRA — compiled what public sources actually have (Maharashtra state totals, one real Gadchiroli district anchor, a Vidarbha-wide regional CFR figure, a few village case studies) — no clean taluka/district-level panel exists publicly, so this stays a narrative data point for the write-up, not a Phase 4 regression variable
- [x] Modern Amravati/Nagpur Division boundary built from taluka dissolve — historical cross-check still pending, see Phase 2

## Phase 2 — The Boundary

- [x] Dissolve the 11-district taluka layer into the two divisions and extract the modern boundary line (384.7 km, verified clean at the seam)
- [x] Build the analysis corridor: 25 km buffer on either side of the line, split by division (32 talukas fall inside it — this is the working discontinuity-test sample)
- [ ] Digitize or source the precise historical Berar/Central Provinces line (candidate sources: 1901-1931 Imperial Gazetteer district maps, Central Provinces & Berar administrative atlases) and sanity-check it against the modern division line built above — note and handle any places where they diverge (some taluka-level boundary changes are likely over 120+ years)

## Phase 3 — Outcome Variables from Earth Observation

- [x] Found and fixed a DN=0 NoData bug in the existing LST/NDVI pipelines (fill pixels were leaking in as fake data) — reprocessed thermal and reflectance bands correctly for the corridor footprint (2 of 12 scenes, 97.7% of corridor area)
- [x] First single-date (June 2026, pre-monsoon) LST and NDVI comparison across the corridor — Berar side reads hotter/less green than Central Provinces side; directionally consistent with the hypothesis but not yet the real test
- [x] Cotton dependency / cropping diversity — kharif-to-rabi NDVI seasonal signature done (Entry 7): 0.325 decline Berar vs 0.255 Central Provinces region-wide, gap narrows sharply at the immediate corridor
- [ ] Second-year NDVI confirmation — `download_seasonal_scenes_year2.py` written and handed off (kharif 2024 / rabi 2024-25, same footprint), waiting on the local run to confirm the kharif-to-rabi decline isn't a one-season fluke
- [ ] Drought vulnerability — have single-date LST (Entry 3) and rainfall climatology totals (Entry 8), but no LST anomaly analysis and no true interannual rainfall variability yet (WorldClim is a climatology, not a time series) — would need a second data source for real year-to-year variability
- [x] Agrarian stress proxy — done (Entry 4): cotton share, net sown %, cropping intensity, foodgrain output, holding size, all 11 districts
- [x] Land fragmentation — `avg_holding_ha` compared corridor-wise (Berar 1.81 vs CP 1.90 ha) — flat result, see Phase 4
- [ ] Reprocess the remaining 10 scenes for a full 11-district LST/NDVI mosaic, if a district-level (not just corridor-level) comparison is ever needed

## Phase 4 — Spatial Discontinuity Analysis

- [x] Elevation control sourced (SRTM, 32 corridor talukas) and master regression dataset assembled (32 talukas x 19 variables)
- [x] Ran the RD regression (`side + signed_dist_km + side×signed_dist_km + rainfall + elevation`) for NDVI decline, ag-laborer ratio, net area %, and LST — no clean level jump at the boundary at this sample size (n=28-32), one significant slope-difference (ag-laborer ratio interaction, p=0.036), rainfall/elevation controls themselves frequently significant as expected
- [x] Land fragmentation (avg holding size) checked against the corridor split — flat result, no real Berar/CP divide (1.81 vs 1.90 ha)
- [x] Robustness-checked the ag-laborer interaction via leave-one-out jackknife — direction/magnitude stable across all 32 runs, but significance is borderline (holds in 26/32, a few individual talukas can flip it) — "suggestive, not bulletproof"
- [x] Retested NDVI decline and LST at the full 68/66-taluka scene footprint (not just the 25km corridor) — no level jump at the boundary here either, but the side×distance interaction is now significant in BOTH outcomes (p=0.035, p=0.010), backing up the corridor-scale ag-laborer result with real statistical power — gradient, not discontinuity, is holding up as the read
- [x] Sourced and processed Bhandara/Gondiya/Gadchiroli population+land-use census data (was already downloaded, just unprocessed) — reran ag-laborer ratio and net area % at full footprint (n=67-68); net area % stays non-significant either way, ag-laborer ratio flips from a slope-difference (corridor) to a level-jump (full footprint) — traced to the Berar side barely extending past 20km in this scene vs. CP reaching 160km+, so treating the corridor-only read as the more trustworthy one for "right at the boundary" and flagging the full-footprint version as a broader-scale signal instead
- This is a boundary/border-effect design, not a treatment-effect causal design — the question is pattern persistence, not policy attribution

## Phase 5 — Synthesis and Narrative

- Tie the boundary-effect finding back to the 1900 famine geography and the modern agrarian-distress geography as historical bookends
- Full write-up: Project Report, Research Paper (with the institutional-economics literature — Banerjee-Iyer and the Central Provinces recoding dispute — properly engaged, not just cited), Development Log, interactive dashboard with the historical boundary as its own map layer

## Explicitly Not Doing

- No difference-in-differences, event-study, or synthetic-control design — this project is a spatial-discontinuity / boundary-persistence analysis, deliberately distinct in method from the rest of this portfolio
- Not framing this as a policy evaluation of any specific present-day scheme
