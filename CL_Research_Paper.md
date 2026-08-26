# The Cotton Line: Testing the Institutional Persistence of an Erased Colonial Land-Tenure Boundary Across Vidarbha's Agrarian and Vegetation Geography

**Sakshi D. Maske**
Independent Geospatial Researcher

## Abstract

The British took control of the Berar region in 1853, and at that time, Berar consisted of Amravati, Akola, Buldhana, Washim, and Yavatmal districts. There, they introduced and enforced a new system of land tenure named the “Ryotwari system” to manage and settle the land. The British pressurized the Berar region to produce more cotton when the supply of cotton from America stopped reaching Lancashire during the American Civil War, and they eventually turned Berar into a cotton-producing region on a monoculture basis. In contrast to this, the six districts which were to the east of Berar (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli) were the backbone of the Central Provinces. And in this region, there was a different system of land settlement named “Malguzari.” So, this administrative boundary was officially discontinued in 1956, but still, as of today, this matches the modern boundary between Amravati Division and Nagpur Division. The main question of this research paper is: Does this 150-year-old institutional line still remain measurable today in the form of a spatial signature, specifically in vegetation phenology (cotton signatures), agrarian labor structure, land use, and land surface temperature? And its design is not something like a before/after comparison or synthetic control comparison. This is actually a spatial discontinuity test to check whether I can still notice a measurable difference spatially across this historical administrative line.

I constructed a 384.7 km modern boundary, for which I dissolved 120 talukas into their two historical divisions. Then, by using the common edges and boundaries of these talukas, I defined the boundary. I compared this result to the documented district lineage of 1903–56 rather than assuming that it matched the historical boundary due to similar geography. I tested the kharif-to-rabi NDVI decline signature across two independent annual cycles. I got a difference of 0.070 in year one between Berar and the Central Provinces: 0.325 for Berar versus 0.255 for the Central Provinces, with a total of 68 talukas. I re-ran the test in year two with a completely separate set of scenes, and the result was almost exactly the same. The difference was 0.074, where Berar was 0.316 and Central Provinces was 0.241. So, this was not just a result from one unusual year. The same seasonal pattern appeared repeatedly in two different annual cycles. And honestly, this consistency is what convinced me that this is a real, stable seasonal signature.


So, by using spatial-discontinuity regression (`outcome ~ side + signed_dist_km + side×signed_dist_km + rainfall + elevation`), I did analysis on the 32-taluka immediate-boundary corridor and on the full 66–68-taluka scene footprint. And no significant level jump was detected on the historical line for any outcome at any scale. But this analysis identified a significant side×distance interaction on the full-footprint case for both Earth-observation outcomes: NDVI decline (p = 0.0348) and land-surface temperature (p = 0.0105). And this indicates that both sides follow different curves/trends while moving away from the old boundary. But a sharp drop/jump doesn't happen at the boundary on either side. The agricultural-laborer-to-cultivator ratio showed a similar slope difference at the corridor scale (p = 0.0361), and its direction was consistent in all 32 leave-one-out jackknife runs. But at the full-footprint scale, this slope difference flips into a level jump (p = 0.014). This difference in the slope is not some kind of contradiction in the underlying story; instead, the reason behind this is that the territory from both sides is not equal inside the satellite scene; it means they are lopsided. And if I look at these results from a combined lens, it suggests that there is no sudden institutional change at the old Berar/Central Provinces border. It refers to something quieter: a true gradient that increases as you move away from the boundary, not a “jump” at the boundary. And I honestly think that this result is more authentic than expecting a perfect/pristine discontinuity, even if it is not exciting. In order to substantiate the underlying NDVI signal, I conducted a field ground-truth check on Karanja Ghadge and Sawardoh villages of Wardha district against another field-monitoring project carried out on the same land, and the underlying NDVI signal corresponded with the actual crop canopy at the seven real field boundaries (with the scale caveat it deserves, not that it is a bigger claim than it is).

**Keywords:** institutional persistence, colonial land tenure, Ryotwari, Malguzari, spatial discontinuity, boundary persistence, NDVI phenology, Vidarbha, remote sensing

---

## 1. Introduction

Vidarbha's farmer-distress geography is usually explained in terms of rainfall, market prices, or crop selection. I wanted to see if something else was still left in the land — whether the 1853 British annexation of Berar and the Ryotwari land-tenure system introduced to supply cotton to Lancashire mills left any imprint on this land that did not completely disappear through the decades since India's Independence. Berar’s five districts (Amravati, Akola, Buldhana, Washim, and Yavatmal) were settled under the Ryotwari, under which the colonial state used to directly deal with the individual cultivator or ryot, who had formal, individually titled rights on a specific plot of land. The six Central Provinces districts to the east (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli) were settled under Malguzari by 1863, in which land was recorded in the name of an intermediary landholder, and he was responsible for the entire estate rather than individual cultivators (Iversen, Palmer-Jones, & Sen, 2013). These two settlement types, and the difference between them, are laid out in the original colonial land-revenue record itself (Baden-Powell, 1892).

