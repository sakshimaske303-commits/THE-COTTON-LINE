# THE COTTON LINE — Development Log

Running log of every decision, data source, and pivot in this project. Format: one dated entry per work session, most recent at the bottom.


## Index

1. [Entry 1](#entry-1)
2. [Entry 2](#entry-2)
3. [Entry 3](#entry-3)
4. [Entry 4](#entry-4)
5. [Entry 5](#entry-5)
6. [Entry 6](#entry-6)
7. [Entry 7](#entry-7)
8. [Entry 8](#entry-8)
9. [Entry 9](#entry-9)
10. [Entry 10](#entry-10)
11. [Entry 11](#entry-11)
12. [Entry 12](#entry-12)
13. [Entry 13](#entry-13)
14. [Entry 14](#entry-14)
15. [Entry 15](#entry-15)
16. [Entry 16](#entry-16)
17. [Entry 17](#entry-17)
18. [Entry 18](#entry-18)
19. [Entry 19](#entry-19)
20. [Entry 20](#entry-20)
21. [Entry 21](#entry-21)
22. [Entry 22](#entry-22)

---

## Entry 1

I started pulling data for this region back in late May, under the working name Project Prism, with a broad "climate-resilient Vidarbha" framing and no fixed research question yet — just a conviction that this was the region I most needed to build something on, and a first pass at acquiring every dataset a comprehensive regional study would eventually need. Before settling on a real hypothesis I want to record exactly what I already have on disk, since a chunk of it was collected before the actual research question existed and I don't want to lose track of provenance.

**Already collected, before the pivot:**

- **Administrative boundaries** — taluka-level shapefiles for all 11 Vidarbha districts (Akola, Amravati, Bhandara, Buldhana, Chandrapur, Gadchiroli, Gondia, Nagpur, Wardha, Washim, Yavatmal), sourced from IIT Bombay's POCRA Maharashtra Census shapefile portal. Also have the 1994 Development Boards Order for Vidarbha, Marathwada and the rest of Maharashtra on file — the formal government recognition of the region's backwardness, which is useful primary-source context for the regional-disparity framing.
- **Climate** — Landsat 8/9 Collection 2 Level-2 thermal band (Band 10, surface temperature) scenes covering the full Vidarbha extent, plus a merged/mosaicked land-surface-temperature raster for the region.
- **Agriculture** — district-wise Area-Production-Yield (APY) statistics for 2024-25, Cotton Corporation of India MSP procurement figures (2019-20 through 2024-25), and the Maharashtra Economic Survey 2025-26 (Agriculture chapter and district indicators chapter).
- **Hydrology** — WorldClim 2.1 monthly precipitation climatology (10 arc-minute global grid) clipped to Vidarbha.
- **Infrastructure** — road and rail network vector data for the state, sourced from OpenStreetMap.
- **Terrain** — SRTM 1 arc-second (~30 m) digital elevation tiles covering the full region, merged, clipped, and reprojected, with slope derived from the merged DEM.
- **Vegetation** — Landsat 8/9 Level-2 surface-reflectance red and near-infrared bands (Band 4, Band 5) across the same scene footprint as the climate data, for NDVI computation.

Two categories are still genuinely empty: **Land_use** and **Economics**. Forest Rights Act data — claims filed, titles distributed, community forest resource area — turned out not to exist anywhere as a clean, ready-to-download district-wise dataset; what's out there is scattered across parliamentary answers, CAG audit reports, and individual district-office PDF notices rather than one usable source. That's still an open problem, not solved yet.

**Today's addition — Population.** Downloaded village-level Census shapefiles for all 11 districts from the same IIT Bombay POCRA portal I'd already used for the administrative boundaries — this version carries 600+ census attributes per village (population counts, literacy, sex ratio, and more), not just boundary geometry. All 11 district files are on disk now.

**The pivot.** The original "climate-resilient Vidarbha" framing was too broad and too close to what everyone building a regional geospatial project already does — land monitoring, vulnerability indices, the same toolkit I've already used across the rest of this portfolio. What I actually want for this project is something that could only come out of my specific academic background — Economics, Political Science, History, and Geography — not just a technically competent satellite analysis.

The reframe: Vidarbha's own internal administrative history gives me a real natural pair to test. The five western districts (Amravati, Akola, Buldhana, Washim, Yavatmal) were the former province of Berar — annexed directly by the British in 1853, settled under a Ryotwari system, and pushed hard into cotton monoculture once the American Civil War cut off Lancashire's usual supply. The six eastern districts (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli) were the core of the Central Provinces, settled instead under the very different Malguzari system. That boundary was officially erased at Independence, but it runs almost exactly along the modern Amravati Division / Nagpur Division line — a boundary I already had shapefiles for. It also traces almost exactly onto the geography of the 1900 Berar famine (which hit the most cotton-specialized districts hardest) and onto the modern agrarian-distress geography of Vidarbha, which is still worst in the same western districts.

New project name: **THE COTTON LINE**. Core question: does that 150-year-old colonial economic-institutional boundary still register as a measurable spatial discontinuity in present-day cotton dependency, drought vulnerability, and agrarian stress — checked directly against satellite-derived data rather than assumed from the history alone. The full theoretical grounding — institutional persistence theory, the historical-geography basis for why Berar was pushed into cotton specifically, and the physics behind the remote-sensing measurements this project uses — will get its own dashboard page later, same as the theory pages in the rest of this portfolio, rather than living as a separate standalone document right now.

**Still open after this entry:**
- Land_use / LULC data — not sourced yet.
- Economics category — not sourced yet (may fold into the Agriculture MSP/Economic Survey data already on hand rather than needing a separate source).
- FRA data — no clean dataset found; will likely need manual compilation from the scattered PDF sources rather than a single download.
- The historical Berar / Central Provinces boundary itself still needs to be properly digitized and checked against the modern Amravati/Nagpur Division line rather than just assumed identical — they're described as "roughly corresponding," not confirmed geometrically identical.
- No analysis has been run yet. This entry is data-audit and reframing only.

---

## Entry 2

First real geometry for this project. Renamed the working folder from Project Prism to THE_COTTON_LINE at this point, so this entry also marks the switch to the new folder identity everywhere going forward.

**What I did.** Loaded the taluka-level administrative layer (120 talukas across all 11 districts, already on disk from the original data pull) and split it into the two historical zones by district name: Amravati Division — Akola, Amravati, Buldhana, Washim, Yavatmal — standing in for the old Berar/Ryotwari territory, and Nagpur Division — Nagpur, Wardha, Bhandara, Gondia, Chandrapur, Gadchiroli — standing in for the old Central Provinces/Malguzari territory. Dissolved each group of talukas into one polygon per division (56 talukas → Amravati Division, 64 talukas → Nagpur Division), then took the shared edge between the two dissolved polygons as the modern boundary line.

That shared-edge extraction came out as 256 tiny disconnected line fragments at first — not a bug, just an artefact of adjacent taluka polygons not sharing exact vertices at their shared edges. Ran a line-merge pass on it and it collapsed cleanly into one continuous line, 384.7 km long, running from the Akola/Amravati/Wardha corner in the north down through the Yavatmal/Chandrapur corner in the south.

Built a 25 km buffer corridor centered on that line and split it by division — a "Berar side" and a "Central Provinces side" near-boundary zone, 7,387 km² and 7,987 km² respectively. 32 of the 120 talukas fall inside this corridor, spread across Amravati, Yavatmal, Wardha, Chandrapur, and a sliver of Nagpur district — this is the working sample the actual discontinuity test will run on in Phase 4, rather than the full 11-district set.

Generated a verification map overlaying the two divisions, the dissolved boundary, and the corridor against the taluka grid to visually sanity-check that the line sits where it should and that the corridor is roughly symmetric on both sides. It is — no stray gaps or overlaps at the seam.

**What this is not yet.** This is the *modern administrative* proxy for the boundary, built entirely from present-day Census/POCRA taluka shapefiles. I still haven't cross-checked it against an actual historical map of the Berar/Central Provinces line — the Roadmap always flagged these as "roughly corresponding," not confirmed identical, and that check is still outstanding. Candidate sources for that remain the Imperial Gazetteer district maps (1901-1931 editions) and Central Provinces & Berar administrative atlases; haven't located a usable digitized version of either yet.

**Files produced this entry** (`03_Data_Processed/Administrative/`): `divisions_dissolved.geojson` (2 polygons), `division_boundary_line.geojson` (the 384.7 km line), `discontinuity_zone_25km.geojson` (the two-sided corridor), `boundary_verification_map.png`.

**Still open after this entry:**
- Historical boundary cross-check against period maps — not done, no source located yet.
- Land_use, Economics, FRA data — still not sourced (carried over from Entry 1).
- Next step is Phase 3: pulling the actual outcome variables (cotton-dependency signature from NDVI, drought/LST anomaly, agrarian-stress proxy) for the 32 talukas inside the corridor, so the discontinuity test in Phase 4 has something to run on.

---

## Entry 3

Went looking for the Climate-category thermal data referenced in Entry 1 and found it wasn't actually where it should be — the raw Landsat ST_B10 thermal scenes, the two merged LST attempts (`vidarbha_lst_merge.tif`, `vidarbha_mergedLST.tif`), and an 8-byte broken stub (`A1_LST_Celcius.tif`) were all sitting inside the `Land_use` folder instead of `Climate`. The actual Climate folder is empty. Leaving this as-is for now rather than moving ~3.5GB of rasters around, but noting it here so it's not confusing later — real LULC/land-cover data still hasn't been sourced, despite the folder being non-empty.

**The bug.** Both existing merged LST rasters were reading impossible temperatures — a minimum of -123.15°C, which isn't a real land-surface temperature anywhere on Earth. Root cause: Landsat Collection 2 Level-2 ST_B10 scenes use DN=0 as the fill/no-data value for cloud-masked and off-swath pixels (roughly a third of every scene), and the original conversion pipeline applied the Kelvin scale/offset directly to the raw DN without masking DN=0 out first. DN=0 run through the formula produces exactly 149K = -124.15°C, which is exactly the floor value both broken merges were showing. Same root-cause bug was sitting in the vegetation pipeline too — `vegetation_mergedB4.tif` reports 100% valid pixels, which isn't possible given the same ~33% fill-pixel rate confirmed on a real scene; those fill pixels were never masked and are silently sitting in the merged raster as fake "reflectance = 0" values.

**The fix.** Mask DN=0 as NoData *before* applying the scale/offset, not after. Reprocessed both the thermal (ST_B10 → Celsius) and reflectance (SR_B4, SR_B5 → true reflectance) pipelines from the raw scenes with this fix, then computed NDVI = (B5-B4)/(B5+B4) from the corrected bands, clipping anything outside the physically valid [-1, 1] range (a handful of pixels — 4,750 out of 73.7 million — blew up from near-zero denominators at reprojection edges and needed dropping).

**Scope of this pass.** Rather than reprocessing the full 12-scene mosaic that covers all 11 districts, I used just the two scenes that cover WRS-2 path 144 (rows 045 and 046) — together they cover 97.7% of the 25km discontinuity corridor's area, which is the only zone this project's actual test runs on. There's a small uncovered sliver (2.3% of the corridor area, a corner near the Amravati/Wardha edge, roughly lat 21.30-21.46) where two scene footprints don't quite meet — flagging it rather than chasing it down with more downloads right now, since it doesn't materially change the pattern below.

**First read of the result.** For the 28 corridor talukas with usable pixel coverage (11 on the Berar/Amravati-Division side, 17 on the Central-Provinces/Nagpur-Division side), this single June 2026 snapshot shows the Berar side running hotter (mean LST 56.4°C vs 54.6°C) and less green (mean NDVI 0.245 vs 0.292) than the Central Provinces side, right at the corridor. Directionally this is what the project's hypothesis would predict — but it's one pre-monsoon date, not the seasonal signature the actual cotton-dependency test in the Roadmap calls for, and the sample is small enough (11 vs 17 talukas) that I'm treating this as a first working data point, not a result to lean on yet.

**Files produced this entry:**
- `03_Data_Processed/Climate/lst_fixed_300m_June2026.tif` — corrected LST mosaic (300m, downsampled from native 30m for file size; full-resolution version used for the zonal stats below but not saved to disk here)
- `03_Data_Processed/Climate/taluka_lst_ndvi_stats.csv` — per-taluka mean LST and NDVI for all 66 talukas with usable data across the 2-scene footprint
- `03_Data_Processed/Vegetation/ndvi_fixed_300m_June2026.tif` — corrected NDVI mosaic (300m)
- `03_Data_Processed/Vegetation/corridor_taluka_lst_ndvi_stats.csv` — same stats, subset to the 28 corridor talukas
- `07_Outputs/lst_ndvi_corridor_comparison.png` — NDVI map, LST map, and division boxplots for both variables

**Still open after this entry:**
- The two old buggy merges (`vidarbha_lst_merge.tif`, `vidarbha_mergedLST.tif`) and the broken 8-byte stub are still sitting in `Land_use` — safe to delete once the fixed version above is checked.
- Full 11-district mosaic (all 12 scenes) not reprocessed — only the corridor-relevant 2-scene subset. Worth doing the rest if a district-level (not just corridor-level) comparison is ever needed.
- This is a single pre-monsoon (June) snapshot. The Roadmap's actual outcome variable is a multi-date seasonal NDVI signature (single sharp green-up = cotton monoculture vs staggered multi-crop signal) — need post-monsoon and pre-harvest scenes too before that comparison can be made properly.
- Land_use/LULC, Economics, FRA — still not sourced.
- Agrarian-stress proxy (MSP dependency, APY variability, population-weighted exposure) — not started yet.
- **Ground-truth idea, noted for later:** I'm physically in Karanja Ghadge (Wardha district) right now — this taluka sits inside the 25km corridor, on the Central Provinces/Malguzari side (June 2026 taluka-mean: LST 55.97°C, NDVI 0.264, but only 45.8% valid pixel coverage since it's partly outside this pass's 2-scene footprint). Plan: photograph 2-3 actual field patches around Karanja Ghadge with GPS coordinates, note visible crop type/canopy density/soil moisture, then pull the exact NDVI/LST pixel value at those coordinates and compare against what the ground actually shows. This becomes a dedicated ground-truthing spotlight in the eventual dashboard — a real methodological check on the remote-sensing signal, not just a hometown mention. Waiting on the field photos before this can move forward.

---

## Entry 4

Two things going in parallel here.

**Seasonal NDVI scenes.** The June snapshot in Entry 3 is pre-sowing/fallow season — not the actual cotton-signature test, which needs a kharif-peak date (post-monsoon, when cotton canopy is fullest) and a rabi-peak date (to catch whether a field gets re-sown with wheat/gram after cotton, which is the signature of mixed-cropping rather than monoculture). I can't pull new satellite scenes directly through this pipeline -- the network access I have set up here doesn't reach a public STAC catalog's search API. Wrote `download_seasonal_scenes.py`, sitting at the project root — it pulls the same WRS-2 path 144 / rows 045+046 footprint from Microsoft's Planetary Computer catalog (public, no login, no cost) for a post-monsoon window (Sept 15 – Nov 15, 2025) and a pre-harvest window (Jan 15 – Mar 15, 2026), lowest-cloud-cover scene per window. Needs `pip install requests` if that's not already there. Once it's run, I'll pull the results in and rerun the same DN=0-fix + NDVI pipeline from Entry 3 across all three dates.

**Agrarian-stress proxy — first pass, from data already on hand.** No new sourcing needed for this one; built it entirely from the APY 2024-25 workbook and the Economic Survey 2025-26 District Indicators PDF, both already sitting in the Agriculture folder since before this project's pivot.

From the APY workbook: computed each district's cotton area as a share of total cropped area (foodgrains + oilseeds + sugarcane + cotton + rabi jowar + wheat, since that's what this workbook actually covers). From the District Indicators PDF: pulled net sown area (% of geographical area), per-capita foodgrain production, cropping intensity, and average operational holding size for all 11 districts — these sit in a merged-header table (columns 25-31) that needed careful column-by-column sanity-checking against known district profiles before I trusted the alignment (Gadchiroli showing 14% net sown area and Bhandara/Gondia showing 500+ kg per-capita foodgrain production, matching their real reputation as forest-heavy and rice-bowl districts respectively, is what confirmed I had the right columns). Left out the MGNREGA/malnutrition/mortality columns (52-59) on the same page — the table extraction didn't give me confident column alignment there, and I'd rather skip a variable than risk reporting a mislabeled one.

**What it actually shows, honestly.** Cotton share is noisier than the clean west/east story I was expecting: Yavatmal (51%) and Wardha (49%) — one Berar, one Central Provinces — are nearly tied for the highest cotton dependency in the region, and Chandrapur (38%) and Nagpur (38%) also run high despite being on the Central Provinces side. Bhandara and Gondia sit at essentially zero (0.15% and 0%) — they're rice districts, not just "not-cotton." So cotton-as-a-crop was never confined to old Berar; the British pushed it hardest there but cotton cultivation itself spread into parts of the neighboring Central Provinces districts too (Wardha in particular has its own long cotton history, unrelated to Berar's Ryotwari system).

Net sown area is the cleaner, more consistent divide: all five Amravati Division districts sit in a tight 60-75% band; the six Nagpur Division districts spread from 14% (Gadchiroli, mostly forest) to 57% (Nagpur), averaging around 41% with much higher spread (std. dev. 15.4 vs 6.8 on the Berar side). That's the real structural signature — Berar is uniformly under the plough, Central Provinces is a mix of heavily-cultivated and heavily-forested/water-covered districts, which tracks the historical picture (Ryotwari brought the whole province under individual cultivation; Malguzari CP kept more land under zamindari forest/estate control that was never as fully converted to cropland).

**Files produced this entry:**
- `download_seasonal_scenes.py` (project root) — script to run for the two extra Landsat dates
- `03_Data_Processed/Agriculture/vidarbha_agrarian_indicators.csv` — cotton share, net sown %, per-capita foodgrain, cropping intensity, avg holding size, per district, with division labels
- `07_Outputs/agrarian_indicators_comparison.png` — the four-panel comparison chart

**Still open after this entry:**
- Need to actually run `download_seasonal_scenes.py` and get the post-monsoon + pre-harvest scenes back to build the real cotton-signature classification.
- MGNREGA employment days and child-malnutrition indicators (District Indicators PDF, columns 52-59) — skipped this pass over column-alignment uncertainty; worth a second attempt with a more careful table extraction if these turn out to matter for the write-up.
- Land_use/LULC, FRA, Economics-as-a-separate-category — still not sourced.
- Population census data (already downloaded) not touched yet — the agrarian-stress proxy so far is purely agricultural-structure; a population-weighted version (e.g. share of workforce that's agricultural labour vs cultivator) would strengthen it and is the natural next addition.

---

## Entry 5

While `download_seasonal_scenes.py` was running on my machine, went ahead and processed the village-level Population census data (downloaded a while back, never actually opened) for the five corridor-relevant districts — Amravati, Yavatmal, Wardha, Chandrapur, Nagpur. 9,161 villages across those five districts, 600+ census attributes each.

Aggregated to taluka level and pulled two things: the ratio of agricultural laborers to cultivators (main + marginal workers combined — this is the classic landlessness/distress indicator: a high ratio means more people working someone else's land for wages rather than their own), and literacy %.

**Tried to pull irrigation coverage too, and had to drop it.** The `area_irri` / `net_area` fields gave irrigation rates of 58-92% across Yavatmal villages, which flatly contradicts the well-documented fact that Vidarbha's cotton belt is overwhelmingly rainfed (real regional irrigation coverage is usually cited around 15-20%). Checked it against total village area as a second denominator too — still implausibly high. Whatever these two fields actually encode, it isn't straightforwardly "irrigated area vs. cultivated area" the way the column names suggest, and I'd rather leave a gap than report a number I don't trust. Flagging this for a proper look later, maybe by cross-referencing a data dictionary for this shapefile if one exists.

**What held up.** The agricultural-laborer-to-cultivator ratio, for the 32 corridor talukas with matched data (15 Berar side, 17 Central Provinces side): 2.90 on the Berar/Amravati Division side vs 1.96 on the Central Provinces/Nagpur Division side — meaning for every cultivator in the corridor's Berar talukas, there are nearly 3 agricultural laborers, versus about 2 on the other side. That's a real, fairly consistent gap (not just one or two outlier talukas dragging the average) and it lines up with the historical read: Ryotwari gave individual peasants formal ownership, but the push into cotton monoculture is exactly the kind of single-crop, price-exposed cash economy that's associated with land loss and a growing landless-labor class over generations, which is the core of the actual Vidarbha agrarian-distress literature (not my invention — this is the standard account of why the farmer-suicide crisis concentrated in this specific belt). Literacy was close either way (75.1% vs 72.5%) — not a meaningful divide on its own.

**Files produced this entry:**
- `03_Data_Processed/Population/taluka_population_agri_stats.csv` — full taluka-level aggregates (population, households, cultivator/laborer breakdown, literacy) for all matched talukas across the 5 districts
- `03_Data_Processed/Population/corridor_taluka_population_stats.csv` — same, subset to the 32 corridor talukas with division labels
- `07_Outputs/population_agrarian_comparison.png` — boxplots of the ag-laborer ratio and literacy by division

**Still open after this entry:**
- Irrigation coverage from this dataset — untrustworthy as extracted, needs a second look or a different source (state agriculture department irrigation statistics would be more reliable than trying to reverse-engineer this shapefile's schema).
- Only processed 5 of 11 districts (the corridor-relevant ones) — the other 6 (Akola, Buldhana, Washim, Bhandara, Gondia, Gadchiroli) aren't touched, same scope decision as the LST/NDVI pass.
- Land use fields in this same census dataset (forest, fallow, barren, misc_crop, per village) could partially fill the still-missing Land_use/LULC category — worth coming back to.
- Still waiting on `download_seasonal_scenes.py` to finish so the real cotton-signature NDVI classification can happen.

---

## Entry 6

Same Population census shapefiles from Entry 5 turned out to carry a full village-level land-use breakdown too — forest, non-agricultural use, barren/uncultivable, permanent pasture, miscellaneous tree crops, cultivable waste, fallow (current + other), and net sown area, all in hectares, all summing cleanly to each village's total area (checked this explicitly — the nine categories add up to 99-100% of `area_ha` for every village, so unlike the irrigation fields in Entry 5, this one I trust). That's the Land_use/LULC category the Roadmap has been carrying as unsourced since Entry 1 — not satellite-derived land cover, but a real independent land-use classification from the same census, which is arguably more useful for this project since it's already got the forest/cropland/fallow distinction done by hand rather than needing a classifier.

Sanity-checked it hard before trusting it: Chikhaldara (Amravati district, sits in the Melghat hill/tiger-reserve tract) comes out at 30.9% forest, Jiwati (Chandrapur, a genuinely forested taluka) at 36.4% forest — both match what these places are actually known for, which is what convinced me the columns mean what they say.

**Corridor comparison (32 talukas):** net cultivated area 68.9% (Berar side) vs 61.5% (Central Provinces side) — same direction as the district-wide PDF numbers from Entry 4, but the gap is narrower here because the corridor only touches the more-cultivated CP districts (Wardha, Nagpur, Chandrapur), not the deep-forest ones (Gadchiroli) that pulled the district-wide CP average down further. Forest % is actually almost identical at the corridor (12.5% vs 12.6%) for the same reason — the corridor is a farming transition zone, not where CP's forest tracts actually are. The one new finding here: fallow land is nearly double on the Central Provinces side of the corridor (5.8% vs 3.3%) — more land sitting temporarily uncultivated. Not reading too much into this yet (could be crop-rotation practice as much as distress), but it's worth carrying into the eventual write-up as another small piece alongside the cotton-share and agricultural-labor findings.

**Files produced this entry:**
- `03_Data_Processed/Land_use/taluka_landuse_stats.csv` — full land-use breakdown for all matched talukas, 5 districts
- `03_Data_Processed/Land_use/corridor_taluka_landuse_stats.csv` — corridor subset with division labels
- `07_Outputs/landuse_corridor_comparison.png` — net cultivated area, fallow, and forest boxplots by division

**Still open after this entry:**
- This is village-census-derived land use, not a satellite land-cover classification — still worth getting an actual LULC raster (ISRO Bhuvan or similar) at some point for a proper remote-sensing cross-check, but the core Land_use gap is no longer empty.
- Same 5-district (corridor-only) scope as Entries 3 and 5 — the other 6 districts untouched.
- `download_seasonal_scenes.py` finished downloading while I was doing this — pulling the scenes in next and running the actual cotton-signature NDVI classification.

---

## Entry 7

This is the real Phase 3 outcome variable, not the June placeholder from Entry 3. With three dates now — June (pre-sowing), November 2025 (kharif/monsoon peak), March 2026 (rabi/pre-harvest) — ran the same DN=0-fix pipeline on the two new dates and built the actual seasonal signature: how much each taluka's NDVI drops between the kharif peak and the rabi period. A big drop means the land goes back to bare/fallow after the kharif crop comes off — a single-crop (cotton) signature. A smaller drop means a rabi crop (wheat, gram) is following the kharif one and keeping the land green through winter — a double-cropped, more diversified signature.

**Result, full footprint (68 talukas, both scene rows):** the Berar/Amravati Division side shows a mean decline of 0.325 NDVI points from kharif peak to rabi period; the Central Provinces/Nagpur Division side shows 0.255 — noticeably smaller, and with much more spread (std. dev. 0.062 vs 0.041), meaning the "some fields get a second crop" pattern is real but uneven across the Central Provinces side rather than uniform. Both sides peak at almost the same kharif NDVI (0.66 vs 0.64) — the divide isn't in how green things get during the monsoon, it's in what happens after. That's exactly the shape of signature the Roadmap set out to find: a single-crop economy that goes fallow once cotton is picked, versus a mixed-crop economy that keeps part of its land working through the dry season.

**At the corridor specifically, this gap nearly disappears** (0.310 vs 0.299, 29 talukas) — same pattern I saw with cotton-share in Entry 4: the corridor's Central Provinces talukas (Wardha, Nagpur, Chandrapur) are themselves substantial cotton growers, so right at the boundary the two sides look more alike than the region-wide averages suggest. The effect is real at the regional scale but doesn't produce a sharp jump right at the historical line — it's a gradient that strengthens further from the boundary in both directions, not a clean discontinuity. Worth being upfront about this for Phase 4: a spatial-discontinuity test run only on the immediate corridor may find a weaker signal than the region-wide contrast implies, and that's a genuine finding about how this boundary behaves, not a failure of the method.

**Files produced this entry:**
- `03_Data_Processed/Vegetation/ndvi_postmonsoon_300m.tif`, `ndvi_preharvest_300m.tif` — the two new corrected NDVI mosaics (300m, same downsampling as the June one)
- `03_Data_Processed/Vegetation/taluka_seasonal_ndvi_signature.csv` — all three dates + the kharif-to-rabi decline, all 68 matched talukas
- `03_Data_Processed/Vegetation/corridor_taluka_seasonal_ndvi_signature.csv` — corridor subset (29 talukas)
- `07_Outputs/seasonal_ndvi_signature.png` — the seasonal trajectory line chart and the decline boxplot

**Still open after this entry:**
- This is one annual cycle (kharif 2025 / rabi 2025-26), opportunistically dated a year apart from the June 2026 baseline — a second year's worth of dates would confirm this isn't just one unusual season.
- Phase 4 (the actual spatial-discontinuity statistical test, controlling for distance-to-boundary/elevation/rainfall) hasn't started — this entry produced the outcome variable it needs, not the test itself.
- Land_use, FRA still open from earlier entries. Karanja Ghadge ground-truth still waiting on field photos.

---

## Entry 8

Pulled in the WorldClim precipitation data I'd already downloaded (monthly climatology, clipped to Vidarbha) — this one's been sitting untouched since the original data pull. Sampled all 12 months at every taluka centroid and computed annual total, the share falling in the monsoon months (Jun-Sep), and month-to-month seasonality.

**Important framing note before the numbers:** this is a rainfall *climatology* (long-term monthly normals, not a specific year's actual rainfall), and the resolution is coarse — WorldClim's 10 arc-minute grid works out to about 18.5km per pixel, larger than most individual talukas, so nearby talukas often share close to the same value. Good enough to establish the regional gradient, not fine enough for taluka-by-taluka precision.

**What it shows:** the Central Provinces/Nagpur Division side gets substantially more rain than the Berar/Amravati Division side — 1,249mm/year vs 903mm/year district-wide, narrowing to 1,109mm vs 1,005mm right at the corridor. Monsoon concentration is nearly identical on both sides (~88% of the year's rain falls Jun-Sep either way) — the difference is in the total, not the seasonal shape.

This one is NOT a finding about the historical boundary — it's a natural west-to-east rainfall gradient across Vidarbha that has nothing to do with Ryotwari or Malguzari (it predates both by geological time). I'm logging it here because it's exactly the kind of thing the Roadmap flagged needing to control for in Phase 4: if Berar is both historically cotton-monoculture AND drier, any "Berar looks more drought-stressed" result could just be reflecting less rainfall rather than the land-tenure legacy. Phase 4 needs to net this out before the boundary effect can be trusted.

**Files produced this entry:**
- `03_Data_Processed/Hydrology/taluka_precipitation_stats.csv` — monthly + annual precipitation, all 120 talukas
- `03_Data_Processed/Hydrology/corridor_taluka_precipitation_stats.csv` — corridor subset
- `07_Outputs/precipitation_corridor_comparison.png` — annual total and monsoon-share boxplots by division

That closes out Phase 3 — cotton-signature NDVI (Entry 7), agrarian-stress and land-use (Entries 4-6), and now the climate control variable. Moving to Phase 4 next: the actual spatial-discontinuity test.

---

## Entry 9

This is the real test the whole project has been building toward: does each outcome variable jump right at the historical boundary once distance-to-boundary, rainfall, and elevation are controlled for, or is what I've been seeing in Entries 3-8 just a broad regional gradient that happens to look different on either side.

**Getting the dataset together.** Needed elevation as a control, so pulled 9 SRTM 1-arc-second tiles covering the corridor's bounding box and sampled all 32 corridor taluka centroids — came out 194-497m, plausible for this stretch of the Deccan plateau edge. Everything else in this table comes from prior entries: `side` (1=Berar, 0=Central Provinces) and `signed_dist_km` (each taluka centroid's distance to the dissolved division boundary line, computed in UTM 44N, signed positive on the Berar side) from Entry 2's boundary work; the three-date NDVI and kharif-to-rabi decline from Entry 7; LST from Entry 3; agricultural-laborer-to-cultivator ratio and literacy from Entry 5; land-use percentages from Entry 6; annual rainfall from Entry 8; cotton share from Entry 4. 32 corridor talukas, one row each.

**The model.** Standard regression-discontinuity setup: `outcome ~ side + signed_dist_km + side×signed_dist_km + rainfall + elevation`, run via OLS. `side` captures the level jump right at the boundary — the actual question. The interaction term captures whether the *slope* with distance differs by side (does the effect get stronger/weaker moving away from the line, and does that differ on the two sides). Ran it for five outcomes: kharif-to-rabi NDVI decline (with and without controls, to see what the controls actually change), the ag-laborer ratio, net cultivated area %, and June LST.

**Being straight about what came back:** at n=28-32, most of the `side` coefficients don't clear statistical significance. NDVI decline: side p=0.458. Ag-laborer ratio: side p=0.960. Net area %: side p=0.577. LST: side p=0.792. None of these show a clean jump in level right at the boundary once controls are in. I'm not going to dress that up — a corridor-only sample this small has limited power to detect anything short of a large, sharp effect, and Entry 7 already flagged that the cotton-signature gap itself nearly vanishes at the immediate corridor even before any regression. This result is consistent with that: whatever's driving the region-wide contrasts in Entries 4-8 looks like a broad gradient across Vidarbha, not a hard discontinuity exactly on the old Berar/CP line.

**The one result that did clear significance:** the `side_x_dist` interaction on the ag-laborer-to-cultivator ratio came back coef=0.0374, p=0.036. That's not a level jump — it's a difference in *slope*. Moving away from the boundary, the ag-laborer ratio changes at a different rate on the Berar side than on the CP side. I'm reading this cautiously rather than as a boundary-jump finding: it says the relationship between distance-from-the-old-line and labor structure isn't flat and isn't the same shape on both sides, which is itself interesting, but it's one significant coefficient out of twenty across five models, and with this sample size that's the kind of thing I'd want to see hold up before leaning on it in the eventual write-up.

**What was significant, consistently: the controls themselves.** Rainfall and elevation show up as real predictors in multiple models — rainfall p=0.015 and elevation p=0.002 in the NDVI-decline model, rainfall p<0.001 in the ag-laborer model, both rainfall (p=0.046) and elevation (p=0.020) in the net-area% model. This is exactly what Entry 8 flagged going in: the natural geography of Vidarbha (wetter/lower in the Central Provinces, drier/higher on the Berar side) is doing real work in these outcomes, separate from anything about the old administrative line. Good that it's coming through as a control rather than getting mistaken for a boundary effect — that's the whole reason Entry 8 got built before this one.

**Honest read overall:** at the immediate 25km corridor and this sample size, I'm not finding a sharp statistical discontinuity right at the historical boundary — I'm finding a real regional gradient (documented across Entries 4-8) that fades out approaching the line itself, plus one slope difference worth flagging rather than a level jump. That's a legitimate finding, not a null result to bury: it says the persistence effect this project set out looking for, if it's there, isn't showing up as a hard edge at the old line — it's showing up as a broader east-west pattern across Vidarbha that the corridor-only test isn't well-powered to pin down. Worth carrying two things forward into Phase 5: (1) whether a wider corridor or the full 68-taluka footprint gives the regression more power without diluting the "near the boundary" logic, and (2) that this null-at-the-line, gradient-at-the-region result is itself part of the story, not a setback to the story.

**Files produced this entry:**
- `03_Data_Processed/Phase4/phase4_master_dataset.csv` — the 32-row, 19-column regression dataset
- `03_Data_Processed/Terrain/corridor_taluka_elevation.csv` — corridor taluka elevations from SRTM
- `07_Outputs/phase4_discontinuity_plots.png` — outcome vs. distance-to-boundary scatter + fitted lines by side, for the four headline outcomes

**Still open after this entry:**
- Sample size is the real limiting factor here (n=28-32) — worth testing whether the full 68-taluka footprint (not just the 25km corridor) gives cleaner power, even though that moves away from the strict "right at the boundary" logic.
- The one significant interaction (ag-laborer slope) needs a robustness check before it goes in any final write-up — right now it's one coefficient, not a confirmed pattern.
- Karanja Ghadge ground-truth still waiting on field photos from Sawardoh village.
- Historical boundary cross-check, FRA compilation, second-year NDVI confirmation all still open from earlier entries.

---

## Entry 10

Three things left over from Entry 9, taken one at a time.

**Land fragmentation.** The `avg_holding_ha` column was already sitting in the Entry 4 agrarian dataset (district-level, from the APY workbook) — just hadn't been pulled into the corridor comparison yet. Broadcast it onto the 32 corridor talukas by district and compared sides: Berar corridor talukas average 1.81 ha per holding, Central Provinces corridor talukas average 1.90 ha — CP actually running slightly *larger* holdings, not smaller. That's the opposite of what a naive "Ryotwari system → more fragmented smallholdings" story would predict, and both numbers are close enough (within a quarter-hectare, similar spread) that I'm not reading a real divide into it either way. Filing it as a genuinely flat result rather than stretching it into a finding — the district-level holding-size data just doesn't show a Berar/CP split at the corridor.

**Robustness check on the Entry 9 interaction.** The one significant result from Entry 9 — the `side_x_dist` interaction on the ag-laborer-to-cultivator ratio (coef=0.0374, p=0.036) — got a leave-one-out jackknife: refit the model 32 times, each time dropping one corridor taluka, and watched what happened to that coefficient. It stayed positive and in a tight band (0.026 to 0.044) across every single run — good sign, no one taluka is secretly driving the whole thing. But the p-value moved around more: it stays under 0.05 in 26 of 32 runs, and crosses back over 0.05 (up to as high as 0.138) when a handful of specific talukas are dropped — Amravati taluka itself, Seloo, Samudrapur, Narkhed, Korpana, Yavatmal taluka. So: the direction and rough size of the effect is stable, but the statistical significance is right on the edge and a few individual talukas are doing a lot of the work of pushing it under the p<0.05 line. Calling this "suggestive but not bulletproof" rather than either dismissing it or overselling it.

**Full-footprint retest.** This is the more substantial one. Entry 9's regression ran on the 32-taluka corridor only, and I'd flagged that as underpowered. NDVI and LST both actually have full scene-footprint data already sitting from Entries 3 and 7 (68 and 66 talukas — the whole path-144 row-045/046 coverage, not just the 25km-either-side corridor), so reran those two outcomes at that larger sample. Needed two more SRTM tiles (n20_e080, n21_e080) to extend elevation sampling out to the full footprint — pulled those in and resampled cleanly, all 68 talukas got a valid elevation this time. Population, land-use, and the ag-laborer ratio don't have this option — that census data only covers 5 of Vidarbha's districts, so those stay corridor-only for now (would need to source three more districts' worth of village shapefiles to extend them, which is its own separate task, not a quick add-on).

Worth flagging up front: the full footprint is lopsided — 49 Central Provinces talukas to 19 Berar talukas, because the scene simply covers more CP-side territory. Keeping that in mind reading the result.

**What changed with the bigger sample:** the boundary-level jump (`side`) is still not significant in either model — NDVI decline p=0.821, LST p=0.512 — consistent with Entry 9's read that there's no sharp jump right at the old line. But the interaction term, which was only significant for one variable at the corridor scale, is now significant for *both* Earth-observation outcomes at the full-footprint scale: NDVI decline side×distance p=0.035, LST side×distance p=0.010. And `signed_dist_km` on its own is now strongly significant too (p<0.001 both models) — meaning there's a real, well-powered gradient with distance from the boundary, it just isn't the same gradient on both sides. That's a more consistent version of exactly what Entry 9 already suspected from the corridor-only run: not a discontinuity at the line, but a genuine difference in how these outcomes trend with distance depending on which side you're on. Getting the same shape of result in two independent outcome variables, with real statistical power behind it this time, is the strongest evidence yet for that read.

**Files produced this entry:**
- `03_Data_Processed/Agriculture/phase4_master_dataset.csv` — updated with `avg_holding_ha` column added
- `03_Data_Processed/Phase4/phase4_robustness_jackknife.csv` — all 32 leave-one-out coefficients and p-values
- `03_Data_Processed/Phase4/phase4_fullfootprint_dataset.csv` — the 68-taluka full-footprint regression dataset (NDVI + LST only, per the data-availability limits above)
- `07_Outputs/phase4_fullfootprint_plots.png` — NDVI decline and LST vs. distance-to-boundary, full footprint, fitted lines by side

**Still open:**
- Ag-laborer ratio, net cultivated area %, and land-use variables are still corridor-only (32 talukas) — extending those to the full footprint needs population/land-use census data for Bhandara, Gondiya, and Gadchiroli districts, which hasn't been sourced.
- The Entry 9 interaction result, now backed up by the same slope-difference pattern showing up independently in NDVI and LST at a larger sample — three variables pointing the same direction is a real pattern, not proof, but it's the strongest signal in the project so far for "gradient, not discontinuity."
- Karanja Ghadge ground-truth (Sawardoh photos), historical boundary cross-check, FRA compilation, second-year NDVI confirmation all still open from earlier entries.

---

## Entry 11

Turned out I didn't actually need to go find new data for Bhandara, Gondiya, and Gadchiroli — the raw census shapefiles (`bhandara.zip`, `gondia.zip`, `gadchiroli.zip`) were already sitting in the Population raw folder alongside the other 8 district zips. They'd just never been processed past the download stage. Ran them through the exact same village-to-taluka aggregation as Entry 5/6 — sum the worker/land-use columns by (district, taluka), recompute the ratios — and all 27 talukas across the three districts came out clean: land-use category totals check out to exactly 100% of `area_ha` for every one of them, same as before, and taluka name spelling matched the Administrative layer exactly (no "Gondia vs Gondiya" style mismatch this time).

With that in hand, rebuilt the full-footprint Phase 4 dataset again — this time with all four outcome variables (NDVI decline, LST, ag-laborer ratio, net cultivated area %) instead of just the two Earth-observation ones from Entry 10.

**NDVI decline and LST came back basically unchanged from Entry 10** — no level jump at the boundary (side p=0.821 and p=0.512), significant side×distance interaction in both (p=0.035, p=0.010). That part of the story holds.

**Ag-laborer ratio did something different, and it's worth being upfront about it.** At the corridor scale (Entry 9), this variable showed a significant *slope* difference (side×distance interaction, p=0.036) but no level jump. At the full footprint (n=67, now that Bhandara and Gondiya are in the sample — Gadchiroli's talukas fall outside the actual NDVI scene footprint, so they didn't end up in this particular regression, though the processed data for them is saved and available if a wider footprint is used later), it flips: now there IS a significant level jump right at the boundary (`side`, coef=0.622, p=0.014), and the slope interaction is no longer significant (p=0.579).

That's not necessarily a contradiction, but it needs an honest explanation rather than picking whichever result sounds better. Checked the distance ranges on each side of this expanded sample: the Berar side barely extends past ~20km from the boundary here, because Amravati is the only Berar-division district that falls inside this particular satellite scene — the deeper Berar interior (Akola, Buldhana, Washim) was never in the path-144/row-045-046 footprint to begin with. The Central Provinces side, by contrast, now reaches out past 160km (Bhandara, Gondiya are that far east). So this isn't two clean parallel lines being compared anymore — it's a short, boundary-hugging Berar segment against a much longer, far-ranging CP segment. A "level jump near the boundary" read is more defensible under those conditions than a "different slope across the whole range" read, since only one side actually has much range to have a slope over. I'd trust the corridor-only interaction result (Entry 9) more for what's happening right at the line, and treat this full-footprint level-jump result as suggestive of a genuine gap between the two divisions at a broader regional scale, not as a competing measurement of the same thing.

**Net cultivated area % stayed non-significant either way** (side p=0.121 full-footprint vs p=0.577 corridor) — consistent null across both specifications, no split story needed there.

**Files produced this entry:**
- `03_Data_Processed/Population/taluka_population_agri_stats.csv`, `03_Data_Processed/Land_use/taluka_landuse_stats.csv` — both updated, now cover 8 of 11 districts (added Bhandara, Gondiya, Gadchiroli to the existing 5)
- `03_Data_Processed/Phase4/phase4_fullfootprint_dataset.csv` — updated with all 4 outcome variables, 67-68 talukas depending on variable
- `07_Outputs/phase4_fullfootprint_all4_plots.png` — all four full-footprint outcomes plotted against distance-to-boundary

**Still open:**
- Gadchiroli's population/land-use data is processed and saved but has no corresponding NDVI/LST scene coverage — only useful if a wider Landsat footprint is ever pulled in.
- The ag-laborer result now has two different, both-defensible reads depending on which sample it's run on — worth flagging explicitly in any final write-up rather than quietly picking one.
- Karanja Ghadge ground-truth (Sawardoh photos), historical boundary cross-check, FRA compilation, second-year NDVI confirmation still open from earlier entries.

---

## Entry 12

Two of the remaining open items, taken together this session.

**FRA compilation.** This was flagged all the way back in Entry 1 as "no clean source found yet; likely manual PDF compilation," so went looking properly this time instead of leaving it as a placeholder. Bottom line up front: there is no clean taluka-level, or even consistent district-level, FRA dataset for Vidarbha in the public domain — I looked, and this isn't a case of me not searching hard enough. What exists is fragmented across a few different documents at a few different scales:

- Maharashtra state-level totals from two different points in time: the state Tribal Development Department's 2020-21 Administrative Report (as of March 2021: 379,881 individual-rights claims received, 95.84% disposed, 1.31 lakh acres distributed; 11,985 community-rights claims received, 81.59% disposed, 28.28 lakh acres distributed), and a 2024 fact-finding committee report citing newer numbers as of June 2023 (35,654 new individual claims and 90,626 new individual titles since 2017, but only 1,290 new community titles in that same window — 30% of claims still pending statewide, 18% rejected).
- One genuinely useful district-level anchor: Gadchiroli specifically, from the same 2024 fact-finding report, citing 2016 data — 1,355 community forest rights titles covering 4,34,181 hectares, against an estimated minimum potential of 5,57,137 hectares (77.9% recognized, explicitly classified "high performing" in that report, in contrast with Nashik district elsewhere in the state at just 5%). That's a real, sourced, district-specific number — just for one district, and nearly a decade old now.
- A Vidarbha-wide regional figure (not broken out by district): roughly 6,500 villages and 7,94,118 hectares recognized under community forest rights across the region since 2013, cited via an EPW journal piece referenced in a Scroll.in report on Gondia's community forestry work.
- A handful of village-level case studies with real numbers attached but no way to aggregate them into a district total: Menda-Lekha village in Gadchiroli (1,800 hectares secured in 2009, ₹75 lakh in bamboo revenue by 2012), Dhamditola and Paulzhola villages in Gondia (290 and 600+ hectares respectively, both 2013).

I also found that the Ministry of Tribal Affairs runs a live public dashboard (forestrights.nic.in/mpr/common/dashboard) that in principle supports state/district drill-down — but it's an interactive government portal, not a fetchable document, and I can't reach it programmatically from here. If district-by-district numbers for all of Gadchiroli, Chandrapur, Gondia, Bhandara, Yavatmal, Wardha, Nagpur, and Amravati ever become essential (rather than contextual), that dashboard is the place to go — someone would need to click through it by hand, one district at a time.

**Given all that, I'm treating FRA as a contextual/narrative data point for the eventual write-up, not a Phase 4 regression variable.** There just isn't a consistent enough measurement across enough districts to add it to the taluka-level dataset the way NDVI or rainfall are in there. It's useful institutional-history color — Gadchiroli's CFR recognition rate is a real, striking number worth having in the eventual narrative about Vidarbha's forest-tenure geography — but it can't do statistical work in this project the way the earth-observation and census variables can.

**Second-year NDVI check.** Wrote `download_seasonal_scenes_year2.py` for the field-side run — same pattern as the original seasonal-scenes script, same WRS-2 footprint (path 144, rows 045/046), but pulled back a year: kharif-peak window Sep-Nov 2024 and rabi-peak window Jan-Mar 2025, instead of the 2025/2026 pair Entry 7 used. This is the check I flagged in Entry 7: the 0.325 (Berar) vs 0.255 (Central Provinces) kharif-to-rabi decline gap was only measured on one annual cycle. If the same gap, or something close to it, shows up independently in the year-2024 cycle, that's real evidence of a stable seasonal cropping signature rather than one unusual season. Handing this off — it needs to run on the local machine and pull from Planetary Computer the same way the first seasonal script did.

**Files produced this entry:**
- `03_Data_Processed/Economics/fra_compilation_vidarbha.csv` — everything found above, one row per figure, each tagged with scope (state/district/village), value, unit, as-of date, and source URL — built as a sourced compilation, not a clean panel dataset, because the underlying data isn't one
- `download_seasonal_scenes_year2.py` (project root) — ready to run locally, same pattern as the original seasonal-scenes script

**Still open:**
- FRA: only Gadchiroli has a real anchor number; the other 7 districts have no district-level figure I could find publicly — this stays a narrative point, not a quantitative one, unless someone manually pulls per-district numbers off the MoTA dashboard.
- Second-year NDVI: waiting on the script to be run — once the year-2024 scenes land, will rerun the DN=0-fix NDVI pipeline against them and compare the kharif-to-rabi decline directly against Entry 7's year-2025 numbers.
- Karanja Ghadge ground-truth (Sawardoh photos) — holding on this until told to pick it back up.
- Historical boundary cross-check against period maps still open, no source located.

---

## Entry 13

The Roadmap always framed this as "find a digitized 1901-1931 Imperial Gazetteer map and overlay it against the modern division line." Never found a digitized map or shapefile like that — doesn't seem to exist in an accessible form. What I found instead does the same job a different way: the actual district-membership lists for Berar Division and the Central Provinces' Nagpur Division from the 1903-1956 period, which let me check whether the same territory sits on each side of my modern boundary, district by district, without needing a pixel-level map overlay.

**Berar Division, historical (1903-1956):** Amraoti (Amravati), Akola, Ellichpur, Buldhana, Basim, Wun. Cross-checking against what these places are called today: Ellichpur is now a taluka inside Amravati district, not a separate district — absorbed early on. Wun was renamed Yavatmal. Basim was renamed Washim, and folded into Akola district for a stretch before being recreated as its own district on 1 July 1998. Net effect: **Berar's historical footprint maps district-for-district onto my modern Amravati Division (Akola, Amravati, Buldana, Washim, Yavatmal)** — same 5-district territory, just renamed and re-split internally over 120 years, no actual boundary redraw. That's a clean, reassuring match for the whole premise of using the modern division dissolve as a stand-in for the historical Berar line.

**Central Provinces' Nagpur Division, historical:** Nagpur, Bhandara, Chanda (renamed Chandrapur), Wardha, and — this is the one real wrinkle — **Balaghat**. Gondiya (split from Bhandara, 1999) and Gadchiroli (split from Chandrapur, 26 August 1982) are both later internal subdivisions of that same historical territory, not new land, so they fold in cleanly. Balaghat doesn't: on 1 November 1956, during the linguistic States Reorganisation, Balaghat went to Madhya Pradesh's Jabalpur Division, while the Marathi-speaking remainder of the old Nagpur Division (Nagpur, Bhandara, Wardha, Chandrapur) went to Bombay State and eventually Maharashtra in 1960.

**What this means for the project:** Balaghat was never in my dataset to begin with — it's not a Maharashtra district, so it was never going to be part of Vidarbha's 11 districts regardless. Nothing about Phase 2's boundary construction needs fixing. But it's worth being precise in any final write-up: my "Central Provinces" side of this project is specifically the Maharashtra-Vidarbha portion of the old CP Nagpur Division, which is very slightly smaller than the historical division's full extent — and the piece that's missing fell away because of a 1956 language-based state boundary redraw, which has nothing to do with the Ryotwari/Malguzari land-tenure distinction this project is actually testing. Good to have that as a clean caveat rather than an unexplained gap.

**Bottom line:** the modern Amravati/Nagpur division boundary built in Entry 2 is, as far as documented district lineage can show, the same line as the historical Berar/Central-Provinces boundary — confirmed by tracing every district's administrative history rather than by a literal old-map overlay. A genuine 1900s-era digitized map would still be nice to have for a visual in the final write-up, but the substantive question the Roadmap was actually asking — "does my modern boundary sit where the historical one sat?" — now has a well-sourced yes.

**Files produced this entry:**
- Nothing new in `03_Data_Processed/` — this was a documentation/verification pass, not a data-processing one. The finding itself lives here in the dev log.

**Still open:**
- A genuine period map (Imperial Gazetteer-era or CP&Berar atlas) for visual use in the final write-up is still not sourced — the district-lineage cross-check answers the substantive question but doesn't give a map image.
- Second-year NDVI script is running now -- pulling results in once it lands.
- FRA, Karanja Ghadge ground-truth still open as noted above.

---

## Entry 14

The year-2024 scenes (`download_seasonal_scenes_year2.py`) finished downloading — same WRS-2 footprint as before, path 144 rows 045/046, kharif-peak window Sep-Nov 2024 and rabi/pre-harvest window Jan-Mar 2025, both again landing at 0% cloud cover. Ran them through the same DN=0-fix NDVI pipeline from Entry 3/7 and recomputed the per-taluka kharif-to-rabi decline, then set it side by side with Entry 7's original year (kharif 2025 / rabi 2025-26).

**This is the check I've been wanting since Entry 7, and it held up.** Year 1: Berar corridor-and-beyond talukas averaged a 0.325 NDVI-point decline from kharif peak to rabi, Central Provinces talukas averaged 0.255 — a 0.070 gap. Year 2, a completely independent annual cycle a year earlier: Berar averaged 0.316, Central Provinces averaged 0.241 — a 0.074 gap. Both the direction (Berar always declines more) and the size of the gap (0.070 vs 0.074) reproduce almost exactly across two years that don't share a single scene. That's a real seasonal cropping signature, not something that happened to show up in one unusual season — which was the whole point of running this check before leaning on the Entry 7 result in any final write-up.

Four talukas (Chandur Railway, Goregaon, Ner, Digras) came back with no valid year-2 pixels — small cloud/edge-coverage gaps in this particular scene pair, not present in year 1. Left them as NaN rather than guessing at a value; the comparison ran on 64 of 68 talukas instead of the full 68, which doesn't change the read given how consistent the two years already are.

**Files produced this entry:**
- `03_Data_Processed/Vegetation/ndvi_postmonsoon_y2_300m.tif`, `ndvi_preharvest_y2_300m.tif` — the two year-2 corrected NDVI mosaics
- `03_Data_Processed/Vegetation/taluka_seasonal_ndvi_signature_both_years.csv` — both years side by side, all 68 talukas, for direct comparison
- `07_Outputs/year2_ndvi_comparison.png` — boxplot of the kharif-to-rabi decline, both years, both divisions

**Still open:**
- A genuine period map for the final write-up, FRA (as far as documented), Karanja Ghadge ground-truth (Sawardoh photos, on hold) all still open from earlier entries.
- This is now 2 years of confirmation — a 3rd year would be nice-to-have but isn't blocking anything; the signature is holding up well enough to treat as established rather than provisional.

---

## Entry 15

Every remaining open item from Entries 9-14 is either the Karanja Ghadge ground-truth photo (on hold, mine to pick back up) or genuinely diminishing-returns overkill for where the project stands. That closes out the analysis phase for now, so this entry is the dashboard build -- `06_Streamlit`, which already existed as a folder but was still carrying the empty 8-page skeleton (`Study_Area`, `Environmental_Dashboard`, `Socioeconomic_Dashboard`, `Spatial_analysis`, `Priority_Ranking`, `Intervention_Simulator`, `Policy_Recommendations`, `Downloads`) from before the Entry 1 pivot away from the broad "climate-resilient Vidarbha" framing -- none of it matched what this project actually turned out to be.

**Matched to the rest of the portfolio, not built from scratch.** Read through BORDER_OPTICS, GREEN_ALIBI, and GREEN_POLICY_INTELLIGENCE_SYSTEM's dashboards first -- all three share the same skeleton (`app.py` + `utils/theme.py` + `pages/1_Theoretical_Foundations.py` onward + a Methodology page + an Interactive Maps page + a closing Findings page), the same card-and-border CSS structure, and the same graceful-fallback pattern for images/PDFs that aren't added yet (`os.path.exists` check, plain message instead of a crash). BORDER_OPTICS specifically -- same historical-institutional-persistence design as this project -- is the one this dashboard's structure is matched to most closely.

**11 pages:** Theoretical Foundations, Study Design, Data & Methodology, Cotton Signature (NDVI), Agrarian & Land Structure, Climate Controls, Spatial Discontinuity Regression, Historical & Institutional Context, Ground Truth, Interactive Maps, Findings & Conclusion. Every chart and table reads live from the actual CSVs in `03_Data_Processed/` rather than hardcoded numbers -- including the Phase 4 regression itself, refit live with `statsmodels` on the dashboard page using the exact same formula as Entries 9-11, checked against the dev-log numbers and matching to 3-4 decimal places.

**New color theme, dark background, as specified:** Prussian Blue / Teal Blue for the Berar side, Mughal Green for the Central Provinces side, Pastel Blue and Light Silver for text on a near-black navy base -- a different palette from any other project in the portfolio, not reused.

**Left deliberately incomplete, on instruction:**
- The Theoretical Foundations page has a diagram slot, same pattern as BORDER_OPTICS -- left blank (shows a placeholder note) until an actual image is generated and dropped in.
- The Ground Truth page is a placeholder -- the plan and the one taluka-level data point already on record (Karanja Ghadge, June 2026: LST 55.97C, NDVI 0.264, 45.8% valid coverage) are there, but the actual Sawardoh field photos and pixel comparison are still to come.
- The four document-download buttons on the home page (Executive Summary, Research Paper, Project Report, Development Log) all point at real filenames and gracefully show "not added yet" until those are built -- per the standing instruction that those three get written only once the whole project, including ground truth, is finished. Development Log itself is the exception (kept current throughout) but its PDF export hasn't been generated yet either.

**One real bug caught before delivery:** `pandas.Styler.applymap` doesn't exist anymore in the installed pandas version -- crashed the Spatial Discontinuity Regression page's p-value highlighting on first test. Fixed with a version-safe `.map()`/`.applymap()` fallback. Caught this and confirmed every other page (including the live regression numbers and the interactive taluka map) by actually running all 11 pages + home through Streamlit's `AppTest` harness against the real data before delivering, not just by reading the code back.

**One honest data-quality gap on the interactive map:** the taluka boundary shapefile and the Phase 4 processed dataset don't share identical taluka-name spelling for 3 of 68 talukas (`Nagpur (Rural)` vs `Nagpur`, `Hinganghat` vs the shapefile's variant, `Zari-Jamani` vs `Zari Jamni`) -- those 3 aren't drawn on the interactive map yet. Disclosed directly on the map page rather than silently dropped.

**Also delivered:** `cleanup_streamlit_stub_pages.ps1`, same hand-off pattern as `cleanup_docs.ps1` -- deletes the 8 stale pre-pivot stub files, kept as a script rather than a direct delete, same as every other cleanup pass in this project.

**Still open:**
- The 8 stale stub pages need the cleanup script run to actually go.
- Diagram for Theoretical Foundations -- not generated yet.
- Karanja Ghadge / Sawardoh ground truth -- still on hold, mine to start when told.
- CL_Development_Log.pdf and the other three document exports -- not generated yet; home page's download buttons will start working once these exist at the project root.

---

## Entry 16

Two fixes after actually seeing Entry 15's dashboard live, both fair -- 11 pages was checked against BORDER_OPTICS alone, and Mughal Green never got tested against the dark background it was actually going to sit on.

**Page count, checked against all 7 sibling dashboards this time, not one.** DOUBLE_JEOPARDY, ECOCIDE, and GHOST_INFRASTRUCTURE (the three most recently touched, so the most current version of the convention) all converge on 8-9 pages: `1_Study_Design`, `1_Theoretical_Foundations`, 2-4 domain-finding pages, `Interactive_Maps`, then `Methodology_Data` *last* -- not early. GREEN_ALIBI and GPIE run to 11, but they're the older layout, before that convention settled. Entry 15's 11 pages matched the outlier, not the norm, and included a standalone Findings & Conclusion page and a standalone Climate Controls page that no sibling dashboard has as separate pages.

Restructured to 9, matching the settled pattern exactly:

`1_Study_Design.py`, `1_Theoretical_Foundations.py`, `2_Cotton_Signature_NDVI.py`, `3_Agrarian_Land_Structure.py`, `4_Spatial_Discontinuity_Regression.py`, `5_Historical_Institutional_Context.py`, `6_Interactive_Maps.py`, `7_Methodology_Data.py` (moved from position 3 to the end, matching every sibling), `8_Ground_Truth.py` (kept as its own page, the way GHOST_INFRASTRUCTURE keeps its own project-specific extra page after Methodology).

Nothing was cut, only folded in: Climate Controls (LST + rainfall) is now a collapsible section on the Spatial Discontinuity Regression page, right next to the model it's actually a control for -- a better home for it than a standalone page anyway, since it was never a headline finding. Findings & Conclusion's content closes out that same page instead of getting its own.

**Color fix.** Mughal Green (#366B2B) was one of the five colors given, but on the dark navy background it was assigned to (headers, card borders, sidebar-selected state, button hovers) it barely registered -- too close in darkness to the background it was supposed to stand out on. Swapped every one of those roles to a bright pastel icy green (#8FE8B4) instead, keeping Prussian Blue and Teal Blue as given. Also caught and fixed two spots where button/link text was staying light-colored against this now-light green background (the primary button hover state, and the GitHub link button's gradient) -- both would have been unreadable.

**Also delivered:** the cleanup script now covers all 18 stale files in one pass -- the original 8 pre-pivot stubs plus the 10 first-draft page files this restructure superseded -- so it only needs running once.

**Still open:** same as Entry 15 -- the cleanup script still needs running, the diagram for Theoretical Foundations isn't generated yet, Karanja Ghadge/Sawardoh ground truth is still on hold, and the four document PDFs don't exist yet.

---

## Entry 17

Two small closeouts and one real one.

**Theoretical Foundations diagram.** Generated the diagram from a brief matching BORDER_OPTICS/GREEN_ALIBI's visual style directly (white background, navy border frame, serif title, panel-based layout, bottom icon-flow chain) -- four panels: the landscape split with a satellite overhead, the NDVI leaf-physics schematic, the seasonal kharif-to-rabi decline chart, and the causal-chain icon flow (land tenure → cropping pattern → NDVI signature → measurable gradient). Saved as `imgg1.png` in `07_Outputs/Figures`, matching the exact filename convention both sibling projects use rather than the `theoretical_foundations_diagram.png` placeholder name the page was originally wired to -- updated `1_Theoretical_Foundations.py`'s image call to point at the real filename, smoke-tested via `AppTest`, no code changes needed beyond that.

**Cleanup script confirmed run.** Checked `06_Streamlit/pages` on disk directly -- only the 9 final page files are there, so the execution-policy fix worked and the 18 stale files are gone.

**GitHub repo.** Repo created (`THE-COTTON-LINE`, hyphenated). Built what the repo actually needed rather than a bare `git init`: a `.gitignore` excluding `02_Data_Raw` (23.2 GB of Landsat scenes, DEM tiles, WorldClim grids -- none of it needed to reproduce a single processed CSV or dashboard chart), the large intermediate `.tif` rasters and the unused `Infrastructure`/village-boundary geometry inside `03_Data_Processed`, and the empty pre-pivot `04_QGIS`/`08_Documentation`/`09_Refrences` skeleton folders; a filled-in root `requirements.txt` (was sitting empty since the original project setup); and a full README rewrite matching the rest of the portfolio's structure (repo layout, data sources table, running-locally instructions), replacing the stale one still describing the project as "data collection underway." Also caught and fixed a hardcoded GitHub link in `app.py`'s footer button that still pointed at the underscored `THE_COTTON_LINE` name instead of the actual hyphenated repo. Handed off the `git init`/`add`/`commit`/`remote`/`push` sequence to run locally myself -- push credentials and repo write access only live on that machine. Hit and resolved one Windows-specific snag along the way: git refusing to operate on the D: drive as "dubious ownership" until `safe.directory` was whitelisted for it.

**Still open:** Karanja Ghadge/Sawardoh ground truth, still on hold. The four document PDFs -- now three, see Entry 18.

---

## Entry 18

Roadmap's Phase 5 always flagged this as needing "the institutional-economics literature -- Banerjee-Iyer and the Central Provinces recoding dispute -- properly engaged, not just cited," so did that properly rather than dropping in a name-check. Read Banerjee & Iyer (2005, AER) directly -- their core finding that Indian districts settled under landlord-based revenue systems show worse agricultural outcomes today than non-landlord districts, a century-plus after the systems were abolished -- and then Iversen, Palmer-Jones & Sen's (2013, JDS) direct challenge to it: Banerjee-Iyer coded almost the entire Central Provinces as wholly landlord-based, lumping Malguzari in with Bengal/Bihar-style zamindari, when the actual 1863 Malguzari settlement came with cadastral surveys and real statutory tenant protection -- a meaningfully different, more mixed system. When IPS recoded Central Provinces districts using the archival settlement records, six of Banerjee-Iyer's eight headline coefficients lost significance, and dropping Central Provinces from the sample entirely made the whole result disappear. That's directly relevant to this project, not just adjacent to it -- it's the same six districts on the Central Provinces side of my own boundary, and it's the reason I've treated Malguzari as its own distinct category throughout rather than folding it into a generic "landlord system" the way the original Banerjee-Iyer coding did. Also brought in Dell (2010, Econometrica) on Peru's mining mita and Keele & Titiunik (2015) on geographic RD design as the closest methodological precedent for testing a specific historical institutional line with a distance-to-boundary running variable -- both real, verified, directly on point for a spatial-discontinuity design rather than a diffuse regional comparison.

Verified every citation before using it rather than trusting memory -- searched and confirmed Banerjee-Iyer's exact AER volume/page numbers, the IPS recoding paper's exact argument (via its Manchester working-paper text, not just the abstract), Beckert's *Empire of Cotton* as the actual source for the 8.5%-Berar-famine-mortality figure the project's own README has been carrying, and the WorldClim/SRTM/Landsat citations against their original publications.

**Structure matched to the rest of the portfolio** -- read BO_Research_Paper.md and GI_Research_Paper.md first: Abstract, Keywords, Introduction, Literature Review, Data & Methodology, Results, Discussion, Limitations, Future Work, Conclusion, References, same section shape and the same practice of embedding the actual output figures inline rather than just describing them in prose. Pulled every number in the paper directly from Entries 2-16 rather than re-deriving anything -- the corridor-vs-full-footprint regression split (Entries 9-11), the two-year NDVI confirmation (Entries 7 and 14), the jackknife robustness numbers (Entry 10), the historical district-lineage verification (Entry 13), all reported exactly as they read in the dev log, including the genuinely mixed, not-uniformly-clean results (the ag-laborer ratio's level-jump-vs-slope-difference reversal between corridor and full-footprint scale, reported as an open asymmetry rather than smoothed over).

**Ground truth reported as open, not implied complete.** The Karanja Ghadge/Sawardoh field check is still on hold -- the paper's Limitations and Future Work sections say so directly, with the one taluka-level data point already on record (June 2026: LST 55.97°C, NDVI 0.264, 45.8% coverage) carried in as what it actually is, a single reference point, not a completed verification.

Built both `CL_Research_Paper.md` and a matching `CL_Research_Paper.pdf` (via pandoc/wkhtmltopdf, 18 pages, 11 embedded figures pulled straight from `07_Outputs/`) -- home page's download button for it will start working now that the file exists at the project root.

**Still open:** Project Report and Executive Summary -- per the standing rule, those come once the whole project (including ground truth) is actually finished, not before. Karanja Ghadge/Sawardoh ground truth still on hold, mine to start when told.

---

## Entry 19

Read the Research Paper back after Entry 18 and it read stiff -- too much "this study" as the subject of every sentence, too many "not X, but Y" constructions stacked on top of each other, one massive abstract paragraph doing everything at once. None of the actual numbers or citations were wrong, it just didn't sound like something I'd actually write. Rewrote it end to end in first person where I'm describing a decision or a judgment call ("I built," "I checked," "I'm reading this cautiously"), kept "the data show" or "the result" as the subject only where a finding is actually the subject, split the abstract into three shorter paragraphs instead of one dense block, and cut the repetitive contrast phrasing down to where it's actually doing work instead of showing up in every other sentence. Every figure, number, and citation carried over unchanged -- this was a voice pass, not a re-analysis.

**Dashboard hookup.** `app.py`'s document-download section has pointed at `CL_Research_Paper.pdf` and `CL_Development_Log.pdf` since Entry 15 with a graceful "not added yet" fallback for whichever files don't exist -- no code change needed there. Built `CL_Development_Log.pdf` for the first time (pandoc + wkhtmltopdf, 23 pages, this file as of Entry 18) and regenerated `CL_Research_Paper.pdf` off the rewritten text. Both now sit at the project root, so both download buttons on the dashboard home page are live.

**Project Report and Executive Summary are still not built.** Ground truth (Karanja Ghadge/Sawardoh) hasn't happened yet, and the standing rule is those two get written once the whole project actually is -- not sooner just because the Research Paper and Dev Log are ready. Said this directly rather than building placeholder versions to fill out the set.

---

## Entry 20

The first portfolio card draft pointed the INTERACTIVE MAPS button straight at the live Streamlit app's `/Interactive_Maps` subpage. That doesn't match how the rest of the portfolio actually works -- every other project's map button is either a single static export or, when there's more than one map worth surfacing, a dropdown of separate static exports hosted off the project's own GitHub Pages, never a link into the live app itself. Fixed it to match.

`6_Interactive_Maps.py` on the live dashboard is one choropleth with a "color by" selectbox across six metrics (side of the boundary, kharif-to-rabi NDVI decline, LST, ag-laborer-to-cultivator ratio, net cultivated area, signed distance to the boundary), not six separate pages -- so I wrote a one-off export script (`export_interactive_maps.py`) that rebuilds the exact same choropleth logic against the real taluka boundary/division-line/Phase 4 data and bakes each of the six metric views out to its own self-contained static HTML file, same palette and boundary overlay as the live version, with a small top nav bar linking between all six. That gives the portfolio card a genuine six-entry dropdown -- matching the STOLEN_STRATA/GPIE pattern -- instead of a flat single link.

Files sit at `outputs/interactive_maps/*.html` at the repo root (a new folder, separate from `07_Outputs/`, matching how the other projects keep their GitHub-Pages-served output separate from their own numbered pipeline folders) -- once pushed and GitHub Pages is switched on for the repo, they'll resolve at `https://sakshimaske303-commits.github.io/THE-COTTON-LINE/outputs/interactive_maps/<metric>.html`.

Also cut the project card's description down -- the first draft ran three sentences longer than every sibling card on the page. Kept the boundary, the null discontinuity result, the NDVI gradient finding, and the open ground-truth check; dropped the restated methodology detail that was already covered by the LIVE DASHBOARD button itself.

**Still open:** GitHub Pages needs enabling on the `THE-COTTON-LINE` repo (Settings → Pages → deploy from the main branch, root) before the six map links actually resolve -- that's a one-time account action still to do, same as it was for every other project's Pages-hosted output. Project Report, Executive Summary, and ground truth remain exactly where Entry 19 left them.

---

## Entry 21

Picked the ground truth check back up. Didn't schedule the separate Karanja Ghadge field visit the plan called for — I already had exactly the right data sitting in a different project. I run a GPS-mapped, weekly-photographed field-monitoring setup on family land in this same taluka (Roots & Reflectance, a separate repo, unrelated in purpose but same physical ground), with a Sentinel-2 NDVI/NDRE pipeline already built for it. Two of those fields are literally in Karanja Ghadge village; five more are in Sawardoh, a few kilometers off. That's GPS coordinates, dated ground photos, and a real field-level satellite time series for seven boundaries — more than the original 2–3-patch plan asked for, and I didn't have to leave a second dataset lying around unused to get it.

**Built it as real processed data, not hardcoded page content.** `03_Data_Processed/Ground_Truth/karanja_sawardoh_field_ground_truth.csv` holds all 7 fields, long-format, matching how every other theme folder in `03_Data_Processed` is structured — role (primary/supporting), village, GPS centroid, crop mix, sowing date, and NDVI/NDRE by date. Eight ground photos (compressed from the originals, ~9 MB each down to under 700 KB, still clean at dashboard size) went into a new `06_Streamlit/assets/ground_truth/` folder. `8_Ground_Truth.py` got rewritten end to end off that CSV and those photos — `utils.data.safe_read_csv` and `show_image_or_placeholder` for both, no new loading pattern invented.

**The honest part.** This isn't a pixel-identical check against the June 2026 taluka number (LST 55.97°C, NDVI 0.264, 45.8% coverage) — that's Landsat at 30 m, taluka-averaged; the field-level numbers are Sentinel-2 at 10 m, at the exact polygon, mostly a different date. Said that directly on the page and in the paper rather than implying a tighter match than what's actually there. What it does show: Karanja Ghadge's two fields came back at NDVI 0.329 and 0.287 on 14 July 2026 — a plausible range next to the coarser taluka read — and the ground photos from the same coordinates show closed, healthy canopy, consistent with those numbers rather than contradicting them. Sawardoh's five fields moved the same direction over the same stretch, supporting evidence, not the named check.

**One genuinely interesting side-finding.** Karanja's 21 June Sentinel-2 pass came back with zero valid pixels for both fields — full cloud mask, not a bug. That's a second, independent sensor losing data over the exact same corner of the scene footprint where Landsat's own taluka read already sits at just 45.8% coverage. Two different platforms, same conclusion: this specific patch of Wardha is genuinely hard to see cleanly from orbit. Wrote that into the page rather than treating it as a nuisance to hide.

**Research paper updated to match.** Section 6.6 goes from "Not Yet Complete" to reporting the actual check, with the scale caveat kept in instead of dropped. Section 7's "Completing the Karanja Ghadge/Sawardoh ground-truth check" bullet is gone — it's done. Both the Abstract's closing line and the Conclusion's closing line, which used to flag this as the one open thread, now close it out the same honest way: confirmed, with the caveat, not oversold.

**Still open:** Project Report and Executive Summary — the standing rule said those come once ground truth actually closes, and it just did, so those are next. README, `app.py`'s nav description, and the portfolio card still say "still open" and need updating to match. GitHub Pages activation for the interactive maps, from Entry 20, is still sitting there too.

---

## Entry 22

Closed out everything Entry 21 left open, then caught two real accuracy problems in the ground truth page itself once I actually looked at it running.

**Project Report and Executive Summary, finally.** Wrote `CL_Project_Report.md` (seven sections — overview, objectives, methodology, key findings, the ground-truth validation from Entry 21, limitations, conclusion — plus a data-sources table) and `CL_Executive_Summary.md` (a tighter, five-section version for anyone who isn't going to read the full paper). Every number in both — the 0.070/0.074-point NDVI gaps, the corridor 0.310 vs 0.299 near-null, the p=0.0348/p=0.0105 full-footprint interactions, the ag-laborer 0.0374/p=0.0361 corridor result with its jackknife range, the Karanja Ghadge taluka reference — pulled straight from the Research Paper and Entries 9-21, nothing re-derived or rounded differently. Built both as PDFs the same way as the Research Paper and Dev Log (pandoc to HTML, then wkhtmltopdf) — hit one new snag doing it, an em-dash in a PDF metadata title field coming out garbled in Document Properties, harmless and cosmetic, fixed by switching that one string to a plain hyphen. README, `app.py`'s document-download section, and the portfolio's own docs menu all got pointed at the finished files, replacing the "still open" language they'd been carrying since before Entry 21.

**Then I actually looked at the page instead of just the data.** The two Karanja fields are correctly soyabean and tur — that's what's growing there, the CSV and the photos both say so — but sitting on a page called THE COTTON LINE, a full photo block of soyabean and pigeon pea read as thematically off, even though it was factually right. Sawardoh has cotton-only ground right there in the same dataset, so I swapped the photo lineup to lead with that instead: cotton close-up and soil texture pulled to the front, generic overview and tur close-up dropped. Went a step further after that — Sawardoh has five fields, but only two (Field 3 and Field 5) are actually cotton with nothing intercropped in; the other three mix in tur, orange, or turmeric. If Sawardoh is standing in as cotton evidence, it should be specifically those two, not the village in general — so I narrowed both the photo selection and the NDVI/NDRE data table down to just Fields 3 and 5, sourced their own field-specific overview photos, and left the other three Sawardoh fields out of the featured view entirely (they're still in the underlying CSV, just not pulled into this page).

**Final pass: reordered and made it interactive.** Flipped the page order so Sawardoh's cotton-only fields lead and Karanja follows — the cotton evidence up front on a project named for cotton, with Karanja still fully present as the taluka the original plan actually named. Both zones now carry their own soil photo side by side with their crop close-up, nine ground photos total across the two sections. Added a real interactive chart at the bottom — Plotly, not a static image, matching the exact pattern already used on the Cotton Signature NDVI page (`go.Figure`, `plotly_layout` for the dark-theme styling, `st.tabs` to flip between NDVI and NDRE) — plotting all four featured fields (Sawardoh 3 & 5, Karanja 1 & 2) on the same axis, one line per field, hoverable and zoomable. Karanja's missing 21 June date shows up honestly as a line that only starts at 14 July rather than getting padded or interpolated.

**Checked every number against the CSV directly before shipping this.** Field 3: NDVI 0.2808 → 0.281, NDRE 0.1553 → 0.155. Field 5: NDVI 0.3277 → 0.328, NDRE 0.1957 → 0.196. Karanja Field 1: NDVI 0.3288 → 0.329, NDRE 0.1813 → 0.181. Field 2: NDVI 0.2874 → 0.287, NDRE 0.1599 → 0.160. Every metric card on the page matches the source CSV to three decimal places, no rounding drift, nothing eyeballed.

Ran a syntax check and a full sweep for stale or placeholder language across every page and every document in the project — nothing left over, nothing pointing at data that doesn't exist yet.

**Still open:** GitHub Pages activation for the interactive maps, from Entry 20 — a one-time account setting, not a code change. Everything else this project set out to do — the boundary construction, both regression scales, the ground-truth check, the full document set, and now a fully current, accurate Ground Truth page — is done.
