import streamlit as st
import pandas as pd
from utils.theme import inject_theme, PALETTE

st.set_page_config(page_title="Data & Methodology — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>DATA &amp; METHODOLOGY</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Sources, a Real Processing Bug and Its Fix, "
    "and the Scope Decisions Behind Every Number on This Dashboard</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### Data Sources")

sources = pd.DataFrame({
    "Category": ["Administrative boundaries", "Vegetation (NDVI)", "Climate (LST)", "Hydrology",
                 "Terrain", "Population & land use", "Agriculture", "Economics (FRA)"],
    "Source": ["IIT Bombay POCRA Maharashtra Census shapefile portal", "Landsat 8/9 Collection 2 Level-2, Bands 4/5",
               "Landsat 8/9 Collection 2 Level-2, thermal Band 10", "WorldClim 2.1 monthly precipitation climatology",
               "SRTM 1 arc-second (~30m) digital elevation tiles", "IIT Bombay POCRA village-level Census shapefiles",
               "APY 2024-25 workbook, Maharashtra Economic Survey 2025-26", "State Tribal Development Dept + fact-finding reports (contextual only)"],
    "Coverage": ["120 talukas, 11 districts (Census 2011 / LGD sub-districts)", "WRS-2 paths 144-146, rows 045-047; 98 talukas >= 50 % of cropland observed",
                 "One June scene, path 144; 56 talukas", "All 120 talukas", "All 120 talukas (centroid)",
                 "All 11 districts, 119 talukas; 2011 Census attributes, rural villages", "11 districts, district-level values only", "State/regional + 1 district anchor (Gadchiroli)"],
})
st.dataframe(sources, use_container_width=True, hide_index=True)

st.markdown("---")

st.markdown("### The DN=0 Bug, Found and Fixed")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:10px;">
        A real pipeline bug, not a data-source problem
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.92rem; line-height:1.65; margin:0;">
        Landsat Collection 2 Level-2 scenes use <strong>DN=0</strong> as the fill/no-data value for
        off-swath pixels -- roughly a third of every scene. It does not mark clouds: no QA_PIXEL
        cloud or shadow mask has been applied yet, and scenes were chosen by low scene-level cloud
        cover only. An early version of
        this project's LST and NDVI pipeline applied the Kelvin/reflectance scale-and-offset
        directly to the raw digital number without masking DN=0 out first, which produces exactly
        149K = &minus;124.15&deg;C for those fill pixels -- an impossible land-surface temperature
        that was silently sitting in the merged rasters as fake data. The fix: mask DN=0 as NoData
        <em>before</em> applying the scale/offset, not after, then reprocess. Every LST and NDVI
        number on this dashboard is from the corrected pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Masks, Coverage and Common Pixels")
st.markdown("""
- **NDVI is computed at 30 m** from nine Landsat scenes per date (paths 144-146, rows 045-047).
  Fill, cloud, cirrus, shadow and water are masked with the QA_PIXEL band, and only ESA WorldCover
  2021 cropland is kept.
- **The decline uses only pixels valid on both dates,** so November and March describe the same fields.
- **Coverage is counted against the taluka's cropland** (LST: against the polygon). The first
  version divided by the taluka's bounding box, which made complete talukas look half-empty;
  Karanja in Wardha was shown at 45.8 % but is 100 % covered.
- **Talukas with less than half their cropland observed are excluded:** 5 of the 103 the scenes touch.
- **Paths agree.** Where two paths see the same taluka, their values differ by 0.036 on average.
""")
st.markdown("---")
st.markdown("### Reproducibility")
st.markdown("""
`python 05_Python/run_all.py` rebuilds every table, result and figure from the data in the
repository, using numpy, pandas, scipy, matplotlib and tifffile. `--full` also rebuilds the 30 m
NDVI table from the raw scenes downloaded by `00_download_inputs.py`. Order: geometry → census → NDVI/LST
and rainfall → elevation → analysis dataset → regressions and robustness → figures.
""")
st.markdown("---")
st.markdown("### Scope Decisions, Stated Plainly")

st.markdown("""
- **Satellite footprint.** NDVI covers paths 144-146: all of Berar (to 228 km) and the Central
  Provinces side to 156 km. Gadchiroli and most of Gondiya (path 143) are not covered. LST is a
  single path-144 scene.
- **Census coverage.** All 11 districts are now processed (119 talukas). Census outcomes are tested
  on every taluka, not only those inside the Landsat footprint.
- **Irrigation coverage, dropped.** The census `area_irri` field produced 58-92% irrigation rates
  across Yavatmal villages, which flatly contradicts the well-documented fact that this cotton belt
  is overwhelmingly rainfed (real regional coverage is closer to 15-20%). Left out rather than
  reported at a value that isn't trusted.
- **MGNREGA / malnutrition columns, dropped.** The District Indicators PDF's columns 52-59 didn't
  extract with confident column alignment. Skipped rather than risk a mislabeled number.
- **FRA data, treated as narrative, not quantitative.** No clean taluka- or district-level Forest
  Rights Act dataset exists in the public domain for Vidarbha. What's compiled (Historical &
  Institutional Context page) is a sourced set of figures at state/regional/single-district scale --
  useful institutional-history color, not a variable that can do statistical work in the Phase 4
  regression.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Data &amp; Methodology</p>",
    unsafe_allow_html=True,
)
