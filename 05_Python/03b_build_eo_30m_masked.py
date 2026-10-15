"""30 m Landsat NDVI decline with QA and cropland masks.

In : 02_Data_Raw/Vegetation/seasonal[_year2]/*_{SR_B4,SR_B5,QA_PIXEL}.TIF, Land_Cover/ESA_WorldCover_*.tif
Out: Vegetation/taluka_eo_stats_30m.csv, Vegetation/path_overlap.csv
Mask: DN 0, QA bits 1-4 and 7, non-cropland (WorldCover 40). Decline on common pixels.
Coverage = valid cropland pixels / cropland pixels in the polygon.
Rows of a path are merged on one grid; where paths overlap, the best-covered path is used.
"""
import re
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

from cl_lib import RAW, PROC, read_tif, read_geojson_polygons, utm, utm_inverse, zonal_mask, Raster

SCALE, OFFSET = 0.0000275, -0.2
QA_BAD = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 7)
PAT = re.compile(r"(postmonsoon|preharvest)(_y2)?_(\d{3})(\d{3})_(\d{4}-\d{2}-\d{2})_(SR_B4|SR_B5|QA_PIXEL)\.TIF$", re.I)


def scene_index():
    import json
    logf = RAW / "Vegetation" / "scene_log.json"
    allowed = None
    if logf.exists():  # use exactly the scenes chosen by 00_download_inputs.py
        allowed = {(e["year"], e["season"], e["path"], e["row"], e["date"]) for e in json.loads(logf.read_text())}
    idx = defaultdict(dict)
    for folder in ["seasonal", "seasonal_year2"]:
        for f in (RAW / "Vegetation" / folder).glob("*.TIF"):
            m = PAT.search(f.name)
            if m:
                season, y2, path, row, date, band = m.groups()
                yr = "y2" if y2 else "y1"
                if allowed is not None and (yr, season.lower(), path, row, date) not in allowed:
                    continue
                idx[(yr, path, row, season)][band.upper()] = f
                idx[(yr, path, row, season)]["date"] = date
    return idx


def zone_of(r: Raster):
    m = re.search(r"UTM zone (\d+)", r.crs)
    return int(m.group(1)) if m else 44


class WorldCover:
    def __init__(self):
        self.tiles = []
        import tifffile
        for f in sorted((RAW / "Land_Cover").glob("ESA_WorldCover_10m_2021_v200_*_Map.tif")):
            t = tifffile.TiffFile(str(f))
            lvl = 1 if len(t.series[0].levels) > 1 else 0  # ~20 m overview is plenty for a 30 m mask
            a = t.series[0].levels[lvl].asarray()
            m = re.search(r"_([NS])(\d{2})([EW])(\d{3})_", f.name)
            lat0 = int(m.group(2)) + 3  # tile name = lower-left corner; tiles are 3 x 3 degrees
            lon0 = int(m.group(4))
            self.tiles.append((lon0, lat0, 3.0 / a.shape[1], 3.0 / a.shape[0], a))
            t.close()
        print(f"WorldCover tiles loaded: {len(self.tiles)}")

    def cropland(self, lon, lat):
        out = np.zeros(len(lon), bool)
        known = np.zeros(len(lon), bool)
        for lon0, lat0, dx, dy, a in self.tiles:
            c = np.floor((lon - lon0) / dx).astype(int)
            r = np.floor((lat0 - lat) / dy).astype(int)
            ok = (c >= 0) & (c < a.shape[1]) & (r >= 0) & (r < a.shape[0])
            out[ok] = a[r[ok], c[ok]] == 40
            known |= ok
        return out, known