This administrative boundary was officially dismantled in 1956 when India's internal borders were restructured on linguistic grounds. But still, as of today, this follows the same boundary which is between the Amravati Division and Nagpur Division, which I already had as taluka geometry. And this traces two more important things closely, which are worth noting in the start itself. One is the 1900 Berar famine geography, in which approximately 8.5% of the population died, and the biggest impact was seen in those districts which were specialised in cotton (Beckert, 2014) — Berar's push into cotton monoculture was part of a much larger pattern across colonial India, where cash-crop specialization for export reshaped agrarian regions well beyond just this one boundary (Roy, 2011). The second one is the modern period’s agrarian distress geography — Vidarbha region, which is still worst in the same western districts today, a disparity persistent enough that the state government set up a standing statutory board for the region under Article 371(2) (Government of Maharashtra, 1994). This isn't a new observation either — the farmer-suicide crisis concentrated in exactly these western Vidarbha cotton districts has been documented for two decades now (Mohanty, 2005; Mishra, 2006), which is part of why I wanted to test whether it traces back to something this specific and this old.

I am not going to ask the question whether it is colonialism which is behind the agrarian distress of Vidarbha because this is too broad a question to test properly. The narrow and the falsifiable version of it is whether the historical Berar/Central Provinces boundary is still measurable as of today in the form of spatial discontinuity, specifically in cotton-signature vegetation phenology, agrarian labor structure, land use, and land surface temperature, once the effects of distance-to-boundary, rainfall, and elevation are controlled for. This is not a part of some kind of policy evaluation, nor is it a before/after test of a specific intervention. Here, the question is whether the signature of one erased administrative geography is still present on the land even today, which is closer to landscape pattern analysis and historical GIS when compared to treatment-effect estimation, and whether this signature can be validated by combining Earth-observation and census data rather than being assumed from the history alone.


Three questions follow from that. First, does the cotton-signature NDVI, which represents the size of a taluka's kharif-to-rabi vegetation decline, a monoculture-vs-mixed-cropping signature, show a jump at the historical line once geography is controlled for?

Second, is there a similar pattern in the agrarian labor structure, meaning the proportion of agricultural laborers when compared to the cultivators, and does this pattern remain consistent in both the immediate corridor and wider regional coverage?

Third, is the modern administrative boundary actually the same line as the historical Berar/Central Provinces boundary, verified against documented district lineage rather than assumed?


## 2. Literature Review

### 2.1 Institutional Persistence and Colonial Land Tenure in India

One of the clearest empirical precedents for this project is Banerjee and Iyer (2005). They showed us that agricultural investment and productivity are significantly worse even today in those districts of India which were historically settled under landlord-based (zamindari) revenue systems than in districts settled under non-landlord (ryotwari or mahalwari) systems. Even though these tenure systems were abolished during the time of Independence, this gap still survives after more than a century. They classified the historical tenure type of every district from the colonial settlement records and then compared the present-day outcomes on the basis of the resulting split. I adapted this logic for the geographically contiguous line rather than British India's scattered districts. This changes the nature of the test.

Their classification is not uncontested, and interestingly, this dispute is exactly related to that territory which I am studying. Iversen, Palmer-Jones, and Sen (2013) argue that in Banerjee and Iyer’s original coding, almost all the Central Provinces districts were grouped together with Bengal and Bihar’s harsher zamindari settlements. It means the entire province was treated like landlord land. But in the Central Provinces, where there was Malguzari settlement from 1863, the settlement came with cadastral surveys and real statutory protection for 3 classes of tenants: occupancy, absolute-occupancy, and malik makbuza rights — which was a more mixed system than a pure landlord system. When Iversen and his colleagues recoded the Central Provinces using archival settlement records so that the actual proportion of the protected-tenant land gets reflected, 6 of Banerjee and Iyer’s 8 headline coefficients lost their significance. And when the Central Provinces were completely removed from the sample, the entire result disappeared. It means those districts were coded wrong, driving the major part of the published finding. I followed the corrected reading here rather than the original reading. In the entire paper, I treated Malguzari as a separate, distinct category rather than folding it into a generic landlord system as opposed to Ryotwari. The difference between this project and both papers is that I am using a continuous distance-to-boundary variable at a fine spatial resolution (taluka level), not a district-level cross-section spanning multiple provinces. It is more of a geographic discontinuity test than either of the papers' original cross-sectional designs.

This project also sits next to two other strands of the same colonial-persistence literature. Iyer (2010) finds that areas under direct British colonial rule in India show worse development outcomes today than areas left under indirect rule through princely states — a different axis of colonial institution (direct vs. indirect rule) than the tenure-type axis Banerjee and Iyer look at, but the same basic logic: a colonial-era administrative choice, not just geography, doing measurable work a century later. Dell and Olken (2020) make an even closer case for agriculture specifically — villages inside the Dutch colonial cultivation-system boundary in Java, where the Dutch forced a very Malguzari-like intermediary system to extract cash-crop production, still show different manufacturing and living-standard outcomes today than villages just outside it. That's essentially this same paper's question — does a colonial cash-crop institution leave a boundary-shaped mark — already answered once for a different crop and a different empire.


### 2.2 Geographic Regression Discontinuity and Persistent Colonial-Era Effects

