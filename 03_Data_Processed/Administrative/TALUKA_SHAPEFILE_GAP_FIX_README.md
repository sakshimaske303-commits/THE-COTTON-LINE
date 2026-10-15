# Taluka shapefile gap: fixed

## Source

`datta07/INDIAN-SHAPEFILES` on GitHub, `INDIA/INDIAN_SUB_DISTRICTS.geojson`
(https://github.com/datta07/INDIAN-SHAPEFILES). Census 2011 / LGD-linked sub-district boundaries for
all of India: 5,966 features, EPSG:4326, no invalid or empty geometries.

Filtered to the 11 Vidarbha districts it gives **120 talukas**, matching the official per-district counts:

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

## What was wrong with the original shapefiles

Two separate problems had been mixed together.

**Missing talukas in 7 districts** (never in the file):

- **Nagpur**: 5 of 14 missing (Hingna, Kalameshwar, Mauda, Nagpur (Rural), Nagpur (Urban))
- **Wardha**: Hinganghat
- **Gondia**: Arjuni Morgaon
- **Gadchiroli**: Desaiganj (Vadasa)
- **Amravati**: Chandurbazar, Nandgaon-Khandeshwar
- **Yavatmal**: Zari-Jamani
- **Buldhana**: 4 of 13 missing (Chikhli, Deolgaon Raja, Jalgaon (Jamod), Sindkhed Raja)

**Duplicate and sliver rows** in Bhandara, Chandrapur, Akola and Washim, which were otherwise complete.
The dissolve script fixed these. The two problems are independent, which is why the gap remained after
the dissolve fix.

## Files

- `vidarbha_talukas_complete.geojson`: all 120 talukas in one file (EPSG:4326).
- `taluka_shapefiles_complete/<district>/<district>_talukas.shp` (+ `.shx/.dbf/.prj/.cpg`): one
  shapefile per district, same layout as `02_Data_Raw/Administrative/<district>/`.
- `taluka_gap_comparison_report.txt`: the full old-vs-new name comparison.

## Attribute fields

`stname`, `dtname`, `sdtname` (taluka name; joins to `taluka_nam`), `sdtcode11` / `Subdt_LGD`
(LGD is the stable identifier), `Dist_LGD`, `State_LGD`, `Shape_Length`, `Shape_Area`.

## Decision

I replaced the original files with this complete set and rebuilt all taluka-level joins from it
(`03_Data_Processed/Administrative/vidarbha_talukas_120.geojson`). Its vertex placement differs
from the old files, so partial patching would have left mismatched edges.
