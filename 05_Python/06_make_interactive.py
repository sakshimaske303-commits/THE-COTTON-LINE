"""Standalone interactive maps and plots (outputs/), plotly.js from CDN."""
import json

import numpy as np
import pandas as pd

from cl_lib import ROOT, PROC

import sys
sys.path.insert(0, str(ROOT / "06_Streamlit" / "utils"))
from mapfig import build_map  # noqa: E402


OUT_M = ROOT / "outputs" / "interactive_maps"
OUT_P = ROOT / "outputs" / "plots" / "interactive"
OUT_M.mkdir(parents=True, exist_ok=True)
OUT_P.mkdir(parents=True, exist_ok=True)
CDN = "https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"
BE, CP = "#eb6834", "#2a78d6"

D = pd.read_csv(PROC / "Phase4" / "analysis_taluka_dataset.csv")
gj = json.loads((PROC / "Administrative" / "vidarbha_talukas_120.geojson").read_text(encoding="utf-8"))
for ft in gj["features"]:
    ft["id"] = ft["properties"]["dtname"] + "|" + ft["properties"]["sdtname"]
    ft["properties"] = {"n": ft["properties"]["sdtname"]}
    # round coordinates to ~10 m to keep pages small
    g = ft["geometry"]
    rnd = (lambda ring: [[round(x, 4), round(y, 4)] for x, y, *_ in ring])
    if g["type"] == "Polygon":
        g["coordinates"] = [rnd(r) for r in g["coordinates"]]
    else:
        g["coordinates"] = [[rnd(r) for r in p] for p in g["coordinates"]]
line = json.loads((PROC / "Administrative" / "division_boundary_line.geojson").read_text())["features"][0]["geometry"]["coordinates"]
D["id"] = D.dtname + "|" + D.sdtname


