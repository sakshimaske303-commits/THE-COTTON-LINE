"""Taluka NDVI, LST (300 m Landsat) and WorldClim rainfall.

Out: Vegetation/taluka_eo_stats.csv, Hydrology/taluka_rainfall_worldclim.csv
Coverage = valid pixels / pixels inside the polygon. Decline on common pixels only,
NDVI <= 0 dropped. The 30 m masked version is 03b.
"""
import numpy as np
import pandas as pd

from cl_lib import PROC, RAW, read_tif, read_geojson_polygons, zonal_mask, sample_values

VEG, CLI = PROC / "Vegetation", PROC / "Climate"
talukas = read_geojson_polygons(PROC / "Administrative" / "vidarbha_talukas_120.geojson")

PAIRS = {
    "y1": ("ndvi_postmonsoon_300m.tif", "ndvi_preharvest_300m.tif"),
    "y2": ("ndvi_postmonsoon_y2_300m.tif", "ndvi_preharvest_y2_300m.tif"),
}
R = {k: (read_tif(VEG / a), read_tif(VEG / b)) for k, (a, b) in PAIRS.items()}
JUNE_NDVI = read_tif(VEG / "ndvi_fixed_300m_June2026.tif")
LST = read_tif(CLI / "lst_fixed_300m_June2026.tif")


def sample_at(r, X, Y):
    rows = np.floor((r.y0 - Y) / r.dy).astype(int)
    cols = np.floor((X - r.x0) / r.dx).astype(int)
    return sample_values(r, rows, cols)


rows = []
for props, polys in talukas:
    out = dict(dtname=props["dtname"], sdtname=props["sdtname"])
    for yr, (post, pre) in R.items():
        rr, cc = zonal_mask(post, polys)
        X = post.x0 + (cc + 0.5) * post.dx
        Y = post.y0 - (rr + 0.5) * post.dy
        a = sample_values(post, rr, cc)
        b = sample_at(pre, X, Y)
        common = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        npoly = len(rr)
        out[f"cov_{yr}_pct"] = 100 * common.sum() / npoly if npoly else np.nan
        out[f"npix_{yr}"] = int(common.sum())
        if common.sum():
            out[f"ndvi_post_{yr}"] = a[common].mean()
            out[f"ndvi_pre_{yr}"] = b[common].mean()
            out[f"decline_{yr}"] = (a[common] - b[common]).mean()
    for name, r in [("ndvi_june", JUNE_NDVI), ("lst_june", LST)]:
        rr, cc = zonal_mask(r, polys)
        v = sample_values(r, rr, cc)
        ok = np.isfinite(v)
        out[f"cov_{name}_pct"] = 100 * ok.sum() / len(rr) if len(rr) else np.nan
        out[name] = v[ok].mean() if ok.any() else np.nan
    rows.append(out)

E = pd.DataFrame(rows)
E.to_csv(VEG / "taluka_eo_stats.csv", index=False)
inscene = E[E.npix_y1 > 0]
print(f"EO stats: {len(inscene)} talukas with any year-1 pixel; "
      f"{(inscene.cov_y1_pct >= 50).sum()} with >= 50 % common-pixel coverage")

# ---------------------------------------------------------------- WorldClim at centroids
geo = pd.read_csv(PROC / "Administrative" / "taluka_geometry.csv")
months = []
for m in range(1, 13):
    r = read_tif(RAW / "Hydrology" / f"wc2.1_10m_prec_{m:02d}.tif")
    months.append(sample_at(r, geo.lon.to_numpy(), geo.lat.to_numpy()))
P = pd.DataFrame(np.array(months).T, columns=[f"prec_m{m:02d}" for m in range(1, 13)])
P.insert(0, "sdtname", geo.sdtname.values)
P.insert(0, "dtname", geo.dtname.values)
P["annual_total_mm"] = P.filter(like="prec_m").sum(axis=1)
P["monsoon_share_pct"] = 100 * P[["prec_m06", "prec_m07", "prec_m08", "prec_m09"]].sum(axis=1) / P.annual_total_mm
P.to_csv(PROC / "Hydrology" / "taluka_rainfall_worldclim.csv", index=False)
print(f"Rainfall: {P.annual_total_mm.notna().sum()} talukas")
