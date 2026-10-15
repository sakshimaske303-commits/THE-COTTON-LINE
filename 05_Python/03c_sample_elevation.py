"""SRTM elevation at all 120 taluka centroids.

In : 02_Data_Raw/Terrain/n{LAT}_e{LON}_1arc_v3.tif
Out: Terrain/taluka_elevation_srtm.csv
"""
import numpy as np
import pandas as pd

from cl_lib import RAW, PROC, read_tif

geo = pd.read_csv(PROC / "Administrative" / "taluka_geometry.csv")
cache, vals = {}, []
for lon, lat in zip(geo.lon, geo.lat):
    name = f"n{int(np.floor(lat)):02d}_e{int(np.floor(lon)):03d}_1arc_v3.tif"
    if name not in cache:
        f = RAW / "Terrain" / name
        cache[name] = read_tif(f) if f.exists() else None
    r = cache[name]
    if r is None:
        vals.append(np.nan)
        continue
    row = int(round((r.y0 - lat) / r.dy))
    col = int(round((lon - r.x0) / r.dx))
    v = float(r.a[row, col])
    vals.append(np.nan if v == r.nodata else v)
out = geo[["dtname", "sdtname"]].copy()
out["elevation_m"] = vals
out["source"] = "SRTM 1 arc-second, cell under taluka centroid (03c_sample_elevation.py)"
old = PROC / "Terrain" / "taluka_elevation_srtm.csv"
if old.exists():
    prev = pd.read_csv(old)
    o = prev.merge(out, on=["dtname", "sdtname"], suffixes=("_old", "")).dropna(subset=["elevation_m", "elevation_m_old"])
    if len(o):
        print(f"check vs previous values ({len(o)} talukas): max |difference| = "
              f"{(o.elevation_m_old - o.elevation_m).abs().max():.0f} m")
    # keep a previous value where the tile is not on disk
    out = out.merge(prev[["dtname", "sdtname", "elevation_m"]].rename(columns={"elevation_m": "prev"}),
                    on=["dtname", "sdtname"], how="left")
    out["elevation_m"] = out.elevation_m.fillna(out.prev)
    out = out.drop(columns="prev")
out.to_csv(old, index=False)
print(f"elevation for {out.elevation_m.notna().sum()} of {len(out)} talukas; missing tiles: "
      f"{[k for k, v in cache.items() if v is None]}")