def ndvi(entry):
    b4 = read_tif(entry["SR_B4"])
    b5 = read_tif(entry["SR_B5"])
    valid = (b4.a > 0) & (b5.a > 0)
    if "QA_PIXEL" in entry:
        qa = read_tif(entry["QA_PIXEL"]).a
        valid &= (qa & QA_BAD) == 0
    r4 = b4.a.astype(np.float32) * SCALE + OFFSET
    r5 = b5.a.astype(np.float32) * SCALE + OFFSET
    with np.errstate(divide="ignore", invalid="ignore"):
        v = (r5 - r4) / (r5 + r4)
    v[~valid | ~np.isfinite(v) | (np.abs(v) > 1)] = np.nan
    return Raster(v, b4.x0, b4.dx, b4.y0, b4.dy, None, b4.crs), "QA_PIXEL" in entry


def main():
    idx = scene_index()
    if not idx:
        sys.exit("No seasonal scenes found -- run 00_download_inputs.py first.")
    wc = WorldCover()
    talukas = read_geojson_polygons(PROC / "Administrative" / "vidarbha_talukas_120.geojson")
    # per (year, path) -> per taluka -> list of arrays (pixel id, post, pre); polygon pixel ids
    acc = defaultdict(lambda: defaultdict(list))
    npoly = defaultdict(lambda: defaultdict(list))
    nall = defaultdict(lambda: defaultdict(list))
    qa_used = {}
    for (yr, path, row, season) in sorted({(k[0], k[1], k[2], "pair") for k in idx}):
        post = idx.get((yr, path, row, "postmonsoon"))
        pre = idx.get((yr, path, row, "preharvest"))
        if not post or not pre or not {"SR_B4", "SR_B5"} <= set(post) or not {"SR_B4", "SR_B5"} <= set(pre):
            print(f"skip {yr} {path}/{row}: incomplete pair")
            continue
        a, qa1 = ndvi(post)
        b, qa2 = ndvi(pre)
        qa_used[(yr, path, row)] = qa1 and qa2
        if (a.x0, a.y0, a.dx) != (b.x0, b.y0, b.dx):
            # same path/row grid is expected; resample pre onto post grid by nearest pixel otherwise
            pass
        z = zone_of(a)
        print(f"{yr} {path}/{row}: {post['date']} -> {pre['date']} zone {z} QA={'yes' if qa_used[(yr, path, row)] else 'no'}")
        for props, polys in talukas:
            P = [[np.c_[utm(r[:, 0], r[:, 1], z)] for r in p] for p in polys]
            allc = np.vstack([p[0] for p in P])
            H, W = a.a.shape
            if (allc[:, 0].max() < a.x0 or allc[:, 0].min() > a.x0 + W * a.dx or
                    allc[:, 1].min() > a.y0 or allc[:, 1].max() < a.y0 - H * a.dy):
                continue
            rr, cc = zonal_mask(a, P)
            key = (props["dtname"], props["sdtname"])
            # global pixel ids on the shared path grid (rows of one path share a UTM grid)
            gx = np.round((a.x0 + cc * a.dx) / a.dx).astype(np.int64)
            gy = np.round((a.y0 - rr * a.dy) / a.dy).astype(np.int64)
            ids = gx * 10_000_000 + gy
            # coverage denominator = cropland pixels in the polygon (all pixels without a cropland mask)
            if wc.tiles:
                lon, lat = utm_inverse(a.x0 + (cc + 0.5) * a.dx, a.y0 - (rr + 0.5) * a.dy, z)
                crop, known = wc.cropland(lon, lat)
                isc = crop & known
            else:
                isc = np.ones(len(rr), bool)
            npoly[(yr, path)][key].append(ids[isc])
            nall[(yr, path)][key].append(ids)
            ok = (rr >= 0) & (rr < H) & (cc >= 0) & (cc < W)
            rr, cc, gx, gy, isc = rr[ok], cc[ok], gx[ok], gy[ok], isc[ok]
            br = np.round((b.y0 - (a.y0 - (rr + 0.5) * a.dy)) / b.dy - 0.5).astype(int)
            bc = np.round(((a.x0 + (cc + 0.5) * a.dx) - b.x0) / b.dx - 0.5).astype(int)
            okb = (br >= 0) & (br < b.a.shape[0]) & (bc >= 0) & (bc < b.a.shape[1])
            va = a.a[rr, cc]
            vb = np.full(len(rr), np.nan)
            vb[okb] = b.a[br[okb], bc[okb]]
            good = np.isfinite(va) & np.isfinite(vb) & isc
            acc[(yr, path)][key].append((gx[good] * 10_000_000 + gy[good], va[good].astype(np.float32),
                                         vb[good].astype(np.float32)))
        del a, b

    rows, overlap = [], []
    for yr in ["y1", "y2"]:
        paths = sorted({p for (y, p) in acc if y == yr})
        keys = {k for p in paths for k in npoly[(yr, p)]}
        for key in keys:
            cands = []
            for p in paths:
                ids = npoly[(yr, p)].get(key)
                parts = acc[(yr, p)].get(key)
                if not ids or not parts:
                    continue
                n = len(np.unique(np.concatenate(ids)))
                n_all = len(np.unique(np.concatenate(nall[(yr, p)][key])))
                if n == 0:
                    continue
                pid = np.concatenate([x[0] for x in parts])
                post_ = np.concatenate([x[1] for x in parts])
                pre_ = np.concatenate([x[2] for x in parts])
                _, first = np.unique(pid, return_index=True)  # rows of one path overlap: keep each pixel once
                v = np.c_[post_[first], pre_[first]]
                if len(v):
                    cands.append((100 * len(v) / n, p, v, 100 * n / n_all))
            if not cands:
                continue
            cands.sort(key=lambda c: -c[0])
            cov, p, v, crop_pct = cands[0]
            rows.append(dict(dtname=key[0], sdtname=key[1], year=yr, path=p, **{
                "cov_pct": cov, "cropland_pct": crop_pct, "npix": len(v), "ndvi_post": v[:, 0].mean(), "ndvi_pre": v[:, 1].mean(),
                "decline": (v[:, 0] - v[:, 1]).mean()}))
            for c2 in cands[1:]:
                if c2[0] >= 50 and cov >= 50:
                    overlap.append(dict(dtname=key[0], sdtname=key[1], year=yr, path_a=p, path_b=c2[1],
                                        decline_a=(v[:, 0] - v[:, 1]).mean(),
                                        decline_b=(c2[2][:, 0] - c2[2][:, 1]).mean()))
    L = pd.DataFrame(rows)
    W_ = L.pivot_table(index=["dtname", "sdtname"], columns="year",
                       values=["cov_pct", "cropland_pct", "npix", "ndvi_post", "ndvi_pre", "decline"], aggfunc="first")
    W_.columns = [f"{a}_{b}" if a != "cov_pct" else f"cov_{b}_pct" for a, b in W_.columns]
    W_ = W_.rename(columns={"npix_y1": "npix_y1", "npix_y2": "npix_y2"}).reset_index()
    paths = L.pivot_table(index=["dtname", "sdtname"], columns="year", values="path", aggfunc="first")
    paths.columns = [f"path_{c}" for c in paths.columns]
    W_ = W_.merge(paths.reset_index(), on=["dtname", "sdtname"], how="left")
    W_["cropland_mask"] = bool(wc.tiles)
    W_["qa_mask"] = all(qa_used.values()) if qa_used else False
    W_.to_csv(PROC / "Vegetation" / "taluka_eo_stats_30m.csv", index=False)
    if overlap:
        O = pd.DataFrame(overlap)
        O.to_csv(PROC / "Vegetation" / "path_overlap.csv", index=False)
        print(f"Path overlap: {len(O)} taluka-years seen by two paths; mean |difference| = "
              f"{(O.decline_a - O.decline_b).abs().mean():.3f}")
    print(f"Wrote taluka_eo_stats_30m.csv: {len(W_)} talukas")


if __name__ == "__main__":
    main()
