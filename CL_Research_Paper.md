# The Cotton Line: Testing the Institutional Persistence of an Erased Colonial Land-Tenure Boundary Across Vidarbha's Agrarian and Vegetation Geography

**Sakshi D. Maske**
Independent Geospatial Researcher

## Abstract

In 1853 the British annexed Berar — the five districts that are today Amravati, Akola, Buldhana, Washim, and Yavatmal — directly into colonial administration. They settled it under a Ryotwari land-tenure system and pushed it hard into cotton monoculture once the American Civil War cut off Lancashire's usual supply. The six districts to its east — Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli — were instead the core of the Central Provinces, settled under a different system, Malguzari. That administrative line was abolished in 1956, but it runs almost exactly along the modern boundary between Amravati Division and Nagpur Division. This paper asks whether that 150-year-old institutional line still shows up as a measurable spatial signature in present-day cotton-signature vegetation phenology, agrarian labor structure, land use, and land-surface temperature. The design is a spatial discontinuity test, not a before/after or synthetic-control comparison.

I built a 384.7 km modern boundary by dissolving 120 talukas into the two historical divisions and extracting their shared edge, then checked it against documented district lineage from 1903–1956 rather than assuming it matched the historical line just because the geography looked similar. The kharif-to-rabi NDVI decline — a monoculture-vs-mixed-cropping signature — was tested across two independent annual cycles: a 0.070 gap between Berar and the Central Provinces in year one (0.325 vs. 0.255, 68 talukas), which came back almost exactly the same in year two, a 0.074 gap (0.316 vs. 0.241) on a completely separate set of scenes. That kind of repeat is what convinced me this is a real, stable seasonal signature and not one unusual year.

A spatial-discontinuity regression (`outcome ~ side + signed_dist_km + side×signed_dist_km + rainfall + elevation`), run both on the 32-taluka immediate-boundary corridor and on the full 66–68-taluka scene footprint, found no significant level jump in any outcome right at the historical line, at either scale. What it did find was a significant side×distance interaction in both of the Earth-observation outcomes at the full-footprint scale — NDVI decline (p = 0.0348) and land-surface temperature (p = 0.0105) — meaning the two sides trend differently with distance from the old boundary even though neither one jumps sharply at it. The agricultural-laborer-to-cultivator ratio showed a similar slope difference at the corridor scale (p = 0.0361, and the direction held up across all 32 leave-one-out jackknife runs), but at the full-footprint scale that flips into a level jump instead (p = 0.014) — a reversal I trace to how lopsided the two sides' territory is within the satellite scene, not a contradiction in the underlying story. Put together, none of this points to a sharp institutional break at the old Berar/Central Provinces line. It points to something quieter: a real gradient that gets stronger the further you move from the boundary, rather than a jump right at it. I think that's a more honest finding than a clean discontinuity would have been, even if it's a less dramatic one. A planned ground-truth check at Karanja Ghadge and Sawardoh villages in Wardha district is still open, and I'm reporting it that way rather than pretending it's done.

**Keywords**: institutional persistence, colonial land tenure, Ryotwari, Malguzari, spatial discontinuity, boundary persistence, NDVI phenology, Vidarbha, remote sensing

---

## 1. Introduction

Vidarbha's farmer-distress geography usually gets explained by rainfall, market prices, or crop choice. I wanted to test something else: whether the 1853 British annexation of Berar, and the Ryotwari land-tenure system pushed onto it to feed cotton into Lancashire's mills, left a mark on this land that hasn't gone away in a century of shared statehood since Independence. Berar's five districts — Amravati, Akola, Buldhana, Washim, Yavatmal — were settled under Ryotwari, where the colonial state dealt directly with the individual cultivator (the *ryot*), who held formal, individually-titled rights to a specific plot. The six Central Provinces districts to the east — Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli — were settled from 1863 under Malguzari instead, where revenue passed through an intermediary landholder, the *malguzar*, responsible for a whole estate rather than dealing with each cultivator individually (Iversen, Palmer-Jones, & Sen, 2013).

That administrative boundary was formally abolished in 1956, when the States Reorganisation redrew India's internal borders along linguistic lines. But it runs almost exactly along the modern boundary between Amravati Division and Nagpur Division — a boundary I already had as present-day taluka geometry — and it also traces closely onto two other things worth noting up front. One is the geography of the 1900 Berar famine, in which an estimated 8.5% of the population died, with the worst of it concentrated in the districts most specialized in cotton (Beckert, 2014). The other is the modern agrarian-distress geography of Vidarbha, which is still worst in the same western districts today.

I'm deliberately not asking "did colonialism cause Vidarbha's agrarian distress" — that's too broad to test properly. The narrower, falsifiable version is: does the historical Berar/Central Provinces boundary still register as a measurable spatial discontinuity in cotton-signature vegetation phenology, agrarian labor structure, land use, and land-surface temperature, once distance-to-boundary, rainfall, and elevation are controlled for? This isn't a policy evaluation and it isn't a before/after test of any specific intervention. It's a spatial-discontinuity, boundary-persistence problem — closer to landscape pattern analysis and historical GIS than to treatment-effect estimation — and the question is whether an erased administrative geography left a fingerprint on the land, checked directly against Earth-observation and census data rather than assumed from the history alone.