Dell (2010) is the closest methodological model for my project. She showed us that mining mita, which was a kind of forced labor system that Spain imposed on a fixed set of districts in Peru from 1573 to 1812, still produces statistically significant discontinuity in household consumption and child stunting today. This discontinuity was detected using a spatial regression-discontinuity design which was directly centered on the old mita boundary and used the distance from that boundary as a running variable. This is basically the exact approach I used here: testing whether a specific mappable historical institution, and not some kind of vague regional difference, leaves any kind of present-day discontinuity, and for this using distance from a line rather than district or state comparison. Keele and Titiunik (2015) explain what conditions are needed to be satisfied for a geographic boundary to function in the form of a valid regression-discontinuity design, and they also pointed out one important issue which I considered seriously here. A boundary which passes through a variety of terrain can easily mix a real institutional effect with natural geography that also changes across that line, and due to this reason, rainfall and elevation are included as controls in this model and not something which was added later as an afterthought. Michalopoulos and Papaioannou (2016) show the same design working at a much bigger scale — the arbitrary partition lines colonial powers drew across Africa still split ethnic homelands into measurably different development outcomes today, which is the same claim I'm testing here, just at the scale of one boundary inside one Indian region instead of a whole continent.

### 2.3 Remote-Sensing Detection of Cropping Pattern

NDVI comes from real leaf optics, which means chlorophyll strongly absorbs the red light while the internal cell structure of a leaf heavily scatters near-infrared light, and that's why healthy, chlorophyll-rich canopy reads in the form of large positive NDVI — this is the original vegetation index formulation from Tucker (1979), and it's still the standard way to turn that leaf-optics contrast into one comparable number. The agronomic fact which I am actually relying on is much simpler than the physics. A single-cropped field returns to bare/fallow soil after one crop harvest, whereas a mixed-cropped field gets sown again and remains green. If one measures NDVI at a kharif peak just after the monsoon, when the canopy is at its fullest, and then measures it again during the rabi/pre-harvest point, then the gap between the two gives the direct indication of the cropping pattern. A bigger kharif-to-rabi decline indicates single-crop cotton, whereas a smaller decline indicates that something followed it. The second channel which I used is land surface temperature, which comes from Landsat's thermal band. Bare or sparsely vegetated soil heats much faster and holds less moisture when compared to dense, transpiring canopy, and that's why LST and NDVI are physically connected, but they are not measuring the same thing twice. NDVI tells us what is growing, whereas LST tells us how it appears in the form of surface heat.

## 3. Data and Methodology

### 3.1 Study Design

