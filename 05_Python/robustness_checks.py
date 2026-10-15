"""All regressions, robustness checks and summary numbers.

In : Phase4/analysis_taluka_dataset.csv
Out: Phase4/results/*.csv, results/key_numbers.json

y = b0 + b1*side + b2*dist + b3*side*dist + rainfall [+ elevation]
b1 = step at the line (H1), b3 = slope change (H2).
Primary p = max(HC3, Conley 50 km, Conley 100 km). Holm and BH over 20 tests.
"""
import json
import warnings

import numpy as np
import pandas as pd

from cl_lib import PROC, ols, cooks_distance, morans_i, holm, bh

warnings.filterwarnings("ignore")
OUT = PROC / "Phase4" / "results"
OUT.mkdir(parents=True, exist_ok=True)
D = pd.read_csv(PROC / "Phase4" / "analysis_taluka_dataset.csv")
D["sxd"] = D.side * D.signed_dist_km
D["xy"] = list(zip(D.x_km, D.y_km))

EO = ["ndvi_decline_y1", "ndvi_decline_y2", "lst_june_c"]
CEN = ["ag_laborer_to_cultivator", "net_area_pct"]
LABEL = {"ndvi_decline_y1": "NDVI decline, year 1 (Nov 2025-Mar 2026)",
         "ndvi_decline_y2": "NDVI decline, year 2 (Nov 2024-Mar 2025)",
         "lst_june_c": "Land surface temperature, 20 June 2026 (C)",
         "ag_laborer_to_cultivator": "Agricultural labourers per cultivator (2011)",
         "net_area_pct": "Net sown area, % of village area (2011)"}
KEY = {}


def sample(outcome, scale):
    d = D.dropna(subset=[outcome, "annual_total_mm"])
    if scale == "corridor":
        d = d[d.in_corridor]
    return d


def controls(d):
    """Use elevation when it is available for every row of the sample, else rainfall only."""
    return ["annual_total_mm", "elevation_m"] if d.elevation_m.notna().all() else ["annual_total_mm"]


X = ["side", "signed_dist_km", "sxd"]


def fit_all(d, y, ctrl=None):
    ctrl = controls(d) if ctrl is None else ctrl
    xs = X + ctrl
    xy = np.array(d.xy.tolist())
    res = {c: ols(d, y, xs, cov=c if c != "c100" else "conley", groups=d.dtname,
                  coords=xy, cutoff_km=100 if c == "c100" else 50)
           for c in [None, "HC3", "cluster", "conley", "c100"]}
    return res, ctrl


# ======================================================================= 1. main table (20 tests)
SCALES = {o: ["corridor", "footprint"] for o in EO} | {o: ["corridor", "census_wide"] for o in CEN}
rows = []
for y, scales in SCALES.items():
    for sc in scales:
        d = sample(y, sc)
        r, ctrl = fit_all(d, y)
        m = r[None]
        rows.append(dict(
            outcome=y, scale=sc, n=int(m.nobs), n_berar=int(d.side.sum()), n_cp=int((1 - d.side).sum()),
            n_districts=d.dtname.nunique(), controls="+".join(ctrl),
            berar_reach_km=d.loc[d.side == 1, "dist_to_boundary_km"].max(),
            cp_reach_km=d.loc[d.side == 0, "dist_to_boundary_km"].max(),
            side_coef=m.params["side"], side_se_conley=r["conley"].bse["side"],
            p_side_ols=m.pvalues["side"], p_side_hc3=r["HC3"].pvalues["side"],
            p_side_cluster=r["cluster"].pvalues["side"], p_side_conley50=r["conley"].pvalues["side"],
            p_side_conley100=r["c100"].pvalues["side"],
            int_coef=m.params["sxd"],
            p_int_ols=m.pvalues["sxd"], p_int_hc3=r["HC3"].pvalues["sxd"],
            p_int_cluster=r["cluster"].pvalues["sxd"], p_int_conley50=r["conley"].pvalues["sxd"],
            p_int_conley100=r["c100"].pvalues["sxd"],
            slope_cp_per_km=m.params["signed_dist_km"], slope_berar_per_km=m.params["signed_dist_km"] + m.params["sxd"],
            p_rain=m.pvalues["annual_total_mm"], r2=m.rsquared,
            mde_side_80pct=2.8 * max(r["conley"].bse["side"], r["HC3"].bse["side"], r["c100"].bse["side"]),
            sd_outcome=d[y].std(),
        ))
