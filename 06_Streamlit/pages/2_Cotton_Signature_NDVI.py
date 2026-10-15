import streamlit as st
import plotly.graph_objects as go
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import load_analysis, load_result, key_numbers, output_path, show_image_or_placeholder

st.set_page_config(page_title="Cotton Signature (NDVI) — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>THE NOVEMBER-TO-MARCH NDVI DECLINE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>A Cropping-Intensity Index from Landsat, "
            "Two Years, Checked Against Cotton Statistics</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
The index is the fall in NDVI between an early-November and an early-March Landsat scene, averaged
over the pixels of each taluka that are valid **on both dates** (common pixels). A large fall means
the land loses its green cover after the monsoon crop; a small fall means a second crop, irrigation
or perennial cover keeps it green. It is a cropping-intensity index, not a direct cotton detector.

**How the taluka values are built (30 m, Landsat paths 144-146):**
- **Fill, cloud, cirrus, shadow and water pixels are masked** using DN = 0 and the QA_PIXEL band.
- **Only cropland is kept,** using ESA WorldCover 2021 (class 40).
- **Coverage is counted against the taluka's cropland.**
- **Talukas with less than half their cropland observed are left out** (5 of 103).
""")

D = load_analysis()
K = key_numbers()
if D is None:
    st.warning("Run `python 05_Python/run_all.py` to build the analysis dataset.")
    st.stop()

fp = D[D.eo_ok_y1]
c1, c2, c3, c4 = st.columns(4)
g1 = fp.groupby("side").ndvi_decline_y1.mean()
g2 = D[D.eo_ok_y2].groupby("side").ndvi_decline_y2.mean()
c1.metric("Year 1 — Berar", f"{g1[1]:.3f}", "Nov 2025 → Mar 2026")
c2.metric("Year 1 — Central Provinces", f"{g1[0]:.3f}", f"gap {g1[1] - g1[0]:.3f}")
c3.metric("Year 2 — Berar", f"{g2[1]:.3f}", "Nov 2024 → Mar 2025")
c4.metric("Year 2 — Central Provinces", f"{g2[0]:.3f}", f"gap {g2[1] - g2[0]:.3f}")

st.info(f"""
**A ridge, not a step.** The decline is highest within 50 km of the line on both sides (0.29) and
falls away towards Buldhana in the west and the paddy districts in the east, so the side averages
are close and the gap moves between years. Taluka values correlate at
r = {K.get('y1_y2_corr', float('nan')):.2f} between years. Both years use the same scenes and
method, so year 2 **replicates the regional pattern**; it is not an independent test of the
boundary.

**Near the line the sides are almost identical** (0.294 against 0.290 in the corridor, year 1).
Once distance is in the model there is no step at the line (see Spatial Discontinuity Regression).

**Who is in the sample.** All 56 Berar talukas and 42 Central Provinces talukas. Gadchiroli and
most of Gondiya lie outside the scenes used.
""")

st.markdown("### Distribution by side")
tab1, tab2 = st.tabs(["Year 1 (2025-26)", "Year 2 (2024-25)"])
for tab, col, ok in [(tab1, "ndvi_decline_y1", "eo_ok_y1"), (tab2, "ndvi_decline_y2", "eo_ok_y2")]:
    with tab:
        d = D[D[ok]]
        fig = go.Figure()
        for side, name, color in [(1, "Berar", "#eb6834"), (0, "Central Provinces", "#2a78d6")]:
            fig.add_trace(go.Box(y=d[d.side == side][col], name=f"{name} (n={int((d.side == side).sum())})",
                                 marker_color=color, boxmean=True))
        fig.update_layout(yaxis_title="NDVI decline (common pixels)", showlegend=False)
        st.plotly_chart(plotly_layout(fig, height=400), use_container_width=True)

st.markdown("---")
show_image_or_placeholder(output_path("v2_fig3_seasonal_ndvi.png"),
                          caption="Mean NDVI in early November and early March by side, and the decline by side. "
                                  "Talukas valid in both years.")
st.markdown("### Does the index track cotton?")
show_image_or_placeholder(output_path("v2_fig6_validation_cotton_share.png"),
                          caption=f"District mean decline against APY cotton share: r = {K.get('validation_r', float('nan')):.2f} "
                                  f"(7 districts), r = {K.get('validation_r_cotton_districts', float('nan')):.2f} "
                                  "without the two paddy districts. A sanity check with 7 points, not a calibration.")
st.markdown("<p class='caption-text' style='text-align:center;'>THE COTTON LINE — NDVI decline</p>",
            unsafe_allow_html=True)
