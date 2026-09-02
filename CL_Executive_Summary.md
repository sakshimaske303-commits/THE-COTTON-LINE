# The Cotton Line — Executive Summary

**Sakshi D. Maske**
Independent Geospatial Researcher

---

## Overview

When it comes to these problems such as market prices of crops and rain, most people usually find a answer, why is the farmer under such stress in Vidarbha? I wanted to know if there is any deeper seated reason which is embedded in the very topography and morphology of the land itself. That is because very much the same question can be traced back to a border between two distinct land use systems set up by the British during a period of colonial rule when land was divided in the colonial state in 1853: on the west-side, they forced the implementation of the pure cotton set-up of Berar and on the east-side of the Malguzari set-up on mixed farming of the Central Provinces. I won't draw conclusions about that old border line that was erased in 1956, but it's what I'm here to do with the satellite data and census books; check to see if it still separates two sides today.

## The Question

Once the natural variations in rainfalls and topography were removed from the equation, does a 150-year-old law show up on satellite images of heat, crop greenness and ratios of farm workers? That's the very straightforward testable question that I'm asking. It comes back to 1853 when the British captured Berar and imposed on the five districts almost full-fledged cotton cultivation to placate their large cloth mills back in England, and began to impose on the more mixed farming six districts to the east their own landlord system. This administrative map line was officially wiped off the maps in 1956, and it is still an almost exact match to the division line border today.

## Approach

I created the line of the border, which is 384.7 km long. This line was formed by overlaying the 120 taluka shapes within the two old historical blocks and then I looked at the old map papers from offices of 1903 to 1956 to draw up history — I didn't want to simply assume that the current map line was the same as the old colonial one without any proof. To differentiate between an abrupt level change at the line due to such a rapid-level jump and a gradual level change at the line with distance due to a recent trend, I performed a special spatial boundary jump math test (ordinary least squares models), one way with a narrow corridor with 32 talukas, and another with a much wider satellite footprint with 68 talukas. Lastly, because I wanted to make sure my findings were representative of a consistent trend rather than a single odd season of weather, I was able to compare the crop greenness numbers from two entirely separate years.

## Key Findings

There is no point trying to fake a major jump when the equations just don't add up, hence just writing the zero result down at the exact "old historical" line: Absolutely no outcome, whether it is crop greenness drops, farm labourer counts, land use and ground heat, etc., shows a sudden sharp mathematical level jump right at the old historical line. Once geography is blocked out, it remains level at the tight corridor level and wide regional level.

But there was a key regional trend found nonetheless. In the first test year, the winter crop greenness drop, which measures the pure cotton signature, came out 0.070 points bigger on the old Berar side than on the Central Provinces side, with the gap at 0.325 versus 0.255 across 68 talukas. A year earlier, on a completely separate independent satellite cycle, this same greenness drop held up again — 0.075 points bigger on the Berar side, at 0.316 versus 0.241. Both channels of greenness drops and ground heat numbers exhibited a significant side-by-distance trend interaction, where p=0.0348 and p=0.0105 respectively (and neither of these exhibits a sharp step-jump right at the border seam itself), on the big footprint map.

Where it gets more complex is the farm labourer ratio. Within its "tight corridor" area it exhibits a slope difference (p=0.0361) that remains positive as I remove one talei (taluka) at a time, but flips abruptly into a "big flat jump" (p=0.014) when I open up the entire lopsided footprint. I am recording this straight as a scale issue because well I was seeing a big part of the interior with the satellite path and only a small sliver of the interior Berar side of course.

Not only did I do all of this, but I also did one additional investigation that my modern border line is where my old colonial border line is. As these records of the district office did not offer any usable digitized period map, I used those records for the period 1903-1956 rather than a map, and as far as those records can reveal, my modern Amravati/Nagpur Division line is identical to the old Berar/Central Provinces line.

## Ground-Truth Validation

The plots at seven field boundaries in Karanja Ghadge and Sawardoh villages which are in the corridor are on the Central Provinces side where I conducted a double check on my data obtained through orbital satellites with the ground reality of the farms. No need to make an explicit trip for this, I already have a GPS with coordinates and phone pictures of such family fields each week for another project. The match-up was good: my refined 10-meter crop line product for Sentinel-2 is matching up quite closely with the coarser 30-meter crop-line product for Landsat, and my blurry old phone images of green, healthy crop leaves are appearing exactly on top of where my Sentinel-2 values would predict that to be. Be aware of one big warning about this check: the sensors, pixel coverage and dates are all different, so one should not consider this as a 1-to-1 match.

## What This Means

There is obviously a geography legacy on the fields left over with the old colonial land laws but not the form of sharp jump right where old lines were drawn. On the other hand, it gives a slow trend which becomes more pronounced as you go deeper into the thing – a much more detailed and interesting observation for my concluding paper than either a clean step-jump or a flat zero result would have been. All of my math models, each individual regression number, and all of my pictures of my raw grounds are viewable inside my main Research Paper and on my live website dashboard.