main = pd.DataFrame(rows)
for t in ["side", "int"]:
    main[f"p_{t}_primary"] = main[[f"p_{t}_hc3", f"p_{t}_conley50", f"p_{t}_conley100"]].max(axis=1)
prim = np.r_[main.p_side_primary, main.p_int_primary]
h, q = holm(prim), bh(prim)
k = len(main)
main["p_side_holm"], main["p_int_holm"] = h[:k], h[k:]
main["p_side_bh"], main["p_int_bh"] = q[:k], q[k:]
main["mde_in_sd"] = main.mde_side_80pct / main.sd_outcome
main.round(6).to_csv(OUT / "main_models.csv", index=False)
KEY["n_tests"] = int(len(prim))
KEY["n_raw_sig_primary"] = int((prim < 0.05).sum())
KEY["n_holm_sig"] = int((h < 0.05).sum())
KEY["min_holm"] = float(h.min())
KEY["min_bh"] = float(q.min())
pd.set_option("display.width", 250)
print("== Main models ==")
print(main[["outcome", "scale", "n", "n_berar", "controls", "side_coef", "p_side_ols", "p_side_primary",
            "int_coef", "p_int_ols", "p_int_hc3", "p_int_conley50", "p_int_primary", "p_int_holm"]].round(4).to_string(index=False))
print(f"raw p<0.05 (primary): {KEY['n_raw_sig_primary']}/{KEY['n_tests']}; Holm-significant: {KEY['n_holm_sig']}; "
      f"min Holm {KEY['min_holm']:.3f}; min BH {KEY['min_bh']:.3f}")

# ======================================================================= 2. descriptives
desc = []
for y in EO + CEN:
    for sc in (["corridor", "footprint"] if y in EO else ["corridor", "census_wide"]):
        d = sample(y, sc)
        g = d.groupby("side")[y]
        desc.append(dict(outcome=y, scale=sc, mean_berar=g.mean().get(1), mean_cp=g.mean().get(0),
                         sd_berar=g.std().get(1), sd_cp=g.std().get(0), n_berar=g.size().get(1), n_cp=g.size().get(0)))
desc = pd.DataFrame(desc)
desc["gap"] = desc.mean_berar - desc.mean_cp
desc.round(5).to_csv(OUT / "descriptives_by_side.csv", index=False)
both = D[D.eo_ok_y1 & D.eo_ok_y2]
yr = both.groupby("side")[["ndvi_decline_y1", "ndvi_decline_y2"]].mean()
KEY["matched_years_n"] = int(len(both))
KEY["matched_y1"] = {"berar": float(yr.loc[1, "ndvi_decline_y1"]), "cp": float(yr.loc[0, "ndvi_decline_y1"])}
KEY["matched_y2"] = {"berar": float(yr.loc[1, "ndvi_decline_y2"]), "cp": float(yr.loc[0, "ndvi_decline_y2"])}
KEY["y1_y2_corr"] = float(both[["ndvi_decline_y1", "ndvi_decline_y2"]].corr().iloc[0, 1])
f1 = sample("ndvi_decline_y1", "footprint")
KEY["raw_side_only_y1"] = {k_: float(v) for k_, v in ols(f1, "ndvi_decline_y1", ["side"]).params.items()}
KEY["dist_only_side_y1"] = float(ols(f1, "ndvi_decline_y1", X).params["side"])
KEY["dist_only_p_y1"] = float(ols(f1, "ndvi_decline_y1", X).pvalues["side"])
print("\n== Descriptives ==\n", desc.round(3).to_string(index=False))

# ======================================================================= 3. Moran's I of residuals
mor = []
for _, r in main.iterrows():
    d = sample(r.outcome, r.scale)
    m = ols(d, r.outcome, X + r.controls.split("+"))
    I, p = morans_i(m.resid, np.array(d.xy.tolist()))
    mor.append(dict(outcome=r.outcome, scale=r.scale, n=len(d), morans_I=I, p_perm=p))
pd.DataFrame(mor).round(4).to_csv(OUT / "morans_i_residuals.csv", index=False)

# ======================================================================= 4. symmetric windows
win = []
for y in EO + CEN:
    sc = "footprint" if y in EO else "census_wide"
    for w in [40, 60, 80, 105]:
        d = sample(y, sc)
        d = d[d.dist_to_boundary_km <= w]
        if d.side.sum() < 5 or (1 - d.side).sum() < 5:
            continue
        r, ctrl = fit_all(d, y)
        win.append(dict(outcome=y, window_km=w, n=int(r[None].nobs), n_berar=int(d.side.sum()),
                        side_coef=r[None].params["side"], p_side_conley50=r["conley"].pvalues["side"],
                        int_coef=r[None].params["sxd"], p_int_conley50=r["conley"].pvalues["sxd"]))
