"""Same DN=0-as-real-data bug as the LST fix, here in SR_B4/SR_B5
reflectance. Reprocesses all 12 scenes with proper masking.
Requires rasterio, numpy.
"""
import glob
import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.merge import merge

RAW_DIR = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\PROJECT_PRISM\02_Data_Raw\Vegetation"
OUT_DIR = RAW_DIR
DST_CRS = "EPSG:4326"
SCALE, OFFSET = 0.0000275, -0.2


def process_band(band_suffix, out_name):
    raw_scenes = sorted(glob.glob(os.path.join(RAW_DIR, f"*_{band_suffix}.TIF")))
    print(f"\n[{band_suffix}] Found {len(raw_scenes)} raw scenes")
    reprojected_paths = []

    for scene in raw_scenes:
        name = os.path.splitext(os.path.basename(scene))[0]
        tmp_refl = os.path.join(OUT_DIR, f"_tmp_{name}_refl.tif")
        tmp_wgs84 = os.path.join(OUT_DIR, f"_tmp_{name}_wgs84.tif")

        with rasterio.open(scene) as src:
            dn = src.read(1).astype(np.float32)
            dn_masked = np.where(dn == 0, np.nan, dn)
            refl = dn_masked * SCALE + OFFSET
            out = np.where(np.isnan(refl), -9999, refl).astype(np.float32)

            profile = src.profile.copy()
            profile.update(dtype="float32", nodata=-9999, count=1)
            with rasterio.open(tmp_refl, "w", **profile) as dst:
                dst.write(out, 1)

        with rasterio.open(tmp_refl) as src:
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
        os.remove(tmp_refl)
        reprojected_paths.append(tmp_wgs84)
        print(f"  done: {name}")

    srcs = [rasterio.open(p) for p in reprojected_paths]
    mosaic, out_trans = merge(srcs, nodata=-9999)
    meta = srcs[0].meta.copy()
    meta.update({"height": mosaic.shape[1], "width": mosaic.shape[2],
                 "transform": out_trans, "nodata": -9999})
    out_path = os.path.join(OUT_DIR, out_name)
    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(mosaic)
    for s in srcs:
        s.close()
    for p in reprojected_paths:
        os.remove(p)

    valid = mosaic[mosaic != -9999]
    print(f"[{band_suffix}] Final merged: min={valid.min():.4f} max={valid.max():.4f} "
          f"mean={valid.mean():.4f} valid_pct={100*len(valid)/mosaic.size:.2f}%")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    process_band("SR_B4", "vegetation_mergedB4_FIXED.tif")
    process_band("SR_B5", "vegetation_mergedB5_FIXED.tif")
    print("\nNOTE: this replaces vegetation_mergedB4.tif. Once checked, delete the old one.")
    print("SR_B5 is included too so NDVI = (B5-B4)/(B5+B4) can be computed cleanly later.")