Three questions follow from that. First, does cotton-signature NDVI — the size of a taluka's kharif-to-rabi vegetation decline, a monoculture-vs-mixed-cropping signature — jump at the historical line once geography is controlled for? Second, does agrarian labor structure, specifically the ratio of agricultural laborers to cultivators, show the same pattern, and does it hold up at both the immediate corridor and the full regional footprint? Third, is the modern administrative boundary actually the same line as the historical Berar/Central Provinces one — verified against documented district lineage, not just assumed?

## 2. Literature Review

### 2.1 Institutional Persistence and Colonial Land Tenure in India

The clearest empirical precedent for this project is Banerjee and Iyer (2005), who show that Indian districts historically settled under landlord-based (zamindari) revenue systems have significantly worse agricultural investment and productivity today than districts settled under non-landlord (ryotwari or mahalwari) systems — a gap that survives more than a century after the tenure systems themselves were abolished at Independence. They classify each district's historical tenure type from colonial settlement records and compare present-day outcomes across the resulting split. I've adapted that logic to a single, geographically contiguous line rather than a scattered set of districts across British India, which changes what kind of test it is.

Their classification isn't uncontested, and the dispute happens to concern the exact territory I'm studying. Iversen, Palmer-Jones, and Sen (2013) argue that Banerjee and Iyer's original coding lumped almost every Central Provinces district in with the harsher zamindari settlements of Bengal and Bihar, treating the whole province as landlord land. But the Malguzari settlement the Central Provinces actually got from 1863 came with cadastral surveys and real statutory protection for three classes of tenant — occupancy, absolute-occupancy, and *malik makbuza* rights — a meaningfully more mixed arrangement than a pure landlord system. When Iversen and colleagues recoded the Central Provinces using archival settlement records to reflect the actual proportion of protected-tenant land, six of Banerjee and Iyer's eight headline coefficients lost significance, and dropping the Central Provinces from the sample entirely made the whole result disappear. In other words, the districts that were coded wrong were doing most of the work in the published finding. I've followed the corrected reading here, not the original one — Malguzari gets treated throughout as its own distinct category, not folded into a generic "landlord system" opposite Ryotwari. Where this project departs from both papers is scale: I'm testing one boundary at fine spatial resolution, taluka by taluka, with a continuous distance-to-boundary variable, rather than a district-level cross-section spanning multiple provinces. It's closer to a geographic discontinuity test than to either paper's original cross-sectional design.

### 2.2 Geographic Regression Discontinuity and Persistent Colonial-Era Effects

Dell (2010) is the closest methodological model for what I've done here. She shows that the *mining mita*, a forced-labor system Spain imposed on a fixed set of Peruvian districts from 1573 to 1812, still produces a statistically significant discontinuity in household consumption and child stunting today — detected with a spatial regression-discontinuity design centered directly on the old mita boundary, using distance from it as the running variable. That's the same basic move: test whether a specific, mappable historical institution — not a vague regional difference — leaves a present-day discontinuity, using distance to the line rather than a district or state comparison. Keele and Titiunik (2015) lay out what has to hold for a geographic boundary to work as a valid regression-discontinuity design, and flag something I took seriously here: a boundary running through varied terrain can easily conflate a real institutional effect with whatever natural geography also happens to change across the line. That's exactly why rainfall and elevation are in the model as controls, not an afterthought.

### 2.3 Remote-Sensing Detection of Cropping Pattern

NDVI comes from real leaf optics — chlorophyll absorbs red light strongly, while a leaf's internal cell structure scatters near-infrared light heavily, so healthy chlorophyll-rich canopy reads as a large positive NDVI. The agronomic fact I'm actually leaning on is simpler than the physics behind it: a single-cropped field goes back to bare or fallow soil once its one crop comes off, while a mixed-cropped field gets re-sown and stays green. Measure NDVI at the kharif peak (right after the monsoon, when canopy is fullest) and again at the rabi/pre-harvest point, and the gap between the two is a direct read on cropping pattern — a big kharif-to-rabi decline means single-crop cotton, a small one means something followed it. Land Surface Temperature, from Landsat's thermal band, is the second channel I used: bare or sparsely-vegetated soil heats faster and holds less moisture than dense, transpiring canopy, so LST and NDVI are physically connected but not measuring the same thing twice — NDVI is what's growing, LST is how that shows up as surface heat.

## 3. Data and Methodology

### 3.1 Study Design