I built a modern proxy of the historical Berar/Central Provinces boundary by using present-day taluka administrative geometry (120 talukas across Vidarbha's 11 districts). I dissolved the talukas into two historical divisions and created one continuous line by extracting their shared edge. Then I checked it against district lineage documented in 1903–1956 rather than just trusting it because it appeared to be completely fine (Section 3.3). A 25 km buffer corridor, which was split on the basis of division, defines an immediate-boundary sample in which there are 32 talukas. The same outcomes are separately tested at the full satellite-scene footprint (66–68 talukas depending on data availability) to see whether the corridor test is just underpowered or is genuinely finding nothing. Every outcome was run through a spatial-discontinuity regression, which separates a level jump directly at the boundary from a difference in slope with distance from the boundary. Rainfall and elevation were controlled throughout the analysis so that Vidarbha's actual west-drier/east-wetter gradient is not mistaken for an institutional effect.

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

I split the 120-taluka administrative layer into two historical zones on the basis of the district: Amravati Division (Akola, Amravati, Buldhana, Washim, Yavatmal), which represents Berar/Ryotwari territory, and Nagpur Division (Nagpur, Wardha, Bhandara, Gondia, Chandrapur, Gadchiroli), which represents Central Provinces/Malguzari territory. Then I dissolved both into one polygon each and extracted a shared edge between them. In the first pass, I got 256 disconnected line fragments, which happened just because adjacent taluka polygons didn't share exact vertices along their common edge. This wasn't some kind of topological problem. A line-merge pass collapsed it cleanly into one continuous 384.7 km line, which runs from the Akola/Amravati/Wardha corner in the north to the Yavatmal/Chandrapur corner in the south. A 25 km buffer split on the basis of division gives just a discontinuity corridor: 7,387 km² on the Berar side and 7,987 km² on the Central Provinces side, containing 32 talukas out of the total 120 talukas of Vidarbha.

This is a present-day administrative proxy, and I wanted to check it against the actual historical line rather than just assuming that these two match exactly just because the geography is similar. I didn't get any digitized period map. I did search for Imperial Gazetteer district maps of 1901–1931 and Central Provinces and Berar administrative atlases, but I didn't get them in an accessible form. That's why I traced the documented administrative lineage of every modern district back through 1903–1956 instead. Berar Division's historical districts (Amraoti, Akola, Ellichpur, Buldhana, Basim, Wun) cleanly map onto the modern Amravati Division. Ellichpur was absorbed into the Amravati district in the form of a taluka. Wun was renamed Yavatmal, and Basim was renamed Washim (folded into Akola for some period of time, then recreated as a separate district on 1 July 1998). Nagpur Division of the Central Provinces, that is, Nagpur, Bhandara, Chanda (renamed Chandrapur), Wardha and Balaghat, similarly maps onto the modern Nagpur Division, in which Gondia, which was split in 1999 from Bhandara, and Gadchiroli, which was split in 1982 from Chandrapur, were the later internal subdivisions of the same territory. The one real wrinkle is Balaghat, which went into Madhya Pradesh's Jabalpur Division in 1956 after States Reorganisation on the linguistic basis, whereas the remaining portion of the old Nagpur Division went into Bombay State and then into Maharashtra in 1960. From the start, Balaghat was never part of my 11-district Vidarbha sample. That's why no fix was needed in the boundary that I built first, but this means that my Central Provinces side is a little smaller than the full extent of the historical division, and this gap is due to the language-based state redraw of 1956 and not because of Ryotwari or Malguzari. With this caveat, the modern Amravati/Nagpur Division line is, as far as documented district lineage can show, the same line as the historical Berar/Central Provinces boundary.

![Figure 1](03_Data_Processed/Administrative/boundary_verification_map.png)

**Figure 1.** The two dissolved divisions, the 384.7 km boundary line, and the 25 km discontinuity corridor shown over the taluka grid.

### 3.4 Outcome Variables

Cotton-signature NDVI — derived from the surface-reflectance bands SR_B4 (red) and SR_B5 (near-infrared) of the Landsat 8/9 Collection 2 Level-2 data at three seasonal times in two independent annual cycles (kharif-peak and rabi/pre-harvest dates for 2025–26 and, as an independent replication, 2024–25). The result is the drop in NDVI observed in each taluka between kharif and rabi.

Land-surface temperature — Landsat’s thermal band (ST_B10), which was converted into Celsius, was used with NDVI in the form of a second and physically independent outcome.

Agrarian labor structure — the ratio of agricultural laborers (main and marginal workers combined) to cultivators, which was calculated by aggregating the village-level Census data to the taluka level. This is the standard landlessness indicator in the Indian agrarian economy.

Land use — nine-category breakdown at the village level (forest, non-agricultural use, barren/uncultivable, permanent pasture, misc. tree crops, cultivable waste, current and other fallow, net sown area). Before trusting the dataset blindly, I checked whether these nine categories actually sum to 99–100% of the recorded area of every village.

Cotton share and holding size — share of district-level cotton area in the total cropped area and average operational landholding size, both obtained from the Area-Production-Yield workbook.

Before trusting all these results, I found and fixed a pipeline bug. Landsat Collection 2 Level-2 thermal and reflectance bands use digital number (DN) = 0 as a fill value for cloud-masked and off-swath pixels — roughly one-third of every scene. In an earlier processing step, I applied the Kelvin scale/offset directly to the raw DN without first masking DN = 0. When 0 goes through that formula, it gives exactly 149 K, or −124.15°C — which is not a real temperature anywhere on Earth, and this was exactly the floor value that the broken output was showing. The same bug, unmasked fill pixels, was also present in the reflectance pipeline: a merged raster was showing 100% valid pixels, while the actual fill rate in the source scene was around 33%. I fixed both by masking DN = 0 as no-data before applying the scale/offset, and then reprocessed everything from the raw scenes.

### 3.5 Spatial-Discontinuity Regression

Every outcome was run through the same ordinary least squares specification.

outcome ~ side + signed_dist_km + side×signed_dist_km + annual_total_mm + elevation_m

Side is an indicator for the Berar/Ryotwari division. Signed_dist_km is a distance from the dissolved boundary line for the centroid of every taluka, which was calculated in UTM 44N, and a positive sign was given to the Berar side. Rainfall and elevation are the controls. Side coefficient is the actual question — does the outcome directly jump at the boundary. Side×signed_dist_km interaction checks a different thing: does the outcome change differently with distance from the boundary on the two sides, even without a jump at the boundary. Wherever the data was available, I ran it two times for every outcome. One time on the 32 taluka corridor and one time on the full satellite scene footprint (66–68 talukas, depending on what variables are actually supported by the footprint's coverage), so that I can check whether the corridor's result came out because it was underpowered or because it was actually null.

Elevation has been taken from SRTM 1 arc-second tiles and sampled at every taluka centroid (in the corridor 194–497 m, it is roughly accurate for this stretch of the Deccan Plateau). Rainfall data was taken from the WorldClim 2.1 monthly precipitation climatology and summed into an annual total by sampling at centroids. Both are long-term normals and not a specific year's actual weather or a fine-grained surface. WorldClim's ~18.5 km grid cell is bigger than most of the individual talukas, so this control establishes the regional gradient, not taluka-by-taluka precision.

### 3.6 Robustness Checks and Scope Decisions

I ran a leave-one-out jackknife on every interaction coefficient which came out significant, in which the model was refitted 32 times and every time one corridor taluka was dropped out, in order to ensure that no single taluka quietly drove the result on its own. The full-footprint extension in Section 3.5 works with the same spirit in the form of a second robustness check — does a result found at one scale also hold in the same direction in a much larger sample with different power.

Two things were completely scoped out of the regression instead of forcing them on shaky ground. Irrigation coverage, which was calculated from the Census shapefiles' area_irri/net_area fields, came out to be 58-92% on the sampled villages, which is completely inconsistent with the well-documented reality that Vidarbha's cotton belt is 15-20% irrigated at max. Whatever these fields actually measure, they are not clearly showing irrigated versus cultivated area as their column names suggest, so I dropped them instead of reporting a number I don't trust. For Vidarbha, there is no clean taluka-level or even consistent district-level public dataset available for Forest Rights Act recognition, that is, claims filed, titles distributed, community forest resource area. Some scattered reliable datasets which I got my hands on are: a state-level administrative report, a 2024 fact-finding committee report, one genuinely solid district anchor (Gadchiroli), a regional Vidarbha-wide total, and some individual village case studies, all at incompatible scales. I have compiled this in the form of a sourced, tagged table. I have tagged every figure with scope, value, unit, as-of date, and source, rather than forcing it onto the taluka-level panel that the public record simply doesn't support. Here in the discussion, this appears in the form of institutional-history context and not as a regression variable.

## 4. Results

### 4.1 Cotton-Signature NDVI: A Reproducible Regional Gradient, Vanishing at the Immediate Corridor

In the full scene footprint (68 talukas), on the Berar/Amravati Division side, the mean kharif-to-rabi NDVI decline came out as 0.325 whereas it was 0.255 on the Central Provinces/Nagpur Division side. It means there was a gap of 0.070 points. Also, there was a larger spread on the Central Provinces side (std. dev. 0.062 vs. 0.041), so the "some fields get a second crop" story is real there but uneven, not uniform. The NDVI peak was almost the same for both sides (Berar 0.66, Central Provinces 0.64). The difference does not lie in how green the land is during the monsoon, it lies in what happens to it afterward.

The gap held up independently a year earlier, too: in kharif 2024/rabi 2024-25, Berar's decline was 0.316 and the Central Provinces' decline was 0.241 — it means a gap of 0.074 points. This comparison was based on such data in which there was no overlap of scenes with the first year (64 talukas out of 68 gave out valid data in both years).

![Figure 2](07_Outputs/seasonal_ndvi_signature.png)

**Figure 2.** Seasonal NDVI trajectory (kharif peak to rabi/pre-harvest) and the kharif-to-rabi decline, by division, year one.

![Figure 3](07_Outputs/year2_ndvi_comparison.png)

**Figure 3.** Kharif-to-rabi NDVI decline, both independent annual cycles, by division.

At the immediate 25 km corridor, though, this gap nearly disappears: 0.310 (Berar) vs. 0.299 (Central Provinces), 29 talukas — barely distinguishable. The Central Provinces talukas sitting inside the corridor — Wardha, Nagpur, Chandrapur — are themselves substantial cotton growers, so the two sides look far more alike right at the boundary than the region-wide numbers suggest. I don't read this as a weaker version of the regional result. It's a real finding about how the boundary actually behaves: the effect is a gradient that gets stronger moving away from the historical line in both directions, not something concentrated right at it.

![Figure 4](07_Outputs/lst_ndvi_corridor_comparison.png)

**Figure 4.** NDVI and land-surface-temperature maps and division boxplots, June 2026 single-date snapshot, corridor.

### 4.2 Agrarian Labor Structure, Land Use, and Cotton Dependency

I calculated the agricultural-laborer-to-cultivator ratio across the 32 corridor talukas and found a big difference: it hits 2.90 on the Berar side but drops to 1.96 on the Central Provinces side (this includes 15 Berar and 17 Central Provinces talukas). This means Berar has nearly three laborers for every cultivator. On the other side, it is just about two. This is a real pattern across the whole area. It is not a mistake caused by just one or two strange talukas.

My data shows that used farming land is 68.9% in Berar compared to 61.5% across the border. Forest cover looks almost exactly the same on both sides (12.5% vs 12.6%). This is simply because this specific corridor goes through a shared farming zone (the real, deep forests of the Central Provinces are actually much further east in Gadchiroli, totally outside this zone).

Then I looked at empty or fallow land. It is almost double on the Central Provinces side (5.8% against Berar's 3.3%). I am looking at this gap very carefully. I will not call it a bad sign of money trouble yet, because normal crop rotation can easily leave land empty without it being an economic failure.

Cotton farming shares do not just split cleanly at the old border when I look at the district numbers. Yavatmal has 51% of its farming land under cotton, and Wardha sits right behind at 49% (the funny thing is, one was Berar and one was Central Provinces, yet they are almost tied). Central Provinces districts like Chandrapur and Nagpur are also high at 38% each. Bhandara has just 0.15% cotton and Gondia has 0%, but that is simply because farmers there grow rice (it has nothing to do with old borders). So cotton clearly grew past the old line. Wardha itself has a long cotton history completely separate from Berar.

I found that net sown area is a much cleaner line to look at. All five districts in the Amravati Division stay inside a tight 60% to 75% range, with a tiny standard deviation of 6.8. On the other hand, the six Nagpur Division districts are scattered from 14% in Gadchiroli (which is mostly heavy jungle) up to 57% in Nagpur. This side averages around 41% and spreads out much more with a standard deviation of 15.4. My data shows Berar reads as uniformly under the plough, while the Central Provinces reads as a mix of heavily-cultivated and heavily-forested districts. This makes sense historically since the Ryotwari system brought almost all land into private farming, while Malguzari left large chunks under estate or forest management that were never fully turned into cropland.

I also checked the average farm holding size to see if land was split up differently. The corridor showed no real difference at all. Berar averages 1.81 hectares, while Central Provinces is at 1.90 hectares. This actually goes against the simple guess that Ryotwari means smaller, broken-up farms. I am leaving this result exactly as it is because it is flat, and I see no point in forcing a story that is not there.

![Figure 5](07_Outputs/population_agrarian_comparison.png)

**Figure 5.** Agricultural-laborer-to-cultivator ratio and literacy, by division, corridor talukas.

![Figure 6](07_Outputs/landuse_corridor_comparison.png)

**Figure 6.** Net cultivated area, fallow land, and forest cover, by division, corridor talukas.

![Figure 7](07_Outputs/agrarian_indicators_comparison.png)

**Figure 7.** Cotton share, net sown area, per-capita foodgrain production, and average holding size, all 11 districts.

![Figure 8](07_Outputs/precipitation_corridor_comparison.png)

**Figure 8.** Annual precipitation total and monsoon-season share, by division, district-wide and corridor.

### 4.3 Spatial-Discontinuity Regression: No Level Jump, a Real Slope Difference

I used spatial-discontinuity regression on the 32-taluka corridor data and found no sudden jump at the old line. I looked at four main things and checked them against rainfall and elevation. None showed a real jump (`side`) right at the historical border. The numbers speak for themselves: kharif-to-rabi NDVI decline was at p = 0.458, the agricultural-laborer ratio sat at p = 0.9601, net cultivated area was p = 0.577, and land-surface temperature came out to p = 0.792. It is just flat at the line.

Instead, weather and height are the things that actually matter here. My models showed that rainfall and elevation are the real drivers. In the NDVI-decline model, rainfall hit p = 0.015 and elevation hit p = 0.002. For the agricultural-laborer numbers, rainfall was super clear at p < 0.001. Then for the net-area model, rainfall was p = 0.046 and elevation was p = 0.020.

This confirms a big point about the region. Vidarbha's real geography (the west is drier and lower, while the east is wetter and higher) changes these numbers on its own. This happens completely separate from the old colonial boundary. My control variables caught exactly what they were supposed to catch.

![Figure 9](07_Outputs/phase4_discontinuity_plots.png)

**Figure 9.** Outcome vs. distance-to-boundary, fitted lines by side, corridor scale, four headline outcomes.

I found just one number that was truly significant at the corridor scale. This was the `side × signed_dist_km` interaction for the agricultural-laborer ratio, which had a coefficient of 0.0374 and a p-value of 0.0361. It is not a sudden jump at the line. Instead, it shows that the relationship changes differently as you move further away from the border on each side.

To double-check this, I ran a leave-one-out jackknife test across all 32 corridor talukas. The coefficient stayed quite steady in its direction and overall size, hovering between 0.026 and 0.044 every single time a taluka was dropped. The p-value was a bit more jumpy. It stayed below 0.05 in 26 out of the 32 test runs, but it climbed up to 0.138 when I left out a few specific talukas (Amravati taluka, Seloo, Samudrapur, Narkhed, Korpana, Yavatmal taluka). Because of this shifting, I am treating this specific result as a good hint rather than a solid, bulletproof fact.

The NDVI decline and land-surface temperature results got re-tested next, using the bigger 66 to 68 taluka footprint. These two things have full remote-sensing data across the whole satellite scene (unlike the census numbers which have missing district gaps), and expanding the area changed my results a bit. The sudden jump term was still not significant for either of them. Specifically, NDVI decline `side` was at p = 0.821 and LST `side` was at p = 0.5123. This matches what I found in the smaller corridor area—there is just no sharp jump at the line.

The slopes told a different story, though. The `side × signed_dist_km` interaction was now significant for both satellite outcomes on this larger scale (NDVI decline interaction hit p = 0.0348 and LST interaction hit p = 0.0105). Before this, it was only significant for one thing. On top of that, `signed_dist_km` by itself was super strong in both models at p < 0.001.

This makes a solid point. There is a real, well-powered gradient that changes as you move away from the old border. It has a different shape on each side. This trend shows up in two completely different physical measurements, not just one.

![Figure 10](07_Outputs/phase4_fullfootprint_plots.png)

**Figure 10.** NDVI decline and land-surface temperature vs. distance-to-boundary, full-footprint scale, fitted lines by side.

The agricultural-laborer ratio behaved very differently when I looked at the full footprint data. This includes 67 talukas after I finished processing the population and land-use numbers for Bhandara and Gondia. This time, the sudden jump term became significant with a `side` coefficient of 0.622 and a p-value of 0.014. Meanwhile, the interaction term showed nothing significant at p = 0.579 (which is basically the exact opposite of my smaller corridor results).

I do not think this is a real contradiction. It is simply a clear sign of how uneven and lopsided my data sample is for this area. Inside this particular satellite view, the Berar side barely goes past 20 kilometers from the actual line (this happens because Amravati is the only district from the Berar division that fits in the frame). On the other hand, the Central Provinces side stretches out over 160 kilometers all the way to Bhandara and Gondia.

It makes a lot more sense to read this as a jump near the border rather than a different trend or slope across the whole range. One side simply does not have enough geographic space to map out a proper slope in the first place. Because of this issue, I trust the interaction result from my smaller corridor data much more when talking about what happens right at the line. I see the full footprint jump as a hint about a much wider regional gap rather than a second way to measure the exact same thing. Finally, net cultivated area stayed non-significant across both scales with a corridor p-value of 0.577 and a full footprint p-value of 0.121. It is a very clean null result that does not need any extra explanation.

![Figure 11](07_Outputs/phase4_fullfootprint_all4_plots.png)

**Figure 11.** All four full-footprint outcomes (NDVI decline, LST, agricultural-laborer ratio, net cultivated area) vs. distance-to-boundary, fitted lines by side.

## 5. Discussion

The main thing I found in this project is that there is no sudden jump at the old Berar and Central Provinces line. In fact, it is completely missing. Instead, my data shows a long gradient that looks quite different on each side of the old border. I tested four main things: cotton-signature NDVI, agrarian labor structure, net cultivated area, and land-surface temperature. None of them showed any statistically significant jump right at the line (this is true for both the small corridor area and the bigger regional view) once I controlled for rainfall and elevation.

That said, I don't read this null result as a failure of my design. It simply tells me that whatever institutional legacy this old border has left behind, it does not show up as a sharp edge. It is just not a classic jump result. Forcing a sudden jump where the numbers do not show one would have been worse than just reporting the actual shape I found.

My data actually points to a real gradient. I looked at the kharif-to-rabi NDVI decline numbers, which is the main cotton-monoculture signature here. I found a big gap that was confirmed independently across two separate years (0.070 points in year one and 0.074 points in year two). But this gap shrinks down to almost nothing right at the immediate border area. The simple reason is that the Central Provinces talukas right next to the line grow a lot of cotton too.

When I look at the whole footprint scale, things change. The side-by-distance interaction is significant in both the NDVI decline and land-surface temperature, independently. This means two totally different physical measurements show the exact same trend, which makes me trust the results much more than either one alone.

If I put all of this together, it tells a clear story. The institutional legacy works across the broader region instead of just sticking tightly to the border line. The deeper interior parts of each old province look like their own institutional type, while the border areas just blur together. This is a clear, falsifiable claim. It makes way more sense than expecting a sharp jump on a border that was wiped out 150 years ago. It also fits with Iversen et al.'s (2013) recoding of the Central Provinces as a mixed system with tenant protection rather than just big landlords everywhere. A tenure system with real differences on the inside (which Malguzari definitely had) is exactly why I see a slow gradient instead of a sharp drop right at the edge.

The agricultural-laborer numbers flipped between the small corridor and the big footprint. I got a slope difference at one scale, but a sudden jump at the other (which points to a real limitation of testing an old historical line using a fixed modern satellite view instead of the real historical territory). The two sides inside this satellite frame do not have the same size or shape. This means the conflicting results across scales might partly be an artifact of this mismatch rather than the underlying institutional geography.

I chose to write down both findings here. I did not want to just pick the one that looked more convenient. In the end, I trust the smaller corridor numbers much more. They stay much closer to the main "right at the boundary" question that I wanted to answer from the very start.

## 6. Limitations

### 6.1 Sample Size at the Corridor Scale

My 32-taluka corridor area is genuinely underpowered to find anything unless it is a huge, super sharp jump. I checked this with the jackknife test in Section 4.3. The results showed that the trend direction stays the same, but the actual significance numbers change a lot depending on which exact taluka I drop. This is a real constraint at this scale (it is definitely not something I can just ignore).

### 6.2 Rainfall as a Long-Term Climatology, Not a Time Series

I used WorldClim rain data, which is just a long-term average over many decades at a rough 18.5 km grid size. That is actually wider than most single talukas. It works fine as a basic control variable to catch the overall regional rainfall gradient. But it cannot show year-to-year changes or tiny details inside a taluka.

### 6.3 Full-Footprint Sample Asymmetry

I used a full satellite scene to expand my data for NDVI, LST, and the agricultural-laborer ratio. But this area is fixed by the path and row settings of the satellite itself (specifically WRS-2 path 144, rows 045/046). It has nothing to do with where the actual historical provinces ended. As I showed in Section 4.3 with the laborer numbers, this leaves one side of the border with a much shorter or longer distance range than the other side. This mismatch makes it very messy to compare a level jump against a slope difference when I look across different scales.

### 6.4 Irrigation Data Dropped as Untrustworthy

The Census irrigation numbers I found looked completely wrong. They did not match the real, rain-dependent cotton areas of Vidarbha at all, so I just threw the variable out (I see no point in writing down data that I do not trust). If someone wants to do a better version of this study later, data directly from the state agriculture department would be a much better source to check.

### 6.5 FRA Data as Narrative, Not Quantitative Evidence

There is simply no clean or steady Forest Rights Act data online for Vidarbha at the taluka or district level. The few numbers I managed to put together in Section 3.6 use totally different scales and dates. Because of this mess, I am using them only as institutional-history context here, not as part of my main math or statistical tests.

### 6.6 Ground-Truth Verification, With A Caveat On Scale

I built most of this study using satellite and census data. I checked this data against itself and against a basic Landsat taluka-level reference map from June 2026. This map showed a mean LST of 55.97°C, a mean NDVI of 0.264, and 45.8% valid pixel coverage. But I wanted to be extra sure, so I checked it against real ground data too. I looked at seven real field boundaries in Karanja Ghadge and Sawardoh villages inside the Wardha district (this sits right in the corridor on the old Central Provinces/Malguzari side). I used GPS coordinates, dated ground photos, and a field-level Sentinel-2 NDVI/NDRE time series that I got from a separate family field-monitoring project I run on that exact same land. The NDVI numbers at the two Karanja Ghadge fields came back at 0.329 and 0.287 on 14 July 2026. This makes total sense next to the coarser taluka numbers I mentioned before. Also, the crop leaves in my ground photos match what those numbers predict — closed canopy, healthy, not stressed.

Here is the main caveat about scale. This is definitely not an exact, pixel-for-pixel match. The taluka reference uses Landsat data at a rough 30-meter block size which is just averaged out. My field numbers use Sentinel-2 data at a much sharper 10-meter block size on the exact polygon, and they were mostly taken on a different day. This check simply verifies that the same type of greenness signal shows up consistently when I look closer at the land with my own eyes. I do not expect the two numbers to match up perfectly down to three decimal points. If you want to see the whole setup, the full breakdown and the actual photos are on the dashboard's Ground Truth page.

### 6.7 A Historical-Lineage Verification, Not a Literal Map Overlay

I based the historical accuracy of my border (Section 3.3) on documented district administrative lineage from 1903 to 1956. This means I tracked the administrative lineage of district lines instead of laying an old digitized map over the modern border lines (the truth is, I just could not find one in accessible form). Checking the lineage gave me the exact answers I needed for my project. Still, finding a real period map would definitely make any future visual presentation of the boundary's history stronger.

## 7. Future Work

**A wider or differently-shaped analysis footprint.** I want to process the rest of the Landsat scenes to cover all 11 districts of Vidarbha later on. Right now, I am only using a smaller area covered by just two satellite scenes. Doing this would fix the scene-geometry asymmetry I talked about in Section 6.3. It will also give me a fair distance range to compare both historical provinces equally.

**Extending population and land-use coverage to all 11 districts.** My numbers for the agricultural-laborer ratio and land use only cover 8 out of the 11 districts at this moment. I need to find and process the data for the last three missing districts. I already started working on Gadchiroli, but its data sits outside my current NDVI/LST scene. Adding these final pieces will let me test everything across the whole region on a genuinely consistent scale.

**A digitized historical boundary map.** I want to get a digital copy of an old Imperial Gazetteer map or an old administrative atlas of the Central Provinces and Berar. Having this would let me lay the modern border directly over a period source, on top of the lineage-based verification already done.

## 8. Conclusion

I don't find a statistically significant discontinuity in cotton-signature NDVI, agrarian labor structure, land use, or land-surface temperature right at the 150-year-erased Berar/Central Provinces boundary, at either the 25-kilometer corridor or the full regional footprint, once rainfall and elevation are controlled for. I am writing down this missing discontinuity exactly as it is (I will not pretend it is some weak or hidden border effect).

But I did find a real, twice-confirmed regional gradient in cotton-signature NDVI. My data shows a clear regional cotton NDVI trend that I verified across two different years. This signal gets stronger as you travel away from the historical line instead of showing up right at the edge. Also, there is a significant difference in how both NDVI decline and land-surface temperature trend with distance from the boundary on each side. This shows up across two physically independent Earth-observation channels, at a well-powered sample.

The agricultural-laborer-to-cultivator ratio shows a slightly more qualified picture. I found a slope difference right at the boundary that stayed directionally stable when I ran the jackknife tests, but it is not fully robust when I dropped a few specific talukas. Also, this result flips into a different shape on the larger footprint because the satellite view is structurally lopsided.

I checked the documented administrative lineage records from 1903 to 1956 to verify my border line — the boundary itself dates back to 1853, when Berar was assigned to British administration, but that's as far back as I could trace it in documented district records. As far as this documented administrative history can show, my modern map line is the same as the old Berar/Central Provinces boundary. So the honest final summary of my project is simple: there is a real institutional-geography legacy left on the land, but it looks like a gradient across Vidarbha rather than a discontinuity right at the old line. I think this is a much more precise answer than either a confirmed sharp boundary effect or a flat null would have been, even if it's a quieter one. Finally, my field check at Karanja Ghadge and Sawardoh villages is now closed. Even with the caveat I noted in Section 6.6, the satellite NDVI signal this project runs on holds up against real crop canopy at seven field boundaries that I can personally vouch for, at least for NDVI, at these coordinates, this season.

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