def page(title, subtitle, data, layout, note):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<script src="{CDN}"></script>
<style>body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#fcfcfb;color:#0b0b0b}}
header{{padding:14px 18px 4px}}h1{{font-size:18px;margin:0}}p{{margin:4px 0;color:#52514e;font-size:13px}}
#c{{width:100%;height:calc(100vh - 120px);min-height:460px}}footer{{padding:6px 18px;font-size:12px;color:#52514e}}</style>
</head><body><header><h1>{title}</h1><p>{subtitle}</p></header><div id="c"></div>
<footer>{note} · The Cotton Line v2.1 · Sakshi D. Maske</footer>
<script>Plotly.newPlot('c',{json.dumps(data)},{json.dumps(layout)},{{responsive:true,displaylogo:false}});</script>
</body></html>"""


MAPS = {
    "boundary_side": ("side", "Side of the old boundary", "Blues", "Berar = 1, Central Provinces = 0"),
    "ndvi_decline": ("ndvi_decline_y1", "NDVI decline, November 2025 to March 2026", "Greens",
                     "Landsat, common pixels; talukas at least 50 % observed"),
    "land_surface_temp": ("lst_june_c", "Land surface temperature, 20 June 2026 (deg C)", "Oranges",
                          "Landsat thermal band, single pre-monsoon date"),
    "ag_laborer_ratio": ("ag_laborer_to_cultivator", "Agricultural labourers per cultivator (Census 2011)", "Purples",
                         "Rural villages, 119 talukas"),
    "net_cultivated_area": ("net_area_pct", "Net sown area, % of village area (Census 2011)", "YlOrBr",
                            "Rural villages, 119 talukas"),
    "distance_to_boundary": ("signed_dist_km", "Signed distance to the old boundary (km)", "RdBu",
                             "Positive = Berar side; centroid distance in UTM 44N"),
}
for name, (col, title, cs, note) in MAPS.items():
    d = D.dropna(subset=[col])
    data, layout = build_map(gj, line, dict(zip(d.id, d[col].round(4))), dict(zip(D.id, D.sdtname + ", " + D.dtname)),
                             cs, title, base="#e6e6e3", edge="#ffffff", base_edge="#ffffff", text_color="#52514e",
                             diverging=(col == "signed_dist_km"))
    (OUT_M / f"{name}.html").write_text(page(title, "Black line: the 384.7 km boundary proxy. Blank talukas are "
                                             "outside this outcome's sample.", data, layout, note), encoding="utf-8")

# ---------------------------------------------------------------- plots
both = D[D.eo_ok_y1 & D.eo_ok_y2]
data = []
for yr, lab in [("ndvi_decline_y1", "Year 1 (2025-26)"), ("ndvi_decline_y2", "Year 2 (2024-25)")]:
    for side, nm, colr in [(1, "Berar", BE), (0, "Central Provinces", CP)]:
        g = both[both.side == side]
        data.append({"type": "box", "y": g[yr].round(4).tolist(), "x": [lab] * len(g), "name": nm,
                     "marker": {"color": colr}, "boxmean": True, "legendgroup": nm, "showlegend": yr.endswith("1"),
                     "text": g.sdtname.tolist()})
layout = {"boxmode": "group", "yaxis": {"title": "NDVI decline (common pixels)"}, "margin": {"t": 20}}
(OUT_P / "cotton_signature_ndvi.html").write_text(page(
    "November-to-March NDVI decline by side, two years",
    f"{len(both)} talukas valid in both years. Same footprint and method: year 2 replicates the regional "
    "pattern, it is not an independent test.", data, layout, "Landsat 8/9"), encoding="utf-8")

main = pd.read_csv(PROC / "Phase4" / "results" / "main_models.csv")
specs = [("ndvi_decline_y1", "footprint", "NDVI decline, year 1"), ("ndvi_decline_y2", "footprint", "NDVI decline, year 2"),
         ("lst_june_c", "footprint", "LST, 20 June 2026"), ("ag_laborer_to_cultivator", "census_wide", "Labourers per cultivator"),
         ("net_area_pct", "census_wide", "Net sown area (%)")]
data, buttons = [], []
for i, (y, sc, lab) in enumerate(specs):
    d = D.dropna(subset=[y])
    r = main[(main.outcome == y) & (main.scale == sc)].iloc[0]
    for side, nm, colr in [(0, "Central Provinces", CP), (1, "Berar", BE)]:
        g = d[d.side == side]
        data.append({"type": "scatter", "mode": "markers", "x": g.signed_dist_km.round(1).tolist(), "y": g[y].round(4).tolist(),
                     "text": g.sdtname.tolist(), "name": nm, "marker": {"color": colr, "size": 8}, "visible": i == 0,
                     "hovertemplate": "%{text}<br>%{x} km, %{y}<extra></extra>"})
        b = np.polyfit(g.signed_dist_km, g[y], 1)
        xx = [float(g.signed_dist_km.min()), float(g.signed_dist_km.max())]
        data.append({"type": "scatter", "mode": "lines", "x": xx, "y": [float(np.polyval(b, v)) for v in xx],
                     "line": {"color": colr, "width": 3}, "showlegend": False, "hoverinfo": "skip", "visible": i == 0})
    vis = [False] * (4 * len(specs))
    for j in range(4):
        vis[4 * i + j] = True
    buttons.append({"label": lab, "method": "update", "args": [{"visible": vis}, {
        "title": {"text": f"{lab}: step p = {r.p_side_primary:.2f}, slope-change p = {r.p_int_primary:.3f} (n = {int(r.n)})"}}]})
r0 = main[(main.outcome == specs[0][0]) & (main.scale == specs[0][1])].iloc[0]
layout = {"updatemenus": [{"buttons": buttons, "x": 0, "y": 1.15, "xanchor": "left"}],
          "title": {"text": f"{specs[0][2]}: step p = {r0.p_side_primary:.2f}, slope-change p = {r0.p_int_primary:.3f} (n = {int(r0.n)})",
                    "y": 0.93, "font": {"size": 13}},
          "xaxis": {"title": "km from the old boundary (Central Provinces < 0 < Berar)", "zeroline": True},
          "shapes": [{"type": "line", "x0": 0, "x1": 0, "yref": "paper", "y0": 0, "y1": 1, "line": {"dash": "dot", "color": "#52514e"}}],
          "margin": {"t": 90}}
(OUT_P / "spatial_discontinuity.html").write_text(page(
    "Outcomes against distance to the old boundary",
    "Per-side linear fits for display. p-values from the full model with rainfall and elevation, conservative "
    "(largest of HC3 and Conley) standard errors.", data, layout, "Landsat sample / 119 census talukas"), encoding="utf-8")

jk = pd.read_csv(PROC / "Phase4" / "phase4_robustness_jackknife.csv")
data = [{"type": "bar", "x": (jk.dropped_sdtname + " (" + jk.dropped_dtname + ")").tolist(), "y": jk.p.round(4).tolist(),
         "marker": {"color": [CP if p < 0.05 else BE for p in jk.p]}, "hovertemplate": "drop %{x}<br>p = %{y}<extra></extra>"}]
layout = {"yaxis": {"title": "p-value (OLS) with this taluka dropped"}, "xaxis": {"tickangle": -60},
          "shapes": [{"type": "line", "xref": "paper", "x0": 0, "x1": 1, "y0": 0.05, "y1": 0.05, "line": {"dash": "dash"}}],
          "margin": {"b": 160, "t": 20}}
(OUT_P / "jackknife_robustness.html").write_text(page(
    "Leave-one-out jackknife: corridor labour-ratio slope change",
    f"p < 0.05 in {(jk.p < 0.05).sum()} of {len(jk)} runs (range {jk.p.min():.3f}-{jk.p.max():.3f}); with robust "
    "errors the full-sample p is 0.063. Suggestive at most.", data, layout, "32 corridor talukas"), encoding="utf-8")
print("Interactive pages written.")
