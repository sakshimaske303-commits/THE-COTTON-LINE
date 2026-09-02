# The Cotton Line: Testing the Institutional Persistence of an Erased Colonial Land-Tenure Boundary Across Vidarbha's Agrarian and Vegetation Geography

**Sakshi D. Maske**
Independent Geospatial Researcher

## Abstract

Are there 150-year-old institutional legacies measurable in the 21st century as a spatial signature, in patterns of vegetation phenology (cotton signatures), agrarian labor structure, land use and land surface temperature? That is the core question this paper addresses and the design is not a ‘before’-‘after', it's a ‘spatial discontinuity' test to see if there is still a measurable gap across an administrative line following a historical change. It was in 1853 when the British stormed the Berar region, consisting of the districts Amravati, Akola, Buldhana, Washim, and Yavatmal, and implemented a new land-tenure system in the region known as the "Ryotwari system. The American Civil War brought an end to the export of cotton from America to Lancashire, and Lancashire pressured Berar to fill that gap, which led to Berar becoming a producer of cotton on a monoculture basis. The six districts in the East of Berar (Nagpur, Wardha, Chandrapur, Bhandara, Gondia and Gadchiroli), the heart of the Central Provinces, were administered on a somewhat different system of settlement which was known as “Malguzari.” The administrative boundary was officially renamed and discontinued in 1956, but it still corresponds, as would be the case today, to the current administrative division between Amravati Division and Nagpur Division.

Two annual seasons of kharif-rabi NDVI reducing indicate a similar signature. The negative difference for Berar was 0.325 in its performance as compared with 0.255 of Central Provinces in year one, showing difference of 0.070 points across 68 talukas in Berar. Back in Year two, which was a new set of scenes, the picture was virtually the same: Berar scored 0.316 and Central Provinces 0.241, a difference of 0.075. I wasn't convinced by that repetition over a single unusual year, but by the repetition over two independent cycles. Before constructing the boundary was possible, it had to be built – a 384.7 km new line formed by joining 120 talukas in their two historical segregations and separating them by extracting the common frontier between the two – but only after double-checking that it did not assume that the frontier aligned with the old boundary because they shared geographical characteristics, but made sure also that it matched the documented old boundary from 1903–56.

