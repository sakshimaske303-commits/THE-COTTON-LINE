import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import safe_read_csv, output_path, show_image_or_placeholder

st.set_page_config(page_title="Agrarian & Land Structure — THE COTTON LINE", page_icon="👥", layout="wide")
inject_theme()

st.markdown("<h1>👥 AGRARIAN &amp; LAND STRUCTURE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Cotton Dependency, Labor Structure, "
    "Land Use, and Holding Size</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

DIV_COLORS = {"Amravati (Berar)": PALETTE["berar"], "Nagpur (Central Provinces)": PALETTE["cp"]}

# ============================================================
# DISTRICT-LEVEL AGRARIAN INDICATORS
# ============================================================
st.markdown("### District-Level: Cotton Share and Net Sown Area")

agr = safe_read_csv("Agriculture", "vidarbha_agrarian_indicators.csv")
if agr is None:
    st.warning("vidarbha_agrarian_indicators.csv not found yet.")
else:
    tab1, tab2 = st.tabs(["Cotton share of cropped area", "Net sown area"])
    with tab1:
        fig = px.bar(agr.sort_values("cotton_share_pct", ascending=False), x="district", y="cotton_share_pct",
                     color="division", color_discrete_map=DIV_COLORS)
        fig.update_layout(yaxis_title="Cotton share of cropped area (%)", xaxis_title="")
        st.plotly_chart(plotly_layout(fig, height=420), use_container_width=True)
        st.caption(
            "Noisier than a clean west/east story: Yavatmal (51%) and Wardha (49%) -- one Berar, "
            "one Central Provinces -- are nearly tied for highest. Cotton was never confined to "
            "old Berar; the British pushed it hardest there, but it spread into neighboring "
            "Central Provinces districts too."
        )
    with tab2:
        fig = px.bar(agr.sort_values("net_sown_pct", ascending=False), x="district", y="net_sown_pct",
                     color="division", color_discrete_map=DIV_COLORS)
        fig.update_layout(yaxis_title="Net sown area (% of geographical area)", xaxis_title="")
        st.plotly_chart(plotly_layout(fig, height=420), use_container_width=True)
        berar_std = agr[agr["division"] == "Amravati (Berar)"]["net_sown_pct"].std()
        cp_std = agr[agr["division"] == "Nagpur (Central Provinces)"]["net_sown_pct"].std()
        st.caption(
            f"The cleaner divide: all five Amravati Division districts sit in a tight band "
            f"(std. dev. {berar_std:.1f}); Nagpur Division spreads from Gadchiroli's forest-heavy "
            f"14% to Nagpur's 57% (std. dev. {cp_std:.1f}) -- Ryotwari brought all of Berar under "
            f"the plough uniformly, Malguzari CP stayed a mix of heavily-cultivated and "
            f"heavily-forested/estate land."
        )

st.markdown("---")

# ============================================================
# AG-LABORER RATIO
# ============================================================
st.markdown("### Agricultural-Laborer-to-Cultivator Ratio (Corridor)")

pop = safe_read_csv("Population", "corridor_taluka_population_stats.csv")
if pop is None:
    st.warning("corridor_taluka_population_stats.csv not found yet.")
else:
    means = pop.groupby("division")["ag_laborer_to_cultivator"].mean()
    lit = pop.groupby("division")["literacy_pct"].mean()
    c1, c2 = st.columns(2)
    c1.metric("Berar side", f"{means.get('Amravati (Berar)', float('nan')):.2f}",
              "Ag laborers per cultivator")
    c2.metric("Central Provinces side", f"{means.get('Nagpur (Central Provinces)', float('nan')):.2f}",
              "Ag laborers per cultivator")

    fig = go.Figure()
    for div, color in DIV_COLORS.items():
        fig.add_trace(go.Box(y=pop[pop["division"] == div]["ag_laborer_to_cultivator"],
                              name=div, marker_color=color, boxmean=True))
    fig.update_layout(yaxis_title="Ag laborers per cultivator", showlegend=False)
    st.plotly_chart(plotly_layout(fig, height=380), use_container_width=True)

    st.markdown(f"""
    <div class="recon-card">
        <p style="color:{PALETTE['text_primary']}; font-size:0.9rem; margin:0; line-height:1.6;">
            For every cultivator in the corridor's Berar talukas, there are more agricultural
            laborers than on the Central Provinces side -- a real, fairly consistent gap, not one
            or two outlier talukas dragging the average. This lines up with the standard account of
            why Vidarbha's farmer-distress crisis concentrated in this specific belt: Ryotwari gave
            individual peasants formal ownership, but pushing them into single-crop, price-exposed
            cotton is exactly the kind of cash economy associated with land loss and a growing
            landless-labor class over generations. Literacy, by contrast, was close either way
            ({lit.get('Amravati (Berar)', float('nan')):.1f}% vs
            {lit.get('Nagpur (Central Provinces)', float('nan')):.1f}%) -- not a meaningful divide
            on its own.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# LAND USE
# ============================================================
st.markdown("### Land Use (Corridor)")

lu = safe_read_csv("Land_Use", "corridor_taluka_landuse_stats.csv")
if lu is None:
    st.warning("corridor_taluka_landuse_stats.csv not found yet.")
else:
    lu_means = lu.groupby("division")[["net_area_pct", "forest_pct", "fallow_total_pct"]].mean()
    cats = ["Net cultivated %", "Forest %", "Fallow %"]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Berar (Amravati Division)",
                          x=cats,
                          y=[lu_means.loc["Amravati (Berar)", c] for c in
                             ["net_area_pct", "forest_pct", "fallow_total_pct"]],
                          marker_color=PALETTE["berar"]))
    fig.add_trace(go.Bar(name="Central Provinces (Nagpur Division)",
                          x=cats,
                          y=[lu_means.loc["Nagpur (Central Provinces)", c] for c in
                             ["net_area_pct", "forest_pct", "fallow_total_pct"]],
                          marker_color=PALETTE["cp"]))
    fig.update_layout(barmode="group", yaxis_title="% of taluka area")
    st.plotly_chart(plotly_layout(fig, height=420), use_container_width=True)
    st.caption(
        "Net cultivated area runs higher on the Berar side, forest % is almost identical at the "
        "corridor (the corridor doesn't reach CP's deep-forest tracts like Gadchiroli), and fallow "
        "land is nearly double on the Central Provinces side -- more land sitting temporarily "
        "uncultivated. Could be crop-rotation practice as much as distress; carried forward as a "
        "small additional data point, not over-read on its own."
    )

st.markdown("---")

# ============================================================
# LAND FRAGMENTATION
# ============================================================
st.markdown("### Land Fragmentation (Average Holding Size)")

ph4 = safe_read_csv("Agriculture", "phase4_master_dataset.csv")
if ph4 is not None and "avg_holding_ha" in ph4.columns:
    hold_means = ph4.groupby("division")["avg_holding_ha"].mean()
    c1, c2 = st.columns(2)
    c1.metric("Berar corridor talukas", f"{hold_means.get('Amravati (Berar)', float('nan')):.2f} ha")
    c2.metric("Central Provinces corridor talukas", f"{hold_means.get('Nagpur (Central Provinces)', float('nan')):.2f} ha")
    st.caption(
        "CP actually runs slightly larger holdings, not smaller -- the opposite of what a naive "
        "'Ryotwari → more fragmented smallholdings' story would predict. Both numbers are close "
        "enough that this is filed as a genuinely flat result, not stretched into a finding either way."
    )
else:
    st.warning("avg_holding_ha column not found in Agriculture/phase4_master_dataset.csv yet.")

st.markdown("---")

col_a, col_b, col_c = st.columns([0.1, 5.9, 0.1])
with col_b:
    show_image_or_placeholder(output_path("agrarian_indicators_comparison.png"))
    show_image_or_placeholder(output_path("population_agrarian_comparison.png"))
    show_image_or_placeholder(output_path("landuse_corridor_comparison.png"))

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Agrarian &amp; Land Structure</p>",
    unsafe_allow_html=True,
)
