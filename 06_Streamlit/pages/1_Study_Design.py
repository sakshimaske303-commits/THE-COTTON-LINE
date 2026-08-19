import streamlit as st
from utils.theme import inject_theme, PALETTE
from utils.data import data_path, show_image_or_placeholder

st.set_page_config(page_title="Study Design — THE COTTON LINE", page_icon="🗺️", layout="wide")
inject_theme()

st.markdown("<h1>🗺️ STUDY DESIGN</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Building the Modern Boundary, "
    "the Discontinuity Corridor, and the Test Itself</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
The two historical zones are stood in for by their modern division equivalents: **Amravati
Division** (Akola, Amravati, Buldhana, Washim, Yavatmal) for the old Berar/Ryotwari territory, and
**Nagpur Division** (Nagpur, Wardha, Bhandara, Gondia, Chandrapur, Gadchiroli) for the old Central
Provinces/Malguzari territory -- confirmed, not just assumed, on the Historical & Institutional
Context page. All 120 talukas across the 11 districts were dissolved into these two division
polygons, and the shared edge between them was extracted as the boundary line itself.
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Boundary Line Length", "384.7 km", "Akola/Amravati/Wardha → Yavatmal/Chandrapur")
with col2:
    st.metric("Corridor Width", "±25 km", "Either side of the line")
with col3:
    st.metric("Berar-Side Corridor Area", "7,387 km²", "Amravati Division")
with col4:
    st.metric("CP-Side Corridor Area", "7,987 km²", "Nagpur Division")

st.markdown("---")

col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    show_image_or_placeholder(
        data_path("Administrative", "boundary_verification_map.png"),
        caption="Figure. The two dissolved divisions, the 384.7 km boundary line, and the 25 km "
                "discontinuity corridor, checked against the full taluka grid for gaps or overlaps at the seam.",
    )

st.markdown("---")

st.markdown("### Two Sample Scales, Used Deliberately")

s1, s2 = st.columns(2)
with s1:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 210px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px;">32-Taluka Corridor</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            The 32 talukas falling inside the ±25 km corridor (15 Berar side, 17 Central Provinces
            side) -- the tightest, most literal test of "does the effect jump right at the old
            line." Smallest sample, most statistical-power-limited, but the most spatially honest
            reading of a discontinuity right at the boundary itself.
        </p>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 210px;">
        <p style="color: {PALETTE['accent2']}; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px;">68-Taluka Full Footprint</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            The full extent of the two Landsat scenes (WRS-2 path 144, rows 045/046) covering the
            NDVI and LST data -- 68 talukas across the whole scene, not just the corridor. Much
            better statistical power, at the cost of moving away from strict "right at the
            boundary" logic. Used as a deliberate robustness check on the corridor-only result, not
            a replacement for it.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### The Model")

st.latex(r"\text{outcome} = \beta_0 + \beta_1 \cdot side + \beta_2 \cdot signed\_dist\_km + \beta_3 \cdot (side \times signed\_dist\_km) + controls + \varepsilon")

st.markdown("""
A standard spatial-discontinuity setup, run via OLS (`statsmodels`) -- **not** a
difference-in-differences, event-study, or synthetic-control design, since there's no treatment
date here, only a spatial line. `side` (1 = Berar, 0 = Central Provinces) captures a level jump
right at the boundary -- the literal discontinuity test. The `side × signed_dist_km` interaction
captures whether the *slope* with distance from the boundary differs by side, independent of any
level jump. `signed_dist_km` is each taluka centroid's distance to the dissolved division boundary
line (computed in UTM 44N, signed positive on the Berar side). Rainfall and elevation are included
as controls, since Entry 8 confirmed a real west-drier/east-wetter climate gradient across
Vidarbha that has nothing to do with the historical land-tenure line and needs to be netted out
before any boundary effect can be trusted.
""")

st.markdown("---")

st.markdown("### Hypotheses")

h1, h2, h3 = st.columns(3)
with h1:
    st.info("**H1**\n\nCotton-signature NDVI decline jumps at the boundary (`side` significant), "
            "once rainfall and elevation are controlled for.")
with h2:
    st.info("**H2**\n\nAgrarian labor structure (ag-laborer-to-cultivator ratio) shows the same "
            "level jump, and it holds at both the corridor and full-footprint scale.")
with h3:
    st.info("**H3**\n\nThe modern Amravati/Nagpur Division boundary is, in fact, the same line "
            "as the historical Berar/Central Provinces one -- not just a convenient stand-in.")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Study Design</p>",
    unsafe_allow_html=True,
)
