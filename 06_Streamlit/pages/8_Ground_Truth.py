import streamlit as st
from utils.theme import inject_theme, PALETTE

st.set_page_config(page_title="Ground Truth — THE COTTON LINE", page_icon="📸", layout="wide")
inject_theme()

st.markdown("<h1>📸 GROUND TRUTH: KARANJA GHADGE / SAWARDOH</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>A Real Methodological Check on the "
    "Remote-Sensing Signal — Coming Soon</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:12px;">
        This page is a placeholder
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0;">
        Field photos from Sawardoh village, Karanja Ghadge taluka (Wardha district), have not been
        added yet. The plan and the pixel values this check will be compared against are already
        recorded below — the field visit itself is still to be scheduled.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### The Plan")

st.markdown("""
Karanja Ghadge sits inside the 25km discontinuity corridor, on the Central Provinces/Malguzari
side. The idea: photograph 2-3 actual field patches around Karanja Ghadge with GPS coordinates,
note visible crop type, canopy density, and soil moisture, then pull the exact NDVI/LST pixel value
at those coordinates and compare against what the ground actually shows. This becomes a dedicated
ground-truthing spotlight — a real check on whether the satellite-derived signal used everywhere
else in this project actually matches physical reality on site, not just another data point.
""")

st.markdown("### What's Already on Record for This Taluka")

c1, c2, c3 = st.columns(3)
c1.metric("June 2026 LST", "55.97°C", "Karanja Ghadge taluka mean")
c2.metric("June 2026 NDVI", "0.264", "Karanja Ghadge taluka mean")
c3.metric("Valid Pixel Coverage", "45.8%", "Partly outside the 2-scene footprint")

st.info("""
Coverage is partial here since Karanja Ghadge sits at the edge of the WRS-2 path 144, rows
045/046 scene footprint this project's NDVI/LST pipeline uses — worth keeping in mind when the
field comparison eventually runs: the pixel value being checked against isn't from full-confidence
coverage.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Ground Truth (to be completed)</p>",
    unsafe_allow_html=True,
)
