"""Field-level check of the NDVI decline on the 7 Roots & Reflectance fields.

In : Ground_Truth/field_decline_bridge.csv (from gee_field_decline_bridge.js), field_crop_history.csv
Out: Ground_Truth/field_decline_summary.csv, 07_Outputs/v2_fig8_field_bridge.png
Does a large Nov-Mar fall go with a single kharif crop, and a small one with rabi or irrigation?
Descriptive only.
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from cl_lib import PROC, OUTFIG

GT = PROC / "Ground_Truth"
f_dec, f_hist = GT / "field_decline_bridge.csv", GT / "field_crop_history.csv"
if not f_dec.exists():
    print("field_decline_bridge.csv not found -- skipping.")
    sys.exit(0)
d = pd.read_csv(f_dec)
w = d.pivot_table(index=["zone", "field_num", "field_id", "name", "sensor", "year"], columns="season",
                  values="mean", aggfunc="first").reset_index()
w["decline"] = w["nov"] - w["mar"]
cnt = d.pivot_table(index=["field_id", "sensor", "year"], columns="season", values="count", aggfunc="first")
cnt.columns = [f"pixels_{c}" for c in cnt.columns]
w = w.merge(cnt.reset_index(), on=["field_id", "sensor", "year"], how="left")
if f_hist.exists():
    h = pd.read_csv(f_hist)
    w = w.merge(h, on=["zone", "field_num", "field_id"], how="left")
    w["rabi_crop"] = w.apply(lambda r: r.get(f"rabi_{'2025_26' if r.year == 'y1' else '2024_25'}_crop"), axis=1)
w.to_csv(GT / "field_decline_summary.csv", index=False)

taluka = pd.read_csv(PROC / "Phase4" / "analysis_taluka_dataset.csv")
k = taluka[(taluka.dtname == "Wardha") & (taluka.sdtname == "Karanja")].iloc[0]
lab = lambda r: f"{r.zone.title()} {r.field_num}"
status = (lambda r: "none" if str(r.get("rabi_crop", "")) in ("none", "nan", "") else str(r.rabi_crop))
COL = {"none": "#eb6834", "chickpea": "#2a78d6", "chickpea?": "#8fb3e6"}
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
L = w[w.sensor == "landsat"].sort_values(["zone", "field_num", "year"], ascending=[False, True, True]).reset_index(drop=True)
fields = list(dict.fromkeys(L.apply(lab, axis=1)))
for _, r in L.iterrows():
    x = fields.index(lab(r)) + (-0.15 if r.year == "y1" else 0.15)
    s2 = w[(w.field_id == r.field_id) & (w.year == r.year) & (w.sensor == "sentinel2")]
    c = COL.get(status(r), "#888888")
    axs[0].scatter(x, r.decline, color=c, s=46, marker="o" if r.year == "y1" else "s", zorder=3, edgecolor="white")
    if len(s2):
        axs[0].plot([x, x], [r.decline, s2.decline.iloc[0]], color=c, lw=1, alpha=0.6)
for yv, ls, name, dy in [(k.decline_y1, "--", "year 1", -0.016), (k.decline_y2, ":", "year 2", 0.005)]:
    axs[0].axhline(yv, color="#52514e", ls=ls, lw=0.9)
    axs[0].text(1.5, yv + dy, f"Karanja taluka mean, {name}: {yv:.2f}", fontsize=7, ha="left", color="#52514e")
axs[0].set_xticks(range(len(fields)), fields, fontsize=8)
axs[0].set_ylabel("NDVI decline, early Nov to early Mar")
axs[0].set_title("a  Decline per field (Landsat; circle = year 1, square = year 2;\n    whisker to the Sentinel-2 value)",
                 loc="left", fontsize=9)
for st_, c in [(s, c) for s, c in COL.items() if s in set(L.apply(status, axis=1))]:
    axs[0].scatter([], [], color=c, s=40, label={"none": "no rabi crop", "chickpea": "rabi chickpea",
                                                "chickpea?": "chickpea, farmer unsure"}[st_])
axs[0].legend(fontsize=7.5, frameon=False, loc="lower left")
for _, r in L.iterrows():
    c = COL.get(status(r), "#888888")
    axs[1].scatter(r.nov, r.mar, color=c, s=40, marker="o" if r.year == "y1" else "s", edgecolor="white", zorder=3)
    axs[1].annotate(f"{r.zone[0].upper()}{r.field_num}", (r.nov, r.mar), xytext=(4, 2), textcoords="offset points", fontsize=7)
axs[1].set_xlabel("NDVI, early November")
axs[1].set_ylabel("NDVI, early March")
axs[1].set_title("b  Where the decline comes from (Landsat)", loc="left", fontsize=9)
fig.suptitle("Field check of the decline index on 7 Roots & Reflectance fields (Central Provinces side)", fontsize=10, x=0.01, ha="left")
fig.tight_layout()
fig.savefig(OUTFIG / "v2_fig8_field_bridge.png", bbox_inches="tight", dpi=150)
print(w[["zone", "field_num", "sensor", "year", "nov", "mar", "decline"] + (["rabi_crop"] if "rabi_crop" in w else [])].round(3).to_string(index=False))
