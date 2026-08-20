"""Second year of the same kharif/rabi Landsat pair as
download_seasonal_scenes.py, to check the NDVI decline reproduces
independently (Entry 7). Requires requests.
"""
import os
import requests

OUT_DIR = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\THE_COTTON_LINE\02_Data_Raw\Vegetation\seasonal_year2"
os.makedirs(OUT_DIR, exist_ok=True)

STAC_SEARCH = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SIGN_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
BBOX = [77.7, 19.1, 80.4, 21.3]  # corridor footprint, same as both prior passes
ROWS = [45, 46]                  # WRS-2 path 144, rows 045 and 046

WINDOWS = {
    "postmonsoon_y2": "2024-09-15/2024-11-15",
    "preharvest_y2": "2025-01-15/2025-03-15",
}


def search_best_scene(window_name, date_range, row):
    body = {
        "collections": ["landsat-c2-l2"],
        "bbox": BBOX,
        "datetime": date_range,
        "query": {
            "eo:cloud_cover": {"lt": 60},
            "landsat:wrs_path": {"eq": "144"},
            "landsat:wrs_row": {"eq": f"{row:03d}"},
        },
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
        "limit": 5,
    }
    r = requests.post(STAC_SEARCH, json=body, timeout=60)
    r.raise_for_status()
    features = r.json().get("features", [])
    if not features:
        print(f"  [{window_name} row{row:03d}] no scenes found in this window")
        return None
    best = features[0]
    cc = best["properties"].get("eo:cloud_cover")
    dt = best["properties"].get("datetime")
    print(f"  [{window_name} row{row:03d}] picked {best['id']}  date={dt}  cloud_cover={cc:.1f}%")
    return best


def sign_and_download(href, out_path):
    r = requests.get(SIGN_URL, params={"href": href}, timeout=30)
    r.raise_for_status()
    signed_url = r.json()["href"]
    with requests.get(signed_url, stream=True, timeout=300) as resp:
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    print(f"    saved -> {out_path}  ({os.path.getsize(out_path) / 1e6:.1f} MB)")


if __name__ == "__main__":
    for window_name, date_range in WINDOWS.items():
        print(f"\n=== {window_name} ({date_range}) ===")
        for row in ROWS:
            item = search_best_scene(window_name, date_range, row)
            if item is None:
                continue
            for band_key, band_label in [("red", "SR_B4"), ("nir08", "SR_B5")]:
                asset = item["assets"].get(band_key)
                if asset is None:
                    print(f"    missing asset {band_key} for {item['id']}")
                    continue
                out_name = f"{window_name}_144{row:03d}_{item['properties']['datetime'][:10]}_{band_label}.TIF"
                out_path = os.path.join(OUT_DIR, out_name)
                if os.path.exists(out_path):
                    print(f"    already have {out_name}, skipping")
                    continue
                sign_and_download(asset["href"], out_path)

    print("\nDone. Files landed in:", OUT_DIR)
    print("Next: pull these into the NDVI pipeline and compare against the year-1 result.")
