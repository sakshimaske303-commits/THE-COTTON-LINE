"""One row per taluka with every variable and sample flag.

Out: Phase4/analysis_taluka_dataset.csv (+ legacy phase4_master / phase4_fullfootprint tables)
Samples: corridor (25 km, 32 talukas); footprint (>= 50 % common-pixel coverage, per outcome);
census (119 talukas). Uses the 30 m NDVI stats when present.
"""
import numpy as np
import pandas as pd

from cl_lib import PROC

MIN_COV = 50.0

geo = pd.read_csv(PROC / "Administrative" / "taluka_geometry.csv")
eo = pd.read_csv(PROC / "Vegetation" / "taluka_eo_stats.csv")
EO_SOURCE = "300 m rasters, water/shadow screen (03)"
f30 = PROC / "Vegetation" / "taluka_eo_stats_30m.csv"
if f30.exists():  # 30 m masked rebuild (03b) replaces the 300 m NDVI columns
    e30 = pd.read_csv(f30)
    cols30 = [c for c in e30.columns if c.endswith(("_y1", "_y2", "_y1_pct", "_y2_pct")) or c.startswith("path_")]
    eo = eo.drop(columns=[c for c in cols30 if c in eo.columns]).merge(
        e30[["dtname", "sdtname"] + cols30], on=["dtname", "sdtname"], how="outer")
    EO_SOURCE = (f"30 m Landsat, QA mask={bool(e30.qa_mask.iloc[0])}, "
                 f"cropland mask={bool(e30.cropland_mask.iloc[0])} (03b)")
cen = pd.read_csv(PROC / "Population" / "census_taluka_stats_11districts.csv")
rain = pd.read_csv(PROC / "Hydrology" / "taluka_rainfall_worldclim.csv")[
    ["dtname", "sdtname", "annual_total_mm", "monsoon_share_pct"]]
elev = pd.read_csv(PROC / "Terrain" / "taluka_elevation_srtm.csv")

D = (geo.merge(eo, on=["dtname", "sdtname"], how="left")
        .merge(cen, on=["dtname", "sdtname"], how="left")
        .merge(rain, on=["dtname", "sdtname"], how="left")
        .merge(elev[["dtname", "sdtname", "elevation_m"]], on=["dtname", "sdtname"], how="left"))

D["in_footprint"] = D.npix_y1.fillna(0) > 0
D["eo_ok_y1"] = D.cov_y1_pct >= MIN_COV
D["eo_ok_y2"] = D.cov_y2_pct >= MIN_COV
D["eo_ok_lst"] = D.cov_lst_june_pct >= MIN_COV
D["has_census"] = D.ag_laborer_to_cultivator.notna()

# outcome columns used by the analysis, set to NaN where the sample rule excludes them
D["ndvi_decline_y1"] = D.decline_y1.where(D.eo_ok_y1)
D["ndvi_decline_y2"] = D.decline_y2.where(D.eo_ok_y2)
D["lst_june_c"] = D.lst_june.where(D.eo_ok_lst)
D.to_csv(PROC / "Phase4" / "analysis_taluka_dataset.csv", index=False)

legacy = D.rename(columns={"ndvi_decline_y1": "kharif_to_rabi_decline", "lst_june_c": "lst_mean_c",
                           "ndvi_post_y1": "ndvi_postmonsoon", "ndvi_pre_y1": "ndvi_preharvest"})
cols = ["dtname", "sdtname", "division", "side", "dist_to_boundary_km", "signed_dist_km", "ndvi_june",
        "ndvi_postmonsoon", "ndvi_preharvest", "kharif_to_rabi_decline", "ndvi_decline_y2", "lst_mean_c",
        "ag_laborer_to_cultivator", "literacy_pct", "net_area_pct", "forest_pct", "fallow_total_pct",
        "annual_total_mm", "elevation_m", "cov_y1_pct", "cov_y2_pct", "cov_lst_june_pct"]
legacy[legacy.in_corridor][cols].to_csv(PROC / "Phase4" / "phase4_master_dataset.csv", index=False)
legacy[legacy.in_footprint][cols].to_csv(PROC / "Phase4" / "phase4_fullfootprint_dataset.csv", index=False)

print(f"NDVI source: {EO_SOURCE}")
print(f"talukas {len(D)} | corridor {int(D.in_corridor.sum())} | footprint {int(D.in_footprint.sum())} | "
      f"NDVI y1 ok {int(D.eo_ok_y1.sum())} (Berar {int((D.eo_ok_y1 & (D.side == 1)).sum())}) | "
      f"y2 ok {int(D.eo_ok_y2.sum())} | LST ok {int(D.eo_ok_lst.sum())} | census {int(D.has_census.sum())} | "
      f"elevation {int(D.elevation_m.notna().sum())}")