I built a modern proxy for the historical Berar/Central Provinces boundary out of present-day taluka administrative geometry (120 talukas across Vidarbha's 11 districts), dissolved the talukas into the two historical divisions, and extracted their shared edge as one continuous line — then checked that against documented 1903–1956 district lineage rather than trusting it just because it looked right (Section 3.3). A 25 km buffer corridor split by division defines the immediate-boundary sample, 32 talukas. The same outcomes are separately tested at the full satellite-scene footprint (66–68 talukas depending on data availability) to see whether the corridor test is just underpowered rather than genuinely finding nothing. Every outcome gets run through a spatial-discontinuity regression that separates a level jump right at the boundary from a difference in slope with distance from it, with rainfall and elevation controlled throughout so Vidarbha's real west-drier/east-wetter gradient doesn't get mistaken for an institutional effect.

### 3.2 Data Sources

| Variable | Source | Coverage |
|---|---|---|
| Administrative boundaries (taluka-level) | IIT Bombay POCRA Maharashtra Census shapefile portal; cross-checked against `datta07/INDIAN-SHAPEFILES` (Census 2011/LGD-linked) for 17 talukas missing from the original source | 120 talukas, 11 districts |
| Vegetation (NDVI), Climate (LST) | Landsat 8/9 Collection 2 Level-2 Science Products (U.S. Geological Survey), Level-2 surface reflectance (SR_B4, SR_B5) and thermal (ST_B10) bands, WRS-2 path 144, rows 045/046 | 66–68 talukas |
| Hydrology (rainfall) | WorldClim 2.1 monthly precipitation climatology, ~18.5 km (10 arc-minute) grid (Fick & Hijmans, 2017) | 120 talukas (long-term normals, not a specific-year time series) |
| Terrain (elevation) | SRTM 1 arc-second digital elevation model (Farr et al., 2007) | 32 corridor talukas (68 in the full-footprint extension) |
| Population, agrarian labor, land use | Census village-level shapefiles (600+ attributes/village), aggregated to taluka level | 8 of 11 districts (Amravati, Yavatmal, Wardha, Chandrapur, Nagpur, Bhandara, Gondia, Gadchiroli) |
| Agriculture (cotton share, holding size) | Maharashtra Area-Production-Yield 2024-25 workbook; Maharashtra Economic Survey 2025-26, Chapter 7 and District Indicators annexure | 11 districts |
| Economics (FRA compilation) | Maharashtra Tribal Development Department Administrative Report (2020-21); 2024 fact-finding committee report; EPW/Scroll.in secondary reporting on Vidarbha community forest rights | Contextual/narrative, not a regression variable (Section 3.6) |

### 3.3 Boundary Construction and Historical Verification

I split the 120-taluka administrative layer by district into the two historical zones — Amravati Division (Akola, Amravati, Buldhana, Washim, Yavatmal) standing in for Berar/Ryotwari territory, Nagpur Division (Nagpur, Wardha, Bhandara, Gondia, Chandrapur, Gadchiroli) for Central Provinces/Malguzari territory — dissolved each into one polygon, and extracted the shared edge between them. That first pass came out as 256 disconnected line fragments, which turned out to just be adjacent taluka polygons not sharing exact vertices along their common edge, not a real topological problem. A line-merge pass collapsed it cleanly into one continuous 384.7 km line, running from the Akola/Amravati/Wardha corner in the north to the Yavatmal/Chandrapur corner in the south. A 25 km buffer split by division gives the discontinuity corridor — 7,387 km² on the Berar side, 7,987 km² on the Central Provinces side — containing 32 of Vidarbha's 120 talukas.

That's a present-day administrative proxy, and I needed to check it against the actual historical line rather than just assume they matched because the geography looked similar. I couldn't find a digitized period map — I looked for Imperial Gazetteer district maps from 1901–1931 and Central Provinces & Berar administrative atlases, and neither turned up in accessible form — so I traced each modern district's documented administrative lineage back through 1903–1956 instead. Berar Division's historical districts — Amraoti, Akola, Ellichpur, Buldhana, Basim, Wun — map cleanly onto the modern Amravati Division: Ellichpur got absorbed into Amravati district as a taluka, Wun was renamed Yavatmal, and Basim was renamed Washim (folded into Akola for a while, then recreated as its own district on 1 July 1998). The Central Provinces' Nagpur Division — Nagpur, Bhandara, Chanda (renamed Chandrapur), Wardha, and Balaghat — mostly maps onto the modern Nagpur Division the same way, with Gondia (split from Bhandara in 1999) and Gadchiroli (split from Chandrapur in 1982) as later internal subdivisions of the same territory. The one real wrinkle is Balaghat, which went to Madhya Pradesh's Jabalpur Division in the 1956 language-based States Reorganisation, while the rest of the old Nagpur Division went to Bombay State and then, in 1960, to Maharashtra. Balaghat was never in my 11-district Vidarbha sample to begin with, so this doesn't require any fix to the boundary I'd already built — but it does mean the Central Provinces side of my boundary is a touch smaller than the historical division's full extent, and that gap is down to a 1956 language-based state redraw, not anything to do with Ryotwari or Malguzari. With that caveat on the record, the modern Amravati/Nagpur Division line is, as far as documented district lineage can show, the same line as the historical Berar/Central Provinces boundary.

![Figure 1](03_Data_Processed/Administrative/boundary_verification_map.png)

**Figure 1.** The two dissolved divisions, the extracted 384.7 km boundary line, and the 25 km discontinuity corridor, overlaid against the taluka grid.

### 3.4 Outcome Variables

**Cotton-signature NDVI.** Landsat 8/9 Collection 2 Level-2 surface-reflectance bands (SR_B4 red, SR_B5 near-infrared) were processed into NDVI at three seasonal points across two independent annual cycles — a kharif-peak date and a rabi/pre-harvest date, in both 2025–26 and, as an independent replication, 2024–25. The outcome is each taluka's kharif-to-rabi NDVI decline.

**Land-surface temperature.** The Landsat thermal band (ST_B10), converted to Celsius, as a second and physically independent outcome alongside NDVI.

**Agrarian labor structure.** The ratio of agricultural laborers (main and marginal workers combined) to cultivators, aggregated from village-level Census data up to taluka level — the standard landlessness indicator in Indian agrarian-economy work.

**Land use.** A nine-category village-level breakdown (forest, non-agricultural use, barren/uncultivable, permanent pasture, misc. tree crops, cultivable waste, current and other fallow, net sown area). I checked that these nine categories actually sum to 99–100% of each village's recorded area before trusting the dataset.

**Cotton share and holding size.** District-level cotton area as a share of total cropped area, and average operational landholding size, both from the Area-Production-Yield workbook.

One pipeline bug had to be found and fixed before any of this could be trusted. Landsat Collection 2 Level-2 thermal and reflectance bands use digital number (DN) = 0 as the fill value for cloud-masked and off-swath pixels — roughly a third of every scene. An earlier processing pass had applied the Kelvin scale/offset straight to the raw DN without masking DN = 0 out first, and running 0 through that formula gives exactly 149 K, or −124.15°C — not a real temperature anywhere on Earth, and exactly the floor value the broken output was showing. The same bug, unmasked fill pixels, was quietly sitting in the reflectance pipeline too: a merged raster was reporting 100% valid pixels when the true fill rate on the source scene is around 33%. I fixed both by masking DN = 0 as no-data before applying the scale/offset, and reprocessed everything from the raw scenes.

### 3.5 Spatial-Discontinuity Regression

Every outcome went through the same ordinary-least-squares specification:

*outcome ~ side + signed_dist_km + side×signed_dist_km + annual_total_mm + elevation_m*

`side` is an indicator for the Berar/Ryotwari division. `signed_dist_km` is each taluka centroid's distance to the dissolved boundary line, computed in UTM 44N and signed positive on the Berar side. Rainfall and elevation are controls. The `side` coefficient is the actual question — does the outcome jump right at the boundary. The `side × signed_dist_km` interaction asks something different: does the outcome's slope with distance from the boundary differ by side, independent of any jump in level. I ran this twice for each outcome where the data allowed it — once on the 32-taluka corridor, once on the full satellite-scene footprint (66–68 talukas, depending on which variables that footprint's coverage actually supports) — to check whether the corridor result was simply underpowered rather than genuinely null.

Elevation came from SRTM 1 arc-second tiles sampled at each taluka centroid (194–497 m across the corridor, which is about right for this stretch of the Deccan plateau edge). Rainfall came from WorldClim 2.1's monthly precipitation climatology, sampled at centroids and summed to an annual total. Both are long-term normals, not a specific year's actual weather or a fine-grained surface — WorldClim's ~18.5 km grid cell is bigger than most individual talukas, so this control is establishing the regional gradient, not taluka-by-taluka precision.

### 3.6 Robustness Checks and Scope Decisions

I ran a leave-one-out jackknife on every interaction coefficient that came back significant, refitting the model 32 times with one corridor taluka dropped each time, to make sure no single taluka was quietly driving the result on its own. The full-footprint extension in Section 3.5 works as a second robustness check in the same spirit — does a result found at one scale hold up, in the same direction, at a much larger and differently-powered sample.

Two things got scoped out of the regression entirely rather than forced in on shaky ground. Irrigation coverage, computed from the Census shapefiles' `area_irri`/`net_area` fields, came back at 58–92% across sampled villages — flatly inconsistent with the well-documented reality that Vidarbha's cotton belt runs 15–20% irrigated at most. Whatever those fields actually measure, it isn't straightforwardly irrigated-vs-cultivated area the way the column names suggest, so I dropped it rather than report a number I don't trust. Forest Rights Act recognition — claims filed, titles distributed, community forest resource area — has no clean taluka-level or even consistent district-level public dataset for Vidarbha. What exists is scattered across a state-level administrative report, a 2024 fact-finding committee report, one genuinely solid district anchor (Gadchiroli), a regional Vidarbha-wide total, and a few individual village case studies, all at incompatible scales. I compiled that as a sourced, tagged table — each figure tagged with scope, value, unit, as-of date, and source — rather than forcing it into a taluka-level panel the public record simply can't support. It shows up in the discussion here as institutional-history context, not as a regression variable.

## 4. Results

### 4.1 Cotton-Signature NDVI: A Reproducible Regional Gradient, Vanishing at the Immediate Corridor

At the full scene footprint (68 talukas), the Berar/Amravati Division side showed a mean kharif-to-rabi NDVI decline of 0.325, against 0.255 on the Central Provinces/Nagpur Division side — a 0.070-point gap. The Central Provinces side also had a lot more spread (std. dev. 0.062 vs. 0.041), so the "some fields get a second crop" story is real there but uneven, not uniform. Both sides peaked at nearly the same kharif NDVI (0.66 Berar, 0.64 Central Provinces) — the divide isn't in how green the land gets during the monsoon, it's in what happens to it afterward.

That gap held up independently a year earlier, too: kharif 2024/rabi 2024-25 gave Berar a 0.316 decline and the Central Provinces a 0.241 decline — a 0.074-point gap, on a comparison that shares no scene at all with the first year (64 of 68 talukas returned valid data in both years).

![Figure 2](07_Outputs/seasonal_ndvi_signature.png)

**Figure 2.** Seasonal NDVI trajectory (kharif peak to rabi/pre-harvest) and the kharif-to-rabi decline, by division, year one.

![Figure 3](07_Outputs/year2_ndvi_comparison.png)

**Figure 3.** Kharif-to-rabi NDVI decline, both independent annual cycles, by division.

At the immediate 25 km corridor, though, this gap nearly disappears: 0.310 (Berar) vs. 0.299 (Central Provinces), 29 talukas — barely distinguishable. The Central Provinces talukas sitting inside the corridor — Wardha, Nagpur, Chandrapur — are themselves substantial cotton growers, so the two sides look far more alike right at the boundary than the region-wide numbers suggest. I don't read this as a weaker version of the regional result. It's a real finding about how the boundary actually behaves: the effect is a gradient that gets stronger moving away from the historical line in both directions, not something concentrated right at it.

![Figure 4](07_Outputs/lst_ndvi_corridor_comparison.png)

**Figure 4.** NDVI and land-surface-temperature maps and division boxplots, June 2026 single-date snapshot, corridor.

### 4.2 Agrarian Labor Structure, Land Use, and Cotton Dependency

Across the 32 corridor talukas, the agricultural-laborer-to-cultivator ratio came out at 2.90 on the Berar side against 1.96 on the Central Provinces side (15 Berar talukas, 17 Central Provinces talukas). For every cultivator in the corridor's Berar talukas there are nearly three agricultural laborers, against roughly two on the other side, and it isn't one or two outlier talukas dragging that average. Net cultivated land at the corridor stood at 68.9% (Berar) against 61.5% (Central Provinces); forest cover, though, was almost identical on both sides of the corridor specifically (12.5% vs. 12.6%), because the corridor sits in a farming transition zone on both sides — the Central Provinces' real deep-forest tracts are further east, in Gadchiroli, well outside this zone. Fallow land was nearly double on the Central Provinces side of the corridor (5.8% vs. 3.3%), which I'm reading cautiously rather than as a confirmed distress signal, since it's just as consistent with crop-rotation practice as with land genuinely sitting idle.

Cotton dependency at the district level doesn't split cleanly along the historical line. Yavatmal (51% of cropped area) and Wardha (49%) — one historically Berar, one historically Central Provinces — are nearly tied for the highest cotton share in the region, and Chandrapur (38%) and Nagpur (38%), both Central Provinces districts, also run high. Bhandara (0.15%) and Gondia (0%) sit at essentially zero, but that's because they're rice districts, not because cotton stopped at some line. Cotton cultivation clearly spread well past the old Berar boundary — Wardha in particular has its own substantial cotton history that has nothing to do with Berar. Net sown area is the cleaner, more consistent divide: all five Amravati Division districts sit in a tight 60–75% band (std. dev. 6.8), while the six Nagpur Division districts range from 14% (Gadchiroli, mostly forest) up to 57% (Nagpur), averaging around 41% with much more spread (std. dev. 15.4). Berar reads as uniformly under the plough; the Central Provinces reads as a mix of heavily-cultivated and heavily-forested districts — which tracks the history, since Ryotwari brought the whole province under individual cultivation while Malguzari left more land under estate or forest control that was never fully converted to cropland. Average operational holding size, which I tested as a possible fragmentation signature, showed no real corridor divide at all (Berar 1.81 ha vs. Central Provinces 1.90 ha) — actually the opposite of what a naive "Ryotwari means smaller, more fragmented holdings" story would predict. I'm treating that as a genuinely flat result, not stretching it into something it isn't.

![Figure 5](07_Outputs/population_agrarian_comparison.png)

**Figure 5.** Agricultural-laborer-to-cultivator ratio and literacy, by division, corridor talukas.

![Figure 6](07_Outputs/landuse_corridor_comparison.png)

**Figure 6.** Net cultivated area, fallow land, and forest cover, by division, corridor talukas.

![Figure 7](07_Outputs/agrarian_indicators_comparison.png)

**Figure 7.** Cotton share, net sown area, per-capita foodgrain production, and average holding size, all 11 districts.

![Figure 8](07_Outputs/precipitation_corridor_comparison.png)

**Figure 8.** Annual precipitation total and monsoon-season share, by division, district-wide and corridor.

### 4.3 Spatial-Discontinuity Regression: No Level Jump, a Real Slope Difference

At the 32-taluka corridor scale, none of the four tested outcomes showed a statistically significant level jump (`side`) right at the historical boundary once rainfall and elevation were controlled for: kharif-to-rabi NDVI decline (p = 0.458), agricultural-laborer ratio (p = 0.9601), net cultivated area (p = 0.577), land-surface temperature (p = 0.792). Rainfall and elevation, on the other hand, kept showing up as real predictors across these same models — rainfall p = 0.015 and elevation p = 0.002 in the NDVI-decline model, rainfall p < 0.001 in the agricultural-laborer model, rainfall p = 0.046 and elevation p = 0.020 in the net-area model. That's confirmation that Vidarbha's actual west-drier/east-wetter, lower/higher geography is doing real work in these outcomes on its own, separate from anything about the old administrative line — which is exactly the confound these controls were meant to catch.

![Figure 9](07_Outputs/phase4_discontinuity_plots.png)

**Figure 9.** Outcome vs. distance-to-boundary, fitted lines by side, corridor scale, four headline outcomes.

One coefficient at the corridor scale did clear significance: the `side × signed_dist_km` interaction on the agricultural-laborer ratio, coefficient 0.0374, p = 0.0361. That's not a level jump — it's a difference in how the ratio's relationship with distance from the boundary plays out on each side. A leave-one-out jackknife across all 32 corridor talukas found this coefficient stable in both direction and rough size throughout, staying between 0.026 and 0.044 no matter which taluka got dropped. The p-value moved around more, though — it stayed under 0.05 in 26 of 32 runs and climbed as high as 0.138 when a few specific talukas (Amravati taluka, Seloo, Samudrapur, Narkhed, Korpana, Yavatmal taluka) were excluded. I'm calling this suggestive rather than fully robust on its own.

Retesting NDVI decline and land-surface temperature at the full 66–68-taluka footprint — the two outcomes with scene-wide remote-sensing coverage, not limited by the census data's district gaps — changed the picture somewhat. The level-jump term stayed non-significant for both (NDVI decline `side` p = 0.821; LST `side` p = 0.5123), consistent with the corridor finding of no sharp jump. But the `side × signed_dist_km` interaction, which had only cleared significance for one variable at the corridor scale, was now significant for both Earth-observation outcomes independently at the full-footprint scale (NDVI decline interaction p = 0.0348; LST interaction p = 0.0105), and `signed_dist_km` on its own was strongly significant in both models too (p < 0.001). That's a well-powered, real gradient with distance from the historical boundary, differently shaped on each side, showing up in two physically separate measurements rather than just one.

![Figure 10](07_Outputs/phase4_fullfootprint_plots.png)

**Figure 10.** NDVI decline and land-surface temperature vs. distance-to-boundary, full-footprint scale, fitted lines by side.

The agricultural-laborer ratio did something different again at the full footprint (n = 67, once Bhandara and Gondia's population and land-use data were processed): the level-jump term turned significant (`side` coefficient = 0.622, p = 0.014), while the interaction term that had cleared significance at the corridor scale did not (p = 0.579) — basically the reverse of the corridor result. I don't think that's a real contradiction so much as a symptom of how lopsided this particular sample is. Within this specific satellite scene, the Berar side barely gets past 20 km from the boundary, because Amravati is the only Berar-division district the scene actually covers, while the Central Provinces side stretches past 160 km, out to Bhandara and Gondia. A "jump near the boundary" reading makes more sense than a "different slope across the whole range" reading when one side of the comparison doesn't really have much range to have a slope over in the first place. I trust the corridor-scale interaction result more for describing what's happening right at the line, and I'm treating the full-footprint level-jump result as suggestive of a broader regional gap rather than a second measurement of the same thing. Net cultivated area stayed non-significant at both scales (corridor p = 0.577, full footprint p = 0.121) — a clean null that doesn't need any reconciling.

![Figure 11](07_Outputs/phase4_fullfootprint_all4_plots.png)

**Figure 11.** All four full-footprint outcomes (NDVI decline, LST, agricultural-laborer ratio, net cultivated area) vs. distance-to-boundary, fitted lines by side.

## 5. Discussion

The main thing this project found is not a discontinuity at the historical Berar/Central Provinces line — it's the clear absence of one, alongside real evidence of a longer-range gradient that looks different on each side of the old boundary. Every outcome I tested — cotton-signature NDVI, agrarian labor structure, net cultivated area, land-surface temperature — showed no statistically significant jump right at the line, at either the immediate corridor or the full regional footprint, once rainfall and elevation were controlled for. I don't think that null is a failure of the design. It means whatever institutional legacy this boundary carries doesn't show up as a sharp edge the way a classic discontinuity result would, and forcing a discontinuity where the data doesn't support one would have been worse than just reporting the shape I actually found.

What the data do support is a real gradient. The kharif-to-rabi NDVI decline — the central cotton-monoculture signature here — shows a substantial gap, confirmed independently in two separate years (0.070 and 0.074 points), that narrows to almost nothing specifically at the immediate boundary corridor, because the Central Provinces talukas closest to the line are themselves serious cotton growers. And at the full-footprint scale, the side-by-distance interaction is significant in both NDVI decline and land-surface temperature, independently — two physically different measurements pointing the same way, which is more convincing than either one alone. Put together, this looks like an institutional legacy operating at a broader regional scale than a boundary-hugging test can pick up: the deeper interior of each historical province resembles its own institutional type more than the immediate frontier zone does. That's a specific, falsifiable claim, and I'd argue a more historically plausible shape of persistence than a sharp jump on a boundary erased 150 years ago would have been. It also fits with Iversen et al.'s (2013) recoding of the Central Provinces as a genuinely mixed, protected-tenant system rather than a uniform landlord one — a tenure system with real internal variation, which Malguzari clearly had, is a more plausible source of a gradient than of a sharp, boundary-wide break.

The agricultural-laborer ratio flipping between the corridor and full-footprint scales — a slope difference at one, a level jump at the other — points to a real limitation of testing a historical boundary against a modern satellite scene's fixed extent instead of the historical territory itself. The two sides of this particular scene simply aren't comparably sized or shaped, and a result that looks like a different kind of effect at each scale might partly be an artifact of that mismatch rather than the underlying institutional geography. I've reported both reads here rather than picking whichever looked more convenient, and I lean toward the corridor-scale result as the more trustworthy one, since it's closer to the "right at the boundary" question I actually set out to answer.

## 6. Limitations

### 6.1 Sample Size at the Corridor Scale

The 32-taluka corridor is genuinely underpowered for detecting anything short of a fairly large, sharp discontinuity. The jackknife results in Section 4.3 show a coefficient whose direction holds steady but whose significance is sensitive to which taluka gets dropped — a real constraint at that scale, not something to wave away.

### 6.2 Rainfall as a Long-Term Climatology, Not a Time Series

WorldClim's precipitation data is a multi-decade monthly normal at roughly 18.5 km resolution, coarser than most individual talukas. It gets the regional rainfall gradient right as a control, but it can't capture year-to-year variation or fine within-taluka detail.

### 6.3 Full-Footprint Sample Asymmetry

The full-scene footprint used to extend NDVI, LST, and later the agricultural-laborer ratio is fixed by satellite scene geometry — WRS-2 path 144, rows 045/046 — not by where the historical provinces actually end. As Section 4.3 shows directly for the agricultural-laborer result, this can leave one side of the comparison with a much shorter or longer distance range than the other, which complicates comparing a level jump against a slope difference across scales.

### 6.4 Irrigation Data Dropped as Untrustworthy

The Census-derived irrigation coverage fields came back flatly inconsistent with how rainfed Vidarbha's cotton belt actually is, so I dropped the variable rather than report a number I don't believe. A state agriculture department irrigation dataset would be a better source if this ever becomes essential to a future version of this analysis.

### 6.5 FRA Data as Narrative, Not Quantitative Evidence

There's no clean taluka- or even consistent district-level Forest Rights Act dataset for Vidarbha in the public domain. The figures I compiled (Section 3.6) span incompatible scales and dates and are used here as institutional-history context, not as evidence bearing on the statistical claims.

### 6.6 Ground-Truth Verification Not Yet Complete

Everything in this study is satellite- or census-derived. No field visit has yet checked the remote-sensing signal against actual crop type, canopy density, or soil conditions at specific coordinates on the ground. I have a planned check at Karanja Ghadge and Sawardoh villages in Wardha district — inside the corridor, on the Central Provinces/Malguzari side — with one taluka-level reference point already on record (June 2026: mean LST 55.97°C, mean NDVI 0.264, 45.8% valid pixel coverage in that pass), but the actual field photography and pixel-level comparison haven't happened yet. I'm reporting this as open, not as done.

### 6.7 A Historical-Lineage Verification, Not a Literal Map Overlay

The boundary's historical accuracy (Section 3.3) rests on tracing documented district administrative lineage across 1903–1956, not on overlaying a digitized period map against the modern line — I couldn't find one in accessible form. The lineage-based check answers the question I actually needed answered, but a real period map would still make any future visual presentation of the boundary's history stronger.

## 7. Future Work

**A wider or differently-shaped analysis footprint.** Processing the rest of the Landsat scenes covering all 11 Vidarbha districts, instead of just the two-scene corridor-relevant subset used here, would fix the scene-geometry asymmetry in Section 6.3 and give both historical provinces comparable distance range.

**Extending population and land-use coverage to all 11 districts.** The agricultural-laborer ratio and land-use variables currently cover 8 of 11 districts. Sourcing and processing the remaining three (already partly done for Gadchiroli, whose data is processed but falls outside the current NDVI/LST scene) would let every outcome get tested at a genuinely consistent regional scale.

**Completing the Karanja Ghadge/Sawardoh ground-truth check.** Photographing specific field patches with GPS coordinates, noting the visible crop and canopy density, and comparing that directly against the NDVI/LST pixel values at those exact coordinates would be a direct, if small-sample, test of whether the remote-sensing signal here actually tracks real conditions on the ground.

**A digitized historical boundary map.** An accessible digitized version of an Imperial Gazetteer-era district map, or a Central Provinces & Berar administrative atlas, would let me overlay the modern boundary construction directly against a period source, on top of the lineage-based verification already done.

## 8. Conclusion

I don't find a statistically significant discontinuity in cotton-signature vegetation phenology, agrarian labor structure, land use, or land-surface temperature right at the 150-year-erased Berar/Central Provinces boundary, at either the 25 km corridor scale or the full regional footprint, once rainfall and elevation are controlled for. I'm reporting that absence of a sharp jump directly, not dressing it up as a weaker version of a discontinuity finding. What does hold up is a real, twice-confirmed regional gradient in cotton-signature NDVI that gets stronger moving away from the historical line rather than concentrating at it, and a significant difference in how both NDVI decline and land-surface temperature trend with distance from the boundary on each side — consistent across two physically independent Earth-observation channels, at a well-powered sample. The agricultural-laborer-to-cultivator ratio adds a more qualified piece of evidence on top of that: a slope difference right at the boundary that's directionally stable under jackknife resampling but not fully robust to individual taluka exclusion, and one that turns into a different-shaped result at a larger but structurally lopsided sample. Taken together with a historical-lineage check confirming the modern boundary I've used throughout is, as far as documented administrative history can show, the same line as the 1853–1956 Berar/Central Provinces boundary, the honest summary is this: a real institutional-geography legacy that shows up as a gradient across Vidarbha rather than a discontinuity right where the institutions themselves were once drawn. That's a more precise finding than either a confirmed sharp boundary effect or a flat null would have been, even if it's a quieter one. The one piece of this project's evidence chain I haven't closed yet is the planned field ground-truth check, and I'm leaving it open rather than assuming it away.

## References

Banerjee, A. V., & Iyer, L. (2005). [History, institutions, and economic performance: The legacy of colonial land tenure systems in India](https://www.aeaweb.org/articles?id=10.1257/0002828054825574). *American Economic Review*, 95(4), 1190–1213.

Beckert, S. (2014). *[Empire of Cotton: A Global History](https://www.penguinrandomhouse.com/books/10461/empire-of-cotton-by-sven-beckert/)*. Knopf.

Dell, M. (2010). [The persistent effects of Peru's mining mita](https://onlinelibrary.wiley.com/doi/10.3982/ECTA8121). *Econometrica*, 78(6), 1863–1903.

Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., Seal, D., Shaffer, S., Shimada, J., Umland, J., Werner, M., Oskin, M., Burbank, M., & Alsdorf, D. (2007). [The Shuttle Radar Topography Mission](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005rg000183). *Reviews of Geophysics*, 45(2), RG2004.

Fick, S. E., & Hijmans, R. J. (2017). [WorldClim 2: New 1-km spatial resolution climate surfaces for global land areas](https://rmets.onlinelibrary.wiley.com/doi/10.1002/joc.5086). *International Journal of Climatology*, 37(12), 4302–4315.

Iversen, V., Palmer-Jones, R., & Sen, K. (2013). [On the colonial origins of agricultural development in India: A re-examination of Banerjee and Iyer, "History, institutions and economic performance"](https://www.tandfonline.com/doi/abs/10.1080/00220388.2013.807502). *Journal of Development Studies*, 49(12), 1631–1646.

Keele, L. J., & Titiunik, R. (2015). [Geographic boundaries as regression discontinuities](https://www.cambridge.org/core/journals/political-analysis/article/geographic-boundaries-as-regression-discontinuities/2A59F3077F49AD2B908B531F6E458430). *Political Analysis*, 23(1), 127–155.

Maharashtra State Tribal Development Department. (2021). *[Administrative Report 2020-21](https://tribal.maharashtra.gov.in/Site/Upload/GR/Administrative%20Report%2020-21%20Final%2017092024.pdf)*. Government of Maharashtra. [Forest Rights Act compilation, Section 3.6]

U.S. Geological Survey. *[Landsat 8-9 OLI/TIRS Collection 2 Level-2 Science Products](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-9-olitirs-collection-2-level-2)*. Earth Resources Observation and Science (EROS) Center.

Government of Maharashtra. (2026). *[Economic Survey of Maharashtra 2025-26](https://mahades.maharashtra.gov.in/home.do?lang=en)*, Chapter 7 (Agriculture). Commissionerate of Agriculture.

Government of Maharashtra. (1994, April 30). *[The Development Boards for Vidarbha, Marathwada and the Rest of Maharashtra Order, 1994](https://indiankanoon.org/doc/11824594/)*, Notification No. GS/G/94/DB/432, issued under Article 371(2) of the Constitution of India.
