import streamlit as st
import plotly.graph_objects as go
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import safe_read_csv, output_path, show_image_or_placeholder

st.set_page_config(page_title="Cotton Signature (NDVI) — THE COTTON LINE", page_icon="🌾", layout="wide")
inject_theme()

st.markdown("<h1>🌾 THE COTTON SIGNATURE: KHARIF-TO-RABI NDVI DECLINE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>The Core Phase 3 Outcome Variable, "
    "Confirmed Across Two Independent Growing Years</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
A big NDVI drop between the kharif peak (post-monsoon, cotton canopy fullest) and the rabi
pre-harvest period means the land goes back to bare/fallow once the kharif crop comes off -- a
single-crop (cotton) signature. A smaller drop means a rabi crop follows the kharif one and keeps
the land green through winter -- a mixed-cropping signature. See Theoretical Foundations for the
physical basis.
""")

df = safe_read_csv("Vegetation", "taluka_seasonal_ndvi_signature_both_years.csv")

if df is None:
    st.warning("taluka_seasonal_ndvi_signature_both_years.csv not found yet.")
else:
    means = df.groupby("division")[["kharif_to_rabi_decline", "kharif_to_rabi_decline_y2"]].mean()
    berar_y1 = means.loc["Amravati (Berar)", "kharif_to_rabi_decline"]
    cp_y1 = means.loc["Nagpur (Central Provinces)", "kharif_to_rabi_decline"]
    berar_y2 = means.loc["Amravati (Berar)", "kharif_to_rabi_decline_y2"]
    cp_y2 = means.loc["Nagpur (Central Provinces)", "kharif_to_rabi_decline_y2"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Year 1 — Berar", f"{berar_y1:.3f}", "Kharif 2025 → Rabi 2025-26")
    c2.metric("Year 1 — Central Provinces", f"{cp_y1:.3f}", f"Gap: {berar_y1 - cp_y1:.3f}")
    c3.metric("Year 2 — Berar", f"{berar_y2:.3f}", "Kharif 2024 → Rabi 2024-25")
    c4.metric("Year 2 — Central Provinces", f"{cp_y2:.3f}", f"Gap: {berar_y2 - cp_y2:.3f}")

    st.markdown(f"""
    <div class="recon-card" style="margin-top:8px;">
        <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">
            The check this project needed
        </p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.92rem; line-height:1.6; margin:0;">
            Two independent annual cycles that share not a single scene reproduce almost exactly
            the same gap ({berar_y1 - cp_y1:.3f} vs {berar_y2 - cp_y2:.3f}), and in the same
            direction every time -- Berar always declines more. That's a real seasonal cropping
            signature, not something that happened to show up in one unusual season.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Distribution by Division, Both Years")
    tab1, tab2 = st.tabs(["Year 1 (2025 / 2025-26)", "Year 2 (2024 / 2024-25)"])

    with tab1:
        fig1 = go.Figure()
        for div, color in [("Amravati (Berar)", PALETTE["berar"]), ("Nagpur (Central Provinces)", PALETTE["cp"])]:
            fig1.add_trace(go.Box(
                y=df[df["division"] == div]["kharif_to_rabi_decline"],
                name=div, marker_color=color, boxmean=True,
            ))
        fig1.update_layout(yaxis_title="Kharif-to-rabi NDVI decline", showlegend=False)
        st.plotly_chart(plotly_layout(fig1, height=420), use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        for div, color in [("Amravati (Berar)", PALETTE["berar"]), ("Nagpur (Central Provinces)", PALETTE["cp"])]:
            fig2.add_trace(go.Box(
                y=df[df["division"] == div]["kharif_to_rabi_decline_y2"],
                name=div, marker_color=color, boxmean=True,
            ))
        fig2.update_layout(yaxis_title="Kharif-to-rabi NDVI decline (Year 2)", showlegend=False)
        st.plotly_chart(plotly_layout(fig2, height=420), use_container_width=True)

    n_valid = df["kharif_to_rabi_decline_y2"].notna().sum()
    st.caption(
        f"Year 2 ran on {n_valid} of {len(df)} talukas -- 4 talukas (Chandur Railway, Goregaon, "
        "Ner, Digras) had no valid year-2 pixels due to small cloud/edge-coverage gaps in that "
        "scene pair, left as NaN rather than guessed."
    )

st.markdown("---")

st.markdown("### Seasonal Trajectory")
col_a, col_b, col_c = st.columns([0.1, 5.9, 0.1])
with col_b:
    show_image_or_placeholder(
        output_path("seasonal_ndvi_signature.png"),
        caption="Figure. NDVI trajectory across June (pre-sowing), kharif peak, and rabi/pre-harvest, "
                "both divisions -- and the decline boxplot, Year 1.",
    )
    show_image_or_placeholder(
        output_path("year2_ndvi_comparison.png"),
        caption="Figure. The kharif-to-rabi decline, both years, both divisions, side by side.",
    )

st.markdown("---")

st.info("""
**Worth being upfront about:** I want to be completely honest here -- this gap basically
vanishes at the immediate corridor (0.310 vs 0.299, across the 29 corridor talukas with usable NDVI). The reason is that Central
Provinces talukas closest to the boundary (Wardha, Nagpur, Chandrapur) grow a huge amount of
cotton themselves, so right at the line the two sides actually look very similar compared to
what the region-wide averages suggest. The effect is definitely real across the whole regional
map, but it gets stronger as you move further away from the boundary instead of making a sharp
step-jump right over it. See Spatial Discontinuity Regression for the actual statistical test of
that shape.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Cotton Signature (NDVI)</p>",
    unsafe_allow_html=True,
)
