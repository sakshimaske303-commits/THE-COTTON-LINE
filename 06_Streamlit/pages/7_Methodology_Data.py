import streamlit as st
import pandas as pd
from utils.theme import inject_theme, PALETTE

st.set_page_config(page_title="Data & Methodology — THE COTTON LINE", page_icon="🛰️", layout="wide")
inject_theme()

st.markdown("<h1>🛰️ DATA &amp; METHODOLOGY</h1>", unsafe_allow_html=True)
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
    "Coverage": ["All 11 Vidarbha districts, 120 talukas", "WRS-2 path 144, rows 045/046 (68-taluka footprint)",
                 "Same 2-scene footprint as NDVI", "All 120 talukas", "9-11 SRTM tiles, corridor + full footprint",
                 "All 11 districts (8 processed by Entry 11)", "All 11 districts", "State/regional + 1 district anchor (Gadchiroli)"],
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
        cloud-masked and off-swath pixels -- roughly a third of every scene. An early version of
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

st.markdown("### Scope Decisions, Stated Plainly")

st.markdown("""
- **Corridor vs. full footprint.** LST/NDVI processing initially covered only the 2-scene,
  68-taluka footprint that overlaps the corridor most efficiently -- not a full 11-district, 12-scene
  mosaic. That footprint happens to be lopsided (49 Central Provinces talukas to 19 Berar talukas),
  since the scene simply covers more CP-side territory. This matters directly for how one Phase 4
  result (the ag-laborer ratio) should be read -- see Spatial Discontinuity Regression.
- **Population/land-use census coverage.** Started at 5 of 11 districts (the corridor-relevant
  ones), extended to 8 of 11 by Entry 11 once the Bhandara/Gondiya/Gadchiroli shapefiles -- already
  downloaded, never processed -- were run through the same pipeline. Gadchiroli's processed data has
  no corresponding NDVI/LST scene coverage, so it's saved but unused in the current regression.
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