pd.DataFrame(win).round(5).to_csv(OUT / "symmetric_windows.csv", index=False)

# ======================================================================= 5. local-linear RD (triangular kernel)
llr = []
for y in EO + CEN:
    base = sample(y, "footprint" if y in EO else "census_wide")
    for hbw in [40, 60, 80]:
        d = base[base.dist_to_boundary_km <= hbw].copy()
        if d.side.sum() < 5 or (1 - d.side).sum() < 5:
            continue
        w = (1 - d.dist_to_boundary_km / hbw).to_numpy()
        Xm = np.column_stack([np.ones(len(d)), d.side, d.signed_dist_km, d.sxd])
        Y = d[y].to_numpy(float)
        WX = Xm * w[:, None]
        XtWXi = np.linalg.inv(WX.T @ Xm)
        b = XtWXi @ WX.T @ Y
        e = Y - Xm @ b
        M = (Xm * (w * e)[:, None]).T @ (Xm * (w * e)[:, None])
        V = XtWXi @ M @ XtWXi * len(d) / (len(d) - 4)
        se = np.sqrt(V[1, 1])
        from scipy import stats as _st
        llr.append(dict(outcome=y, bandwidth_km=hbw, n=len(d), n_berar=int(d.side.sum()),
                        jump=b[1], se=se, p=2 * _st.norm.sf(abs(b[1] / se))))
pd.DataFrame(llr).round(5).to_csv(OUT / "local_linear_rd.csv", index=False)

# ======================================================================= 6. placebo cutoffs
plc = []
for y in EO + CEN:
    base = sample(y, "footprint" if y in EO else "census_wide")
    for side_val, cuts in [(0, [-100, -80, -60, -40]), (1, [40, 60, 80, 100])]:
        d0 = base[base.side == side_val].copy()
        for cut in cuts:
            d = d0.copy()
            d["pside"] = (d.signed_dist_km > cut).astype(int)
            d["rd"] = d.signed_dist_km - cut
            d["pxd"] = d.pside * d.rd
            if d.pside.sum() < 5 or (1 - d.pside).sum() < 5:
                continue
            ctrl = controls(d)
            mc = ols(d, y, ["pside", "rd", "pxd"] + ctrl, cov="conley", coords=np.array(d.xy.tolist()))
            plc.append(dict(outcome=y, side_tested="Berar" if side_val else "Central Provinces", placebo_cut_km=cut,
                            n=len(d), p_jump_conley50=mc.pvalues["pside"], p_slope_conley50=mc.pvalues["pxd"]))
plc = pd.DataFrame(plc)
plc.round(5).to_csv(OUT / "placebo_cutoffs.csv", index=False)

# ======================================================================= 7. influence + exclusions
inf = []
for _, r in main.iterrows():
    d = sample(r.outcome, r.scale).reset_index(drop=True)
    xs = X + r.controls.split("+")
    m = ols(d, r.outcome, xs)
    cd = cooks_distance(m)
    top = int(np.argmax(cd))
    d2 = d.drop(top)
    m2 = ols(d2, r.outcome, xs, cov="conley", coords=np.array(d2.xy.tolist()))
    ex = d[~d.sdtname.isin(["Rajura", "Korpana", "Jiwati"])]
    m3 = ols(ex, r.outcome, xs, cov="conley", coords=np.array(ex.xy.tolist()))
    inf.append(dict(outcome=r.outcome, scale=r.scale, most_influential=d.sdtname[top], cooks_d=cd[top],
                    p_side_drop_top=m2.pvalues["side"], p_int_drop_top=m2.pvalues["sxd"],
                    p_side_excl_rajura_korpana_jiwati=m3.pvalues["side"],
                    p_int_excl_rajura_korpana_jiwati=m3.pvalues["sxd"]))
pd.DataFrame(inf).round(5).to_csv(OUT / "influence_and_exclusions.csv", index=False)

# jackknife on the corridor labour interaction (the one corridor result flagged earlier)
d = sample("ag_laborer_to_cultivator", "corridor").reset_index(drop=True)
jk = []
for i in range(len(d)):
    di = d.drop(i)
    m = ols(di, "ag_laborer_to_cultivator", X + controls(di))
    mc = ols(di, "ag_laborer_to_cultivator", X + controls(di), cov="conley", coords=np.array(di.xy.tolist()))
    jk.append(dict(dropped_dtname=d.dtname[i], dropped_sdtname=d.sdtname[i], coef=m.params["sxd"],
                   p=m.pvalues["sxd"], p_conley50=mc.pvalues["sxd"]))
