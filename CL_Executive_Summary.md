# The Cotton Line — Executive Summary

**Sakshi D. Maske**
Independent Geospatial Researcher

---

## Overview

I am testing if an old 1853 colonial land law border line in Vidarbha still leaves a real mark on the ground today. On the west side, the British set up the Ryotwari system to force a pure cotton setup (Berar). On the east side, they used the Malguzari landlord setup for mixed farming (Central Provinces). This old border line was officially wiped off the maps back in 1956. My main goal is to use satellite data and census books to see if that old line still separates the two sides today. People usually blame things like rain or market prices for why farmers face so much stress in Vidarbha. I wanted to see if there is a deeper, older reason built right into the geography of the land itself. 

## The Question

The British took over Berar in 1853 and forced five districts to grow almost nothing but cotton to feed their big cloth mills back in England. The other six districts to the east sat under a completely different landlord system with more mixed crops. Even though that administrative map line died in 1956, it matches today's division border line almost perfectly. I am asking a very direct, testable question here. Does that 150-year-old law line still show up on satellite heat maps, crop greenness charts, and village worker ratios once I block out the natural differences in rain and ground height?

## Approach

I built a 384.7 km border map line by merging 120 taluka shapes into the two old historical blocks. Then I dug up old office papers from 1903 to 1956 to cross-check the history. I did not want to just guess that the modern map line matched the old colonial one without real proof. I ran a special spatial boundary jump math test (running ordinary least squares models) to separate a sudden level jump at the line from a slow trend changing with distance. I ran these math models on both a tight 32-taluka corridor and a much wider 68-taluka satellite footprint. Finally, I tracked the crop greenness numbers across two completely separate years to prove my findings show a steady pattern, not just one weird weather season.

## Key Findings

My data shows that absolutely no outcome—whether it is crop greenness drops, farm laborer counts, land use, or ground heat—shows a sudden, sharp mathematical level jump right at the old historical line. This zero result stays flat at both the tight corridor scale and the wide regional footprint once geography is blocked out. I am writing this zero result down directly in my papers (I see no point in trying to fake a major jump when the math simply says it is not there).

But I did find a very real regional trend. The winter crop greenness drop—which tracks the pure cotton signature—was 0.070 points bigger on the old Berar side during my first test year (0.325 versus 0.255 across 68 talukas). It came back almost completely identical a year earlier in my second independent satellite cycle with a 0.074 gap. On the big footprint map, both greenness drops and ground heat numbers showed a significant side-by-distance trend interaction. The p-values hit p=0.0348 and p=0.0105. This shows that two completely separate satellite channels change at different speeds as you move away from the old line, even if neither shows a sharp step-jump right at the border seam. 

The farm laborer ratio gives me a more mixed story. It shows a slope difference inside the tight corridor area (p=0.0361) that stays positive when I drop talukas out one-by-one. But this trend completely flips into a sudden level jump (p=0.014) when I expand to the full lopsided footprint. I am documenting this directly as a scale issue because the satellite path views a massive chunk of the Central Provinces interior but only a tiny sliver of the Berar side.

On top of all this, I also went back and checked whether my modern border line actually sits where the old colonial one used to. I traced the district office records from 1903 to 1956 instead of relying on an old map, since I never found a usable digitized one. As far as those records can show, my modern Amravati/Nagpur Division line is the same line as the old Berar/Central Provinces boundary.

## Ground-Truth Validation

I double-checked my orbital satellite data against real farm ground reality at seven field boundaries in Karanja Ghadge and Sawardoh villages. These plots sit inside the corridor on the Central Provinces side. I did not have to plan a separate trip because I already track these family fields weekly with GPS coordinates and phone photos for another project. My sharp 10-meter Sentinel-2 crop lines match up very well with the rougher 30-meter Landsat taluka numbers on disk. Plus, my dated phone photos show thick, green, healthy crop leaves exactly where the satellite values predict them. I am reporting this check with a very clear warning that the sensors, pixel block sizes, and dates are completely different so people do not assume it is a perfect match.

## What This Means

My honest summary of the project is simple. The old colonial land laws left a real geography legacy on the fields, but it shows up as a slow trend that gets stronger as you move deep into the interior, not as a sharp jump right where the old lines were drawn. This is a much more precise and interesting finding for my final paper than a clean step-jump or a totally flat zero result. You can view my full math models, every single regression number, and my raw ground photos directly inside my main Research Paper and on my live website dashboard.
