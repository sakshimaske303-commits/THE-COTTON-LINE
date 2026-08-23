# The Cotton Line — Project Report

**Sakshi D. Maske**
Independent Geospatial Researcher

---

## 1. Project Overview

This project tests whether an 1853 colonial land-tenure boundary in Vidarbha — Ryotwari cotton country (Berar) to the west, Malguzari mixed-tenure country (Central Provinces) to the east — still leaves a measurable trace on the landscape, 70 years after it was administratively erased. It's a spatial-discontinuity, boundary-persistence question, closer to landscape pattern analysis and historical GIS than to a policy or treatment-effect evaluation: does a specific, mappable historical institution leave a present-day fingerprint, checked directly against satellite and census data rather than assumed from the history alone.

Vidarbha's farmer-distress geography is usually explained by rainfall, market prices, or crop choice. This project tests a longer-running, more structural explanation on top of those: that a 19th-century land-tenure split, formally abolished in 1956, left an institutional mark that a century of shared statehood since Independence hasn't fully erased.

## 2. Objectives

1. Does cotton-signature NDVI — a taluka's kharif-to-rabi vegetation decline, a monoculture-vs-mixed-cropping signature — jump at the historical Berar/Central Provinces line, once distance-to-boundary, rainfall, and elevation are controlled for?
2. Does agrarian labor structure — the ratio of agricultural laborers to cultivators, a standard landlessness indicator — show the same pattern, at both the immediate boundary corridor and the full regional footprint?
3. Is the modern administrative boundary actually the same line as the historical Berar/Central Provinces one, verified by documented district lineage rather than assumed from geography alone?

## 3. Methodology Summary

**Boundary construction.** The modern boundary was built by dissolving 120 talukas across Vidarbha's 11 districts into the two historical divisions — Amravati Division standing in for Berar/Ryotwari, Nagpur Division for Central Provinces/Malguzari — and extracting their shared edge: a continuous 384.7 km line from the Akola/Amravati/Wardha corner to the Yavatmal/Chandrapur corner. A 25 km buffer split by division defines the 32-taluka immediate-boundary corridor; the same outcomes are separately tested at the full 66–68-taluka satellite-scene footprint to check whether the corridor result is genuinely null or simply underpowered.

**Historical verification.** No digitized period map of the historical boundary was available, so the modern line was checked instead against documented district administrative lineage from 1903–1956. Every historical Berar and Central Provinces district traces cleanly onto its modern successor (renamings, splits, and one boundary adjustment — Balaghat going to Madhya Pradesh in 1956 — are all documented and accounted for). As far as administrative record can show, the modern Amravati/Nagpur Division line is the same line as the historical Berar/Central Provinces boundary.

**Data sources.**

