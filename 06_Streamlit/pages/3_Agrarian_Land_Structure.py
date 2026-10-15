import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import safe_read_csv, load_analysis, output_path, show_image_or_placeholder

st.set_page_config(page_title="Agrarian & Land Structure — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>AGRARIAN &amp; LAND STRUCTURE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>Census 2011 Labour Structure and Land Use, "
            "All 11 Districts, plus District Context</h3>", unsafe_allow_html=True)
st.markdown("---")
BE, CP = "#eb6834", "#2a78d6"
D = load_analysis()
if D is None:
    st.warning("Run `python 05_Python/run_all.py` first.")
    st.stop()

st.markdown("""
Census 2011 village attributes are summed to the taluka for **all 11 districts** (119 talukas;
Nagpur Urban has no villages). Village data cover rural villages only, so every value describes
the rural part of a taluka.

- **Labour ratio:** main plus marginal agricultural labourers, divided by main plus marginal cultivators.
- **Net sown area:** net sown area as a share of the reported village area.
""")

for col, title, unit in [("ag_laborer_to_cultivator", "Agricultural labourers per cultivator", "ratio"),
                         ("net_area_pct", "Net sown area, % of village area", "%")]:
    st.markdown(f"### {title}")
    a, b = st.columns(2)
    for c, (scale, mask) in zip([a, b], [("Corridor (32 talukas)", D.in_corridor), ("All 119 census talukas", D.has_census)]):
        d = D[mask & D[col].notna()]
        fig = go.Figure()
        for side, name, color in [(1, "Berar", BE), (0, "Central Provinces", CP)]:
            fig.add_trace(go.Box(y=d[d.side == side][col], name=f"{name} (n={int((d.side == side).sum())})",
                                 marker_color=color, boxmean=True))
        fig.update_layout(title=scale, yaxis_title=unit, showlegend=False)
        c.plotly_chart(plotly_layout(fig, height=360), use_container_width=True)

st.info("""
**How to read these.** Both outcomes are higher on the Berar side on average. Neither shows a step
at the line in the corridor. In the 119-taluka model the labour ratio differs across the line, but
that difference disappears within 60 km of the line and in local estimates. It is concentrated in
Amravati district (ratios of 3-5), so it is a regional difference, not a break.

Net sown area falls from west to east with no step. Neither pattern can be attributed to
land tenure: the line is also an older frontier, a river and a soil and rainfall transition.
""")
st.markdown("---")

st.markdown("### District context (not tested)")
agr = safe_read_csv("Agriculture", "vidarbha_agrarian_indicators.csv")
if agr is not None:
    t1, t2 = st.tabs(["Cotton share of APY-listed crop area", "Net sown area"])
    for tab, c, lab in [(t1, "cotton_share_pct", "Cotton share of APY-listed crop area (%)"),
                        (t2, "net_sown_pct", "Net sown area (% of geographical area)")]:
        with tab:
            fig = px.bar(agr.sort_values(c, ascending=False), x="district", y=c, color="division",
                         color_discrete_map={"Amravati (Berar)": BE, "Nagpur (Central Provinces)": CP})
            fig.update_layout(yaxis_title=lab, xaxis_title="")
            st.plotly_chart(plotly_layout(fig, height=380), use_container_width=True)
    st.caption("Cotton does not split along the old line: Yavatmal (Berar, 51 %) and Wardha (Central "
               "Provinces, 49 %) are nearly tied; Bhandara and Gondiya grow rice. District values, "
               "11 points, shown for context only.")
show_image_or_placeholder(output_path("v2_fig7_district_context.png"))
st.markdown("<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Agrarian &amp; Land Structure</p>",
            unsafe_allow_html=True)
