"""Download inputs for the 30 m masked rebuild.

Landsat 8/9 C2 L2 (Planetary Computer): paths 144-146 x rows 045-047, both seasonal windows,
both years; SR_B4, SR_B5, QA_PIXEL. One date per path and window, shared by all rows.
ESA WorldCover 2021 tiles for the cropland mask (class 40).
Resumes interrupted downloads; skips files already on disk. About 7-9 GB.

    python 05_Python/00_download_inputs.py
"""
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_Data_Raw"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
PATHS, ROWS = ["144", "145", "146"], ["045", "046", "047"]
WINDOWS = {
    "y1": {"postmonsoon": "2025-10-25/2025-11-20", "preharvest": "2026-02-25/2026-03-20"},
    "y2": {"postmonsoon": "2024-10-25/2024-11-20", "preharvest": "2025-02-25/2025-03-20"},
}
BANDS = {"red": "SR_B4", "nir08": "SR_B5", "qa_pixel": "QA_PIXEL"}
WC_TILES = ["N18E075", "N18E078", "N21E075", "N21E078"]
WC_URL = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_{t}_Map.tif"


def search(path, row, window):
    body = {"collections": ["landsat-c2-l2"], "datetime": window, "limit": 50,
            "query": {"landsat:wrs_path": {"eq": path}, "landsat:wrs_row": {"eq": row},
                      "eo:cloud_cover": {"lt": 30}, "platform": {"in": ["landsat-8", "landsat-9"]}}}
    r = requests.post(STAC, json=body, timeout=60)
    r.raise_for_status()
    return r.json().get("features", [])


def fetch(url_fn, out, tries=8):
    """Stream to <out>.part, resuming with an HTTP Range request after a dropped connection."""
    tmp = out.with_suffix(".part")
    for attempt in range(1, tries + 1):
        have = tmp.stat().st_size if tmp.exists() else 0
        try:
            headers = {"Range": f"bytes={have}-"} if have else {}
            with requests.get(url_fn(), stream=True, timeout=(30, 120), headers=headers) as resp:
                if resp.status_code == 416:  # already complete
                    break
                resp.raise_for_status()
                mode = "ab" if have and resp.status_code == 206 else "wb"
                with open(tmp, mode) as f:
                    for chunk in resp.iter_content(1 << 20):
                        f.write(chunk)
            break
        except (requests.exceptions.RequestException, ConnectionError) as e:
            wait = min(60, 5 * attempt)
            print(f"   connection dropped ({type(e).__name__}); retry {attempt}/{tries} in {wait}s, resuming")
            time.sleep(wait)
    else:
        sys.exit(f"Gave up on {out.name} after {tries} tries -- check the internet and run the script again.")
    tmp.replace(out)


def download(href, out):
    if out.exists() and out.stat().st_size > 0:
        print("   have", out.name)
        return
    # signed URLs expire, so sign again on every attempt
    fetch(lambda: requests.get(SIGN, params={"href": href}, timeout=60).json()["href"], out)
    print(f"   saved {out.name} ({out.stat().st_size / 1e6:.0f} MB)")


def main():
    log = []
    for yr, wins in WINDOWS.items():
        folder = RAW / "Vegetation" / ("seasonal" if yr == "y1" else "seasonal_year2")
        folder.mkdir(parents=True, exist_ok=True)
        prefix_y2 = "" if yr == "y1" else "_y2"
        for season, window in wins.items():
            for path in PATHS:
                per_row = {row: search(path, row, window) for row in ROWS}
                dates = None
                for row, feats in per_row.items():
                    ds = {f["properties"]["datetime"][:10] for f in feats}
                    dates = ds if dates is None else dates & ds
                if not dates:
                    print(f"[{yr} {season} path {path}] no date shared by all rows -- picking per row")
                for row, feats in per_row.items():
                    pool = [f for f in feats if not dates or f["properties"]["datetime"][:10] in dates]
                    if not pool:
                        print(f"[{yr} {season} {path}/{row}] nothing under 30 % cloud in {window}")
                        continue
                    if dates:  # same date for every row of the path: lowest mean cloud across rows
                        best_date = min(dates, key=lambda d: sum(
                            f["properties"]["eo:cloud_cover"] for fs in per_row.values() for f in fs
                            if f["properties"]["datetime"][:10] == d))
                        pool = [f for f in pool if f["properties"]["datetime"][:10] == best_date]
                    item = min(pool, key=lambda f: f["properties"]["eo:cloud_cover"])
                    date = item["properties"]["datetime"][:10]
                    cc = item["properties"]["eo:cloud_cover"]
                    print(f"[{yr} {season} {path}/{row}] {item['id']} {date} cloud {cc:.1f}%")
                    log.append(dict(year=yr, season=season, path=path, row=row, id=item["id"], date=date, cloud=cc))
                    for key, band in BANDS.items():
                        if key in item["assets"]:
                            out = folder / f"{season}{prefix_y2}_{path}{row}_{date}_{band}.TIF"
                            download(item["assets"][key]["href"], out)
    (RAW / "Vegetation" / "scene_log.json").write_text(json.dumps(log, indent=2))

    wc = RAW / "Land_Cover"
    wc.mkdir(parents=True, exist_ok=True)
    for t in WC_TILES:
        out = wc / f"ESA_WorldCover_10m_2021_v200_{t}_Map.tif"
        if out.exists():
            print("   have", out.name)
            continue
        print("WorldCover", t)
        fetch(lambda: WC_URL.format(t=t), out)
    print("\nDone. Scene list: 02_Data_Raw/Vegetation/scene_log.json\nNext: python 05_Python/run_all.py --full")


if __name__ == "__main__":
    sys.exit(main())
