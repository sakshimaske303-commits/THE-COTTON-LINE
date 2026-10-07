# The Cotton Line — Executive Summary

**Sakshi D. Maske**
Independent Geospatial Researcher

---

## Overview

Explanations of farm distress in Vidarbha usually focus on rainfall and crop prices. I wanted to test a different possibility: that part of the regional pattern reflects an older administrative divide. In the nineteenth century, Berar (five districts in the west: Amravati, Akola, Buldhana, Washim, Yavatmal) was administered under the Ryotwari land-revenue system, in which each cultivator dealt directly with the state. The districts of the Nagpur region to the east (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli) were settled under Malguzari, in which an intermediary landholder answered for the whole estate. That provincial boundary was abolished in 1956, but it corresponds at district level to today's line between Amravati Division and Nagpur Division. This project uses satellite and census data to ask whether the old line is still detectable.

## The Question

After controlling for distance to the line, rainfall and elevation, is there a measurable break at the old Berar/Central Provinces boundary in crop greenness change, land surface temperature, agrarian labour structure, or land use?

## Approach

I built the boundary as a 384.7 km line by dissolving 120 taluka polygons into the two historical divisions and extracting their shared edge. I checked it against district lineage from 1903 to 1956 (no digitised period map was available), so the verification is at district level and not a geometric overlay. I then ran a spatial-discontinuity regression (ordinary least squares with a side indicator, signed distance, their interaction, rainfall and elevation) on two samples: a 32-taluka corridor around the line and a 68-taluka Landsat footprint. Crop greenness change is measured as the fall in NDVI from a November scene to a March scene, in two separate years. I added robust standard errors, multiple-testing correction, symmetric distance windows, placebo cutoffs and coverage tests, all reproducible with `05_Python/robustness_checks.py`.

## Key Findings

There is no boundary-specific step in NDVI change, land surface temperature or net cultivated area, at either scale. Reporting that null result is part of the finding.

The raw NDVI decline is larger on the Berar side: 0.325 against 0.255 in year one (68 talukas) and 0.316 against 0.241 in year two. Near the line the gap almost disappears (0.310 against 0.299 in the corridor), and once distance is in the model the boundary term is close to zero. This is a regional gradient, not a boundary effect. Both years use the same footprint and method, so year two replicates the gradient and does not independently test a boundary effect.

On the full footprint the side-by-distance interaction is significant for NDVI decline (p = 0.035) and for land surface temperature (p = 0.011). The two do not share a shape: NDVI decline falls from west to east with a flatter Berar side, while temperature is highest near the line and falls with distance on both sides. The temperature interaction is robust to robust standard errors and symmetric windows; the NDVI interaction is not (p = 0.080 with HC3 errors, p = 0.27 without the most influential taluka).

The agricultural-labourer-to-cultivator ratio behaves differently by scale. In the corridor there is a slope difference (p = 0.036) that depends on one urban taluka (p = 0.138 without Amravati). On the full footprint there is a level difference (Berar higher by 0.62, p = 0.014) that holds in symmetric distance windows (p = 0.004 to 0.041) but not under district-clustered errors, and it rests on two Berar districts only.

Sixteen coefficients were tested. Four are significant at 5%, where chance alone would give about one, and none survives a Holm correction. The results are therefore exploratory.

## Ground-Truth Check

I compared the satellite signal with seven field boundaries in Karanja Ghadge and Sawardoh (Wardha district, Central Provinces side, 16 to 24 km from the line), using data from a separate family field-monitoring project. This is an illustrative check only. It uses Sentinel-2 data from June and July 2026 for young crops, not the November-to-March decline analysed in the paper, and it covers one side of the boundary, so it cannot validate the Berar versus Central Provinces difference.

## What This Means

A regional gradient in cropping intensity and surface temperature coincides with the old boundary, but the analysis cannot attribute it to Ryotwari or Malguzari tenure. The line is also an older political frontier between the Nizam's Berar and the Bhonsle territory, a river line, and an agro-ecological transition. The main limitations are spatial autocorrelation that is not fully modelled, single-date scenes without cloud-shadow masking, 2011 census data compared with 2024–26 satellite data, and a Berar-side census sample of only two districts. The full analysis, all figures and every regression are in the research paper and the dashboard.
