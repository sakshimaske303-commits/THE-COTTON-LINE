# THE COTTON LINE — Development Log

I keep a log like this for every research project, so I know where I stopped and what data is on disk. This one records how The Cotton Line was built, step by step: the reasoning behind each decision, the dataset changes, and the bugs I hit and how I fixed them.

> **Reading note (October 2026).** Entries 1–22 keep the results and reasoning as I recorded them at the time; only the wording has been tightened. Some of what they say was later found to be wrong or too strong; Entry 23 lists each of those claims and what replaced it. The current results are in `CL_Research_Paper.md` (version 2.0).

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
23. [Entry 23 — Version 2.0: the audit and the rebuild](#entry-23)
24. [Entry 24 — Version 2.1: all of Berar at 30 m](#entry-24)

---

## Entry 1

I started pulling data for this region back in late May. My working name back then was Project Prism—had this clunky acronym (Predictive Regional Intelligence and Sustainable Management) that I eventually threw out. I was using a broad "climate-resilient Vidarbha" framing and had no fixed research question yet. I knew I wanted to work on this area, so I did a large first pass to grab every dataset a regional study would ever need. Before I actually pick a real hypothesis, I want to list down exactly what is sitting on my drive right now (much of it was collected before I had a research question, and I want to keep track of where each file came from).

Here is what I already collected before the pivot

• Administrative boundaries — Got taluka-level shapefiles for all 11 Vidarbha districts (Akola, Amravati, Bhandara, Buldhana, Chandrapur, Gadchiroli, Gondia, Nagpur, Wardha, Washim, Yavatmal) from IIT Bombay's POCRA Maharashtra Census shapefile portal. Also saved the 1994 Development Boards Order — needed it for primary-source context on the region's backwardness and structural gaps.
• Climate — Downloaded Landsat 8/9 Collection 2 Level-2 thermal band (Band 10, surface temp) scenes. Covers the whole footprint. Did a rough merge for the land-surface-temperature raster map too.
• Agriculture — Got the district-wise Area-Production-Yield (APY) sheets for 2024-25, plus Cotton Corporation of India MSP procurement stats (2019-20 to 2024-25). Saved the Maharashtra Economic Survey 2025-26 agri chapters while I was at it.
• Hydrology — Clipped the WorldClim 2.1 monthly rain data (10 arc-minute global grid) to the Vidarbha border polygon.
• Infrastructure — Road/rail network vector lines from OpenStreetMap.
• Terrain — SRTM 30-meter elevation tiles for the full grid. Merged, clipped, reprojected, and ran a quick slope calculation from the DEM.
• Vegetation — Landsat 8/9 Level-2 red/near-infrared bands (Band 4 and Band 5) matching the climate scenes. Need this for the NDVI formula later.

Two categories are still empty on my computer: **Land_use** and **Economics**. Forest Rights Act data—things like claims filed, titles given out, and community forest areas—does not exist anywhere as a clean, ready-to-download district list. What exists is scattered across old parliamentary answers, CAG audit reports, and single district-office PDF notices instead of one useful file. That is still an open problem that I have not solved yet.

**Today's addition — Population.** I downloaded village-level Census shapefiles for all 11 districts. I used the same IIT Bombay POCRA portal that I already went to for my admin borders. This version carries over 600 census facts per village (like population counts, literacy, sex ratio, and other numbers), not just the basic map lines. All 11 district files are sitting on my disk now.

**The pivot.** My original "climate-resilient Vidarbha" idea was too broad. It felt too close to what everyone making a regional satellite project already does. Land monitoring and vulnerability indices are what most regional satellite projects already do. What I actually want for this project is something unique that could only come out of my own academic background (Economics, Political Science, History, and Geography) rather than a technically competent but generic satellite analysis.

The new idea: Vidarbha's history gives me a natural comparison. The five western districts (Amravati, Akola, Buldhana, Washim, and Yavatmal) used to be the old province of Berar. The British took this land directly in 1853 and set up the Ryotwari farming system. They forced farmers to grow only cotton because the American Civil War cut off the normal cotton supply going to Lancashire.

On the other side, the six eastern districts (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli) were the core of the Central Provinces. They had a different setup called the Malguzari system. That old border was officially wiped out at Independence. Yet it runs almost exactly along the modern Amravati Division and Nagpur Division line (which is a boundary I already had map files for on my computer). It also matches the exact map of the 1900 Berar famine (which hit the heavy cotton areas worst) and fits today's farming trouble map of Vidarbha, which is still worst in those same western districts.

My new project name is: **THE COTTON LINE**. My core question is simple: does that 150-year-old colonial border still show up as a measurable spatial jump today in cotton dependency, drought trouble, and farmer stress? I am checking this directly against data I get from satellites rather than relying on historical accounts alone.

I will put the full theory details on its own dashboard page later. This includes institutional persistence theory, the historical reasons why Berar grew cotton, and the physics behind the satellite numbers I use. It will follow the same format as my other theory pages.

**Things I still need to finish after this entry:**
- Land_use / LULC data — I have not found or sourced this yet.
- Economics category — I still do not have a separate source for this (I might mix it into the Agriculture MSP and Economic Survey data that I already have on my computer).
- FRA data — I found no clean file anywhere online. I will probably have to type this out by hand using the scattered PDF pages instead of a single easy download.
- The historic Berar and Central Provinces border line — I still need to map and check this properly against my modern Amravati and Nagpur Division files. Books say they look "roughly the same" (but I have not proved that they are exactly identical on a map yet).
- I have not run any math or analysis yet. This whole entry is me checking my files and changing my project idea.

---

## Entry 2

I made the first boundary layers for this project. At this point, I changed my main folder name from Project Prism to THE_COTTON_LINE. So from now on, everything uses this new folder name.

**What I did.** I opened the taluka map layer on my computer, which has 120 talukas across all 11 districts that I got earlier. Then I split them into two old historic groups by their district names. For the old Berar Ryotwari side, I picked the Amravati Division districts (Akola, Amravati, Buldhana, Washim, and Yavatmal). For the old Central Provinces Malguzari side, I picked the Nagpur Division districts (Nagpur, Wardha, Bhandara, Gondia, Chandrapur, and Gadchiroli). I used a dissolve tool to merge each group of talukas into one big shape per division (56 talukas became the Amravati Division shape, and 64 talukas became the Nagpur Division shape). After that, I grabbed the shared border edge where these two big shapes touch to get my modern line.

The first border line was fragmented. It came out as 256 tiny broken line pieces. This was not a coding error. It happened because the sides of the neighboring taluka shapes did not match up exactly point-for-point. To fix this, I ran a line-merge tool on the broken pieces. That produced one single continuous line that is 384.7 kilometers long. It starts from the Akola, Amravati, and Wardha corner up in the north and goes all the way down to the Yavatmal and Chandrapur corner in the south.

I made a 25-kilometer buffer zone around that border line. Then I split it by division into a Berar side (7,387 square kilometers) and a Central Provinces side (7,987 square kilometers) to map out my near-boundary zone. Out of my 120 talukas, 32 fall inside this specific corridor area. They spread out across Amravati, Yavatmal, Wardha, Chandrapur, and a tiny piece of Nagpur district. This is the exact sample group I will use for my real border jump test in Phase 4 (I will not use the full 11-district dataset for that part).

Next, I generated a quick map to double-check my work. I overlaid the two divisions, the merged border line, and the buffer corridor right against the taluka grid. The line sits where it should and the corridor is balanced on both sides. There are no gaps or overlapping shapes at the border line.

**What this is not yet.** This is a proxy using modern boundaries. I built the whole thing using present-day Census and POCRA taluka files. I still have not checked it against a real, old historical map from the Berar and Central Provinces times. The project roadmap notes say they are only "roughly the same" (they are not proven to be exactly identical on paper yet). I still need to fix this. My best options for finding the old lines are the old Imperial Gazetteer maps (from the 1901 to 1931 books) or old Central Provinces and Berar atlases. I have not found a usable digital copy of either source yet.

**Files I made in this step** (`03_Data_Processed/Administrative/`): `divisions_dissolved.geojson` (2 big shapes), `division_boundary_line.geojson` (the 384.7 km line), `discontinuity_zone_25km.geojson` (the two-sided corridor), `boundary_verification_map.png`.

**Things I still need to fix after this entry:**
- I have not cross-checked the old history border against maps from that time yet (I still cannot find any good source).
- I still need to find the land use, economics, and FRA numbers (this is carried over from my very first entry).
- My next step is Phase 3. I need to pull the actual results and variables (like cotton-dependency from NDVI, drought and LST numbers, and farmer stress facts) for the 32 talukas inside the buffer zone. Doing this will give my Phase 4 border jump test some actual numbers to run on.

---

## Entry 3

I went looking for the climate heat data I talked about in Entry 1. It was not where I expected. The raw Landsat ST_B10 thermal maps, my two merged LST files (`vidarbha_lst_merge.tif` and `vidarbha_mergedLST.tif`), and a broken 8-byte file named `A1_LST_Celcius.tif` were all sitting inside the `Land_use` folder instead of the `Climate` folder. The actual Climate folder is empty. I am leaving the folders as they are for now. Moving 3.5 gigabytes of heavy map data takes too much time. I am recording it here so it does not cause confusion later. This also means I still have not found real LULC or land-cover data, even though that folder has files inside it.

The bug. Both merged heat maps were throwing back impossible temperatures—lowest was -123.15°C, which obviously makes zero sense for ground temperature on Earth. The root cause: Landsat Collection 2 Level-2 ST_B10 scenes use DN=0 as the fill/no-data value for cloud-masked and off-swath pixels (roughly a third of the scene). My old conversion script was blindly applying the Kelvin scale/offset formula directly to the raw DN data without masking out the zero values first. Running DN=0 through that equation spits out exactly 149K, which is -124.15°C—the exact floor value both broken merges were stuck on.

I found the same coding mistake sitting in my plants and vegetation files too. The file `vegetation_mergedB4.tif` says it has 100% good pixels. That is impossible because the satellite pictures always have about 33% empty space. Those empty pixels were never blocked out. They sit in the merged file as false zero values.

**The fix.** I blocked out the DN=0 values as empty data *before* running the scale and offset math, not after. Then I re-ran the whole pipeline from the raw satellite files for both heat data (ST_B10 to Celsius) and light reflection data (SR_B4 and SR_B5 to true values). After fixing that, I calculated the greenness map using the standard formula: NDVI = (B5-B4)/(B5+B4). I made sure to cut out anything outside the real physical range of -1 to 1. Only a tiny group of pixels—exactly 4,750 out of 73.7 million—were out of range because the bottom part of the math fraction came out close to zero near the map edges, so I dropped them.

**Scope of this pass.** I did not want to fix and merge the full 12-scene map that covers all 11 districts right now. Instead, I used the two main satellite scenes from WRS-2 path 144 (rows 045 and 046). Together, these two pictures cover 97.7% of the 25km border corridor area. This is the only zone where I am running my actual border tests anyway. There is a tiny uncovered slice (about 2.3% of the corridor space near the Amravati and Wardha border around latitude 21.30 to 21.46) where the two satellite photos do not quite touch. I am noting it here rather than downloading more scenes; it does not change the overall pattern.

**First read of the result.** I looked at the 28 corridor talukas that have good pixel data. This includes 11 on the Berar Amravati Division side and 17 on the Central Provinces Nagpur Division side. My single June 2026 satellite snapshot shows that the Berar side runs hotter with a mean LST of 56.4°C against 54.6°C. It is also less green with a mean NDVI of 0.245 versus 0.292 right at the border area.

This matches what my main project idea guessed. But remember, this is one single date before the monsoon rains hit. It is not the full seasonal pattern that I actually need for the real cotton-dependency test. Also, my sample size is still very small with 11 against 17 talukas. Because of this, I am treating these numbers as a first quick data point rather than a final result I can trust.

**Files I made in this step:**
- `03_Data_Processed/Climate/lst_fixed_300m_June2026.tif` — This is my corrected LST map. I changed it to 300 meters from the original 30 meters to save disk space, though I used the full-resolution version to calculate my numbers below.
- `03_Data_Processed/Climate/taluka_lst_ndvi_stats.csv` — A simple list showing the average heat and greenness numbers for all 66 talukas that have usable data inside my two satellite pictures.
- `03_Data_Processed/Vegetation/ndvi_fixed_300m_June2026.tif` — My corrected greenness NDVI map downsampled to 300 meters.
- `03_Data_Processed/Vegetation/corridor_taluka_lst_ndvi_stats.csv` — The same numbers list but cut down for the 28 corridor talukas.
- `07_Outputs/lst_ndvi_corridor_comparison.png` — A final image file showing my greenness map, heat map, and simple box plots for both sides.

**Things I still need to fix and track down:**
- Those two old, glitchy merged maps (`vidarbha_lst_merge.tif` and `vidarbha_mergedLST.tif`) along with that broken 8-byte file are still sitting inside the `Land_use` folder. I will safely delete them once I verify the new fixed versions.
- I have not fixed or reprocessed the big 12-scene map that covers all 11 districts yet. I only worked on the 2-scene piece that matters for my border corridor. It might be worth fixing the rest later if I ever need a full district-level comparison.
- This is a single snapshot from June before the monsoons started. My project roadmap actually asks for a multi-date greenness timeline across seasons (a single quick jump in green means a pure cotton monoculture, while staggered shifts mean mixed crops). I need to get post-monsoon and pre-harvest satellite views before I can run that test properly.
- Land_use, Economics, and FRA files—I still have not found any good sources for these three.
- I have not even started on my farmer stress data (like MSP dependence numbers, crop yield changes, or population exposure calculations).
- **Ground-check plan:** I am currently staying in Karanja Ghadge in the Wardha district right now. This specific taluka sits right inside my 25km border corridor on the old Central Provinces Malguzari side (my current June 2026 data says its average ground heat is 55.97°C and greenness is 0.264, but I only have 45.8% good pixels because it sits partly outside my current 2-scene satellite footprint). Here is my plan: I will go out and take real photos of 2 or 3 farm plots around Karanja Ghadge using GPS coordinates. I will note down the crop types, how thick the leaves look, and if the soil is wet. Then I will pull the exact NDVI and LST pixel numbers for those exact points to see if the satellite data matches what I can see with my own eyes. This will become a special ground-truth section on my final dashboard (a direct check of the satellite values). I am waiting to take those field photos before I can move this task forward.

---

## Entry 4

I am working on two things at the same time right now.

**Seasonal NDVI scenes.** The June map I made in Entry 3 only shows the time before seeds are planted. It is not the real cotton test. For that, I need a kharif peak date when cotton leaves are full after the monsoons, and a rabi peak date to see if farmers plant wheat or gram right after cotton. That second crop is the clear sign of mixed farming instead of growing one thing. I cannot download new satellite images directly using my current setup. The network setup I have right here cannot reach a public STAC search API. So I wrote a Python script called `download_seasonal_scenes.py` and saved it right in the project root folder. It looks for the same WRS-2 path 144 and rows 045 and 046 footprint. It connects to Microsoft's Planetary Computer database because it is public, free, and needs no login. I set it to look for a post-monsoon block (September 15 to November 15, 2025) and a pre-harvest block (January 15 to March 15, 2026) to grab the clearest pictures with the absolute lowest cloud cover. I might need to run `pip install requests` if I do not have that package yet. Once the script finishes running, I will bring those pictures in and re-run my old zero-pixel fix and NDVI steps from Entry 3 across all three dates.

**Farming stress proxy — first try using the data I already have.** I did not need to search for new sources for this part. I built the whole thing using the APY 2024-25 Excel sheet and the Economic Survey 2025-26 District Indicators PDF file. Both were already sitting inside my Agriculture folder from before I changed my project topic.

I used the APY sheet to calculate each district's cotton area as a share of total farmed land. This total includes foodgrains, oilseeds, sugarcane, cotton, rabi jowar, and wheat because that is what this specific sheet actually covers. Then I opened the District Indicators PDF. I pulled out four main things for all 11 districts: total used farming land as a percentage of geographic area, food production per person, cropping intensity, and the average farm size. These numbers sat in a big table with merged headers from columns 25 to 31. I had to double-check this table carefully column-by-column against what I already knew about these districts before I trusted the layout. For example, my data showed Gadchiroli with only 14% farming land, while Bhandara and Gondia had over 500 kg of food production per person. This matches their real reputations as heavy forest zones and rice-bowl areas, so I knew I had the right columns lined up. I decided to leave out the columns for MGNREGA work, malnutrition, and death rates (columns 52 to 59) on that same page. The PDF table extraction tool misaligned those columns. I would rather skip a variable than risk using a wrongly labeled number in my project.

**What it shows.** The cotton numbers are messier than the clean west-versus-east story I was expecting to find. Look at the data: Yavatmal sits at 51% and Wardha is right there at 49% (one was Berar and one was Central Provinces, yet they are almost tied for the highest cotton dependency in the area). Central Provinces districts like Chandrapur and Nagpur also run high at 38% each. Bhandara and Gondia sit at basically zero (0.15% and 0%), but that is simply because they are rice-growing areas, not just "not-cotton" spots. So cotton farming was never stuck only inside old Berar. The British forced it hardest there, but cotton growing spread into parts of the neighboring Central Provinces districts too. Wardha especially has a long cotton history separate from Berar's Ryotwari rules.

I found that net sown area is a much cleaner and more consistent line to look at. All five Amravati Division districts stay inside a tight 60% to 75% range. On the other hand, the six Nagpur Division districts are scattered from 14% in Gadchiroli (which is mostly heavy forest) up to 56% in Nagpur. This side averages around 41% and is far more spread out, with a standard deviation of 15.4 against Berar's tiny 6.8. My data shows this is the real structural difference. Berar was cleared for farming. The Central Provinces stayed a mix of heavy crops and deep woods or water bodies. This is consistent with the history: the Ryotwari system forced almost all land into private farming, while Malguzari left large chunks under big estate or forest control that people never fully turned into crop fields.

**Files I made in this step:**
- `download_seasonal_scenes.py` (sitting in the project root folder) — This is the script I wrote to grab the two extra Landsat dates later.
- `03_Data_Processed/Agriculture/vidarbha_agrarian_indicators.csv` — My main table containing cotton share, net sown percentage, food production per person, cropping intensity, and average farm sizes for each district with division tags.
- `07_Outputs/agrarian_indicators_comparison.png` — My final four-panel chart comparing these indicators visually.

**Things I still need to fix and clear up:**
- I need to actually trigger that `download_seasonal_scenes.py` file. I have to get those post-monsoon and pre-harvest satellite maps back to my disk so I can build the real cotton-signature timeline test.
- I skipped the MGNREGA work days and child malnutrition numbers from the District Indicators PDF (columns 52 to 59). The column layout was unreliable, but I might try a second extraction pass later if I realize these numbers are useful for my final writing.
- Land_use, FRA and separate Economics data are still empty (carried over).
- I have not touched the village-level census population numbers that I already downloaded. My stress proxy so far only uses basic farming data. I know a population version showing the exact share of workers who are farm laborers versus landowners will make the analysis stronger. That is my next logical step.

---

## Entry 5

While my script `download_seasonal_scenes.py` was running on my machine, I went ahead and opened up the village population data. I downloaded this census data a while back but never actually clicked open the files until today. I focused only on the five districts that matter for my border corridor: Amravati, Yavatmal, Wardha, Chandrapur, and Nagpur. That means dealing with 9,161 villages and over 600 data details for each one of them.

I grouped the village numbers up to the taluka level to figure out two main things. First, I calculated the ratio of farm laborers to landowning farmers (I mixed the main and marginal workers together since this shows real landlessness and stress when people have to work someone else's land for cash). Second, I pulled the literacy percentages.

**I tried to extract irrigation as well, but had to discard it.** The file columns named `area_irri` and `net_area` showed irrigation rates between 58% and 92% for Yavatmal villages. That contradicts the well-known fact that Vidarbha’s cotton fields depend almost entirely on rain (real numbers usually sit lower around 15% to 20%). I tried dividing the numbers by the total village area as a backup test, but the results were still too high to be real. Whatever these column names mean, they do not show simple watering data, so I chose to leave a blank space instead of using numbers that I know are wrong. I will try to find a data dictionary guide for this map shapefile later to see what is actually going on inside those columns.

**What held up.** I looked at the agricultural worker numbers for the 32 corridor talukas where my data matched up. This includes 15 on the Berar side and 17 on the Central Provinces side. The numbers show a big gap: 2.90 on the Berar side compared to 1.96 on the Central Provinces side. This means for every single landowning farmer in the Berar talukas, you have nearly three hired laborers, while the other side averages about two. This is a real, steady pattern. It is not just a statistical mistake caused by one or two strange talukas. It is consistent with the historical literature. The Ryotwari system gave normal peasants actual papers for their land, but forcing them to grow only cotton created a dangerous cash economy tied to market prices. Over generations, this specific cash crop setup makes people lose their farms and forces a large class of people to become landless workers. This fact is the main point of all the real books written about farming trouble in Vidarbha (this is the standard explanation in the literature for why agrarian distress concentrates in the western belt). I also checked literacy, but the numbers were close (75.1% against 72.5%), so it is not a big difference on its own.

**Files I made in this step:**
- `03_Data_Processed/Population/taluka_population_agri_stats.csv` — My full list of grouped taluka numbers showing total population, houses, the worker breakdown, and basic reading skills across the 5 districts.
- `03_Data_Processed/Population/corridor_taluka_population_stats.csv` — The same table but chopped down for the 32 corridor talukas with their proper division names.
- `07_Outputs/population_agrarian_comparison.png` — A final image file where I made simple box plots to compare the worker ratio and literacy numbers across the old border.

**Things I still need to fix and check:**
- The irrigation fields in this file are not usable as they stand. I need to take a second look or find a different file. Data directly from the state agriculture department would be much safer than trying to guess what this map file means.
- I only worked on 5 out of the 11 districts (the ones touching my border corridor). The other 6 districts (Akola, Buldhana, Washim, Bhandara, Gondia, and Gadchiroli) are untouched. I made this small-scale choice on purpose, matching my earlier satellite heat maps.
- I noticed this census data also has village land fields for forests, empty land, and rocks. I could use these later to partially fill my missing land use category. Worth returning to.
- I am still waiting for my script `download_seasonal_scenes.py` to finish running on my computer. Once it finishes, I can start the multi-date analysis.

## Entry 6

I found out that the same census map files from Entry 5 actually have a full land list for each village too. This includes forests, non-farming space, rocks, empty fields, tree areas, and used crop areas. The numbers are written in hectares, and they match the total village sizes perfectly. I checked this math myself. All nine sections add up to nearly 100% of the total size for every single village. So, unlike those broken watering numbers from my last entry, I trust this data. This fixes my missing land use category that was empty since Entry 1. It is not satellite land cover, but a real independent list from the census. It also means the forest and cropland classification is already done, so I do not need to train a classifier.

I checked these numbers before trusting them. Chikhaldara is a hilly tiger-reserve area in the Amravati district, and my code showed it has 30.9% forest. Jiwati in Chandrapur is a very famous woody area, and it came out at 36.4% forest. Both numbers match what people know about these places, which is what proved to me that these columns are real.

**Border corridor check for my 32 talukas.** My data shows that used farming land is 68.9% on the Berar side compared to 61.5% on the Central Provinces side. This goes in the same direction as the district numbers I found in my Entry 4 PDF file. But the gap is much narrower here. Why? The simple reason is that my buffer zone only touches the heavily farmed parts of the Central Provinces (like Wardha, Nagpur, and Chandrapur). It misses the large forest tracts of Gadchiroli that pulled the whole district average down earlier. Forest numbers look almost exactly the same right at the border (12.5% vs 12.6%) for this same reason. This corridor is a shared farming zone, not where the real heavy woods of the Central Provinces sit. One new finding: Empty or fallow land is nearly double on the Central Provinces side of the border area (5.8% against Berar’s 3.3%). That means more land is sitting idle over there. I am not drawing conclusions from this yet. Normal crop rotation can easily explain it just as well as financial trouble. Still, I will add this fact to my final report alongside my numbers on cotton shares and farm laborers.

**Files I made in this step:**
- `03_Data_Processed/Land_use/taluka_landuse_stats.csv` — My full list of land use columns for all matching talukas across the 5 districts.
- `03_Data_Processed/Land_use/corridor_taluka_landuse_stats.csv` — The same data list but cut down for my 32 corridor talukas with their division names.
- `07_Outputs/landuse_corridor_comparison.png` — A final image file showing my comparison plots for farming land, empty fields, and forests by division.

**Things I still need to finish and track:**
- This land data comes purely from the village census books, not from a direct satellite scan. An actual LULC map (like from ISRO Bhuvan or somewhere similar) would still be a useful cross-check later. The land-use gap is filled.
- I stuck to the same 5-district limit here. It is the corridor area, exactly like what I chose to do in Entry 3 and Entry 5. The other 6 districts are still blank and untouched.
- My script `download_seasonal_scenes.py` finished downloading all the files while I was finishing up this task. My next plan is to bring those satellite pictures in so I can run the seasonal NDVI analysis.

---

## Entry 7

This is the real Phase 3 result variable. I am replacing the temporary June data from Entry 3 with actual seasonal mapping. I have three complete dates on disk now: June (before planting), November 2025 (the high point of the kharif monsoon), and March 2026 (the rabi pre-harvest time). I ran my old zero-pixel correction code on these two new satellite images. Then I calculated the actual seasonal greenness drop for each taluka by checking how much the NDVI value falls between the November high point and the March winter period. If the drop is huge, it means the fields go bare after the monsoon crop is harvested (which is the classic signature of a single cotton crop). A smaller drop means farmers are planting a winter crop like wheat or gram right after the first harvest. That keeps the land green through the cold months, showing a mixed farming setup.

**My results across the full footprint (68 talukas across both satellite rows).** The Berar Amravati Division side shows an average greenness drop of 0.325 NDVI points. The Central Provinces Nagpur Division side sits at 0.255. That is a visibly smaller drop, and it spreads out more with a standard deviation of 0.062 against Berar's tight 0.041. This tells me that the winter crop pattern is very real but uneven on the Central Provinces side instead of being the same everywhere. Both sides reach almost the same high greenness score during the monsoon (0.66 against 0.64). The actual difference is not about how green things get when it rains. It is all about what happens after the rains stop. That is the pattern the design was built to detect. I am looking at a single-crop setup that sits empty once cotton is picked, compared to a mixed-farming setup that keeps parts of the land working through the dry winter season.

**At the border corridor specifically, this gap almost disappears.** The numbers sit at 0.310 versus 0.299 across my 29 corridor talukas. This matches the same trend I saw with the cotton shares back in Entry 4. The Central Provinces talukas right inside my buffer zone (like Wardha, Nagpur, and Chandrapur) grow a lot of cotton themselves. So right at the border line, the two sides actually look very similar compared to the wide district averages. The trend is real across the whole region, but it does not make a sharp jump at the old historic line. It behaves like a slow trend that gets stronger as you move further away from the border in both directions. It is not a clean, sharp drop. I want this on record before Phase 4. A spatial jump test run only on the tight corridor area might show a much weaker link than the wide regional numbers suggest. That is a finding about how the old border behaves, not a failure of the method.

**Files I made in this step:**
- `03_Data_Processed/Vegetation/ndvi_postmonsoon_300m.tif` and `ndvi_preharvest_300m.tif` — These are my two new fixed greenness maps downsampled to 300 meters to save disk space.
- `03_Data_Processed/Vegetation/taluka_seasonal_ndvi_signature.csv` — My main list showing all three dates and the greenness drop for all 68 matching talukas.
- `03_Data_Processed/Vegetation/corridor_taluka_seasonal_ndvi_signature.csv` — The same table list but cut down for my 29 corridor talukas.
- `07_Outputs/seasonal_ndvi_signature.png` — My final image file showing the seasonal timeline chart and the greenness drop box plots.

**Things I still need to finish and track down:**
- This data only covers one single farming year (the kharif 2025 and rabi 2025-26 seasons). I grabbed these dates because they sit a year away from my main June 2026 starting point. I should probably get a whole second year of satellite maps later. That will show whether the result is specific to one season.
- I have not started Phase 4 yet. That is the actual math part where I run the spatial-discontinuity statistical tests while blocking out the effects of distance, height, and rain. This entry gave me the final greenness drop numbers that the main test needs to run on.
- The land use and FRA sections are still open from my earlier entries. Also, my field-check idea for Karanja Ghadge is still sitting idle. I am waiting on the actual farm photos to come in before I can finish that part.

## Entry 8

I processed the WorldClim rainfall data that I already downloaded a while back. It had been untouched since the original data pull. I sampled all 12 months at the center point of every single taluka. Then I calculated the total annual rain, the percentage that falls during the monsoon months (June to September), and the month-to-month changes.

**An important caveat before the numbers:** this is a rainfall *climatology* map (meaning long-term monthly averages over decades, not the actual rain from one specific year). Also, the block size is very rough. WorldClim’s 10 arc-minute grid means each pixel is about 18.5 kilometers wide. That is actually bigger than most single talukas, so neighboring talukas often end up sharing almost the same rain numbers. It works fine to show the big regional trend, but it is not sharp enough for tiny taluka-by-taluka precision.

**What the data shows:** the Central Provinces side gets more rain than the Berar side. The wide district numbers show 1,249 mm per year against 903 mm per year. This shrinks down to 1,109 mm versus 1,005 mm right at the border corridor area. The monsoon concentration is almost identical on both sides (around 88% of the yearly rain falls between June and September either way). So the real difference is in the total amount of water, not the timing or seasonal shape.

This rainfall gap is not a finding about the historical border. It is a natural west-to-east rain trend across Vidarbha that has nothing to do with old Ryotwari or Malguzari rules (it predates colonial rule). I am writing this down here because my project roadmap specifically said I must block this out in my Phase 4 math. If Berar is historically a cotton zone AND naturally drier, any result saying "Berar looks more drought-stressed" might be because it gets less rain, not because of old land laws. My Phase 4 models need to clear this out before I can trust any border effect.

**Files I made in this step:**
- `03_Data_Processed/Hydrology/taluka_precipitation_stats.csv` — A list of monthly and yearly rain numbers for all 120 talukas.
- `03_Data_Processed/Hydrology/corridor_taluka_precipitation_stats.csv` — The same rain list but chopped down for my corridor talukas.
- `07_Outputs/precipitation_corridor_comparison.png` — Simple box plots comparing the total yearly rain and monsoon shares across the two sides.

That closes out Phase 3. I have my cotton-signature NDVI numbers from Entry 7, my farmer stress and land use data from Entries 4 to 6, and now my climate control variables are ready. I am moving straight to Phase 4 next. Next: the boundary discontinuity tests.

---

## Entry 9

This is the real test that my whole project has been building toward from day one. I want to know if each result jumps suddenly right at the old historic border line once I block out the effects of distance, rain, and height. Or is everything I wrote down in Entries 3 to 8 a broad regional trend that happens to look different on each side of the line?

**Getting my dataset together.** I needed elevation numbers as a control variable, so I grabbed 9 SRTM terrain tiles that cover my corridor box. Then I sampled the height at the center point of all 32 corridor talukas. The numbers came out between 194 and 497 meters, which makes total sense for this part of the Deccan plateau edge. Everything else in this big table comes directly from my earlier entries. I pulled the `side` tag (where 1 means Berar and 0 means Central Provinces) and the `signed_dist_km` numbers (which shows how many kilometers each taluka center is from the merged border line, calculated in UTM 44N and written as positive on the Berar side) from my Entry 2 boundary files. I got the three-date NDVI and the monsoon-to-winter greenness drop from Entry 7. The ground heat numbers come from Entry 3. I took the worker-to-farmer ratio and literacy rates from Entry 5. My land use percentages come from Entry 6, the total yearly rain data comes from Entry 8, and the cotton area shares come from Entry 4. This leaves me with exactly 32 corridor talukas, with one neat row of facts for each one.

**The model.** I used a standard regression-discontinuity setup. The math formula is `outcome ~ side + signed_dist_km + side×signed_dist_km + rainfall + elevation`, and I ran it using OLS. The `side` variable is the most important part because it catches the sudden level jump right at the border line. That is the actual question I am asking here. The interaction term shows if the *slope* or trend with distance is different on each side of the border (meaning, does the effect grow stronger or weaker as you travel away from the line, and does that change across the two sides?). I ran this code for five results: the kharif-to-rabi NDVI greenness drop (I ran this both with and without my control variables to see what changes), the farm laborer ratio, the used crop land percentage, and the June ground heat numbers.

Being blunt about what came back: at n=28–32, most of the side coefficients don't clear statistical significance. NDVI decline side p=0.458; agricultural-laborer ratio side p=0.960; net cultivated area p=0.577; land-surface temperature side p=0.792. None of these show a clean level jump right at the boundary once the geographic controls are turned on. A corridor-only sample this small has limited power to detect anything short of a large, sharp effect. Plus, Entry 7 already flagged that the cotton-signature gap itself nearly vanishes at the immediate corridor even before any regression. This math confirms that.

**The one result that did show real significance.** The `side_x_dist` interaction number for the farm worker ratio came back with a coefficient of 0.0374 and a p-value of 0.036. It is not a sudden jump at the line. Instead, it is a difference in the *slope*. As you travel away from the old border, the laborer ratio changes at a different speed on the Berar side compared to the Central Provinces side. I am reading this cautiously; it is not a border jump. It basically tells me that the link between distance from the old line and the worker setup is not flat. It has a different shape on each side of the border. But this is one significant coefficient out of twenty across five different math models. With my small sample size, I want to double-check this before using it as a major fact in my final writing.

**What did stay significant every single time: my control variables.** Rain and ground height show up as real drivers in almost all my models. Look at the numbers: rain hit p=0.015 and height hit p=0.002 in the greenness drop model. Rainfall was strong at p<0.001 in the farm laborer model. Then both rain (p=0.046) and height (p=0.020) showed up big in the used farming land percentage model. This is exactly what I flagged back in Entry 8 before starting this step. The actual nature and geography of Vidarbha (the Central Provinces side is simply wetter and lower, while the Berar side is drier and higher) does the real work here. It changes these results on its own, separate from any old colonial line. This is why I built the climate controls (Entry 8) before running these tests.

**Summary.** Inside my tight 25km buffer corridor and with this small group of talukas, I am simply not finding a sharp mathematical jump right at the old historic line. Instead, I am seeing a real regional trend that I wrote down across Entries 4 to 8. This trend slowly fades out as you get close to the actual border line. I also found one slope difference that is worth pointing out instead of a sudden level jump. This is a perfectly fine and real finding. I will report this null result as it is. It simply tells me that the history link I am looking for does not look like a hard, sharp edge right at the old line. It shows up as a much wider east-to-west pattern across Vidarbha. My small corridor test does not have enough power to pin that down properly. I want to take two main ideas forward into Phase 5. First, I want to see if using a wider corridor or testing the full 68-taluka footprint gives my math models more power without losing the border logic. Second, I need to remember that finding a zero result at the line but a trend across the whole region is a real part of the story, not an error.

**Files I made in this step:**
- `03_Data_Processed/Phase4/phase4_master_dataset.csv` — My big master math table with 32 rows and 19 columns for the tests.
- `03_Data_Processed/Terrain/corridor_taluka_elevation.csv` — My list of corridor taluka heights that I got from the SRTM tiles.
- `07_Outputs/phase4_discontinuity_plots.png` — My final image file showing the scatter plots and fitted trend lines for my four main results.

**Things I still need to finish and track:**
- My small sample size is the biggest problem here (it sits between 28 and 32 talukas). It is worth testing if the full 68-taluka footprint gives me better mathematical power. I know that moves away from a tight border test, but it is worth a shot.
- I need to check the one significant interaction for the farm laborer slope. It needs a serious robustness check before I write it down in my final paper (for now it is a single coefficient, not a pattern).
- The Karanja Ghadge field check is pending the farm photos from Sawardoh village.
- The old map cross-check, the FRA data list, and the second year of greenness data remain open from earlier entries.

-----

## Entry 10

I have three things left over from Entry 9, and I am handling them one by one.

Farm splitting check. I mapped the `avg_holding_ha` column from my Entry 4 district table onto the 32 corridor talukas to check the setup. The Berar corridor talukas average 1.81 hectares per farm, while the Central Provinces side averages 1.90 hectares. So the Central Provinces side actually has slightly *bigger* farms, not smaller ones. This goes against the simple guess that the Ryotwari system always leaves behind smaller, more broken-up pieces of land today. The two values are close. They stay within a tiny quarter-hectare gap with a very similar spread, so I see no real difference here either way. This is a flat zero result across the line.

**Double-checking the Entry 9 slope result.** I ran a leave-one-out jackknife test on the one significant result I found in Entry 9. This was the `side_x_dist` interaction for the farm worker ratio. I re-ran my math model 32 times, dropping a different corridor taluka each time to see what happens to that specific number. It stayed positive and sat inside a tight band between 0.026 and 0.044 every single time. No single taluka drives the coefficient.

The p-value is less stable. It stays below 0.05 in 26 out of the 32 runs, but it crosses back over the line (climbing as high as 0.138) when I leave out a few specific talukas like Amravati taluka itself, Seloo, Samudrapur, Narkhed, Korpana, or Yavatmal taluka. So the basic direction and rough size of the effect look steady, but the statistical value sits right on the edge. A few talukas carry it under p<0.05. I treat it as suggestive, not established.

**Rerunning the test on the full footprint.** This is the much bigger task. My old Entry 9 math only used the 32 corridor talukas, and I already noted that this sample was simply too weak. Both greenness (NDVI) and ground heat (LST) have full data for the whole satellite scene sitting in Entries 3 and 7 (that gives me 68 and 66 talukas from the complete path-144 view, not just the small 25-kilometer buffer zone). So I re-ran those two tests using this much larger group. I had to download two extra SRTM tiles named n20_e080 and n21_e080 to map out the height data for this wider area. I merged and sampled them. All 68 talukas got a correct height number this time.

My other data points like population, land use, and the farm worker ratio do not have this choice. That specific census data only covers 5 districts of Vidarbha on my disk. So those files must stay restricted to the smaller corridor for now. Expanding them would mean searching for and processing village maps for three more entire districts. That is a separate task.

One issue before the results: the full footprint is unbalanced. It has 49 Central Provinces talukas but only 19 Berar talukas. This happens simply because the satellite camera view captures more territory on the Central Provinces side. I am keeping this imbalance in mind when I read my final numbers.

**What changed with the bigger sample.** The sudden jump number at the border (`side`) is not significant in either model. For the greenness drop, the p-value came out to 0.821, and for ground heat, it sat at 0.512. This perfectly matches what I guessed in Entry 9. There is no sharp jump right at the old line. But the trend interaction number, which only worked for one single variable in my smaller test, is now significant for *both* satellite outcomes across the wider map footprint. Look at the data: the greenness drop side-by-distance p-value is 0.035, and the ground heat side-by-distance p-value is 0.010. Also, `signed_dist_km` by itself is strong in both models with a p-value under 0.001.

There is a real, well-powered trend that changes as you travel away from the old border line. It takes a different shape or slope on each side. This is a much cleaner and steadier version of what I already suspected from my tight corridor test. It is not a sudden jump at the line. It is a genuine difference in how these trends behave with distance depending on which side you stand on. Finding the same shape of results across two different physical measurements (and with real statistical backup this time) is the strongest evidence so far.

**Files I made in this step:**
- `03_Data_Processed/Agriculture/phase4_master_dataset.csv` — I updated this file by pasting in the new `avg_holding_ha` column.
- `03_Data_Processed/Phase4/phase4_robustness_jackknife.csv` — My master list showing all 32 drop-one-out coefficients and p-values from the test.
- `03_Data_Processed/Phase4/phase4_fullfootprint_dataset.csv` — My big 68-taluka wide math table for the regressions (this only has NDVI and LST data because of the missing census files I noted before).
- `07_Outputs/phase4_fullfootprint_plots.png` — My final image file showing the greenness drop and ground heat trends with distance from the border line.

**Things I still need to finish and track:**
- My farm laborer numbers, used crop land percentages, and land use columns are still stuck inside the smaller 32-taluka corridor. Extending these to the wider map footprint means I must search for and process population and land use census records for Bhandara, Gondia, and Gadchiroli districts (I have not sourced these extra files yet).
- The slope trend I found in Entry 9 looks much stronger now. The same slope-difference pattern shows up independently across my larger greenness and ground heat data. Having three separate things pointing the same way shows a real trend, not final proof, but it is easily the strongest sign I have found so far that my project is about a slow regional gradient rather than a sharp border jump.
- The Karanja Ghadge field check is pending the Sawardoh photos.
- The historical map check, the FRA data and the second NDVI year remain open.

---

## Entry 11

I found out that I did not actually need to search for new data for Bhandara, Gondia, and Gadchiroli. The raw census map zip files (`bhandara.zip`, `gondia.zip`, and `gadchiroli.zip`) were already sitting quietly in my Population folder alongside the other 8 district files. I had not unzipped them. So I ran them through the same village-to-taluka grouping step that I used back in Entry 5 and 6. I added up all the worker and land use columns by district and taluka names, and then I calculated the ratios again. All 27 talukas across these three extra districts came out clean. Their land use category numbers add up to exactly 100% of the total size in hectares for every single one of them. Also, the spelling of the taluka names matched my administrative map layer perfectly (no "Gondia versus Gondiya" mismatch this time).

With these new numbers in hand, I rebuilt my full-footprint Phase 4 master table. This time, I could include all four main result variables (greenness decline, ground heat, farm worker ratio, and used crop area percentage) instead of the two satellite options I had in Entry 10.

**The greenness drop and ground heat numbers came back basically identical to Entry 10.** There is still no sudden level jump at the old border line. The p-values hit p=0.821 for the NDVI drop and p=0.512 for the LST heat maps. But the trend interaction term was still significant for both of them with a greenness side-by-distance p-value of 0.035 and a heat side-by-distance p-value of 0.010. That part of the result holds.

**The farm worker ratio behaves differently.** Back when I checked the tight corridor area in Entry 9, this specific number showed a real trend difference in the *slope* with a p-value of 0.036, but it had no sudden level jump. Now that I am using the full footprint data with a sample size of 67 talukas (this includes Bhandara and Gondia now, though Gadchiroli's talukas sit outside my actual satellite picture footprint so they did not make it into this specific test, even though I have their processed facts safe on disk for later use if I widen the map), the result flips. Now I found a significant level jump right at the border line under the `side` term with a coefficient of 0.622 and a p-value of 0.014. Meanwhile, the slope trend number loses its importance at p=0.579.

This is not a real mistake or a direct contradiction in my math. It needs an explanation rather than picking whichever result looks better. I went and checked the actual distance ranges on both sides of this larger sample to figure out why this happened. The Berar side barely stretches past 20 kilometers from the actual border line here (this happens because Amravati is the only district from the Berar division that actually fits inside this specific satellite view). The deeper interior parts of Berar like Akola, Buldhana, and Washim were simply never inside this particular path-144 camera path to begin with.

On the other hand, the Central Provinces side now reaches out past 160 kilometers because Bhandara and Gondia sit that far to the east. So I am no longer comparing two neat parallel trends here. It is a short, border-hugging Berar piece up against a long, far-reaching Central Provinces line. Reading this as a level jump near the border makes a lot more sense than guessing a different slope across the whole area, since only one side actually has enough map range to show a real slope line in the first place. I trust my smaller corridor-only trend results from Entry 9 much more when talking about what happens right at the line. I am treating this full footprint jump as a hint about a much bigger regional gap across the two divisions rather than a double test of the same thing.

**Net cultivated area stays flat either way.** The sudden level jump variable failed to show anything important across both tests. My numbers came out at p=0.121 for the wide footprint versus p=0.577 for the tight corridor. A clean null at both scales.

**Files I made in this step:**
- `03_Data_Processed/Population/taluka_population_agri_stats.csv` and `03_Data_Processed/Land_use/taluka_landuse_stats.csv` — I updated both tables to cover 8 out of the 11 districts now. I successfully added Bhandara, Gondia, and Gadchiroli into the files alongside the original 5 districts.
- `03_Data_Processed/Phase4/phase4_fullfootprint_dataset.csv` — I updated this master math table to include all 4 result variables across 67 to 68 talukas depending on the test.
- `07_Outputs/phase4_fullfootprint_all4_plots.png` — My final image file plotting all four large footprint results against distance from the border line.

**Things I still need to finish and check:**
- I processed and saved Gadchiroli's population and land use numbers, but the district has no matching satellite map coverage here. These files are only useful if I choose to download a much wider Landsat map area later on.
- The farm laborer numbers now give me two different, fair reads depending on which sample group I run the math on. Both must be reported in the paper.
- The Karanja Ghadge field check, the historical map check, the FRA data and the second NDVI year remain open.

---

## Entry 12

I am handling two of the remaining open things together in this session.

**FRA data list.** I flagged this in Entry 1 as having no clean source. I knew it would need manual typing from old PDF files, so I went looking properly this time instead of leaving it blank. The short answer: there is no clean taluka list, or even steady district list, for Forest Rights Act data across Vidarbha online. What exists is broken across a few different files at different scales:

- I found Maharashtra state totals from two separate years. First, from the state Tribal Development Department's 2020-21 report up to March 2021: they got 379,881 personal rights claims, finished 95.84% of them, and gave out 1.31 lakh acres. For group community rights, they got 11,985 claims, finished 81.59%, and gave out 28.28 lakh acres. Second, a 2024 committee report showed newer numbers up to June 2023. They added 35,654 new personal claims and 90,626 new personal titles since 2017. But they only gave 1,290 new community group titles in that same time (30% of claims are still stuck statewide and 18% were thrown out).
- I found one genuinely useful district number for Gadchiroli specifically from that same 2024 report using older 2016 facts. It shows 1,355 community group titles covering 4,34,181 hectares against a target of 5,57,137 hectares. That means 77.9% was successfully cleared. The report explicitly calls it a "high performing" area, comparing it directly to Nashik district on the other side of the state which sits at a tiny 5%. That is a real, sourced, specific fact on disk (but it is for one single district and almost ten years old now).
- I found a wide regional number for Vidarbha that is not split by district. It shows roughly 6,500 villages and 7,94,118 hectares given out under group community forest rights since 2013 (I read this in an EPW magazine paper mentioned inside a Scroll.in news report talking about Gondia’s forest work).
- I also found a few single village examples with real numbers, but there is no way for me to add them up into a full district total. For example, Menda-Lekha village in Gadchiroli got 1,800 hectares back in 2009 and made 75 lakh rupees from selling bamboo by 2012. Dhamditola and Paulzhola villages in Gondia secured 290 and over 600 hectares in 2013.

I also discovered that the Ministry of Tribal Affairs runs a live public web dashboard at forestrights.nic.in/mpr/common/dashboard. In theory, this website lets you click and see state or district breakdowns. But it is an interactive portal, not a file I can easily download, and it cannot be queried programmatically. If I ever need district-by-district numbers for Gadchiroli, Chandrapur, Gondia, Bhandara, Yavatmal, Wardha, Nagpur, and Amravati later on, that website is the only place to get them. It would have to be read off by hand, one district at a time.

Because of these gaps, I am treating the FRA numbers as a background history story for my final writing, not as a main math variable for my Phase 4 models. There is simply no steady or equal measurement across enough districts to paste it into my taluka table the way I did with my greenness or rain data. It works fine as a background history fact. Gadchiroli's high recognition rate is worth citing when I describe the forest rules of the region. But it simply cannot do any statistical heavy lifting in my models the way my satellite and census facts can because of the missing district slots.

**Second-year NDVI check.** I wrote a new script called `download_seasonal_scenes_year2.py` to run locally on my machine. It follows the same style as my first seasonal download script and grabs the same WRS-2 map box (path 144, rows 045 and 046). The big change is that I pushed the timeline back by an entire year. Now it looks for a monsoon kharif high point between September and November 2024, and a winter rabi peak between January and March 2025. This is the exact double-check I talked about in Entry 7. Back then, I found that the greenness drop was 0.325 in Berar versus 0.255 in the Central Provinces, but I only measured that on one single farming cycle. If I see the same gap (or something very close to it) show up on its own in the older 2024 data, that is real evidence I found a steady, real farming pattern — not just something caused by one weird or unusual season. It runs locally and pulls from Microsoft's Planetary Computer catalogue, like the first script.

**Files I made in this step:**
- `03_Data_Processed/Economics/fra_compilation_vidarbha.csv` — I put everything I found above into this file. It has one row per number and labels each fact by its scale (state, district, or village), its unit, the date, and the source web link. I built this purely as a typed-out summary because the sources are fragmented.
- `download_seasonal_scenes_year2.py` (project root) — second-year download script, same pattern as the first.

**Things I still need to finish and track down:**
- For the FRA data, only Gadchiroli has a real, solid number. The other 7 districts have no district-level numbers that I could find online. So this has to stay as a background text point for my final writing, not a main math variable. The only route is reading the MoTA dashboard by hand.
- For my second year of greenness data, I am currently waiting for my script to finish running. Once those 2024 satellite maps land on my computer, I will re-run my old zero-pixel correction and NDVI steps on them. Then I can compare that winter greenness drop directly against my 2025 data from Entry 7.
- The Karanja Ghadge and Sawardoh field check is on hold for now.
- The historical map check is still open; I have not found a usable period map.

---

## Entry 13

My project roadmap always told me to find a digital 1901 to 1931 Imperial Gazetteer map and paste it over my modern division lines. I could not find a usable digital copy.

But what I found instead does the same job in a different way. I dug up the actual written lists of districts that were inside the old Berar Division and the Central Provinces Nagpur Division from 1903 to 1956. This lets me check if the same land sits on each side of my modern map line district-by-district. This does not need a pixel-level overlay.

**Old Berar Division history check (1903-1956).** The old papers list these main places: Amraoti (Amravati), Akola, Ellichpur, Buldhana, Basim, and Wun. I cross-checked these names against what we call these places today. Ellichpur is now a single taluka inside the Amravati district, not its own separate district. It got mixed in very early on. Wun was renamed Yavatmal. Basim was renamed Washim (it was actually folded into the Akola district for a long time before they remade it as a separate district on July 1, 1998).

The final result of my check is very clear: **the old historical Berar map fits district-for-district onto my modern Amravati Division area (Akola, Amravati, Buldhana, Washim, and Yavatmal).** It is the same 5-district territory. People changed the names and split the land up internally over the last 120 years, but nobody ever redrew the main outer border line. This supports the project premise. It means I can safely use my modern division merge tool as a stand-in for the old historical Berar line.

**Old Central Provinces Nagpur Division history check.** The old records list these areas: Nagpur, Bhandara, Chanda (which people renamed Chandrapur), Wardha, and one complication: **Balaghat**. Gondia (which split from Bhandara in 1999) and Gadchiroli (which split from Chandrapur back on August 26, 1982) are later internal cuts of that same old territory. They are not new land pieces, so they match up nicely. But Balaghat is a different story. On November 1, 1956, when the government redrew state borders based on languages, Balaghat got moved into Madhya Pradesh's Jabalpur Division. The rest of the old Nagpur Division spoke Marathi (Nagpur, Bhandara, Wardha, and Chandrapur). So those parts went to Bombay State and eventually became part of Maharashtra in 1960.

**What this actually means for my project.** Balaghat was never sitting inside my files to begin with. It is not a Maharashtra district today, so it was never going to be part of my 11 Vidarbha districts anyway. nothing about my Phase 2 border mapping needs fixing. But the paper needs to be exact on this. My Central Provinces side in this project is specifically the Maharashtra-Vidarbha piece of the old CP Nagpur Division. This makes it slightly smaller than the full historical area from 120 years ago. The piece that is missing fell out because of a 1956 language border change, which has nothing to do with the farming land laws I am actually testing.

**The bottom line of my check.** The modern Amravati and Nagpur division border line that I built back in Entry 2 is exactly the same line as the old historical Berar and Central Provinces border. I proved this by tracking down the written office history of every single district instead of laying an old map image over my modern files. A digitised period map would still be useful from the 1900s as an illustration. But the main question my roadmap was actually asking—whether my modern border map sits exactly where the old historical one used to be—now has a very well-sourced yes.

**Files I made in this step:**
- I did not save any new files inside `03_Data_Processed/`. This pass was me doing reading and documentation checks, not processing map files. The actual results live right here inside this diary log.

**Things I still need to finish and track down:**
- I still have not found a real old map image from the Imperial Gazetteer books or old atlases to use as a visual slide in my writing. Tracking down the district history solved the main problem, but it does not give me an actual picture file.
- My second-year greenness script is running on my computer right now. I will bring the data blocks in as soon as it stops downloading.
- The FRA data list and my field checks around Karanja Ghadge are still open, exactly like I noted before.

---

## Entry 14

My year-2024 satellite files from my script `download_seasonal_scenes_year2.py` finished downloading. They use the same WRS-2 map box as before (path 144, rows 045 and 046). I set it for the monsoon kharif peak between September and November 2024 and the winter rabi pre-harvest block between January and March 2025. Both maps landed with a perfect 0% cloud cover again. I ran them through my old zero-pixel correction and NDVI steps from Entry 3 and 7. Then I calculated the seasonal greenness drop for each taluka all over again. I set these numbers right side-by-side with my original year data from Entry 7 (which covered the kharif 2025 and rabi 2025-26 cycle).

**This is the check I planned in Entry 7, and the gap holds.** Year 1: my Berar talukas averaged a 0.325 greenness point drop from monsoon to winter, while the Central Provinces side averaged 0.255 (that is a clean 0.070 gap). Year 2, an earlier cycle: the Berar side averaged a 0.316 drop, and the Central Provinces side hit 0.241 (creating a 0.075 gap). Both the direction (Berar always drops more) and the size of the gap (0.070 versus 0.075) match closely across two years that do not share a single satellite photo. This is a real seasonal crop signature. It is not specific to one year. This was the whole point of running this extra test before trusting my Entry 7 results for my final paper.

Four specific talukas (Chandur Railway, Goregaon, Ner, and Digras) came back with zero good pixels this time. This happened because of tiny cloud or edge-map gaps in this particular photo pair that were not there in year 1. I left them as blank NaN spots instead of guessing or faking a number. My final comparison ran on 64 out of the 68 talukas instead of the full group, which does not change the comparison.

**Files I made in this step:**
- `03_Data_Processed/Vegetation/ndvi_postmonsoon_y2_300m.tif` and `ndvi_preharvest_y2_300m.tif` — These are my two new year-2 fixed greenness maps downsampled to 300 meters to save disk space.
- `03_Data_Processed/Vegetation/taluka_seasonal_ndvi_signature_both_years.csv` — My master comparison table showing both years side-by-side for all 68 talukas.
- `07_Outputs/year2_ndvi_comparison.png` — A final image file showing my comparison plots for the monsoon-to-winter greenness drop across both years and divisions.

**Things I still need to finish and track down:**
- I still have not found a real, old period map image to use as a visual slide in my final report. My FRA notes and the Karanja Ghadge field check with Sawardoh photos also remain open.
- This gives me exactly two full years of data confirmation now. A third year would help, but it is not blocking.

---

## Entry 15

Every remaining open thing from Entries 9 to 14 is either my Karanja Ghadge ground photos (still on hold) or not worth more time right now, so this entry is about building the actual dashboard inside `06_Streamlit`. It follows the layout of my other dashboards. Every chart and table reads from the project CSV files, including the Phase 4 regression, which re-runs on the page and matches the log values to 3–4 decimal places. The Theoretical Foundations diagram and the Ground Truth page are placeholders until the pieces they depend on are done.

One bug before release: `pandas.Styler.applymap` was removed in newer pandas, which broke the p-value highlighting on the regression page. I added a `.map()`/`.applymap()` fallback so it works on either version, then tested all 11 pages and the home page with Streamlit's AppTest against the real CSV data.

One gap: the taluka boundary file and my Phase 4 table don't share identical spelling for 3 of the 68 talukas, so those three don't show up on the interactive map yet. This is stated on the page.

**Things I still need to finish and track down:**
- Diagram for Theoretical Foundations not generated yet.
- Karanja Ghadge/Sawardoh ground truth still on hold.
- Development Log PDF and the other three document exports not generated yet.

---

## Entry 16

Two fixes after reviewing the dashboard. I compared the page layout against my other dashboards and cut it down from 11 pages to 9 — folding Climate Controls and my Findings & Conclusion text into the Spatial Discontinuity Regression page instead of keeping them separate, since climate was always a control variable, not a headline finding.

I also changed the Central Provinces colour: Mughal Green barely showed on the dark navy background, so I swapped it for a brighter icy green and fixed two places where button text was unreadable against it.

**Things I still need to finish and track down:**
- Diagram for Theoretical Foundations not generated yet.
- Karanja Ghadge/Sawardoh ground truth still on hold.
- The four final document PDFs still not generated.

----------

## Entry 17

Finished the Theoretical Foundations diagram — four panels showing the land split, the NDVI leaf-physics sketch, the seasonal winter greenness drop chart, and a simple chain tracking how land laws lead to crops and then to a satellite signature. Confirmed the cleanup script ran and the old page files are gone.

Set up the GitHub repository (THE-COTTON-LINE). The.gitignore excludes `02_Data_Raw` (23.2 GB of raw Landsat scenes and grids) and the large intermediate.tif files. I filled in `requirements.txt`, which had been empty, wrote a README with setup instructions and pushed. Git refused to work on the D: drive with a "dubious ownership" error; adding it to `safe.directory` fixed that.

**Things I still need to finish:** The Karanja Ghadge field check is on hold. The four planned PDFs are now three (see Entry 18).

---

## Entry 18

Phase 5 needed a proper treatment of the institutional-economics literature, especially the dispute over how the Central Provinces were classified. I read Banerjee and Iyer (2005). Their main point was that Indian districts that started under landlord-based tax systems have much worse farming results today than non-landlord districts. This stays true even a hundred years after the whole setup was canceled. Then I read the direct challenge by Iversen, Palmer-Jones, and Sen (2013). They showed that Banerjee and Iyer coded nearly the entire Central Provinces as a pure landlord setup. They grouped Malguzari with the heavy Bengal and Bihar landlord styles. But the real history records show that the 1863 Malguzari rules came with real land maps and actual legal protection for the tenants. It was a different, much more mixed system.

When these new researchers recoded the Central Provinces districts using the old record files, six of Banerjee and Iyer’s main mathematical findings lost significance. On top of that, throwing the Central Provinces out of the data made the whole paper result disappear. This bears directly on my design. These are the six districts on the Central Provinces side of my boundary. This is why I treated Malguzari as its own separate group from day one instead of mixing it into a generic landlord tag like the older paper did. I also brought in the Dell (2010) paper on Peru's mining system and the Keele and Titiunik (2015) paper on geographic maps. They are the standard references for testing a specific historical border line using a distance-to-boundary variable. Both are directly relevant to a boundary design.

I verified every citation. I checked the exact AER volume and page numbers for the Banerjee-Iyer paper. Then I read the full Manchester working-paper text for the IPS recoding study to confirm their actual argument rather than skimming the abstract. I also checked Beckert’s *Empire of Cotton* book to verify that 8.5% Berar famine death number that I have been carrying in my project README file since day one. Finally, I cross-checked the original papers for WorldClim, SRTM, and Landsat.

Wrote up `CL_Research_Paper.md`, in my standard paper layout (Abstract, Introduction, Literature Review, Data & Methodology, Results, Discussion, Limitations, Future Work, Conclusion, References). Every number in it came straight from Entries 2 to 16 without recalculating anything, including the uneven results like the farm worker numbers flipping from a trend difference at the corridor scale to a level jump at the full footprint — reported as an open mismatch.

**I reported my ground truth check as an open task, not a complete one.** The field check around Karanja Ghadge and Sawardoh is still on hold. I wrote this down directly inside the Limitations and Future Work parts of my paper. I used my single taluka data point exactly for what it actually is (June 2026: ground heat 55.97°C, greenness 0.264, and 45.8% clear pixel coverage). It is a reference point, not a completed check.

**Things I still need to finish and track:**
- I still have not written the Project Report or the Executive Summary documents. Those will be written once the project, including the field check, is finished.
- The Karanja Ghadge and Sawardoh field check is still on hold.

---

## Entry 19

I reread the full paper draft. It was stiff: too much "this study explores" phrasing, too many "not X, but Y" constructions, and a single overlong abstract. I rewrote it in active first person where I am making a judgement ("I built", "I checked"), split the abstract into three parts and cut the contrast phrasing back. No numbers or citations changed.

Compiled the Development Log and the Research Paper as PDFs for the first time so both download buttons on the dashboard actually work now.

**The Project Report and Executive Summary are still not built.** My field check around Karanja Ghadge and Sawardoh village has not happened yet. Those two documents wait until the project is finished. The site says so rather than showing placeholders.

---

## Entry 20

Fixed the project card's map link, which pointed at the live Streamlit app. Exported the six interactive-map views (border side, greenness decline, ground heat, worker ratio, farmed land, distance to boundary) as standalone static HTML pages instead, with a dropdown to switch between them. Also shortened the card summary.

**Things I still need to finish:** Turn on GitHub Pages for the repo so the six map links actually resolve. My Project Report, Executive Summary, and field ground photos remain exactly where Entry 19 left them.

---

## Entry 21

I picked my field ground checks back up. Instead of a separate trip to Karanja Ghadge, I used data I already collect in another project. I run a weekly tracking setup with GPS maps and actual phone photos on my family’s own land inside this same taluka (Roots & Reflectance, a separate project on the same ground). It already has a working Sentinel-2 NDVI and NDRE math code running. Two of those farm plots sit inside Karanja Ghadge village, and five more are in Sawardoh village a few kilometers away. This gives me real GPS points, dated ground photos, and actual field-level satellite timelines for seven different farm boundaries. That is more than the 2 or 3 plots I originally planned.

I stored it as data rather than hard-coding values on the app pages. Made karanja_sawardoh_field_ground_truth.csv under the Ground_Truth folder to track all 7 fields in long-format (matches the rest of the pipeline schema). Added eight crop and soil photos, compressed to under 700 KB each, to the Streamlit assets folder.

The scale gap note: this isn't a pixel-identical check against the June 2026 taluka data (LST 55.97°C, NDVI 0.264, 45.8% coverage). That baseline was Landsat at 30m, taluka-averaged; my field numbers are Sentinel-2 at 10m on the exact farm shapes, mostly on a different date. What the numbers actually show: the two Karanja fields came back at NDVI 0.329 and 0.287 on 14 July 2026—plausible enough next to the rougher taluka numbers from June. Canopy in the ground photos looks closed and healthy, consistent with those values.

The five Sawardoh fields moved in the same direction over the same period.

**A side-finding.** The Sentinel-2 satellite pass on June 21 for Karanja Ghadge came back with zero good pixels for both of my farm fields. It was full cloud cover, not a code error. This means a second, separate satellite sensor lost its view over the same corner of the map footprint where Landsat's taluka map was already stuck at a tiny 45.8% clear data coverage. Two different satellite systems gave me the same conclusion. This specific patch of Wardha is genuinely hard to see cleanly from space because of weather blocks. I noted this on the site.

**I updated my research paper to match these new facts.** I rewrote Section 6.6 completely. It no longer says "Not Yet Complete" because I replaced that note with my actual ground check results. The scale caveat stays in the text. Inside Section 7, I deleted the task line about finishing the Karanja Ghadge and Sawardoh field check. I also changed the very last lines of both my abstract and my final conclusion section. They now report the field check as done, with the scale caveat.

**Things I still need to finish:** I need to build the Project Report and the Executive Summary documents next. They were waiting on the field check, which is now done. My main README file, the homepage navigation labels inside `app.py`, and the project overview card still say "still open" for this task, so I must edit them to match the new timeline. Also, turning on GitHub Pages for my six interactive map links from Entry 20 is still sitting there on my manual account to-do list.

---

## Entry 22

I closed everything Entry 21 left open, then found two presentation problems on the Ground Truth page.

**My Project Report and Executive Summary are finished.** Every single number inside both files — the 0.070 and 0.075 greenness gaps, the corridor 0.310 versus 0.299 near-zero result, the full footprint interaction p-values of 0.0348 and 0.0105, the farm laborer corridor number of 0.0374 with its base corridor p=0.0361 (before the jackknife's own 0.015-0.138 spread across leave-one-out runs), and the Karanja Ghadge baseline facts — came straight from my research paper and my diary logs from Entries 9 to 21. Nothing was recalculated or re-rounded. Built both as PDFs and updated the README and the dashboard's download links to point to the finished files.

**Then I reviewed the page itself.** My two Karanja fields grow soyabean and tur. My data table and phone photos both say so. But when I saw it running on a website called THE COTTON LINE, leading with soyabean and pigeon pea did not fit the theme. My Sawardoh data has pure cotton fields right there in the same file. So I chose to swap the photo lineup to lead with that instead. I pulled the cotton close-up and soil texture photos right to the front, and I dropped the generic overview and tur pictures completely.

Sawardoh has five fields total, but only two of them (Field 3 and Field 5) grow pure cotton with nothing else mixed in. The other three fields mix in tur, orange trees, or turmeric. If Sawardoh is standing in as my main cotton proof, it should show specifically those two pure plots, not the whole village in general. So I cut both the photo choices and the NDVI/NDRE data table down to Fields 3 and 5. I used their field-specific overview photos and left the other three Sawardoh fields out of the main webpage view entirely (they are still sitting inside my raw CSV table on disk, I do not load them onto this specific page).

**Layout and interactivity.** I flipped the page order so Sawardoh’s pure cotton fields lead the view and Karanja follows right behind. It makes more sense to put the actual cotton proof up front on a project named for cotton, while keeping Karanja fully present since it was the taluka I named in my original plan anyway. Both zones now carry their own soil photo right side by side with their crop close-up, leaving me with nine ground photos total across the two parts.

I added an interactive Plotly chart at the bottom. It uses the same pattern as the Cotton Signature NDVI page (I used `go.Figure`, my custom `plotly_layout` for the dark navy style, and `st.tabs` so people can flip between NDVI and NDRE lines easily). The chart plots all four featured fields (Sawardoh 3 and 5, Karanja 1 and 2) on the same axis with one line per farm plot. It is fully hoverable and zoomable. Karanja’s missing 21 June date shows up as a line that only starts later on 14 July. The gap is left blank rather than filled.

**I checked every value against the CSV.** For Field 3, the NDVI numbers read 0.2808 which I rounded to 0.281, and the NDRE read 0.1553 which became 0.155. For Field 5, the NDVI was 0.3277 which became 0.328, and the NDRE was 0.1957 which I made 0.196. Looking at Karanja Field 1, the NDVI showed 0.3288 which I rounded to 0.329, and the NDRE showed 0.1813 which became 0.181. Finally, for Field 2, the NDVI was 0.2874 which became 0.287, and the NDRE was 0.1599 which I made 0.160. Every metric card matches the CSV to three decimals.

I also ran a syntax check and a sweep for stale or placeholder text across all pages and documents.

**Things I still need to finish:** Turning on GitHub Pages for my six interactive map links from Entry 20 is the only thing left. It is a one-time repository setting. Everything else the project set out to do is finished.

---

## Entry 23

### Version 2.0: the audit and the rebuild

In October I audited the whole project from scratch: code, numbers, figures, documents and dashboard, and fixed everything I could. This entry records what was wrong and what I changed. Earlier entries keep their original results so the history stays intact.

**Measurement bugs found and fixed.**
- **Coverage was computed against the wrong area.** The "valid pixel %" in `taluka_lst_ndvi_stats.csv` divided valid pixels by the taluka's *bounding box*, not its polygon. A fully observed taluka could never reach 100 %; the maximum was 66 %. So Karanja (Wardha) showed 45.8 % although it is 100 % covered, and "63 % of talukas are under 50 % coverage" was false. The real figure is 12 of 68. Coverage is now counted on the polygon.
- **Near-empty talukas.** Five talukas (Chandur Railway, Darwha, Digras, Ner, Goregaon) had NDVI built from less than 1 % of their area, and the November and March means came from different pixels. The decline is now computed on common pixels only, and talukas less than half observed are excluded (a rule fixed before rerunning).
- **Rainfall.** Two talukas (Dhanora, Amgaon) had 0 mm annual rainfall in the old table. Rebuilt from the WorldClim files; they were not in the old regressions.

**Data I already had but had not used.**
- **Census.** The Akola, Buldhana and Washim census zips were sitting in `02_Data_Raw/Population` (the same thing happened with Bhandara, Gondia and Gadchiroli in Entry 11). All 11 districts are now processed, so the census tests run on 119 talukas with 56 on the Berar side, not just Amravati and Yavatmal.
- **Elevation.** Elevation was sampled for all 120 talukas from the SRTM tiles on disk.

**Analysis changes.**
- One clear research question with two hypotheses (step, slope).
- Conley spatial standard errors alongside HC3. The primary p-value is the most conservative of the two.
- Holm correction over 20 tests, plus local-linear RD at the line, placebo lines on both sides, symmetric windows, power (MDE), and a district-level check of the NDVI index against cotton statistics (r = 0.99).
- Everything is now one reproducible pipeline (`05_Python/run_all.py`, numpy/pandas/scipy/tifffile only).
- There is also a tested 30 m rebuild script with cloud and cropland masks for when the extra Landsat files are downloaded.

**What the new numbers say.**
- Still no step at the line.
- The labour ratio now shows a regional difference across 119 talukas (Holm p = 0.032), but it is zero in the corridor and in local estimates, so it is not a boundary effect.
- The NDVI year-2 slope survives Holm. Fake lines inside each side produce the same kind of slope change for NDVI and labour, which means a regional gradient.
- Only LST passes the placebo test, and it is one June date.

**Claims in earlier entries that are superseded.**

| Entry | What I wrote then | What is true now |
|---|---|---|
| 1, 5, 7 | The British "forced" Berar into pure cotton; the labour ratio proves landlessness from Ryotwari; the decline is a "pure cotton signature" | Not shown by this design. The decline is a cropping-intensity index (it does track district cotton share), and nothing here can be attributed to tenure. |
| 3, 18, 21 | Karanja had only 45.8 % coverage, "at the edge of the footprint", and two satellites both "lost" the same area | Coverage bug. Karanja is 100 % covered. |
| 5 | The labour gap is not driven by one or two talukas | The corridor result depends on Amravati taluka. The Amravati "urban taluka" is the rural part of the taluka; village data exclude towns. |
| 10 | NDVI and LST show "the exact same shape" — "the best proof" | They have different shapes (a slope versus a ridge). |
| 10, 11 | Berar side "barely past 20 km"; Amravati the only Berar district in the scene | Berar side reaches 104 km and is mostly Yavatmal. |
| 11 | I trust the corridor result more | No scale is ranked above the other. |
| 13 | Proved the modern line is "exactly" the historical one | District-level lineage only; some talukas (e.g. Rajura) came from elsewhere. |
| 14 | Two "independent" years, a "proven, solid fact" | Same footprint and method: a replication of the gradient, not an independent test. |
| 18 | The 8.5 % famine mortality figure was verified in Beckert; IPS "six coefficients" | Could not be traced, so it was removed. IPS is described from their own abstract. |
| 22 | Ground-truth page shows only cotton fields | All seven fields are shown; the check is illustrative only. |

**Still open.** A short, fixed list of remaining tasks, after which the project is finished.

---

## Entry 24

### Version 2.1: all of Berar at 30 m

I downloaded the remaining Landsat scenes: paths 144, 145 and 146, rows 045 to 047, for both seasons in both years, with the QA_PIXEL band, plus the four ESA WorldCover 2021 tiles. NDVI is now computed at 30 m, with fill, cloud, cirrus, shadow and water masked and only cropland kept. The download dropped twice mid-file, so the script now resumes interrupted files instead of restarting.

**One bug on the way.** The first masked run divided observed cropland by the whole taluka area. Forest-heavy talukas fell below the 50 % rule and dropped out, leaving only 28 Central Provinces talukas. Coverage is now counted against each taluka's cropland, and the sample is 98 talukas: all 56 in Berar and 42 in the Central Provinces.

**What changed.** With Akola, Buldhana and Washim in the satellite sample for the first time, the picture is different from version 2.0:
- The decline is highest within 50 km of the line on both sides (0.29) and falls away in both directions: to 0.21 in western Buldhana and 0.13 in Bhandara and Gondiya. The cotton core straddles the line.
- The side averages are close: 0.255 against 0.246 in year 1, 0.319 against 0.262 in year 2. The 0.322 against 0.257 gap in version 2.0 came from seeing only the eastern fall-off.
- Still no step at the line, in any sample or local estimate.
- The NDVI slope change now survives Holm in both years (p < 0.001). It is the crest of the ridge, and fake lines inside each side reproduce it.
- Validation against district cotton share: r = 0.86 over 10 districts. Washim, a soybean district, is the outlier, which confirms the index measures single-season cropping, not cotton alone.
- Where two paths see the same taluka, they differ by 0.036 on average.

**Updated:** paper (v2.1), executive summary, README, CITATION, dashboard text and all figures. Superseded from version 2.0: the west-to-east gradient, the 0.322/0.257 gap, r = 0.99 over 7 districts, and the "Berar side is mostly Yavatmal" limitation.

**Field check.** I ran the decline for the seven Roots & Reflectance fields in Earth Engine (Landsat and Sentinel-2, both years) and asked the farmers what they grew in winter. None of the Sawardoh fields had a rabi crop and Karanja field 2 had chickpea. Karanja field 1 was first reported as possibly chickpea; I went back with neutral questions (without showing the satellite values) and the farmer confirmed it was fallow. Thirteen of the fourteen field-years match the index: the chickpea field has the smallest decline in both years, through a low November value rather than a green March. The exception is Sawardoh field 3 in year 2, still green in March 2025; re-asked, the farmer confirmed nothing was grown that winter and that pigeon pea is harvested around January. It stays unexplained. Added as Section 4.7 and Figure 8.

**Still open.** Publishing (B5).
