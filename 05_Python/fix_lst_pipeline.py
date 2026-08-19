"""
fix_lst_pipeline.py  --  FIXED VERSION (Aug 2026)

Root-cause bug (confirmed by testing on a real scene):
Landsat Collection 2 Level-2 ST_B10 scenes use DN=0 as the fill/NoData
value (cloud-masked / off-swath pixels -- about a third of every scene).
The original pipeline applied the Kelvin scale/offset (x*0.00341802+149.0)
directly to the raw DN without masking DN=0 first. For DN=0 that produces
a fake reading of 149K = -124.15C, which is exactly the impossible
-123.15C minimum seen in both vidarbha_lst_merge.tif and
vidarbha_mergedLST.tif.

This script reprocesses ALL 12 raw ST_B10 scenes from scratch (not just
the 9 that had been converted before), so it also fixes the missing-3-
scenes gap in the same pass. It:
  1. Masks DN==0 as NoData BEFORE applying the Kelvin scale/offset.
  2. Converts to Celsius.
  3. Reprojects each scene to EPSG:4326.
  4. Merges all 12 into a single clean mosaic, respecting NoData.

Tested fix (on LC08_L2SP_144045_20260620 scene):
  BUGGY (old):   min=-124.15C  max=72.70C  mean=-5.69C
  FIXED (this):  min=13.15C   max=72.70C  mean=51.45C  valid=67.46%

Requires: rasterio, numpy  (pip install rasterio numpy --break-system-packages if missing)
"""
import glob
import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.merge import merge

RAW_DIR = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\PROJECT_PRISM\02_Data_Raw\Land_Use"
OUT_DIR = RAW_DIR
DST_CRS = "EPSG:4326"
SCALE, OFFSET = 0.00341802, 149.0

raw_scenes = sorted(glob.glob(os.path.join(RAW_DIR, "*_ST_B10.TIF")))
print(f"Found {len(raw_scenes)} raw ST_B10 scenes")

reprojected_paths = []

for scene in raw_scenes:
    name = os.path.splitext(os.path.basename(scene))[0]
    tmp_celsius = os.path.join(OUT_DIR, f"_tmp_{name}_celsius.tif")
    tmp_wgs84 = os.path.join(OUT_DIR, f"_tmp_{name}_wgs84.tif")

    with rasterio.open(scene) as src:
        dn = src.read(1).astype(np.float32)
        dn_masked = np.where(dn == 0, np.nan, dn)
        celsius = (dn_masked * SCALE + OFFSET) - 273.15
        out = np.where(np.isnan(celsius), -9999, celsius).astype(np.float32)

        profile = src.profile.copy()
        profile.update(dtype="float32", nodata=-9999, count=1)
        with rasterio.open(tmp_celsius, "w", **profile) as dst:
            dst.write(out, 1)

    # reproject to EPSG:4326
    with rasterio.open(tmp_celsius) as src:
        transform, width, height = calculate_default_transform(
            src.crs, DST_CRS, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({"crs": DST_CRS, "transform": transform,
                        "width": width, "height": height, "nodata": -9999})
        with rasterio.open(tmp_wgs84, "w", **kwargs) as dst:
            reproject(source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
                       src_transform=src.transform, src_crs=src.crs,
                       dst_transform=transform, dst_crs=DST_CRS,
                       src_nodata=-9999, dst_nodata=-9999,
                       resampling=Resampling.bilinear)
    os.remove(tmp_celsius)
    reprojected_paths.append(tmp_wgs84)
    print(f"  done: {name}")

# merge all reprojected scenes
srcs = [rasterio.open(p) for p in reprojected_paths]
mosaic, out_trans = merge(srcs, nodata=-9999)
meta = srcs[0].meta.copy()
meta.update({"height": mosaic.shape[1], "width": mosaic.shape[2],
             "transform": out_trans, "nodata": -9999})
out_path = os.path.join(OUT_DIR, "vidarbha_LST_merged_FIXED.tif")
with rasterio.open(out_path, "w", **meta) as dst:
    dst.write(mosaic)
for s in srcs:
    s.close()

# cleanup temp reprojected tiles
for p in reprojected_paths:
    os.remove(p)

valid = mosaic[mosaic != -9999]
print(f"\nFinal merged LST (fixed): min={valid.min():.2f}C max={valid.max():.2f}C mean={valid.mean():.2f}C")
print(f"Saved to: {out_path}")
print("\nNOTE: this replaces BOTH vidarbha_lst_merge.tif and vidarbha_mergedLST.tif.")
print("Once you've checked the new file, you can delete the two old buggy merges")
print("and the stray 8-byte A1_LST_Celcius.tif (leftover broken test file).")
