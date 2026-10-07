"""
robustness_checks.py -- The Cotton Line
=======================================
Re-runs the headline spatial-discontinuity regressions from the Phase 4 CSVs and adds the
robustness checks that a reviewer will ask for:

  1. Main model, plain OLS + HC3 + district-clustered SEs, for all 8 (scale x outcome) fits
  2. Multiple-testing correction (Bonferroni / Holm / Benjamini-Hochberg) over all 16 tests
     (8 side coefficients + 8 side x distance interactions)
  3. Symmetric distance windows on the full footprint (Berar side is only ~104 km deep,
     the Central Provinces side reaches ~180 km)
  4. Placebo cutoffs on the Central Provinces side only (no historical border there)
  5. Leave-one-out influence (Cook's D, drop the most influential taluka)
  6. Valid-pixel coverage sensitivity (drop talukas with little valid Landsat data)
  7. Collinearity of signed distance with rainfall/elevation

Run from the repository root:
    python 05_Python/robustness_checks.py

Outputs are written to 03_Data_Processed/Phase4/robustness/ as CSV files.
Nothing here touches raw data; it only reads the processed Phase 4 / Climate CSVs.
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "03_Data_Processed"
OUT = DATA / "Phase4" / "robustness"
OUT.mkdir(parents=True, exist_ok=True)

FORMULA = "{o} ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m"
OUTCOMES = ["kharif_to_rabi_decline", "ag_laborer_to_cultivator", "net_area_pct", "lst_mean_c"]
INT = "side:signed_dist_km"

corridor = pd.read_csv(DATA / "Phase4" / "phase4_master_dataset.csv")
full = pd.read_csv(DATA / "Phase4" / "phase4_fullfootprint_dataset.csv")
SCALES = {"corridor": corridor, "full": full}


def fit(df, outcome, cov=None, groups=None):
    d = df.dropna(subset=[outcome, "annual_total_mm", "elevation_m"])
    mod = smf.ols(FORMULA.format(o=outcome), data=d)
    if cov == "cluster":
        return mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[groups])[0]})
    if cov:
        return mod.fit(cov_type=cov)
    return mod.fit()


# ---------------------------------------------------------------- 1 + 2. main table + corrections
rows = []
for scale, df in SCALES.items():
    for o in OUTCOMES:
        m, m3, mc = fit(df, o), fit(df, o, "HC3"), fit(df, o, "cluster", groups="dtname")
        rows.append(dict(
            scale=scale, outcome=o, n=int(m.nobs),
            side_coef=m.params["side"], p_side=m.pvalues["side"],
            p_side_HC3=m3.pvalues["side"], p_side_cluster=mc.pvalues["side"],
            int_coef=m.params[INT], p_int=m.pvalues[INT],
            p_int_HC3=m3.pvalues[INT], p_int_cluster=mc.pvalues[INT],
            slope_CP=m.params["signed_dist_km"],
            slope_Berar=m.params["signed_dist_km"] + m.params[INT],
            n_district_clusters=df.dropna(subset=[o])["dtname"].nunique(),
        ))
main = pd.DataFrame(rows)
all_p = np.r_[main.p_side.values, main.p_int.values]  # 16 tests
for method in ["bonferroni", "holm", "fdr_bh"]:
    adj = multipletests(all_p, method=method)[1]
    main[f"p_side_{method}"] = adj[: len(main)]
    main[f"p_int_{method}"] = adj[len(main):]
main.round(5).to_csv(OUT / "main_models_with_corrections.csv", index=False)
print("== Main models (16 tests) ==")
print(main[["scale", "outcome", "n", "p_side", "p_side_HC3", "p_int", "p_int_HC3", "p_int_holm", "p_int_fdr_bh"]]
      .round(4).to_string(index=False))
print(f"\nRaw p<0.05: {(all_p < 0.05).sum()} of {len(all_p)} "
      f"(chance expectation {0.05 * len(all_p):.1f}); after Holm: "
      f"{(multipletests(all_p, method='holm')[1] < 0.05).sum()}; smallest BH q = "
      f"{multipletests(all_p, method='fdr_bh')[1].min():.3f}")

# ---------------------------------------------------------------- 3. symmetric windows (full footprint)
rows = []
for lim in [120, 105, 80, 60]:
    sub = full[full.dist_to_boundary_km <= lim]
    for o in OUTCOMES:
        m = fit(sub, o)
        rows.append(dict(window_km=lim, outcome=o, n=int(m.nobs),
                         n_berar=int((sub.side == 1).sum()), n_cp=int((sub.side == 0).sum()),
                         side_coef=m.params["side"], p_side=m.pvalues["side"], p_int=m.pvalues[INT]))
win = pd.DataFrame(rows)
win.round(5).to_csv(OUT / "symmetric_windows_full_footprint.csv", index=False)
print("\n== Symmetric windows ==")
print(win.round(4).to_string(index=False))

# ---------------------------------------------------------------- 4. placebo cutoffs on CP side only
rows = []
cp = full[full.side == 0]
for o in ["kharif_to_rabi_decline", "lst_mean_c", "ag_laborer_to_cultivator"]:
    for cut in [-100, -80, -60, -40]:
        d = cp.dropna(subset=[o]).copy()
        d["pside"] = (d.signed_dist_km > cut).astype(int)
        d["rd"] = d.signed_dist_km - cut
        m = smf.ols(f"{o} ~ pside + rd + pside:rd + annual_total_mm + elevation_m", data=d).fit()
        rows.append(dict(outcome=o, placebo_cut_km=cut, n=int(m.nobs),
                         p_jump=m.pvalues["pside"], p_interaction=m.pvalues["pside:rd"]))
plc = pd.DataFrame(rows)
plc.round(5).to_csv(OUT / "placebo_cutoffs_cp_side.csv", index=False)
print("\n== Placebo cutoffs (Central Provinces side only) ==")
print(plc.round(4).to_string(index=False))

# ---------------------------------------------------------------- 5. influence
rows = []
for scale, df in SCALES.items():
    for o in OUTCOMES:
        d = df.dropna(subset=[o, "annual_total_mm", "elevation_m"]).reset_index(drop=True)
        m = smf.ols(FORMULA.format(o=o), data=d).fit()
        cd = m.get_influence().cooks_distance[0]
        top = int(np.argmax(cd))
        m2 = smf.ols(FORMULA.format(o=o), data=d.drop(top)).fit()
        rows.append(dict(scale=scale, outcome=o, most_influential=d.sdtname[top],
                         cooks_d=cd[top], threshold_4_over_n=4 / len(d),
                         p_int_full=m.pvalues[INT], p_int_drop_top=m2.pvalues[INT],
                         p_side_full=m.pvalues["side"], p_side_drop_top=m2.pvalues["side"]))
inf = pd.DataFrame(rows)
inf.round(5).to_csv(OUT / "influence_drop_most_influential.csv", index=False)
print("\n== Influence ==")
print(inf.round(4).to_string(index=False))

# ---------------------------------------------------------------- 6. coverage sensitivity
cov = pd.read_csv(DATA / "Climate" / "taluka_lst_ndvi_stats.csv")[
    ["dtname", "sdtname", "lst_valid_pct", "ndvi_valid_pct"]]
fc = full.merge(cov, on=["dtname", "sdtname"], how="left")
rows = []
for thr in [0, 25, 50]:
    sub = fc[fc.lst_valid_pct.fillna(0) >= thr]
    for o in ["kharif_to_rabi_decline", "lst_mean_c", "ag_laborer_to_cultivator"]:
        m = fit(sub, o)
        rows.append(dict(min_valid_pct=thr, outcome=o, n=int(m.nobs), n_berar=int((sub.side == 1).sum()),
                         p_side=m.pvalues["side"], p_int=m.pvalues[INT]))
cvg = pd.DataFrame(rows)
cvg.round(5).to_csv(OUT / "coverage_sensitivity.csv", index=False)
print("\n== Valid-pixel coverage sensitivity (full footprint) ==")
print(cvg.round(4).to_string(index=False))
print(f"Share of full-footprint talukas with <50% valid LST pixels: {(fc.lst_valid_pct < 50).mean():.0%}")

# ---------------------------------------------------------------- 7. collinearity
c = full[["signed_dist_km", "annual_total_mm", "elevation_m", "side"]].corr().round(2)
r2 = smf.ols("signed_dist_km ~ annual_total_mm + elevation_m", data=full).fit().rsquared
c.to_csv(OUT / "collinearity_full_footprint.csv")
print("\n== Collinearity (full footprint) ==")
print(c.to_string())
print(f"R2 of signed distance on rainfall + elevation: {r2:.2f}")

# ---------------------------------------------------------------- 8. corridor definition
print("\n== Corridor definition ==")
print(f"{(corridor.dist_to_boundary_km > 25).sum()} of {len(corridor)} corridor talukas have centroid "
      f"distance > 25 km (max {corridor.dist_to_boundary_km.max():.1f} km)")
print("Outputs written to", OUT)
