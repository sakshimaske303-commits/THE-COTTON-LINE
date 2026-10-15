"""Taluka centroids, signed distance to the boundary and corridor flag.

In : Administrative/vidarbha_talukas_120.geojson, division_boundary_line.geojson
Out: Administrative/taluka_geometry.csv
UTM 44N (EPSG:32644). signed_dist_km > 0 on the Berar side. Corridor = polygon within 25 km of the line.
"""
import json

import numpy as np
import pandas as pd

from cl_lib import (PROC, BERAR_DISTRICTS, read_geojson_polygons, project_polys, utm,
                    poly_centroid_area, point_line_distance, points_in_polys)

ADMIN = PROC / "Administrative"
line = np.asarray(json.loads((ADMIN / "division_boundary_line.geojson").read_text())
                  ["features"][0]["geometry"]["coordinates"], float)
LU = np.c_[utm(line[:, 0], line[:, 1])]
print(f"Boundary length: {np.sqrt((np.diff(LU, axis=0) ** 2).sum(1)).sum() / 1000:.1f} km")

rows = []
for props, polys in read_geojson_polygons(ADMIN / "vidarbha_talukas_120.geojson"):
    P = project_polys(polys)
    cx, cy, A = poly_centroid_area(P)
    side = int(props["dtname"] in BERAR_DISTRICTS)
    d = point_line_distance(np.array([[cx, cy]]), LU)[0] / 1000
    verts = np.vstack([r for p in P for r in p])
    dmin = point_line_distance(verts, LU).min() / 1000
    in_cor = bool(dmin <= 25 or points_in_polys(P, LU).any())
    lon_c, lat_c, _ = poly_centroid_area(polys)  # planar centroid in degrees, for raster sampling
    rows.append(dict(dtname=props["dtname"], sdtname=props["sdtname"],
                     division="Amravati (Berar)" if side else "Nagpur (Central Provinces)",
                     side=side, lon=lon_c, lat=lat_c, x_km=cx / 1000, y_km=cy / 1000, area_km2=A / 1e6,
                     dist_to_boundary_km=d, signed_dist_km=d if side else -d,
                     in_corridor=in_cor))
G = pd.DataFrame(rows).sort_values(["side", "dtname", "sdtname"], ascending=[False, True, True])
G.to_csv(ADMIN / "taluka_geometry.csv", index=False)
c = G[G.in_corridor]
print(f"{len(G)} talukas; corridor {len(c)} ({int(c.side.sum())} Berar / {int((1 - c.side).sum())} CP); "
      f"{(c.dist_to_boundary_km > 25).sum()} corridor centroids > 25 km (max {c.dist_to_boundary_km.max():.1f})")
