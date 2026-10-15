import json
import os

import plotly.graph_objects as go
import streamlit as st
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import data_path, load_analysis
from utils.mapfig import build_map

st.set_page_config(page_title="Interactive Maps — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>INTERACTIVE MAPS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>All 120 Talukas, Every Outcome, "
            "with the Boundary Line</h3>", unsafe_allow_html=True)
st.markdown("---")


@st.cache_data
def load():
    with open(data_path("Administrative", "vidarbha_talukas_120.geojson"), encoding="utf-8") as f:
        gj = json.load(f)
    for ft in gj["features"]:
        ft["id"] = ft["properties"]["dtname"] + "|" + ft["properties"]["sdtname"]
    with open(data_path("Administrative", "division_boundary_line.geojson"), encoding="utf-8") as f:
        line = json.load(f)["features"][0]["geometry"]["coordinates"]
    return gj, line


D = load_analysis()
if D is None:
    st.warning("Run `python 05_Python/run_all.py` first.")
    st.stop()
gj, line = load()
D["id"] = D.dtname + "|" + D.sdtname

METRICS = {
    "Side (Berar = 1, Central Provinces = 0)": ("side", "Blues"),
    "NDVI decline, year 1": ("ndvi_decline_y1", "Greens"),
    "NDVI decline, year 2": ("ndvi_decline_y2", "Greens"),
    "Land surface temperature, 20 June 2026 (°C)": ("lst_june_c", "Oranges"),
    "Labourers per cultivator (2011)": ("ag_laborer_to_cultivator", "Purples"),
    "Net sown area, % (2011)": ("net_area_pct", "YlOrBr"),
    "Signed distance to the line (km)": ("signed_dist_km", "RdBu"),
    "Landsat coverage, year 1 (% of taluka)": ("cov_y1_pct", "Greys"),
}
choice = st.selectbox("Colour talukas by", list(METRICS))
col, scale = METRICS[choice]
d = D.dropna(subset=[col])
data, layout = build_map(gj, line, dict(zip(d.id, d[col])), dict(zip(D.id, D.sdtname + ", " + D.dtname)),
                         scale, choice, text_color=PALETTE["text_primary"], diverging=(col == "signed_dist_km"))
fig = go.Figure(data=data, layout=layout)
fig.update_layout(height=650)
st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
st.caption("Blank talukas are outside that outcome's sample (Landsat outcomes: at least 50 % of the taluka "
           "observed on both dates; census outcomes: 119 talukas with villages). Polygons: Census 2011 / "
           "LGD sub-districts, 120 talukas.")
