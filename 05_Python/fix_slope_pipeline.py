"""Fixes the impossible ~88.57 deg mean slope (was computed in EPSG:4326
degree-pixels); reprojects to UTM 44N first. Fixed mean=3.65 deg.
Requires rasterio, numpy, scipy.
"""
import os
import gc
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.warp import calculate_default_transform, reproject, Resampling
from scipy.ndimage import binary_dilation

TERRAIN_DIR = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\THE_COTTON_LINE\02_Data_Raw\Terrain"
DEM_SRC = os.path.join(TERRAIN_DIR, "dem_merged.tif")
DEM_UTM = os.path.join(TERRAIN_DIR, "_tmp_dem_utm44n.tif")
SLOPE_OUT = os.path.join(TERRAIN_DIR, "vidarbha_slope_FIXED.tif")
DST_CRS = "EPSG:32644"  # UTM 44N -- correct zone for Vidarbha


def reproject_dem():
    with rasterio.open(DEM_SRC) as src:
        transform, width, height = calculate_default_transform(
            src.crs, DST_CRS, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({"crs": DST_CRS, "transform": transform,
                        "width": width, "height": height, "nodata": -32768})
        with rasterio.open(DEM_UTM, "w", **kwargs) as dst:
            reproject(source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
                       src_transform=src.transform, src_crs=src.crs,
                       dst_transform=transform, dst_crs=DST_CRS,
                       src_nodata=src.nodata, dst_nodata=-32768,
                       resampling=Resampling.bilinear)
    print("Reprojected DEM to EPSG:32644 ->", DEM_UTM)


def compute_slope_chunked():
    with rasterio.open(DEM_UTM) as src:
        H, W = src.height, src.width
        nodata = src.nodata
        xres, yres = src.res
        profile = src.profile.copy()
        profile.update(dtype="float32", nodata=-9999, compress="deflate", predictor=3)

        chunk = 1000
        stats_min, stats_max = np.inf, -np.inf
        stats_sum, stats_sumsq, stats_count = 0.0, 0.0, 0

        with rasterio.open(SLOPE_OUT, "w", **profile) as dst:
            for row0 in range(0, H, chunk):
                row1 = min(row0 + chunk, H)
                buf_top = 1 if row0 > 0 else 0
                buf_bot = 1 if row1 < H else 0
                win = Window(0, row0 - buf_top, W, (row1 + buf_bot) - (row0 - buf_top))
                dem = src.read(1, window=win).astype(np.float32)
                mask = (dem == nodata)
                dem_f = np.where(mask, np.nan, dem)

                dzdy, dzdx = np.gradient(dem_f, yres, xres)
                slope = np.degrees(np.arctan(np.sqrt(dzdx**2 + dzdy**2))).astype(np.float32)
                inv = binary_dilation(mask, iterations=1)
                slope = np.where(inv, np.nan, slope).astype(np.float32)

                trimmed = slope[buf_top: slope.shape[0] - buf_bot if buf_bot else slope.shape[0], :]
                valid = trimmed[~np.isnan(trimmed)]
                if valid.size:
                    stats_min = min(stats_min, float(valid.min()))
                    stats_max = max(stats_max, float(valid.max()))
                    stats_sum += float(valid.sum())
                    stats_sumsq += float((valid.astype(np.float64) ** 2).sum())
                    stats_count += valid.size

                out_chunk = np.where(np.isnan(trimmed), -9999, trimmed).astype(np.float32)
                dst.write(out_chunk, 1, window=Window(0, row0, W, row1 - row0))
                del dem, mask, dem_f, dzdy, dzdx, slope, inv, trimmed, valid, out_chunk
                gc.collect()

    mean = stats_sum / stats_count
    std = (stats_sumsq / stats_count - mean ** 2) ** 0.5
    print(f"\nFinal slope (fixed): min={stats_min:.3f} max={stats_max:.3f} "
          f"mean={mean:.3f} std={std:.3f} valid_pct={100*stats_count/(H*W):.2f}%")
    print(f"Saved to: {SLOPE_OUT}")


if __name__ == "__main__":
    reproject_dem()
    compute_slope_chunked()
    os.remove(DEM_UTM)
    print("\nNOTE: this replaces vidarbha_slope.tif. Once checked, delete the old buggy one.")
