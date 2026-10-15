"""Census 2011 village attributes aggregated to taluka, all 11 districts.

In : 02_Data_Raw/Population/<district>.zip (POCRA village shapefiles, .dbf only)
Out: Population/census_taluka_stats_11districts.csv
Rural villages only. ag_laborer_to_cultivator = labourers / cultivators (main + marginal);
net_area_pct = net sown / reported area. area_irri is not exported (58-92 %, not credible).
"""
import zipfile

import numpy as np
import pandas as pd

from cl_lib import RAW, PROC, read_dbf, norm_name

NEED = ["main_cl_p", "main_al_p", "marg_cl_p", "marg_al_p", "p_lit", "p_ill", "tot_popu", "tot_hh",
        "area_ha", "forest", "area_non_a", "barren_unc", "perm_graze", "misc_crop", "cult_waste",
        "fallow", "curr_fallo", "net_area"]
LU = ["forest", "area_non_a", "barren_unc", "perm_graze", "misc_crop", "cult_waste", "fallow",
      "curr_fallo", "net_area"]

frames = []
for z in sorted((RAW / "Population").glob("*.zip")):
    with zipfile.ZipFile(z) as zf:
        dbf = [n for n in zf.namelist() if n.lower().endswith(".dbf")][0]
        d = read_dbf(zf.read(dbf))
    g = d.groupby(["district_n", "taluka_nam"])[NEED].sum(min_count=1).reset_index()
    g["n_villages"] = d.groupby(["district_n", "taluka_nam"]).size().values
    frames.append(g)
    print(f"{z.stem:12s} {len(d):5d} villages -> {len(g):2d} talukas")
C = pd.concat(frames, ignore_index=True)
C["ag_laborer_to_cultivator"] = (C.main_al_p + C.marg_al_p) / (C.main_cl_p + C.marg_cl_p)
C["literacy_pct"] = 100 * C.p_lit / (C.p_lit + C.p_ill)
for c in ["forest", "net_area"]:
    C[f"{c}_pct"] = 100 * C[c] / C.area_ha
C["fallow_total_pct"] = 100 * (C.fallow + C.curr_fallo) / C.area_ha
C["landuse_closure_pct"] = 100 * C[LU].sum(axis=1) / C.area_ha

# match to the 120-taluka geometry names
geo = pd.read_csv(PROC / "Administrative" / "taluka_geometry.csv")
DIST = {"buldhana": "buldana", "gondia": "gondiya"}
geo["k"] = geo.dtname.map(norm_name) + "|" + geo.sdtname.map(norm_name)
C["k"] = C.district_n.map(lambda s: DIST.get(norm_name(s), norm_name(s))) + "|" + C.taluka_nam.map(norm_name)
ALIAS = {  # census spelling -> geometry spelling, where they differ
    "nagpur|nagpurrural": "nagpur|nagpurrural",
}
C["k"] = C.k.replace(ALIAS)
m = C.merge(geo[["k", "dtname", "sdtname"]], on="k", how="left")
miss = m[m.sdtname.isna()]
if len(miss):
    print("UNMATCHED census talukas:", miss[["district_n", "taluka_nam"]].values.tolist())
out = m.dropna(subset=["sdtname"])[["dtname", "sdtname", "n_villages", "tot_popu", "tot_hh",
                                    "ag_laborer_to_cultivator", "literacy_pct", "net_area_pct",
                                    "forest_pct", "fallow_total_pct", "landuse_closure_pct"]]
(PROC / "Population").mkdir(exist_ok=True)
out.to_csv(PROC / "Population" / "census_taluka_stats_11districts.csv", index=False)
print(f"{len(out)} talukas written; geometry talukas without census villages: "
      f"{sorted(set(geo.sdtname) - set(out.sdtname))}")
