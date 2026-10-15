"""All paper and dashboard figures (07_Outputs/v2_*).

Central Provinces #2a78d6, Berar #eb6834.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPoly, Patch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

from cl_lib import PROC, OUTFIG, BERAR_DISTRICTS, read_geojson_polygons, project_polys, utm

CP, BE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "figure.dpi": 150,
                     "savefig.bbox": "tight", "font.family": "DejaVu Sans"})
RES = PROC / "Phase4" / "results"
D = pd.read_csv(PROC / "Phase4" / "analysis_taluka_dataset.csv")
main = pd.read_csv(RES / "main_models.csv")
OUTFIG.mkdir(exist_ok=True)

talukas = read_geojson_polygons(PROC / "Administrative" / "vidarbha_talukas_120.geojson")
geoms = {(p["dtname"], p["sdtname"]): [[r / 1000 for r in ring] for ring in poly]
         for p, polys in talukas for poly in [project_polys(polys)]}
line = np.asarray(json.loads((PROC / "Administrative" / "division_boundary_line.geojson").read_text())
                  ["features"][0]["geometry"]["coordinates"])
LX, LY = utm(line[:, 0], line[:, 1])
LX, LY = LX / 1000, LY / 1000


def patches_for(keys):
    out = []
    for k in keys:
        for poly in geoms[k]:
            out.append(MplPoly(poly[0], closed=True))
    return out


def basemap(ax, face="#f1f0ec"):
    keys = list(geoms)
    pc = PatchCollection(patches_for(keys), facecolor=face, edgecolor="white", linewidth=0.4)
    ax.add_collection(pc)
    ax.set_aspect("equal")
    allxy = np.vstack([poly[0] for v in geoms.values() for poly in v])
    ax.set_xlim(allxy[:, 0].min() - 5, allxy[:, 0].max() + 5)
    ax.set_ylim(allxy[:, 1].min() - 30, allxy[:, 1].max() + 5)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def scalebar(ax, km=50):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    x, y = x0 + 0.02 * (x1 - x0), y0 + 0.06 * (y1 - y0)
    ax.plot([x, x + km], [y, y], color=INK, lw=2)
    ax.text(x + km / 2, y + 6, f"{km} km", ha="center", fontsize=8, color=INK)
    nx, ny = x1 - 0.03 * (x1 - x0), y1 - 0.04 * (y1 - y0)
    ax.annotate("N", xy=(nx, ny), xytext=(nx, ny - 0.1 * (y1 - y0)), ha="center", fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(x, y - 0.045 * (y1 - y0), "UTM zone 44N (EPSG:32644)", fontsize=7, color=MUTED)


def choropleth(ax, col, cmap, label, vmin=None, vmax=None):
    basemap(ax)
    d = D.dropna(subset=[col])
    vals = d[col].to_numpy()
    pc = PatchCollection(patches_for([]), cmap=cmap)
    polys, v = [], []
    for (_, r) in d.iterrows():
        for poly in geoms[(r.dtname, r.sdtname)]:
            polys.append(MplPoly(poly[0], closed=True))
            v.append(r[col])
    pc = PatchCollection(polys, cmap=cmap, edgecolor="white", linewidth=0.4)
    pc.set_array(np.array(v))
    pc.set_clim(vmin if vmin is not None else np.nanmin(vals), vmax if vmax is not None else np.nanmax(vals))
    ax.add_collection(pc)
    ax.plot(LX, LY, color=INK, lw=1.6)
    cb = plt.colorbar(pc, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label(label, fontsize=8.5)
    cb.outline.set_visible(False)
    scalebar(ax)


# ---------------------------------------------------------------- 1. study design map
fig, ax = plt.subplots(figsize=(9, 5.4))
basemap(ax)
for side, col in [(1, BE), (0, CP)]:
    k = [(r.dtname, r.sdtname) for r in D[D.side == side].itertuples()]
    ax.add_collection(PatchCollection(patches_for(k), facecolor=col, alpha=0.18, edgecolor="white", lw=0.4))
kc = [(r.dtname, r.sdtname) for r in D[D.in_corridor].itertuples()]
ax.add_collection(PatchCollection(patches_for(kc), facecolor="none", edgecolor=INK, lw=0.9, hatch="////", alpha=0.55))
ke = [(r.dtname, r.sdtname) for r in D[D.eo_ok_y1].itertuples()]
ax.add_collection(PatchCollection(patches_for(ke), facecolor="none", edgecolor="#1baf7a", lw=1.4))
ax.plot(LX, LY, color=INK, lw=2.2)
for dname, g in D.groupby("dtname"):
    ax.text(g.x_km.mean(), g.y_km.mean(), dname.upper(), ha="center", va="center", fontsize=6.5, color=MUTED)
scalebar(ax)
ax.legend(handles=[Patch(facecolor=BE, alpha=0.35, label="Berar side (Amravati Division, Ryotwari)"),
                   Patch(facecolor=CP, alpha=0.35, label="Central Provinces side (Nagpur Division, Malguzari)"),
                   Line2D([0], [0], color=INK, lw=2.2, label="Historical boundary proxy, 384.7 km"),
                   Patch(facecolor="none", edgecolor=INK, hatch="////", label="Corridor: 32 talukas within 25 km"),
                   Patch(facecolor="none", edgecolor="#1baf7a", lw=1.4,
                         label=f"Landsat sample: {int(D.eo_ok_y1.sum())} talukas >= 50 % observed")],
          loc="lower right", fontsize=7.5, frameon=False)
ax.set_title("Study design: the line, the corridor, and the three samples\n"
             "(census outcomes use all 119 talukas with villages)", fontsize=10, loc="left")
fig.savefig(OUTFIG / "v2_fig1_study_design_map.png")
plt.close(fig)

# ---------------------------------------------------------------- 2. outcome maps
fig, axs = plt.subplots(2, 2, figsize=(11, 6.8))
choropleth(axs[0, 0], "ndvi_decline_y1", "Greens", "NDVI decline, Nov 2025 -> Mar 2026")
axs[0, 0].set_title("a  Kharif-to-rabi NDVI decline (year 1)", loc="left", fontsize=9.5)
choropleth(axs[0, 1], "lst_june_c", "Oranges", "LST, 20 June 2026 (deg C)")
axs[0, 1].set_title("b  Land surface temperature (single date)", loc="left", fontsize=9.5)
choropleth(axs[1, 0], "ag_laborer_to_cultivator", "Purples", "Agricultural labourers per cultivator")
axs[1, 0].set_title("c  Labour structure (Census 2011, rural)", loc="left", fontsize=9.5)
choropleth(axs[1, 1], "net_area_pct", "YlOrBr", "Net sown area, % of village area", 20, 90)
axs[1, 1].set_title("d  Net sown area (Census 2011)", loc="left", fontsize=9.5)
fig.suptitle("The four outcomes, taluka level. Black line = boundary proxy. Blank = outside the sample.",
             x=0.01, ha="left", fontsize=10)
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig2_outcome_maps.png")
plt.close(fig)

# ---------------------------------------------------------------- 3. seasonal NDVI, both years, matched sample
both = D[D.eo_ok_y1 & D.eo_ok_y2]
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.1, 1]})
for side, col, nm in [(1, BE, "Berar"), (0, CP, "Central Provinces")]:
    g = both[both.side == side]
    for yr, ls in [("y1", "-"), ("y2", "--")]:
        m = [g[f"ndvi_post_{yr}"].mean(), g[f"ndvi_pre_{yr}"].mean()]
        axs[0].plot([0, 1], m, ls, color=col, lw=2, marker="o", ms=7,
                    label=f"{nm}, year {yr[-1]} (n={len(g)})")
axs[0].set_xticks([0, 1], ["Early November\n(post-monsoon)", "Early March\n(pre-harvest)"])
axs[0].set_ylabel("Mean NDVI (common pixels)")
axs[0].set_xlim(-0.25, 1.25)
axs[0].legend(fontsize=7.5, frameon=False)
axs[0].set_title("a  Mean NDVI in early November and early March", loc="left", fontsize=9.5)
pos, data, cols, labs = [], [], [], []
for i, (yr, lab) in enumerate([("ndvi_decline_y1", "Year 1\n2025-26"), ("ndvi_decline_y2", "Year 2\n2024-25")]):
    for j, (side, col) in enumerate([(1, BE), (0, CP)]):
        data.append(both.loc[both.side == side, yr].to_numpy())
        pos.append(i * 3 + j)
        cols.append(col)
bp = axs[1].boxplot(data, positions=pos, widths=0.7, patch_artist=True, showfliers=True,
                    medianprops=dict(color=INK), flierprops=dict(markersize=3))
for patch, col in zip(bp["boxes"], cols):
    patch.set_facecolor(col)
    patch.set_alpha(0.55)
axs[1].set_xticks([0.5, 3.5], ["Year 1\n(Nov 2025-Mar 2026)", "Year 2\n(Nov 2024-Mar 2025)"])
axs[1].set_ylabel("NDVI decline")
axs[1].legend(handles=[Patch(color=BE, alpha=0.55, label="Berar"), Patch(color=CP, alpha=0.55, label="Central Provinces")],
              fontsize=7.5, frameon=False)
axs[1].set_title(f"b  Decline by side, matched {len(both)} talukas", loc="left", fontsize=9.5)
fig.text(0.01, -0.04, "Same Landsat footprint and method in both years: year 2 replicates the regional pattern; "
         "it is not an independent test of the boundary.", fontsize=7.5, color=MUTED)
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig3_seasonal_ndvi.png")
plt.close(fig)


# ---------------------------------------------------------------- 4. outcome vs distance
def scatter_panel(ax, y, d, title):
    for side, col in [(0, CP), (1, BE)]:
        g = d[d.side == side]
        ax.scatter(g.signed_dist_km, g[y], s=16, color=col, alpha=0.75, edgecolor="white", lw=0.4)
        if len(g) > 3:
            b = np.polyfit(g.signed_dist_km, g[y], 1)
            xx = np.linspace(g.signed_dist_km.min(), g.signed_dist_km.max(), 50)
            ax.plot(xx, np.polyval(b, xx), color=col, lw=2)
    ax.axvline(0, color=MUTED, lw=0.8, ls=":")
    ax.set_title(title, loc="left", fontsize=9)
    ax.set_xlabel("km from boundary (CP < 0 < Berar)")


fig, axs = plt.subplots(2, 3, figsize=(12, 6.6))
specs = [("ndvi_decline_y1", "footprint", "NDVI decline, year 1"), ("ndvi_decline_y2", "footprint", "NDVI decline, year 2"),
         ("lst_june_c", "footprint", "LST, 20 June 2026 (deg C)"),
         ("ag_laborer_to_cultivator", "census_wide", "Labourers per cultivator"),
         ("net_area_pct", "census_wide", "Net sown area (%)")]
for ax, (y, sc, t) in zip(axs.ravel(), specs):
    d = D.dropna(subset=[y])
    r = main[(main.outcome == y) & (main.scale == sc)].iloc[0]
    scatter_panel(ax, y, d, f"{t}\nn={int(r.n)} | step p={r.p_side_primary:.2f} | slope diff p={r.p_int_primary:.3f}")
ax = axs.ravel()[-1]
ax.axis("off")
ax.text(0, 0.98, "How to read this", fontsize=9.5, weight="bold", transform=ax.transAxes)
ax.text(0, 0.0, "Lines are simple per-side fits shown for display.\n"
        "The p-values come from the full model with\nrainfall (and elevation) controls, using the most\n"
        "conservative of HC3 and Conley spatial errors.\n\n"
        "'Step' = a jump exactly at the line.\n'Slope diff' = a different gradient on each side.\n\n"
        "Only the labour ratio shows a 'step', and only in\nthe 119-taluka model; a local-linear estimate at\n"
        "the line and the 32-taluka corridor show none.\nSlopes differ for NDVI, LST and labour; NDVI\n"
        "peaks near the line and falls both ways. Fake\ncutoffs produce slope 'effects' for NDVI and\nlabour too: a regional gradient, not a border.",
        fontsize=8, color=INK, transform=ax.transAxes, va="bottom")
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig4_outcome_vs_distance.png")
plt.close(fig)

# ---------------------------------------------------------------- 5. test summary (forest of step estimates)
lab = {"ndvi_decline_y1": "NDVI decline y1", "ndvi_decline_y2": "NDVI decline y2", "lst_june_c": "LST June",
       "ag_laborer_to_cultivator": "Labour ratio", "net_area_pct": "Net sown area"}
m = main.copy()
m["name"] = m.outcome.map(lab) + " | " + m.scale.str.replace("_", " ")
m["z_se"] = m.mde_side_80pct / 2.8
m["std_coef"] = m.side_coef / m.sd_outcome
m["std_se"] = m.z_se / m.sd_outcome
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1.3, 1]})
yy = np.arange(len(m))[::-1]
axs[0].errorbar(m.std_coef, yy, xerr=1.96 * m.std_se, fmt="o", color=INK, ecolor=MUTED, capsize=2, ms=5)
axs[0].axvline(0, color=MUTED, lw=0.8)
axs[0].set_yticks(yy, m.name, fontsize=8)
axs[0].set_xlabel("Step at the line, in SD of the outcome (95% CI, conservative SE)")
axs[0].set_title("a  Step at the boundary (H1), global linear model", loc="left", fontsize=9.5)
sig = m.p_int_primary < 0.05
lp = -np.log10(np.clip(m.p_int_primary.values, 1e-6, 1))
axs[1].scatter(lp, yy, color=np.where(sig, BE, MUTED), s=30, zorder=3)
for x_, y_, p_ in zip(lp, yy, m.p_int_primary.values):
    if p_ < 1e-6:
        axs[1].annotate("p < 1e-6", (x_, y_), xytext=(-46, 4), textcoords="offset points", fontsize=7, color=INK)
axs[1].axvline(-np.log10(0.05), color=MUTED, ls=":", lw=0.8)
axs[1].axvline(-np.log10(0.05 / 20), color=INK, ls="--", lw=0.8)
axs[1].text(-np.log10(0.05) + 0.05, 0.01, "p=0.05", fontsize=7, color=MUTED, transform=axs[1].get_xaxis_transform())
axs[1].text(-np.log10(0.05 / 20) + 0.05, 0.01, "Bonferroni, 20 tests", fontsize=7, color=INK, transform=axs[1].get_xaxis_transform())
axs[1].set_yticks(yy, [""] * len(m))
axs[1].set_xlabel("-log10 p, slope difference (H2), conservative SE")
axs[1].set_title("b  Slope difference across the line (H2)", loc="left", fontsize=9.5)
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig5_test_summary.png")
plt.close(fig)

# ---------------------------------------------------------------- 6. validation: decline vs district cotton share
v = pd.read_csv(RES / "validation_district_cotton_share.csv")
fig, ax = plt.subplots(figsize=(5.2, 3.8))
for r in v.itertuples():
    col = BE if r.dtname in BERAR_DISTRICTS else CP
    ax.scatter(r.cotton_share_pct, r.decline, s=25 + 8 * r.n, color=col, alpha=0.8, edgecolor="white")
    off = {"Nagpur": (-58, 5), "Chandrapur": (6, -11), "Amravati": (2, -14), "Wardha": (6, -11)}.get(r.dtname, (5, 3))
    ax.annotate(f"{r.dtname} ({r.n})", (r.cotton_share_pct, r.decline), xytext=off,
                textcoords="offset points", fontsize=7.5, color=INK)
ax.set_xlabel("District cotton share of APY-listed crop area, 2024-25 (%)")
ax.set_ylabel("Mean taluka NDVI decline, year 1")
rr = v[["decline", "cotton_share_pct"]].corr().iloc[0, 1]
r5 = v[v.cotton_share_pct > 1][["decline", "cotton_share_pct"]].corr().iloc[0, 1]
ax.set_title(f"Does the NDVI index track cotton? District level\nr = {rr:.2f} ({len(v)} districts); "
             f"r = {r5:.2f} without the paddy districts ({(v.cotton_share_pct > 1).sum()})", loc="left", fontsize=9)
fig.savefig(OUTFIG / "v2_fig6_validation_cotton_share.png")
plt.close(fig)

# ---------------------------------------------------------------- 7. census corridor + district descriptive panels
agr = pd.read_csv(PROC / "Agriculture" / "vidarbha_agrarian_indicators.csv")
fig, axs = plt.subplots(1, 4, figsize=(13, 3.4))
for ax, (c, t) in zip(axs, [("cotton_share_pct", "Cotton share of APY-listed area (%)"),
                            ("net_sown_pct", "Net sown area (% geog. area)"),
                            ("foodgrain_kg_percapita", "Foodgrain per capita (kg)"),
                            ("avg_holding_ha", "Average holding (ha)")]):
    a = agr.copy()
    a["col"] = np.where(a.division.str.contains("Berar"), BE, CP)
    ax.bar(a.district, a[c], color=a.col, width=0.7)
    ax.set_title(t, fontsize=8.5, loc="left")
    ax.tick_params(axis="x", rotation=60, labelsize=7)
    ax.grid(axis="x", visible=False)
fig.suptitle("District context, 11 districts (orange = Berar, blue = Central Provinces); district values, not tested",
             x=0.01, ha="left", fontsize=9.5)
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig7_district_context.png")
plt.close(fig)

print("Figures written to", OUTFIG)
