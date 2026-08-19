# Missing-Taluka Shapefile Gap — SOLVED

## Source found

**`datta07/INDIAN-SHAPEFILES`** on GitHub — `INDIA/INDIAN_SUB_DISTRICTS.geojson`
(https://github.com/datta07/INDIAN-SHAPEFILES). This is a Census 2011 / Local Government
Directory (LGD)-linked sub-district (taluka/tehsil) boundary dataset covering all of India,
5,966 features, CRS EPSG:4326, zero invalid/empty/null geometries.

Filtered to your 11 Vidarbha districts: **120 talukas total**, and the per-district counts match
known official taluka counts exactly (cross-checked against Wikipedia/Census figures):

| District | Talukas |
|---|---|
| Nagpur | 14 |
| Wardha | 8 |
| Bhandara | 7 |
| Gondia | 8 |
| Chandrapur | 15 |
| Gadchiroli | 12 |
| Amravati | 14 |
| Akola | 7 |
| Washim | 6 |
| Yavatmal | 16 |
| Buldhana | 13 |
| **Total** | **120** |

## What was actually wrong with your original shapefiles

Comparing this complete source against your original (pre-dissolve-fix) shapefiles by taluka
name, two separate problems turn out to have been mixed together in the earlier QA:

**7 districts had genuinely missing talukas** (not a duplicate/sliver issue — the taluka was
simply never in the file):

- **Nagpur** — missing 5 of 14: Hingna, Kalameshwar, Mauda, Nagpur (Rural), Nagpur (Urban)
- **Wardha** — missing 1 of 8: Hinganghat
- **Gondia** — missing 1 of 8: Arjuni Morgaon
- **Gadchiroli** — missing 1 of 12: Desaiganj (Vadasa)
- **Amravati** — missing 2 of 14: Chandurbazar, Nandgaon-Khandeshwar
- **Yavatmal** — missing 1 of 16: Zari-Jamani
- **Buldhana** — missing 4 of 13: Chikhli, Deolgaon Raja, Jalgaon (Jamod), Sindkhed Raja

**4 districts (Bhandara, Chandrapur, Akola, Washim) were already complete** — every taluka name
that should exist was present; the only issue there was the duplicate/sliver-polygon rows fixed
earlier with the dissolve script. Those two problems (missing talukas vs. duplicate rows of
existing talukas) are independent — fixing one doesn't fix the other, which is why the gap
persisted even after the dissolve fix.

## Files delivered

- `vidarbha_talukas_complete.geojson` — all 120 talukas, all 11 districts, one file (EPSG:4326).
- `taluka_shapefiles_complete/<district>/<district>_talukas.shp` (+`.shx/.dbf/.prj/.cpg`) — one
  shapefile per district, matching your existing `02_Data_Raw/Administrative/<district>/` folder
  layout. Also zipped as `<district>_talukas_complete.zip` for easier transfer.
- `taluka_gap_comparison_report.txt` — the full old-vs-new name comparison this README is based
  on.

## Attribute fields

`stname` (state), `dtname` (district), `sdtname` (taluka name — this is the one to match to your
existing `taluka_nam` column), `sdtcode11` / `Subdt_LGD` (sub-district codes — LGD code is the
more current/stable identifier), `Dist_LGD`, `State_LGD`, plus `Shape_Length`/`Shape_Area`.

## Recommended next step in QGIS

This is a genuinely different, independently-sourced dataset from your original files — it will
NOT have identical boundary topology/vertex placement, even though the taluka set is now
complete. Two reasonable paths:

1. **Simplest:** replace your `02_Data_Raw/Administrative/<district>/<district>.shp` files with
   these complete ones outright, re-run the dissolve/QA scripts to confirm zero issues, and
   redo any downstream taluka-level joins from a clean base.
2. **If you want to keep your original files' exact boundary style:** use this complete dataset
   only to digitize/add the specific missing talukas listed above into your existing files, so
   the rest of your existing work (any taluka-level data already joined) doesn't need to be
   redone.

Given you're this late in the project, option 1 (clean replace) is probably less error-prone
than partial digitizing — but that's your call depending on how much taluka-level analysis
you've already built on the old files.