| Variable | Source | Coverage |
|---|---|---|
| Administrative boundaries | IIT Bombay POCRA Maharashtra Census shapefile portal, cross-checked against a secondary shapefile source for gaps | 120 talukas |
| Vegetation (NDVI), Climate (LST) | Landsat 8/9 Collection 2 Level-2 (USGS), WRS-2 path 144, rows 045/046 | 66–68 talukas |
| Hydrology (rainfall) | WorldClim 2.1 monthly precipitation climatology, ~18.5 km grid | 120 talukas |
| Terrain (elevation) | SRTM 1 arc-second DEM | 32–68 talukas |
| Population, agrarian labor, land use | Census village-level shapefiles, aggregated to taluka | 8 of 11 districts |
| Agriculture (cotton share, holding size) | Maharashtra Area-Production-Yield 2024-25; Economic Survey 2025-26 | 11 districts |
| Economics (FRA) | State administrative reports, fact-finding committee report, secondary reporting | Narrative context, not a regression variable |
| Ground-truth (this report's new evidence) | Field-level GPS, dated photographs, Sentinel-2 NDVI/NDRE from a separate field-monitoring project | 7 fields, Karanja Ghadge & Sawardoh |

**Outcome variables and model.** Cotton-signature NDVI (kharif-to-rabi decline, two independent annual cycles), land-surface temperature, the agricultural-laborer-to-cultivator ratio, and land use were each tested with the same specification: `outcome ~ side + signed_dist_km + side×signed_dist_km + annual_total_mm + elevation_m`, an OLS spatial-discontinuity model separating a level jump right at the boundary (`side`) from a slope difference with distance from it (`side×signed_dist_km`), with rainfall and elevation controlled so Vidarbha's real west-drier/east-wetter geography isn't mistaken for an institutional effect. One data-pipeline bug — Landsat's DN=0 fill value being fed straight into the temperature-scaling formula, producing an impossible −124.15°C floor — was found and fixed before any result was trusted; the same unmasked-fill-pixel issue in the reflectance pipeline was fixed the same way.

**Robustness.** Every significant interaction coefficient was put through a leave-one-out jackknife, refitting the model with each corridor taluka dropped in turn, to confirm no single taluka was driving the result alone.

## 4. Key Findings

**No sharp discontinuity, anywhere tested.** None of the four outcome variables — NDVI decline, land-surface temperature, agricultural-laborer ratio, net cultivated area — showed a statistically significant level jump right at the historical boundary, at either the 32-taluka corridor or the 66–68-taluka full footprint, once rainfall and elevation were controlled for.

**A real, twice-confirmed regional gradient in NDVI.** At the full-footprint scale, the kharif-to-rabi NDVI decline was 0.070 points larger on the Berar side than the Central Provinces side (0.325 vs. 0.255, 68 talukas) — and came back almost identical a year later on an entirely separate set of scenes (0.074-point gap, 0.316 vs. 0.241). At the immediate 25 km corridor, that gap nearly disappears (0.310 vs. 0.299) — not a weaker version of the same finding, but a real pattern in its own right: the Central Provinces talukas closest to the line are themselves substantial cotton growers, so the gradient strengthens moving away from the boundary in both directions rather than concentrating at it.

**Land-surface temperature echoes the same shape.** At the full-footprint scale, the `side × distance` interaction was significant independently for both NDVI decline (p = 0.0348) and land-surface temperature (p = 0.0105) — two physically different Earth-observation channels pointing the same direction, which carries more weight than either alone.

**Agrarian labor structure — a genuine, scale-sensitive result.** At the corridor scale, the agricultural-laborer-to-cultivator ratio showed a significant slope-difference interaction (coefficient 0.0374, p = 0.0361), directionally stable across a 32-run jackknife (staying between 0.026 and 0.044) though its significance moved with which taluka was dropped (p as high as 0.138 in a few cases). At the full-footprint scale this flips into a level jump instead (p = 0.014) with the interaction no longer significant — traced to how lopsided the two sides' territory is within the fixed satellite scene, not treated as a contradiction. The corridor-scale reading is treated as the more trustworthy one for describing what happens right at the line.

**Cotton dependency doesn't split cleanly along the historical line.** Wardha (historically Central Provinces, 49% cotton share) and Yavatmal (historically Berar, 51%) are nearly tied for the region's highest cotton dependency — cotton cultivation clearly spread well past the old boundary. Net sown area is the cleaner divide: Berar's five districts sit in a tight 60–75% band, while the Central Provinces' six range from 14% (largely forested Gadchiroli) to 57% (Nagpur) — a pattern consistent with Ryotwari bringing the whole province under individual cultivation while Malguzari left more land under estate or forest control.

**Historical-lineage verification confirms the boundary.** Every historical Berar and Central Provinces district traces cleanly onto its modern successor district, with one documented exception (Balaghat, ceded to Madhya Pradesh in 1956) that doesn't affect the Vidarbha study area.

## 5. Ground-Truth Validation

Everything above is satellite- or census-derived. This report closes the one open item flagged throughout the project's development: a direct field check of the remote-sensing signal against real, on-the-ground crop and canopy conditions.

Rather than schedule a separate visit, this check draws on a GPS-mapped, weekly-photographed field-monitoring project already running on family land inside the study corridor — seven field boundaries across Karanja Ghadge and Sawardoh villages, Wardha district, both on the Central Provinces/Malguzari side. Two fields sit in Karanja Ghadge itself, the exact taluka this project already holds a reference point for (June 2026 Landsat: mean LST 55.97°C, mean NDVI 0.264, 45.8% valid pixel coverage). Field-level Sentinel-2 NDVI at those two fields came back at 0.329 and 0.287 on 14 July 2026 — a plausible range next to the coarser taluka figure — and dated ground photographs from the same coordinates show closed, healthy canopy consistent with those values. Five more fields in Sawardoh moved the same direction over the same stretch, offered as supporting rather than primary evidence.

This is not a pixel-identical check. The taluka reference is Landsat at 30 m resolution, averaged across the whole taluka; the field-level numbers are Sentinel-2 at 10 m, at the exact polygon, mostly on a different date. What it verifies is that the same kind of signal — a vegetation index tracking real crop growth — shows up consistently at finer resolution against conditions that can be directly seen, not that the two figures should match precisely. One incidental finding worth noting: Karanja Ghadge's own Sentinel-2 pass for 21 June 2026 returned zero valid pixels for both fields, cloud-masked out entirely — an independent sensor losing data over the same corner of the scene footprint where the Landsat taluka reading already sits at less-than-full coverage (45.8%). Two different platforms arriving at the same limitation is a small piece of corroborating evidence that this specific location is genuinely difficult to observe cleanly from orbit, on any sensor.

Full detail, including all seven fields' data and the ground photographs themselves, is on the project dashboard's Ground Truth page.

## 6. Limitations

- **Sample size at the corridor scale** (n = 28–32) is the real constraint on statistical power — the jackknife results hold direction but not always significance under taluka exclusion.
- **Rainfall is a long-term climatology**, not a year-specific time series, and its ~18.5 km grid is coarser than most individual talukas.
- **The full-footprint sample is asymmetric** by satellite scene geometry, not by where the historical provinces actually end — this complicates comparing a level-jump result against a slope-difference result across scales, most visibly in the agricultural-laborer finding.
- **Irrigation data was dropped** as untrustworthy (58–92% reported coverage against a well-documented 15–20% actual irrigated share for this cotton belt).
- **Forest Rights Act figures are narrative context**, not a regression variable — no clean taluka- or consistent district-level public dataset exists for Vidarbha.
- **The historical boundary check is lineage-based**, not a literal overlay against a digitized period map, which wasn't available in accessible form.
- **The ground-truth check is a genuine but small-sample cross-scale comparison** (Section 5) — seven fields, one taluka, one season, checked against a coarser-resolution, different-sensor reference point. It speaks to NDVI specifically, at these coordinates, not a blanket validation of every outcome variable in this report.

## 7. Conclusion and Future Work

The honest summary is a real institutional-geography legacy that shows up as a gradient across Vidarbha rather than a discontinuity right where the historical institutions were once drawn. No outcome jumps sharply at the old Berar/Central Provinces line, at either scale tested — that absence is reported directly. What holds up is a twice-confirmed regional NDVI gradient, echoed independently in land-surface temperature, plus a more qualified, scale-sensitive signal in agrarian labor structure. A historical-lineage check confirms the modern boundary used throughout is, as far as documented administrative history shows, the same line as the 1853–1956 boundary. The ground-truth check, completed as part of this report, confirms the underlying remote-sensing signal tracks real crop conditions at seven real field boundaries.

Future work: extending population and land-use coverage to all 11 districts (currently 8), processing the remaining Landsat scenes to remove the full-footprint sample's scene-geometry asymmetry, and sourcing a digitized historical-era map to overlay directly against the modern boundary construction, on top of the lineage-based verification already completed.

---

*Full methodology, every regression coefficient, and the complete reference list are in the Research Paper (`CL_Research_Paper.md` / `.pdf`). Every decision, data-pipeline bug, and design pivot behind this project is documented in the Development Log (`CL_Development_Log.md`).*
