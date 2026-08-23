import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import data_path, safe_read_csv, show_image_or_placeholder, STREAMLIT_DIR

st.set_page_config(page_title="Ground Truth — THE COTTON LINE", page_icon="📸", layout="wide")
inject_theme()

GT_ASSETS = os.path.join(STREAMLIT_DIR, "assets", "ground_truth")


def gt_image(filename, caption=None):
    show_image_or_placeholder(os.path.join(GT_ASSETS, filename), caption=caption)


st.markdown("<h1>📸 GROUND TRUTH: KARANJA GHADGE / SAWARDOH</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>A Real Methodological Check on the "
    "Remote-Sensing Signal</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:12px;">
        This check is complete
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0;">
        I didn't end up doing a separate field trip for this. I already had a GPS-mapped, weekly-
        photographed field-monitoring project running on family land in this exact taluka —
        Karanja Ghadge village and Sawardoh village, both Wardha district, both inside this
        project's 25 km corridor on the Central Provinces/Malguzari side. That gave me GPS
        coordinates, dated ground photos, and an actual field-level Sentinel-2 NDVI/NDRE time
        series for 7 real field boundaries, which is more evidence than the original 2–3-patch
        plan below called for.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### The Original Plan")

st.markdown("""
Karanja Ghadge sits inside the 25km discontinuity corridor, on the Central Provinces/Malguzari
side. The idea: photograph a few actual field patches with GPS coordinates, note visible crop
type, canopy density, and soil texture, then pull the NDVI/LST value at those coordinates and
compare against what the ground actually shows. That plan is what's carried out below — through
data I already had rather than a dedicated visit.
""")

st.markdown("### What's Already On Record For This Taluka")

c1, c2, c3 = st.columns(3)
c1.metric("June 2026 LST", "55.97°C", "Karanja Ghadge taluka mean")
c2.metric("June 2026 NDVI", "0.264", "Karanja Ghadge taluka mean")
c3.metric("Valid Pixel Coverage", "45.8%", "Partly outside the 2-scene footprint")

st.info("""
Coverage is partial here since Karanja Ghadge sits at the edge of the WRS-2 path 144, rows
045/046 scene footprint this project's NDVI/LST pipeline uses. Worth keeping that in mind
against everything below — this taluka-level number was never a full-confidence read either.
""")

st.markdown("---")

st.markdown("### Read This Before The Numbers Below")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.75; margin:0;">
        This isn't a pixel-identical check against the taluka number above, and I don't want it to
        read like one. That reference point comes from Landsat 8/9 at 30 m resolution, averaged
        across the whole taluka. What's below comes from Sentinel-2 at 10 m resolution, computed at
        the exact field polygon, from a pipeline I built for an unrelated project on the same land.
        Different sensor, different footprint size, mostly different dates. What this actually
        checks is whether the same kind of signal — a vegetation index tracking real crop growth —
        shows up consistently at finer resolution, against something I can see with my own eyes.
        It isn't a claim that the two numbers should match to three decimal places.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

gt_df = safe_read_csv("Ground_Truth", "karanja_sawardoh_field_ground_truth.csv")

# ============================================================
# SAWARDOH — cotton-only fields
# ============================================================
st.markdown("### Sawardoh — Cotton-Only Fields")

st.markdown("""
Sawardoh is a village inside the same Karanja Ghadge taluka, about 7 km from the two Karanja
fields below. It has five field boundaries in total, but Fields 3 and 5 are the ones featured
here — both sit alone across the road from the other three, and both are cotton-only, with no
pigeon pea, orange, or turmeric mixed in. For a project called The Cotton Line, that's the
cleaner comparison: no intercropping to complicate what the NDVI signature is actually responding
to. Both were sown 22 June 2026, and both moved the same direction as everywhere else in this
check — NDVI roughly doubling between 21 June and 14 July as canopy filled in.
""")

if gt_df is not None:
    sawardoh_df = gt_df[(gt_df["role"] == "supporting") & (gt_df["field_num"].isin([3, 5]))].copy()
    sawardoh_df = sawardoh_df[["field_num", "name", "date", "ndvi", "ndre"]]
    sawardoh_df.columns = ["Field", "Crop", "Date", "NDVI", "NDRE"]
    st.dataframe(sawardoh_df, use_container_width=True, hide_index=True)
else:
    st.info("Ground-truth CSV not found at 03_Data_Processed/Ground_Truth/ yet.")

sw1, sw2 = st.columns(2)
with sw1:
    st.metric("Field 3 — Cotton only", "NDVI 0.281 · NDRE 0.155", "14 Jul 2026, 0.78 ha")
with sw2:
    st.metric("Field 5 — Cotton only", "NDVI 0.328 · NDRE 0.196", "14 Jul 2026, 0.66 ha")

st.markdown("#### Ground Photos — 23 August 2026")

sf1, sf2 = st.columns(2)
with sf1:
    gt_image("sawardoh-field3-2026-08-23-overview.jpeg", "Field 3 (Cotton only) — canopy overview")
with sf2:
    gt_image("sawardoh-field5-2026-08-23-overview.jpeg", "Field 5 (Cotton only) — canopy overview")

s1, s2 = st.columns(2)
with s1:
    gt_image("sawardoh-shared-2026-08-23-cotton.jpeg", "Cotton close-up — early boll formation visible")
with s2:
    gt_image("sawardoh-shared-2026-08-23-soil.jpeg", "Soil texture — reddish-brown, finer than Karanja Ghadge's black soil")

st.markdown("---")

# ============================================================
# KARANJA GHADGE — the named taluka check
# ============================================================
st.markdown("### Karanja Ghadge — The Named Taluka Check")

st.markdown("""
Two fields, both sown 27 June 2026, about 100 m apart, in Karanja Ghadge itself — the exact
taluka the original plan named. Both lost their 21 June Sentinel-2 pass entirely to cloud
masking — not a processing error, an actual empty read for that date at 10 m resolution. The
only clean date so far is 14 July 2026, three weeks after sowing.
""")

if gt_df is not None:
    karanja_df = gt_df[gt_df["role"] == "primary"].copy()
    karanja_df = karanja_df[["field_num", "name", "crops", "area_ha", "sown_date", "lat", "lon", "date", "ndvi", "ndre"]]
    karanja_df.columns = ["Field", "Crop", "Crops (raw)", "Area (ha)", "Sown", "Lat", "Lon", "Date", "NDVI", "NDRE"]
    st.dataframe(karanja_df, use_container_width=True, hide_index=True)

k1, k2 = st.columns(2)
with k1:
    st.metric("Field 1 — Soyabean & Tur", "NDVI 0.329 · NDRE 0.181", "14 Jul 2026, 0.79 ha")
with k2:
    st.metric("Field 2 — Soyabean", "NDVI 0.287 · NDRE 0.160", "14 Jul 2026, 0.98 ha")

st.markdown("#### Ground Photos — 23 August 2026")

p1, p2 = st.columns(2)
with p1:
    gt_image("karanja-field1-2026-08-23-overview.jpeg", "Field 1 (Soyabean & Tur) — full canopy overview")
with p2:
    gt_image("karanja-field2-2026-08-23-overview.jpeg", "Field 2 (Soyabean) — full canopy overview")

p3, p4, p5 = st.columns(3)
with p3:
    gt_image("karanja-shared-2026-08-23-soyabean.jpeg", "Soyabean canopy close-up")
with p4:
    gt_image("karanja-shared-2026-08-23-tur.jpeg", "Pigeon pea (tur) close-up")
with p5:
    gt_image("karanja-shared-2026-08-23-soil.jpeg", "Soil texture — dark, clumpy, cracked-surface")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.75; margin:0;">
        Both photos show closed-canopy, healthy-looking soyabean at roughly eight weeks after
        sowing, with pigeon pea running taller between the rows — consistent with an NDVI reading
        in the 0.29–0.33 range rather than a stressed or sparse one. The soil photo is dark,
        clumpy, and cracked on the surface — the same regur (black cotton soil) texture this whole
        project is built around, on the Central Provinces side of the line.
    </p>
    <p style="color:{PALETTE['text_secondary']}; font-size:0.88rem; line-height:1.7; margin:14px 0 0;">
        One more thing worth flagging rather than glossing over: the 21 June date is also <em>before</em>
        Karanja's actual sowing (27 June), so even a valid reading that day would have shown bare or
        pre-monsoon soil, not crop canopy. The useful comparison point was always going to be 14
        July, not 21 June — that field being empty in the data isn't a gap in the finding.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CROSS-SENSOR OBSERVATION
# ============================================================
st.markdown("### A Small Cross-Sensor Observation")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.75; margin:0;">
        Two independent pipelines, two independent sensors, and both lost data over this exact
        corner of Wardha district. Landsat's taluka-level pass came back at only 45.8% valid pixel
        coverage; Sentinel-2's 21 June pass over these same two Karanja fields came back with no
        usable pixels at all. That's not proof of anything on its own, but it's a small piece of
        corroborating evidence that Karanja Ghadge genuinely sits at the edge of reliable
        satellite coverage, regardless of which platform is looking — worth remembering the next
        time either pipeline reports a number for this taluka.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# INTERACTIVE: NDVI / NDRE ACROSS ALL FOUR FEATURED FIELDS
# ============================================================
st.markdown("### Interactive: NDVI & NDRE, All Four Featured Fields")

st.markdown("""
The same four fields above, plotted together — Sawardoh's two cotton-only fields and Karanja's
two fields, all on the same axis. Karanja's missing 21 June point is a real gap, not smoothed
over: the line simply starts at its first valid date.
""")

if gt_df is not None:
    featured = gt_df[
        ((gt_df["zone"] == "sawardoh") & (gt_df["field_num"].isin([3, 5])))
        | ((gt_df["zone"] == "karanja") & (gt_df["field_num"].isin([1, 2])))
    ].copy()
    featured["date"] = pd.to_datetime(featured["date"])
    featured["label"] = featured["zone"].str.title() + " Field " + featured["field_num"].astype(str)

    FIELD_COLORS = {
        "Karanja Field 1": PALETTE["accent"],
        "Karanja Field 2": "#5AA9BE",
        "Sawardoh Field 3": PALETTE["accent2"],
        "Sawardoh Field 5": "#4FBE85",
    }

    tab_ndvi, tab_ndre = st.tabs(["NDVI", "NDRE"])

    with tab_ndvi:
        fig_ndvi = go.Figure()
        for label, color in FIELD_COLORS.items():
            sub = featured[featured["label"] == label].dropna(subset=["ndvi"]).sort_values("date")
            fig_ndvi.add_trace(go.Scatter(
                x=sub["date"], y=sub["ndvi"], mode="lines+markers", name=label,
                line=dict(color=color, width=3), marker=dict(size=9),
            ))
        fig_ndvi.update_layout(yaxis_title="NDVI", xaxis_title="Date", yaxis_range=[0, 0.5])
        st.plotly_chart(plotly_layout(fig_ndvi, height=440), use_container_width=True)

    with tab_ndre:
        fig_ndre = go.Figure()
        for label, color in FIELD_COLORS.items():
            sub = featured[featured["label"] == label].dropna(subset=["ndre"]).sort_values("date")
            fig_ndre.add_trace(go.Scatter(
                x=sub["date"], y=sub["ndre"], mode="lines+markers", name=label,
                line=dict(color=color, width=3), marker=dict(size=9),
            ))
        fig_ndre.update_layout(yaxis_title="NDRE", xaxis_title="Date", yaxis_range=[0, 0.3])
        st.plotly_chart(plotly_layout(fig_ndre, height=440), use_container_width=True)

    st.caption(
        "Karanja's two fields (sown 27 June) only have one valid date -- 14 July -- so their lines "
        "are a single point each rather than a slope; Sawardoh's two cotton fields (sown 22 June) "
        "have both dates and show the actual rise. All four sit in a plausible, tightly-clustered "
        "range by mid-July regardless of crop."
    )
else:
    st.info("Ground-truth CSV not found -- chart will render once it's in place.")

st.markdown("---")

# ============================================================
# WHAT THIS CONFIRMS
# ============================================================
st.markdown("### What This Confirms")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.75; margin:0;">
        The remote-sensing signal this project runs on holds up against what's actually growing on
        the ground, at seven real field boundaries I can personally vouch for. NDVI rises through
        the season the way it should as canopy closes in, the finer-resolution Sentinel-2 numbers
        sit in a plausible range next to the coarser taluka-level Landsat reference for the same
        stretch of land, and the one gap in the record (Karanja's 21 June pass) has an honest
        explanation rather than an invented one. This is a small-sample, single-taluka check, not a
        blanket validation of every outcome variable elsewhere in the project — it speaks to NDVI
        specifically, at these coordinates, this season. Reported as that, not as more.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    f"<p class='caption-text' style='text-align:center;'>Field boundaries, photos, and Sentinel-2 "
    f"NDVI/NDRE sourced from a separate family field-monitoring project on the same land "
    f"(Roots &amp; Reflectance) · Ground photos dated 23 Aug 2026 · Compiled for THE COTTON LINE</p>",
    unsafe_allow_html=True,
)
