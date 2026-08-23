# The Cotton Line — Executive Summary

**Sakshi D. Maske**
Independent Geospatial Researcher

---

## The Question

In 1853 the British annexed Berar — five districts in western Vidarbha — directly into colonial administration and pushed it into cotton monoculture under a Ryotwari land-tenure system. The six districts to its east made up the Central Provinces, settled instead under Malguzari, a landlord-intermediary system. That line was erased administratively in 1956, but it runs almost exactly along today's Amravati Division / Nagpur Division boundary. This project asks a narrow, testable version of a much bigger question: does that 150-year-old institutional line still register as a measurable spatial signature in present-day cotton-crop phenology, agrarian labor structure, land use, and land-surface temperature — once rainfall and elevation are controlled for?

## Approach

I built a 384.7 km modern boundary by dissolving 120 talukas into the two historical divisions and extracting their shared edge, then verified it against documented district administrative lineage from 1903–1956 rather than assuming the modern line matched the historical one. Every outcome was tested with a spatial-discontinuity regression — separating a sharp jump right at the boundary from a difference in slope with distance from it — run on both a 32-taluka immediate corridor and a 66–68-taluka full regional footprint, with rainfall and elevation controlled throughout. The cotton-signature NDVI result was confirmed across two independent annual satellite cycles, not a single season.

## Key Findings

No outcome — cotton-signature NDVI decline, agrarian labor structure, land use, or land-surface temperature — showed a statistically significant level jump right at the historical boundary, at either the corridor or the full-footprint scale, once geography was controlled for. That absence of a sharp discontinuity is reported directly, not dressed up as a weaker version of a positive result.

What does hold up is a real regional gradient. The kharif-to-rabi NDVI decline — the core cotton-monoculture signature — was 0.070 points larger on the historical Berar side than the Central Provinces side in one year (0.325 vs. 0.255, 68 talukas), and came back almost identical a year later on an independent set of scenes (0.074-point gap). At the full-footprint scale, both NDVI decline and land-surface temperature showed a statistically significant side-by-distance interaction (p = 0.0348 and p = 0.0105 respectively) — two physically independent Earth-observation channels trending differently with distance from the old line, even though neither jumps sharply at it. The agricultural-laborer-to-cultivator ratio adds a more qualified third line of evidence: a slope difference at the corridor scale that held direction under jackknife resampling but wasn't fully robust to which taluka got dropped, and that flips into a different-shaped result at the full-footprint scale — reported as a genuine scale sensitivity, not smoothed over.

A historical-lineage check confirms the modern boundary used throughout is, as far as documented administrative history shows, the same line as the 1853–1956 Berar/Central Provinces boundary.

## Ground-Truth Validation

The remote-sensing signal this project runs on was checked against real, GPS-mapped field conditions at seven field boundaries in Karanja Ghadge and Sawardoh villages — inside the corridor, on the Central Provinces side — drawing on a separate field-monitoring project on the same land. Field-level Sentinel-2 NDVI came back in a plausible range next to the coarser taluka-level Landsat reference, and dated ground photographs show canopy conditions consistent with those readings. The check is reported with an explicit scale caveat (10 m field-level vs. 30 m taluka-level, different sensor, mostly different dates) rather than as a tighter validation than it actually is.

## What This Means

The honest reading is a real institutional-geography legacy that shows up as a gradient strengthening away from the historical line, rather than a discontinuity right where the institutions themselves were once drawn — a more precise finding than either a clean boundary effect or a flat null would have been, even if it's a quieter one. Full methodology, every regression coefficient, robustness checks, and the complete ground-truth record are in the Research Paper and on the project's live dashboard.
