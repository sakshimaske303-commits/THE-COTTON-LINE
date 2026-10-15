import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import safe_read_csv, show_image_or_placeholder, STREAMLIT_DIR, load_analysis

st.set_page_config(page_title="Ground Truth — THE COTTON LINE", layout="wide")
inject_theme()
GT = os.path.join(STREAMLIT_DIR, "assets", "ground_truth")

st.markdown("<h1>FROM REGION TO FIELD</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>Seven Fields in Karanja Taluka, "
            "from the Companion Study Roots &amp; Reflectance</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown(f"""
<div class="recon-card">
<p style="color:{PALETTE['accent2']}; font-weight:800; text-transform:uppercase; font-size:0.85rem;">What this page is, and is not</p>
<p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.6; margin:0;">
The Cotton Line works at taluka scale with Landsat. <b>Roots &amp; Reflectance</b>, my field study,
follows seven farm fields in Sawardoh and Karanja Ghadge villages (Karanja taluka, Wardha) with GPS
boundaries, weekly geotagged photos and every Sentinel-2 pass. The fields lie on the Central
Provinces side, 15.6-24.3 km from the line. This page uses them to show what the satellite
record looks like at field scale.
<br><br>
It checks what the satellite index means on fields with known crops. It covers one side of the line,
so it cannot validate the Berar versus Central Provinces comparison.</p></div>
""", unsafe_allow_html=True)

D = load_analysis()
if D is not None:
    k = D[(D.dtname == "Wardha") & (D.sdtname == "Karanja")].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Karanja taluka — Landsat coverage", f"{k.cov_y1_pct:.0f} %", "of the taluka, both dates")
    c2.metric("NDVI decline, year 1", f"{k.decline_y1:.3f}", "Nov 2025 → Mar 2026")
    c3.metric("LST, 20 June 2026", f"{k.lst_june:.1f} °C", "pre-monsoon, bare fields")
    c4.metric("Distance to the line", f"{abs(k.signed_dist_km):.1f} km", "Central Provinces side")
    st.caption("An earlier version reported 45.8 % coverage for this taluka 'at the edge of the scene'. "
               "That was a calculation error (pixels divided by the bounding box); the taluka is fully covered.")

st.markdown("### Why the main study uses November and March scenes")
st.markdown("""
Roots & Reflectance audited every Sentinel-2 pass over these fields after sowing in June 2026.
No field had a usable optical look between 14 July and mid-September: **65-75 days, the weeks the
crop grew most**. A monsoon-season greenness measure would therefore be largely unobserved in this
region. This is why The Cotton Line measures cropping from the post-monsoon (November) and
pre-harvest (March) scenes, when the sky is clear.
""")

st.markdown("### Does the decline index read these fields correctly?")
st.markdown("""
The same November-to-March decline, computed on each field from Landsat and Sentinel-2 for both
years, against what the farmers recall growing in winter. Six fields had no rabi crop and show large
declines (11 of 12 field-years at or above the taluka mean). Karanja field 2 had rabi chickpea and
shows the smallest decline in both years, through a low November value: the soybean was already
harvested and the chickpea just sown. The exception is Sawardoh field 3 in year 2, still green in
March 2025 although the farmer confirms nothing was grown. **13 of 14 field-years match.**
""")
show_image_or_placeholder(os.path.join(os.path.dirname(STREAMLIT_DIR), "07_Outputs", "v2_fig8_field_bridge.png"),
                          caption="Winter crops from farmers' recall, re-checked for two fields.")

gt = safe_read_csv("Ground_Truth", "karanja_sawardoh_field_ground_truth.csv")
if gt is not None:
    st.markdown("### All seven fields: Sentinel-2 NDVI and NDRE, June-July 2026")
    t = gt[["village", "field_num", "name", "area_ha", "sown_date", "date", "ndvi", "ndre"]].copy()
    t.columns = ["Village", "Field", "Crops", "Area (ha)", "Sown", "Date", "NDVI", "NDRE"]
    st.dataframe(t.round(3), use_container_width=True, hide_index=True)
    gt["date"] = pd.to_datetime(gt["date"])
    gt["label"] = gt.village + " " + gt.field_num.astype(str) + " (" + gt.name + ")"
    fig = go.Figure()
    for lab, g in gt.dropna(subset=["ndvi"]).groupby("label"):
        fig.add_trace(go.Scatter(x=g.date, y=g.ndvi, mode="lines+markers", name=lab))
    fig.update_layout(yaxis_title="NDVI (field polygon, Sentinel-2 10 m)", yaxis_range=[0, 0.5])
    st.plotly_chart(plotly_layout(fig, height=420), use_container_width=True)
    st.caption("21 June is the day before sowing (bare soil). The Karanja fields have no 21 June value "
               "because cloud covered them. NDVI of 0.28-0.36 on 14 July is a young canopy about three "
               "weeks after sowing, not closed cover. Different sensor, date and quantity from the "
               "Landsat November-to-March decline: not a pixel-for-pixel check.")

st.markdown("### Ground photos, 23 August 2026")
p = st.columns(3)
for col, (f, cap) in zip(p * 3, [
    ("sawardoh-field3-2026-08-23-overview.jpeg", "Sawardoh field 3 — cotton"),
    ("sawardoh-field5-2026-08-23-overview.jpeg", "Sawardoh field 5 — cotton"),
    ("sawardoh-field1-2026-08-23-overview.jpeg", "Sawardoh field 1 — cotton and tur"),
    ("karanja-field1-2026-08-23-overview.jpeg", "Karanja field 1 — soyabean and tur"),
    ("karanja-field2-2026-08-23-overview.jpeg", "Karanja field 2 — soyabean"),
    ("sawardoh-shared-2026-08-23-cotton.jpeg", "Cotton close-up, Sawardoh"),
    ("sawardoh-shared-2026-08-23-soil.jpeg", "Soil, Sawardoh — reddish-brown"),
    ("karanja-shared-2026-08-23-soil.jpeg", "Soil, Karanja Ghadge — dark, cracking (black cotton soil)"),
    ("karanja-shared-2026-08-23-tur.jpeg", "Pigeon pea (tur), Karanja"),
]):
    with col:
        show_image_or_placeholder(os.path.join(GT, f), caption=cap)

st.markdown("""
**What the fields add.** Two villages 9 km apart differ in soil: reddish-brown in Sawardoh, black
cotton soil in Karanja Ghadge. They also differ in crop mix, with cotton dominant in Sawardoh and
soyabean with tur in Karanja. That is a reminder that taluka averages blend very different fields.
The full field study, with its observability audit, pixel-purity analysis and rabi-season field
alerts, is in the Roots & Reflectance repository.
""")
st.markdown("<p class='caption-text' style='text-align:center;'>Field boundaries, photos and Sentinel-2 values: "
            "Roots &amp; Reflectance (Sakshi D. Maske)</p>", unsafe_allow_html=True)
