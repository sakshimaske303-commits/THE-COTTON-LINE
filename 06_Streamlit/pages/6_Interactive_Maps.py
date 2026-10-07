import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import data_path, safe_read_csv

st.set_page_config(page_title="Interactive Maps — THE COTTON LINE", page_icon="🗺️", layout="wide")
inject_theme()

st.markdown("<h1>🗺️ INTERACTIVE MAP</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>The Boundary, the Corridor, "
    "and Every Full-Footprint Taluka, Explorable Directly</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Every taluka in the full 68-taluka Landsat footprint, colored by whichever variable is selected
below, with the 384.7 km historical boundary line drawn on top. Hover any taluka for its exact
value.
""")


@st.cache_data
def load_map_data():
    boundary_path = data_path("Administrative", "vidarbha_taluka_boundary.gpkg")
    line_path = data_path("Administrative", "division_boundary_line.geojson")
    ff_csv = data_path("Phase4", "phase4_fullfootprint_dataset.csv")

    talukas = gpd.read_file(boundary_path)
    line = gpd.read_file(line_path)
    df = pd.read_csv(ff_csv)

    talukas["k"] = talukas["district_n"].str.lower().str.strip() + "|" + talukas["taluka_nam"].str.lower().str.strip()
    df["k"] = df["dtname"].str.lower().str.strip() + "|" + df["sdtname"].str.lower().str.strip()
    merged = talukas.merge(df, on="k", how="inner")

    line_coords = list(line.geometry.iloc[0].coords)
    line_lons = [c[0] for c in line_coords]
    line_lats = [c[1] for c in line_coords]

    return merged, line_lons, line_lats, len(df) - len(merged)


try:
    merged, line_lons, line_lats, n_missing = load_map_data()
except Exception as e:
    merged = None
    st.warning(f"Map data not available yet: {e}")

if merged is not None:
    METRICS = {
        "Side (Berar / Central Provinces)": "side",
        "Kharif-to-rabi NDVI decline": "kharif_to_rabi_decline",
        "Land surface temperature (°C)": "lst_mean_c",
        "Ag-laborer-to-cultivator ratio": "ag_laborer_to_cultivator",
        "Net cultivated area (%)": "net_area_pct",
        "Distance to boundary (km, signed)": "signed_dist_km",
    }
    choice = st.selectbox("Color talukas by", list(METRICS.keys()))
    metric = METRICS[choice]

    merged_geojson = merged.set_geometry("geometry").__geo_interface__

    if metric == "side":
        colorscale = [[0, PALETTE["cp"]], [1, PALETTE["berar"]]]
        color_col = "side"
    else:
        colorscale = [[0, PALETTE["cp"]], [0.5, PALETTE["prussian"]], [1, PALETTE["berar"]]]
        color_col = metric

    fig = go.Figure(go.Choroplethmapbox(
        geojson=merged_geojson,
        locations=merged.index,
        z=merged[color_col],
        colorscale=colorscale,
        marker_opacity=0.75,
        marker_line_width=0.6,
        marker_line_color=PALETTE["text_secondary"],
        text=merged["sdtname"] + ", " + merged["dtname"] + " (" + merged["division"] + ")",
        hovertemplate="%{text}<br>" + choice + ": %{z:.3f}<extra></extra>",
        colorbar=dict(title=choice, tickfont=dict(color=PALETTE["text_primary"])),
    ))

    fig.add_trace(go.Scattermapbox(
        lon=line_lons, lat=line_lats, mode="lines",
        line=dict(width=3, color="#F2F2F0"),
        name="Historical Berar / CP boundary",
        hoverinfo="skip",
    ))

    try:
        centroid = merged.geometry.union_all().centroid
    except AttributeError:
        centroid = merged.geometry.unary_union.centroid
    fig.update_layout(
        mapbox=dict(
            style="white-bg",  # Esri dark basemap; CARTO tiles now ask for an API key
            layers=[dict(below="traces", sourcetype="raster",
                         sourceattribution="Tiles © Esri — Esri, HERE, Garmin, © OpenStreetMap contributors",
                         source=["https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"])],
            center=dict(lat=centroid.y, lon=centroid.x), zoom=6.4),
        height=650, showlegend=False,
    )
    st.plotly_chart(plotly_layout(fig), use_container_width=True)

    if n_missing:
        st.caption(
            f"{len(merged)} of {len(merged) + n_missing} full-footprint talukas shown — "
            f"{n_missing} are not drawn because they do not match the boundary shapefile "
            "(Nagpur (Rural), Nagpur (Urban), Hingna, Kalameshwar, Mauda, Hinganghat, Arjuni "
            "Morgaon and Zari-Jamani). The boundary file used here is an older 116-taluka layer with "
            "some duplicate keys; the corrected 120-taluka layer should replace it. The data for these "
            "talukas are present in the analysis, only the polygons are missing from this map."
        )

st.markdown("---")
st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">About This Map</p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.9rem; margin:0;">
        Built directly from the same taluka boundary shapefile and Phase 4 full-footprint dataset
        used throughout this dashboard — not a separate pre-rendered export. The historical
        boundary line runs 384.7 km, dissolved from the division polygons built from the 120 Vidarbha talukas described in Study Design. (The polygon layer used for this map is an older, incomplete 116-taluka file.)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Interactive Map</p>",
    unsafe_allow_html=True,
)