jk = pd.DataFrame(jk)
jk.to_csv(PROC / "Phase4" / "phase4_robustness_jackknife.csv", index=False)

# ======================================================================= 8. coverage sensitivity
cov = []
for y, cc in [("decline_y1", "cov_y1_pct"), ("decline_y2", "cov_y2_pct"), ("lst_june", "cov_lst_june_pct")]:
    for thr in [0.001, 25, 50, 90]:
        d = D[(D[cc] >= thr) & D[y].notna() & D.annual_total_mm.notna() & D.elevation_m.notna()]
        r, _ = fit_all(d, y)
        cov.append(dict(outcome=y, min_common_coverage_pct=thr, n=int(r[None].nobs), n_berar=int(d.side.sum()),
                        p_side_conley50=r["conley"].pvalues["side"], p_int_ols=r[None].pvalues["sxd"],
                        p_int_conley50=r["conley"].pvalues["sxd"]))
pd.DataFrame(cov).round(5).to_csv(OUT / "coverage_sensitivity.csv", index=False)

# ======================================================================= 9. collinearity, coverage facts, validation
fp = D[D.eo_ok_y1]
corr = fp[["signed_dist_km", "annual_total_mm", "elevation_m", "side"]].corr()
corr.round(3).to_csv(OUT / "collinearity_footprint.csv")
KEY["corr_dist_rain"] = float(corr.loc["signed_dist_km", "annual_total_mm"])
KEY["r2_dist_on_controls"] = float(ols(fp, "signed_dist_km", ["annual_total_mm", "elevation_m"]).rsquared)
fpall = D[D.in_footprint]
KEY["footprint_talukas"] = int(len(fpall))
KEY["footprint_lt50"] = int((fpall.cov_y1_pct < 50).sum())
KEY["footprint_lt1"] = fpall.loc[fpall.cov_y1_pct < 1, "sdtname"].tolist()
KEY["karanja_wardha_cov"] = float(D.loc[(D.dtname == "Wardha") & (D.sdtname == "Karanja"), "cov_lst_june_pct"].iloc[0])

agr = pd.read_csv(PROC / "Agriculture" / "vidarbha_agrarian_indicators.csv")
agr["dtname"] = agr.district.replace({"Buldhana": "Buldana", "Gondiya": "Gondiya"})
dm = fp.groupby("dtname").agg(decline=("ndvi_decline_y1", "mean"), n=("sdtname", "size")).reset_index()
dm = dm.merge(agr[["dtname", "cotton_share_pct"]], on="dtname")
dm.round(4).to_csv(OUT / "validation_district_cotton_share.csv", index=False)
KEY["validation_n_districts"] = int(len(dm))
KEY["validation_r"] = float(dm[["decline", "cotton_share_pct"]].corr().iloc[0, 1])
KEY["validation_r_cotton_districts"] = float(dm[dm.cotton_share_pct > 1][["decline", "cotton_share_pct"]].corr().iloc[0, 1])

# ======================================================================= 10. key numbers for the documents
KEY["main"] = main.set_index(["outcome", "scale"])[
    ["n", "n_berar", "n_cp", "side_coef", "p_side_ols", "p_side_hc3", "p_side_conley50", "int_coef", "p_int_ols",
     "p_int_hc3", "p_int_conley50", "p_int_cluster", "p_side_primary", "p_int_primary", "p_int_holm", "p_side_holm", "slope_cp_per_km",
     "slope_berar_per_km", "mde_side_80pct", "mde_in_sd", "berar_reach_km", "cp_reach_km", "controls"]
].reset_index().to_dict(orient="records")
KEY["desc"] = desc.to_dict(orient="records")
KEY["jackknife"] = {"n": int(len(jk)), "n_p_lt_05": int((jk.p < 0.05).sum()), "p_min": float(jk.p.min()),
                    "p_max": float(jk.p.max()), "coef_min": float(jk.coef.min()), "coef_max": float(jk.coef.max())}
KEY["placebo_sig"] = plc[(plc.p_jump_conley50 < 0.05) | (plc.p_slope_conley50 < 0.05)].to_dict(orient="records")
(OUT / "key_numbers.json").write_text(json.dumps(KEY, indent=2, default=float))
print("\nWrote", OUT)