The headline null result was the failure to detect any significant level slope, collapse or shift along the historical trend line at any scale (immediate-boundary corridor of 32 talukas, or the extended scene footprint of 66-68 talukas) in the spatial-discontinuity regression (outcome ~ side + signed_dist_km + side×signed_dist_km + rainfall + elevation) of each of the outcomes. At the full footprint level, what the regression did reveal was a significant side×distance interaction for both EO outcomes (NDVI's decline: p = 0.0348; Land-Surface Temperature: p = 0.0105) — meaning the two sides follow different trends moving away from the old boundary, even without a sharp drop at it. The agricultural-laborer-to-cultivator ratio exhibited a similar slope difference at the corridor scale (p = 0.0361), with a similar direction for all 32 leave-one-out jackknife runs, but despite all this the slope difference at the full-footprint scale is offset by a level jump (p = 0.014) — not a contradiction to the underlying story but simply because the territory on the two sides of the corridor is lopsided within the satellite scene. Both these findings together imply no abrupt change of institution at the old Berar/Central Provinces border, but a rather subtle phenomenon: a strengthening gradient of the institution with increasing distance from the border. I believe that's more of the baby than a clean break would, although it is not as great. To reinforce the overall NDVI signal, a field-ground truth effort was carried out against separate field-monitoring efforts for the same field boundaries at Karanja Ghadge and Sawardoh villages of Wardha district, and fulfilled in only 7 boundary tests in small efforts, if it is not a check, what is it?

**Keywords:** institutional persistence, colonial land tenure, Ryotwari, Malguzari, spatial discontinuity, boundary persistence, NDVI phenology, Vidarbha, remote sensing

---

## 1. Introduction

The difference between the systems of Ryotwari and Malguzari was clearly contained in the original colonial land-revenue record itself (Baden-Powell, 1892): that under Ryotwari, which was applied in Berar's five districts – Amravati, Akola, Buldhana, Washim, and Yavatmal – the individual cultivator or ryot possessed formal rights to a specific plot, while under Malguzari, which the six Central Provinces districts to the east were settled under by 1863, the land was instead settled in the name of an intermediary landholder who accounted for the whole estate rather than individual cultivators (Iversen, Palmer-Jones, & Sen, 2013). Vidarbha's farmer-distress geography is usually explained by rainfall, market prices, or crop selection — so I wanted to know if something else was still left in the geography of the land, whether the 1853 British takeover of Berar and the Ryotwari system it introduced to supply cotton to Lancashire mills left an imprint that never fully disappeared through the generations since Independence.

This administrative border was actually abolished in 1956, when redrawing of internal boundaries in India were change by linguistics, but now it is the same as it was before that; taluka geometry was already available in my zip file. There are two main lines to note up front, both of which originate from this same line. The geography of agrarian distress has always been the same: the modern video geography of Vidarbha is witness to the same pattern - worst areas are the same areas of Vidarbha, where there had been farmer suicides for the past two decades (Mohanty, 2005; Mishra, 2006); the state government had established a standing statutory board for the region under Article 371(2) (Government of Maharashtra 1994). Looking further back, some estimate that the 1900 Berar famine claimed about 8.5% of the population with the worst impact occurring in the areas where cotton was the sole cash crop grown ( Beckert, 2014); similarly, in colonial India where cotton was the dominant cashcrop cultivated for export, other agrarian regions suffered far more than this one boundary alone ( Roy, 2011). They'll know about the famine, but it was this intertwining bit of an old line, a documented famine, and an unresolved modern distress geography on one ground that made it better to test the boundary than assume it.

What the assessment of the role of colonialism in Vidarbha's agrarian issues would require is a scientific test of the entire phenomenon of colonisation and that is too much to ask here. The question as narrowed, though still not falsifiable, is this: once the distance to the boundary, amount of rainfall, and land elevation are factored in, can the boundary of the historical Berar/Central Provinces be measured today as a spatial discontinuity, as demonstrated by the cotton signature vegetation phenology, as well as the structure of agrarian workforce, land-use, and land surface temperature? This is not a policy appraisal and is not a pre/post test of a specific intervention. It poses the question of whether the signature of one such administrative geography is still locked in the soil today — closer to landscape pattern analysis and historical GIS than to treatment-effect estimation — with validation that merges earth-observation data with census data, rather than being assumed from history alone.

There are three questions arising from that. Does the cotton-signature NDVI – the size of the change that kharif crops make when compared to the rabi crops in a taluka – jump at the historical line after controlling for geography?

Second, do the same trends apply to the agrarian labor structure, the proportion of agricultural labourers compared with the proportion of cultivators, and does it apply in the immediate corridor and to the broader regional scope?

Third, verified against the line on district records not assumed: Is the present administrative boundary the same as the past Berar/Central Provinces boundary?

## 2. Literature Review

### 2.1 Institutional Persistence and Colonial Land Tenure in India

One of the clearest empirical precedents for this, as mentioned, and interestingly one of the most pertinent, is an article published by Banerjee and Iyer (2005) which lies at exactly the center of a dispute that encroaches upon the territory here explored. They compiled historical data on tenure type from the records of the colonial governments of every district in India and revealed that there has been a continuing gap of more than a century in agriculture investment and productivity between the districts settled under landlord based revenue system (a zamindari system) and non-landlord (ryotwari or mahalwari) based revenue system, even after the zamindari system was phased out at the time of Independence. Iversen, Palmer-Jones, and Sen (2013) claim that Banerjee and Iyer's coding consolidated nearly all the Central Provinces districts with Bengal and Bihar's more severe zamindari settlements, considering them all to be "landlord land". The Central Provinces, however, settled by Malguzari since 1863 introduced instead cadastral surveys and real statutory protection to three forms of land holder rights (occupancy rights, absoluteoccupancy rights and malik makbuza rights), which were more complex than a simple landlord. Iversen and associates re-lecoded the Central Provinces, using archival census records to arrive at the actual proportion of protected-tenant land in these areas, and six of the eight coefficients shown in the table were no longer statistically significant. If the Central Provinces were omitted from the analysis entirely, the whole finding vanished: the districts had been coded in error, and that miscoding was driving much of the published result. I have adopted the corrected reading, to treat Malguzari as a category all by itself as distinct from (and serving as an alternate to) a generic landlord system opposite Ryotwari. It is unlike either paper's district level cross-section covering multiple provinces, as it is a distance to boundary continuous test at fine resolution of the district level (taluka) this is a geographical discontinuity test not a cross sectional design.

This work is part of two other strands of colonial persistence literature. Dell and Olken (2020) make a close case for agriculture especially: within the cultivation-system boundaries set by the Dutch on Java, the cash-crop producing villages inside the boundary produce different manufacturing (and, by inference, living-standard) outcomes than those just outside (this is this paper's question, already answered once before, for a different crop and a different empire). Iyer (2010) takes up a different set of colonial institutions, that of direct versus indirectly British rule, and arrives at similar conclusions — worse development results today in directly ruled states than in ones ruled indirectly through princely states — but his argument is basically the same one, a choice made by the colonial administration in its day, that is still having measurable effects a century later.

### 2.2 Geographic Regression Discontinuity and Persistent Colonial-Era Effects

The best example of methodology found was that of Dell (2010). To date, the historically enforced Spanish system of forced labor on a pre-established list of districts located in Peru known as "mining mita" has created a discontinuity in household consumption and child stunting, which can be observed today through the use of a spatial regression-discontinuity design centered precisely on the old mita boundary with the distance between it included as a running variable. This is essentially done here: assessing if one discrete mappable historical fact or fact/place (the institution in question – not some sort of regional difference) either implies or produces a discontinuity as today, not comparing districts or states. Keele and Titiunik (2015) state the characteristics that must be true for a geographic boundary to be considered a valid regression-discontinuity design, and flag one issue taken seriously here: a boundary crossing varied terrain can easily mix a real institutional effect with natural geography that also changes across the line — which is why rainfall and elevation are built into the model as controls rather than added as an afterthought. More broadly, Michalopoulos and Papaioannou (2016) demonstrate the same design in a continent-wide sample: the colonial-era arbitrary borders across Africa have a measurable impact on development outcomes even today, when applied to one such border within one Indian region.

### 2.3 Remote-Sensing Detection of Cropping Pattern

The simple issue of agronomy on which this project is currently based is more straightforward than the fundamental physics. By measuring NDVI at the peak of the kharif (after the monsoon), while the canopy is fullest, and at the rabi/pre-harvest stage, the difference in the NDVI readings between the kharif and rabi becomes a direct measure of cropping pattern: a large negative value indicates single-cropped cotton, a small negative value indicates a cereal crop grown after the cotton crop. With this, real leaf optics are turned on — the natural reddish leave absorbs a lot of red light, while the cellular structure of the leaf scatters a lot of near-infrared light, and hence healthy, chlorophyll-rich canopy reads as large positive NDVI, the original formulation by Tucker (1979) and still the commonly used formula for converting that leaf-optic contrast into one comparable number. Here, the second channel was acquired is from the Landsat thermal band, where the bare ground or thin canopy are not the subject of this measurement, but they heat up more quickly and have less water than the dense transpiring canopy, so the land surface temperature and NDVI are physically connected, but they measure different things — the bare ground or thin canopy doesn't measure temperature the second time it's measured, but it does read as the heat at ground level.

## 3. Data and Methodology

### 3.1 Study Design

The talukas were present-day administrative geometry, with 120 talukas in the 11 districts of Vidarbha, and the raw material for a contemporary proxy of the historical Berar/Central Provinces boundary was obtained by dissolving these talukas into two distinct historical divisions, removing the shared edge from each division as a single line, and then verifying the line against district lineage from 1903 to 1956, rather than simply appearances of the boundary in maps. The immediate-boundary sample (32 talukas, split by division, and with a 25 km buffer zone) represents a very different group of suburbs, and these are used separately, in addition to representing the full sample of talukas, to test whether the bufferoverlap result is actually null or simply not powerful enough. Each outcome is analyzed using a spatial-discontinuity regression where the level jump in the outcome occurs directly at the boundary, and where the distance from the boundary has no effect on the outcome within the catchment, avoiding misattributing Vidarbha's actual west-drier/east-wetter gradient to some institutional effect.

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

This is the boundary made possible by a line-merge pass. This did not result in a topological issue, but merely resulted from the adjacent polygons of taluka in the two Divisions along the common edge not having the same vertex exactly at the edge — so cleanly did it remove to one line that this resulted in 256 disconnected line fragments in the line-merge pass; which finally in an exact pass yielded 1 line 384.7 km in length, running from the Akola/Amravati/Wardha corner in the north to the Yavatmal/Chandrapur corner in the south. A 25 km buffer divided by division resulted in the following discontinuity corridor: 7,387 km² of Berar talukas and 7,987 km² of Central Provinces talukas (32 out of Vidarbha's 120 talukas).

This was, indeed, an administrative proxy, and should be verified against the actual line, not assumed to be the same because of the geographical resemblance. Documented administrative history of each of the modern districts was followed up to 1903-1956, as there was no period map available, nor were the Imperial Gazetteer district maps and maps of Central Provinces and Berar for 1901-1931 found in accessible form. The historical districts of Berar (Amraoti, Akola, Ellichpur, Buldhana, Basim and Wun) map on to the modern Amravati Division, while Ellichpur was created as a taluka in Amravati district, Wun was renamed Yavatmal, and Basim was renamed Washim (folded into Akola district for some time but recreated as a district on 1 July 1998). The Nagpur Division of the Central Provinces (Nagpur, Bhandara, Chanda (renamed to Chandrapur) and Wardha, and later the internal divisions of Gondia and Gadchiroli) is also represented in present day Nagpur Division (Nagpur, Bhandara, Chandrapur, Wardha, Gondia, and Gadchiroli). The one real snag in the category is Balaghat, which went to the new (1956) Jabalpur Division of Madhya Pradesh, but which never belonged to the 11-district Vidarbha sample; and the other side of the boundary, the Central Provinces side here, is just a little smaller than the old division, because of the 1956 redrawing of states based on language, and not because of the Ryotwari or Malguzari. As can be gathered from the available records of district lineage, the modern line of division between the Amravati and Nagpur Divisions is the same line as the historical Berar/Central Provinces line of division.

![Figure 1](03_Data_Processed/Administrative/boundary_verification_map.png)

**Figure 1.** The two dissolved divisions, the 25 km discontinuity corridor over the taluka grid and the 384.7 km boundary line are indicated.

### 3.4 Outcome Variables

This analysis is carried out with 5 outcomes. The drop in NDVI within each taluka is indicative of Cotton-signature NDVI derived from the surface-reflectance bands (SR_B4 in Red and SR_B5 in near-infrared) of the Landsat 8/9 Collection 2 Level-2 data at three seasonal dates: kharif-peak and rabi/pre-harvest dates for 2025–26 and, as an independent replication, kharif-peak and rabi/pre-harvest dates for 2024–25. Second, a physically independent result, in addition to NDVI, is the land-surface temperature (LST) derived from the thermal band (ST_B10) of Landsat. Agrarian labour structure refers to the ratio of all agricultural labourers (main and marginal) to cultivators on the taluka level, which is the basic indicator for the absence of labour in Indian agrarian economy after aggregating the data from the Census of the villages at the taluka level. Prior to relying on the data, I found that the land use categories do not add up to 100% of the area a village reports at the village level: forest, non-agricultural use, barren/uncultivable, permanent pasture, misc. tree crops, cultivable waste, current and other fallow, net sown area. Cotton share and cotton holding size are both district-level averages, derived from the Area-Production-Yield workbook.

Even before these results could be believed, a pipeline bug came into light. The Landsat Collection 2 Level-2 thermal and reflectance bands have used digital number = 0 as a "fill" value for mask pixels (those that are cloud-masked and those that are off-swath) - these represent about one-third of each scene; an earlier processing step involves applying the Kelvin scale/offset directly to the raw DN (no masking of DN = 0). The broken output was displaying exactly 149 K, or -124.15°C, because there was a zero run through that formula, and the same bug was present in the reflectance pipeline as well, for the merged raster that was claiming 100% valid pixels when in reality the fill rate of the source scene was approximately 33%. The masking was done by setting DN = 0 to no-data prior to the scale/offset and everything was reprocessed from the raw scenes.

### 3.5 Spatial-Discontinuity Regression

Each outcome is specified using the same standard least squares model:

side + signed_dist_km + side×signed_dist_km + annual_total_mm + elevation_m ~ outcome

The questions are carried by two coefficient. Side is an indicator for the Berar/Ryotwari division which asks if the outcome is changing at the boundary; side×signed_dist_km asks a different question: does the outcome change differently with distance from the boundary on the two sides, even though there is no change at the boundary? The distance of each taluka's centroid from the dissolved boundary line which is measured in UTM 44N for Berar side (positive distance) is signed_dist_km, rainfall and elevation are used as controls. All outcomes were run twice, once on the 32-taluka corridor, and once on the full footprint of the satellite-scene (66 to 68 talukas, depending on which variables the footprint's coverage actually supports) to differentiate between an under-powered corridor result and a truly null result.

Elevation is based on SRTM 1 arc-second tiles with values sampled at each taluka centroid (194–497 m in the corridor, reasonably accurate for this part of the Deccan Plateau) and rainfall values are based on WorldClim 2.1 monthly precipitation climatology summed over each year and sampled at centroids. They are both long-term normalizing data and not the actual weather of the year or a fine-grained surface — WorldClim's ~18.5 km grid cell is bigger than most individual talukas, and this control is a long-term normalizing data.

### 3.6 Robustness Checks and Scope Decisions

To ensure that none of the corridors were playing too big a part in the results without anyone noticing, each of the interaction coefficients that came out to be significant was subjected to a leave-one-out jackknife: the model was refitted 32 times, one corridor taluka at a time, with the taluka being left out on each occasion. The full-footprint extension in Section 3.5 is a second type of robustness check, as it involves finding a result at one scale and then at a much larger one, with different power.

The two variables were not forced into the regression, but rather were eliminated from the regression. Irrigation coverage (calculated from the area_irri/net_area fields from the Census shapefiles) across sampled villages was 58-92% which is far off the mark from what is well documented - the cotton belt in Vidarbha is 15-20% irrigated in most villages. The units of the field are not clear to me, but they are definitely not reporting the irrigated to cultivated area, as their column names imply, so they were not reported as a number not trusted. There is no public dataset — anywhere, let alone at taluka level — for forest rights claims, for the distribution of forest rights titles, or for the community forest resource area, in Vidarbha; what little is available is scattered across the state-level administrative report, the report of the fact-finding committee in 2024, one solid taluka anchor in Gadchiroli, the regional total for Vidarbha, and a few individual village case studies, but the available sources have incompatible scales and are assembled here as a sourced, tagged table — every figure tagged with scope, value, unit, as-of date, and source — to avoid being forced onto a taluka-level panel that the public record does not support. This is not a regression variable, but rather a context piece of the discussion in the institutional-history section.

## 4. Results

### 4.1 Cotton-Signature NDVI: A Reproducible Regional Gradient, Vanishing at the Immediate Corridor

The mean NDVI change was observed as 0.325 for the Berar/Amravati Division side and 0.255 for the Central Provinces/Nagpur Division side in the full scene footprint (68 talukas) for the Berar/Amravati Division side. The spread was different too, with a higher standard deviation on the Central Provinces side (0.062 vs. 0.041), so the tale of a second crop is not uniform, but is a reality there. Remarkably, though, there was little difference between both sides, with the NDVI reaching almost the same value on both (Berar 0.66, Central Provinces 0.64); it is not the greenness of the land during the monsoon, but what happens to it afterwards.

In the previous year (64 of 68 talukas giving valid data in both years), the gap stood in isolation with Berar's score coming in at 0.316 while the Central Provinces' score was 0.241, a difference of 0.075 points.

![Figure 2](07_Outputs/seasonal_ndvi_signature.png)

**Figure 2.** Seasonal NDVI trajectory (kharif peak to rabi/pre-harvest) and kharif to rabi reduction, by division, year one.

![Figure 3](07_Outputs/year2_ndvi_comparison.png)

**Figure 3.** Independent annual cycles of NDVI reduction from kharif to rabi, on divisional basis.

But at the immediate level of the 25 km corridor, this gap almost disappears: 0.310 (Berar) vs. 0.299 (Central Provinces) in 29 talukas, barely distinguishable. The talukas situated in the corridor and within it in the central provinces (Wardha, Nagpur, Chandrapur) are also significant cotton producers and in fact the two sides are much the same at the boundary as they are everywhere in the province. This is not a lessened version of the regional result; this is a genuine discovery of the behavior of the boundary — a gradient which gets stronger as one moves further away from the historical boundary in either direction, instead of being focused right at the boundary.

![Figure 4](07_Outputs/lst_ndvi_corridor_comparison.png)

**Figure 4.** NDVI and land-surface-temperature maps and division boxplots, June 2026 single-date snapshot, corridor.

### 4.2 Agrarian Labor Structure, Land Use, and Cotton Dependency

The ratio of agricultural labourers to cultivators is 2.90 to 1 in Berar as compared to 1.96 to 1 on the Central Provinces side — this difference is evident in 32 talukas (15 in Berar and 17 in Central Provinces), and is more of a pattern throughout the area rather than due to a handful of outliers.

Even the active farmland is higher in Berar than in the neighbouring state – 68.9% as compared to 61.5%. Forest cover, however, is close to the same on both sides (12.5% vs 12.6%) – this particular corridor passes through a common farming area, and the Central Provinces' real and deep forests are much further east in Gadchiroli, outside this corridor.

The story of fallow or empty land is more circumspect: it is almost double the rate on the Central Provinces side (5.8% versus 3.3% in Berar) and is something that should be taken seriously, but not yet as a sign of economic distress, because the land can be left fallow for a normal crop rotation without any adverse effect.

The District-level numbers aren't easily divisible when it comes to cotton farming shares. Both Yavatmal (with 51% farmland under cotton) and Wardha (49% farmland under cotton) are almost tied up, with one being in Berar and the other in Central Provinces, while the latter is also followed by two other Central Provinces, namely Chandrapur (38%) and Nagpur (38%). Bhandara (0.15% cotton) and Gondia (0%) are much lower, but that's due to rice production, not the ancient border. It is obvious, however, that cotton did not stay within the confines of the old line; Wardha has a long history of cotton cultivation totally removed from the Berar's story.

A clearer line is drawn with Net sown area. The wide variation of percentages (SD 15.4) across the six Nagpur Division districts is marked in contrast to the tight cluster of 60–75% (SD 6.8) of the five Amravati Division districts. The Central Provinces reads as a combination of heavily-cultivated and heavily-forested districts, and this corresponds to the history of the region; as a result of the Ryotwari system, almost all land was brought under cultivation, while the Malguzari system left much under estate and forest management that was never really farmed.

There is, however, no significant difference between the average farm holding size at the corridor: Berar (1.81 hectares) and Central Provinces (1.90). This is just the opposite of what we could expect: that the word Ryotwari would be translated literally as smaller and more fragmented farms, and that is exactly what it is, a flat no-story farm.

![Figure 5](07_Outputs/population_agrarian_comparison.png)

**Figure 5.** Agricultural-laborer-to-cultivator ratio and literacy, by division, corridor talukas.

![Figure 6](07_Outputs/landuse_corridor_comparison.png)

**Figure 6.** Net cultivated area, fallow land, and forest cover, by division, corridor talukas.

![Figure 7](07_Outputs/agrarian_indicators_comparison.png)

**Figure 7.** Cotton share, net sown area, per-capita foodgrain production, and average holding size, all 11 districts.

![Figure 8](07_Outputs/precipitation_corridor_comparison.png)

**Figure 8.** Annual precipitation total and monsoon-season share, by division, district-wide and corridor.

### 4.3 Spatial-Discontinuity Regression: No Level Jump, a Real Slope Difference

These numbers are not moved by the old boundary, but by rainfall and elevation. In the NDVI-decline model, the rainfall variable had a p-value of 0.015, while elevation had a p-value of 0.002. rainfall variable had a p-value of 0.010 and elevation had a p-value of 0.006 in the agricultural-laborer ratio model; rainfall had a p-value of 0.046 and elevation had a p-value of 0.020 in the net-area model. It makes history in the region as no longer numbers in the west and high numbers in the east; the actual geography of Vidarbha swings the numbers around, so to speak, with drier, lower regions to the west and wettter, higher regions to the east. The control variables were able to identify exactly what they are designed to identify.

Given the backdrop, none of the four headline outcomes showed a real “side” off trend at the historical scale level along the 32-taluka corridor: kharif-to-rabi NDVI decline at p = 0.458; the agricultural-laborer ratio fell by the same amount, at p = 0.9601; net cultivated area had p = 0.577; land-surface temperature had p = 0.792 — everywhere, at the level of the historic scale.

![Figure 9](07_Outputs/phase4_discontinuity_plots.png)

**Figure 9.** The outcome is plotted against the distance to the boundary with fitted lines plotted by each side of the boundary; the corridor scale is plotted and there are four headline outcomes.

Finally, one of the numbers at the corridor scale was actually a surprising discovery: The coefficient of the interaction between "side" and "signed_dist_km" for the agricultural-laborer ratio was .0374, p = .0361; which is not a "jump at the line" discovery, but rather a changing interaction between side with distance from the border. The direction and approximate values of the coefficient were unaltered by our leave-out jackknife, the p-value was more vulnerable to the leave-out; with a few specific talukas dropped out (Amravati taluka, Seloo, Samudrapur, Narkhed, Korpana, Yavatmal taluka), the p-value ranged from 0.026 to 0.138, staying below 0.05 in 26 of 32 runs. Moving on – this was an adequate indication, not a certain answer.

With the larger foot-print (66-68 talukas, complete remote-sensing coverage of the entire satellite scene rather than census numbers which have gaps between the districts) it was a different picture with regard to NDVI decrease and land-surface temperature. The result remained non-significant for the level-jump term in both (declines in NDVI `side`: p = 0.821, LST `side`: p = 0.5123); similar to the corridor finding, no sharp level-jump was observed. At this larger scale, however, both satellite outcomes – NDVI decline interaction (p = 0.0348) and the LST interaction (p = 0.0105) – became significant; prior to this, none of the outcomes were significant, and the `signed_dist_km` interaction was overwhelmingly significant for both models (p < 0.001). A very tangible sense of point – a physical measurement hinting at two different shapes, at a sample with a good power indicates there is a gradient – the shape changes as you move away from the area of the old border.

![Figure 10](07_Outputs/phase4_fullfootprint_plots.png)

**Figure 10.** NDVI change vs distance-to-boundary and LST change vs distance-to-boundary, side-by-side (full footprint scale).

In the agricultural-laborer ratio, the level-jump term was significant (`side' coefficient 0.622, p = 0.014) and dropped to non-significant (p = 0.579) at the full footprint (67 talukas, after completing the population and land-use processing for Bhandara and Gondia); almost a reverse trend from the corridor result. The flip isn't really a contradiction, it's just an illustration as to how disproportionate this particular satellite footprint is: only one district of Berar just fits into this frame: Amravati while the Central Provinces side reaches out over 160 kms to Bhandara and Gondia. Obviously, one side cannot show a proper slope, so for the interaction's results, a small jump near the edge is probably more of a reading of what is going on at that point, than what they actually think is a legitimate “trend difference”. When a jump runs across the whole area it is a better indication of an area trend difference, which is why the “trend difference” result is being believed more on the smaller corridor here than on the full-footprint jump, which is of a different interpretation. Net cultivated area, of course, remained unchanged and saw no significant change on either scale (corridor p = 0.577, the full footprint p = 0.121).

![Figure 11](07_Outputs/phase4_fullfootprint_all4_plots.png)

**Figure 11.** All four full-footprint outcomes (NDVI decline, LST, agricultural-laborer ratio, net cultivated area) vs. distance-to-boundary, fitted lines by side.

## 5. Discussion

That's the bottom line here, and in a way the line across Berar/Central Provinces doesn't exist: it's actually a significant missing point. In all four outcomes tested (cotton-signature NDVI, agrarian labor structure, net cultivated area, land-surface temperature), with both small-corridor and larger regional perspective data sets, when rainfall and the topography are controlled for, there was no statistically significant "spike" at the line. That null result isn't here a design fault; it is simply that no trace of this old frontier could be seen here except as a sharp edge, and a report of a jump where one does not exist would have been worse.

The data do indicate a true gradient. The main signature here for cotton monoculture was the NDVI decline between the kharif and rabi seasons which was confirmed independently across two separate years (0.070 points and 0.075 points, respectively) and reduced to almost nil at the very border, as the talukas of the Central Provinces in the immediate vicinity also grow significant amounts of cotton. The side-by-distance interaction is significant for both land-surface temperature as well as for decrease of NDVI at the whole-footprint scale — two completely different physical measurements are obtained on the same trend in a single channel thus adding credibility, not coincidence.

When this is assembled, it is clear story: the institutional legacy transcends the geographic province boundary, with the core province in each of the old provinces presenting a type of institution and the edges showing some overlapping. This is a falsifiable claim, and a more believable one than a sharp drop on a border erased 150 years ago — it also fits with Iversen et al.'s (2013) recoding of the Central Provinces as a mixed system with real tenant protection rather than just big landlords everywhere, a tenure system with genuine differences on the inside, which is exactly where the slow gradient shows up.

The 2 slopes match in all other places except the agricultural-labourer numbers where the slope differs; and a level jump at the full footprint. The results across the two kinds of scales may be bound up with a mismatch between the physical historical geography and the two sides inside this modern satellite-based frame, rather than a straightforward reflection of the distance between the two institutional geographies. In both cases the numbers are reported here rather than the easier of the two to pick up, for reasons explained below: The smaller corridor numbers are more likely to be trusted, because within the paper's field of interest of determining the direction of an object on the boundary, they remain closer to the original “right at the boundary” question the paper sought to address.

## 6. Limitations

### 6.1 Sample Size at the Corridor Scale

The 32 taluka corridor really cannot detect anything but a large and sharp jump. The directions were pretty consistent after the jack knife test in Section 4.3 with the directions of the significance numbers fluctuated by a lot for each taluka dropped, which, as difficult as it is to deal with at this scale, is not something to be swept off the counter top.

### 6.2 Rainfall as a Long-Term Climatology, Not a Time Series

The rainfall data of WorldClim is based on a long term average rainfall from several decades of analysis over a relatively coarse grid with width of 18.5km which is greater than most Talukas. It only acts as a first order control over the regional rainfall as a whole and cannot explain interannual variations or details within the taluka boundaries.

### 6.3 Full-Footprint Sample Asymmetry

The path and row positioning of the satellite (WRS-2 path 144, rows 045/046) is used to expand the data fields of NDVI, LST, and agricultural-laborer; they are not dependent on the position in which the historical provinces ended. As the labor-ratio results in section 4.3 demonstrated, this creates a side of the border that is either much shorter or longer distance range than the other, making a comparison at different scales of a level jump versus a slope difference involve a really ugly exercise.

### 6.4 Irrigation Data Dropped as Untrustworthy

These were not the numbers with certainty to be confused with the geography of cotton that had been observed by the Census, so the variable was not reported even after giving it serious consideration. However, a more useful study would have used the information on irrigation from the state agriculture department.

### 6.5 FRA Data as Narrative, Not Quantitative Evidence

There is no online cleaning and steady data on Forest Rights Act at taluks/districts level for Vidarbha area. The statistics in Section 3.6 are dispersed across incompatible scales and dates and therefore are not included in the primary statistical tests, but are included here as institutional-history context.

### 6.6 Ground-Truth Verification, With A Caveat On Scale

In fact, a study, which relied entirely on satellite and census data was checked for accuracy by seven actual field boundaries in the villages of Karanja Ghadge and Sawardoh, in the corridor area of Wardha district on the old Central Provinces/Malguzari side. On the date of each instance, both of the corresponding ground photos of the Karanja Ghadge fields showed the crop leaves like those predicted by the NDVI numbers, healthy, not stressed and of closed canopy, while all the GPS coordinates in the karanja ghadhes were over the same set of fields from the same family with a different family field-monitoring project on those very coordinates. These values are comparable to the NDVI, LST, and valid pixel percentages of a basic June 2026 taluka level map displayed in the mask at the Landsat level.

But the caveat with the scale is the point. This is not an exact pixel for pixel match, the 30 m blocks from the Landsat image are averaged all together, the field numbers are in sharper 10 m image from Sentinel-2 on exactly the polygon and they are almost entirely from different days. The idea of this check is to determine that the same type of greenness signal will appear when the land is studied in greater detail, not that the two numbers should be exactly the same to 3 decimal places. Ground Truth info and a complete breakdown of it is on the Ground Truth page of the dashboard.

### 6.7 A Historical-Lineage Verification, Not a Literal Map Overlay

Because of the lack of an old map (the best one could be found was a map from 1903) that could be digitized in modern coordinates, the historical accuracy of the border in Section 3.3 is based on documented district administrative lineage from 1903 to 1956, rather than relying on an old map. While answers provided by the lineage approach were what this project was looking for, a true period map would enrich any future visual presentation of the events of the boundary's history.

## 7. Future Work

This would solve the current two satellite scene-geometry asymmetry (Section 6.3), and provide a fair and equal distance range on either historical province when considering the remaining scenes in the entire Landsat archive to cover all 11 Vidarbha districts.

Expanding the extent of population and land-use coverage across to all 11 districts. Presently, the agricultural-laborer ratio and the number of lands used is available for just 8 out of 11 districts and the data for the remaining 3 (Gadchiroli work has already started but data is not part of the current NDVI/LST scene) needs to be found and processed in order to allow the tests to be performed across the entire region on a truly comparable scale.

A historical boundary map with digitized boundaries. A digital copy of the map or administrative atlas in an old Imperial Gazetteer document for the Central Provinces and Berar would allow the contemporary boundary to be imposed on top of a boundary that has been verified by looking at the lines of descent.

## 8. Conclusion

The boundary itself was set up around 1853 when Berar came under the British administration, and administrative lineage records have been written from the Berar/Central Provinces border from 1903 to 1956 (as far as these records go, the modern map line corresponds to the old one set up by the British in Berar). There is no statistically significant break in cotton-signature NDVI, agrarian labor force structure, land use or land-surface temperature exactly on that 150-year-forgot border when we take into account the two factors that are known to affect the continental equation: rain and elevation, at either the 25-kilometer-long corridor level or the regional footprint as a whole — and no alarming but less-important weak/creeping border effect claimed by slight changes in the NDVI land covers.

Instead it was found that there was a genuine regional gradient of cotton-signature NDVI, which was ascertained over two years of data, and which deepened away from the historical line, rather than focussing at the edge; both sides of the edge showed the same trend in the cotton-signature NDVI in both years and two different physically independent Earth-observation channels. The same story told more qualified is being provided by the agricultural-laborer-to-cultivator ratio too – a slope difference, right on the edges, stable in direction under jackknife testing but not strong enough against removing certain talukas, changes shape at that bigger footprint created by a structurally lopsided satellite view.

The truthful final statement will then be that there is indeed an institutional-geography legacy that can be detected on the land, but that is not a neatly defined effect at the old line — but rather a one in which the legacy is a gradient with the old line of the Vidarbha region instead of a 'hard' boundary akin to that effect confirmed at the old line. Finally, at Karanja Ghadge and Sawardoh villages, the satellite NDVI signal on which this project operates performs well even when scaled, relative to real canopy by the crop at seven field boundaries described here and checked at these locations for NDVI this season.

## References

Baden-Powell, B. H. (1892). *The Land-Systems of British India: Being a Manual of the Land-Tenures and of the Systems of Land-Revenue Administration Prevalent in the Several Provinces* (3 vols.). Oxford: Clarendon Press.

Banerjee, A. V., & Iyer, L. (2005). [History, institutions, and economic performance: The legacy of colonial land tenure systems in India](https://www.aeaweb.org/articles?id=10.1257/0002828054825574). *American Economic Review*, 95(4), 1190–1213.

Beckert, S. (2014). *[Empire of Cotton: A Global History](https://www.penguinrandomhouse.com/books/10461/empire-of-cotton-by-sven-beckert/)*. Knopf.

Dell, M. (2010). [The persistent effects of Peru's mining mita](https://onlinelibrary.wiley.com/doi/10.3982/ECTA8121). *Econometrica*, 78(6), 1863–1903.

Dell, M., & Olken, B. A. (2020). [The development effects of the extractive colonial economy: The Dutch cultivation system in Java](https://academic.oup.com/restud/article/87/1/164/5490392). *Review of Economic Studies*, 87(1), 164–203.

Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., Seal, D., Shaffer, S., Shimada, J., Umland, J., Werner, M., Oskin, M., Burbank, D., & Alsdorf, D. (2007). [The Shuttle Radar Topography Mission](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005rg000183). *Reviews of Geophysics*, 45(2), RG2004.

Fick, S. E., & Hijmans, R. J. (2017). [WorldClim 2: New 1-km spatial resolution climate surfaces for global land areas](https://rmets.onlinelibrary.wiley.com/doi/10.1002/joc.5086). *International Journal of Climatology*, 37(12), 4302–4315.

Iversen, V., Palmer-Jones, R., & Sen, K. (2013). [On the colonial origins of agricultural development in India: A re-examination of Banerjee and Iyer, "History, institutions and economic performance"](https://www.tandfonline.com/doi/abs/10.1080/00220388.2013.807502). *Journal of Development Studies*, 49(12), 1631–1646.

Iyer, L. (2010). [Direct versus indirect colonial rule in India: Long-term consequences](https://direct.mit.edu/rest/article/92/4/693/57986). *Review of Economics and Statistics*, 92(4), 693–713.

Keele, L. J., & Titiunik, R. (2015). [Geographic boundaries as regression discontinuities](https://www.cambridge.org/core/journals/political-analysis/article/geographic-boundaries-as-regression-discontinuities/2A59F3077F49AD2B908B531F6E458430). *Political Analysis*, 23(1), 127–155.

Maharashtra State Tribal Development Department. (2021). *[Administrative Report 2020-21](https://tribal.maharashtra.gov.in/Site/Upload/GR/Administrative%20Report%2020-21%20Final%2017092024.pdf)*. Government of Maharashtra. [Forest Rights Act compilation, Section 3.6]

Michalopoulos, S., & Papaioannou, E. (2016). [The long-run effects of the scramble for Africa](https://www.aeaweb.org/articles?id=10.1257/aer.20131311). *American Economic Review*, 106(7), 1802–1848.

Mishra, S. (2006). [Farmers' suicides in Maharashtra](https://www.epw.in/journal/2006/16/special-articles/farmers-suicides-maharashtra.html). *Economic and Political Weekly*, 41(16), 1538–1545.

Mohanty, B. B. (2005). ['We are like the living dead': Farmer suicides in Maharashtra, western India](https://www.tandfonline.com/doi/abs/10.1080/0306615042000322935). *The Journal of Peasant Studies*, 32(2), 243–276.

Roy, T. (2011). *The Economic History of India, 1857–1947* (3rd ed.). New Delhi: Oxford University Press.

Tucker, C. J. (1979). [Red and photographic infrared linear combinations for monitoring vegetation](https://www.sciencedirect.com/science/article/abs/pii/0034425779900130). *Remote Sensing of Environment*, 8(2), 127–150.

U.S. Geological Survey. *[Landsat 8-9 OLI/TIRS Collection 2 Level-2 Science Products](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-9-olitirs-collection-2-level-2)*. Earth Resources Observation and Science (EROS) Center.

Government of Maharashtra. (2026). *[Economic Survey of Maharashtra 2025-26](https://mahades.maharashtra.gov.in/home.do?lang=en)*, Chapter 7 (Agriculture). Commissionerate of Agriculture.

Government of Maharashtra. (1994, April 30). *[The Development Boards for Vidarbha, Marathwada and the Rest of Maharashtra Order, 1994](https://indiankanoon.org/doc/11824594/)*, Notification No. GS/G/94/DB/432, issued under Article 371(2) of the Constitution of India.
