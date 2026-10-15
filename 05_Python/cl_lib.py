"""Shared helpers: UTM projection, polygons, GeoTIFF and DBF reading,
OLS with HC3 / cluster / Conley errors, Moran's I, Holm and BH corrections.
numpy, pandas, scipy, tifffile only.
"""
from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.path import Path as MplPath
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_Data_Raw"
PROC = ROOT / "03_Data_Processed"
OUTFIG = ROOT / "07_Outputs"

BERAR_DISTRICTS = {"Akola", "Amravati", "Buldana", "Buldhana", "Washim", "Yavatmal"}


# =============================================================== geo
def utm(lon, lat, zone=44):
    """Forward transverse Mercator (Krueger series), WGS84 -> UTM metres (northern)."""
    a = 6378137.0
    f = 1 / 298.257223563
    k0 = 0.9996
    n = f / (2 - f)
    A = a / (1 + n) * (1 + n ** 2 / 4 + n ** 4 / 64)
    al = [None, n / 2 - 2 * n ** 2 / 3 + 5 * n ** 3 / 16,
          13 * n ** 2 / 48 - 3 * n ** 3 / 5, 61 * n ** 3 / 240]
    lon = np.radians(np.asarray(lon, float))
    lat = np.radians(np.asarray(lat, float))
    lon0 = np.radians(zone * 6 - 183)
    t = np.sinh(np.arctanh(np.sin(lat)) - 2 * np.sqrt(n) / (1 + n)
                * np.arctanh(2 * np.sqrt(n) / (1 + n) * np.sin(lat)))
    xi = np.arctan2(t, np.cos(lon - lon0))
    eta = np.arctanh(np.sin(lon - lon0) / np.sqrt(1 + t ** 2))
    E = 500000 + k0 * A * (eta + sum(al[j] * np.cos(2 * j * xi) * np.sinh(2 * j * eta) for j in range(1, 4)))
    N = k0 * A * (xi + sum(al[j] * np.sin(2 * j * xi) * np.cosh(2 * j * eta) for j in range(1, 4)))
    return E, N


def utm_inverse(E, N, zone=44):
    """Inverse transverse Mercator (Krueger series), UTM metres (northern) -> lon, lat degrees."""
    a = 6378137.0
    f = 1 / 298.257223563
    k0 = 0.9996
    n = f / (2 - f)
    A = a / (1 + n) * (1 + n ** 2 / 4 + n ** 4 / 64)
    be = [None, n / 2 - 2 * n ** 2 / 3 + 37 * n ** 3 / 96, n ** 2 / 48 + n ** 3 / 15, 17 * n ** 3 / 480]
    de = [None, 2 * n - 2 * n ** 2 / 3 - 2 * n ** 3, 7 * n ** 2 / 3 - 8 * n ** 3 / 5, 56 * n ** 3 / 15]
    xi = np.asarray(N, float) / (k0 * A)
    eta = (np.asarray(E, float) - 500000) / (k0 * A)
    xi_ = xi - sum(be[j] * np.sin(2 * j * xi) * np.cosh(2 * j * eta) for j in range(1, 4))
    eta_ = eta - sum(be[j] * np.cos(2 * j * xi) * np.sinh(2 * j * eta) for j in range(1, 4))
    chi = np.arcsin(np.sin(xi_) / np.cosh(eta_))
    lat = chi + sum(de[j] * np.sin(2 * j * chi) for j in range(1, 4))
    lon = np.radians(zone * 6 - 183) + np.arctan2(np.sinh(eta_), np.cos(xi_))
    return np.degrees(lon), np.degrees(lat)


def read_geojson_polygons(path):
    """Return list of (properties, polys) where polys = [[outer, hole, ...], ...] in lon/lat."""
    g = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for ft in g["features"]:
        gm = ft["geometry"]
        polys = [gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]
        polys = [[np.asarray(r, float)[:, :2] for r in p] for p in polys]
        out.append((ft["properties"], polys))
    return out


def project_polys(polys, zone=44):
    return [[np.c_[utm(r[:, 0], r[:, 1], zone)] for r in p] for p in polys]


def _ring(xy):
    x, y = xy[:, 0], xy[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    c = x * y1 - x1 * y
    A = c.sum() / 2
    return A, ((x + x1) * c).sum() / (6 * A), ((y + y1) * c).sum() / (6 * A)


def poly_centroid_area(polys_xy):
    At = cx = cy = 0.0
    for rings in polys_xy:
        for i, r in enumerate(rings):
            A, x, y = _ring(r)
            A = abs(A) * (1 if i == 0 else -1)
            At += A
            cx += A * x
            cy += A * y
    return cx / At, cy / At, At


def point_line_distance(P, L):
    """Minimum Euclidean distance from each point in P (n,2) to polyline L (m,2)."""
    P = np.atleast_2d(P)
    A, B = L[:-1], L[1:]
    AB = B - A
    L2 = (AB ** 2).sum(1)
    L2[L2 == 0] = 1
    out = np.empty(len(P))
    for i, p in enumerate(P):
        t = np.clip(((p - A) * AB).sum(1) / L2, 0, 1)
        q = A + t[:, None] * AB
        out[i] = np.sqrt(((q - p) ** 2).sum(1)).min()
    return out


def points_in_polys(polys, pts):
    inside = np.zeros(len(pts), bool)
    for rings in polys:
        m = MplPath(rings[0]).contains_points(pts)
        for h in rings[1:]:
            m &= ~MplPath(h).contains_points(pts)
        inside |= m
    return inside


# =============================================================== raster
class Raster:
    """Minimal north-up GeoTIFF: .a (array), .x0 .dx .y0 .dy (pixel edges), .nodata."""

    def __init__(self, a, x0, dx, y0, dy, nodata, crs=""):
        self.a, self.x0, self.dx, self.y0, self.dy, self.nodata, self.crs = a, x0, dx, y0, dy, nodata, crs

    def valid(self):
        v = np.isfinite(self.a)
        if self.nodata is not None:
            v &= self.a != self.nodata
        return v


def read_tif(path) -> Raster:
    import tifffile
    t = tifffile.TiffFile(str(path))
    p = t.pages[0]
    tags = {k: v.value for k, v in p.tags.items()}
    if p.predictor == 3 and not p.is_tiled:
        H, W = p.shape
        out = np.empty((H, W), np.float32)
        fh = t.filehandle
        r = 0
        for off, cnt in zip(p.dataoffsets, p.databytecounts):
            fh.seek(off)
            raw = zlib.decompress(fh.read(cnt))
            nrows = min(p.rowsperstrip, H - r)
            b = np.frombuffer(raw, np.uint8).reshape(nrows, W * 4).copy()
            b = np.cumsum(b, axis=1, dtype=np.uint8).reshape(nrows, 4, W).transpose(0, 2, 1)[:, :, ::-1]
            out[r:r + nrows] = b.copy().view("<f4").reshape(nrows, W)
            r += nrows
        a = out
    else:
        a = p.asarray()
    sc, tie = tags[33550], tags[33922]
    nd = None
    try:
        nd = float(tags.get(42113))
    except (TypeError, ValueError):
        pass
    crs = str(tags.get(34737, ""))
    t.close()
    return Raster(a, tie[3], sc[0], tie[4], sc[1], nd, crs)


def zonal_mask(r: Raster, polys, to_raster_xy=None):
    """Row/col indices of pixels whose centres fall inside polys (raster CRS)."""
    allc = np.vstack([p[0] for p in polys])
    H, W = r.a.shape
    c0 = int(np.floor((allc[:, 0].min() - r.x0) / r.dx)) - 1
    c1 = int(np.ceil((allc[:, 0].max() - r.x0) / r.dx)) + 1
    r0 = int(np.floor((r.y0 - allc[:, 1].max()) / r.dy)) - 1
    r1 = int(np.ceil((r.y0 - allc[:, 1].min()) / r.dy)) + 1
    cc, rr = np.meshgrid(np.arange(c0, c1), np.arange(r0, r1))
    X = r.x0 + (cc + 0.5) * r.dx
    Y = r.y0 - (rr + 0.5) * r.dy
    ins = points_in_polys(polys, np.c_[X.ravel(), Y.ravel()])
    return rr.ravel()[ins], cc.ravel()[ins]


def sample_values(r: Raster, rows, cols):
    H, W = r.a.shape
    ok = (rows >= 0) & (rows < H) & (cols >= 0) & (cols < W)
    v = np.full(len(rows), np.nan)
    v[ok] = r.a[rows[ok], cols[ok]]
    if r.nodata is not None:
        v[v == r.nodata] = np.nan
    return v


# =============================================================== dbf
def read_dbf(b: bytes) -> pd.DataFrame:
    n = struct.unpack("<I", b[4:8])[0]
    hl, rl = struct.unpack("<HH", b[8:12])
    fields, o = [], 32
    while b[o] != 0x0D:
        name = b[o:o + 11].split(b"\0")[0].decode("latin1")
        fields.append((name, chr(b[o + 11]), b[o + 16]))
        o += 32
    raw = np.frombuffer(b[hl:hl + n * rl], dtype=np.uint8).reshape(n, rl)
    out, pos = {}, 1
    for name, t, ln in fields:
        s = [bytes(x).decode("latin1").strip() for x in raw[:, pos:pos + ln]]
        pos += ln
        out[name] = pd.to_numeric(pd.Series(s).replace("", np.nan), errors="coerce") if t in "NF" else s
    return pd.DataFrame(out)


# =============================================================== stats
class Fit:
    pass


def ols(df, y, xcols, cov=None, groups=None, coords=None, cutoff_km=50.0):
    """OLS; cov in {None, 'HC3', 'cluster', 'conley'}."""
    X = np.column_stack([np.ones(len(df))] + [df[c].to_numpy(float) for c in xcols])
    Y = df[y].to_numpy(float)
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ Y
    e = Y - X @ b
    dfr = n - k
    use_t = False
    if cov is None:
        V = (e @ e / dfr) * XtXi
        use_t = True
    elif cov == "HC3":
        h = np.einsum("ij,jk,ik->i", X, XtXi, X)
        u = e / (1 - h)
        V = XtXi @ (X.T * u ** 2) @ X @ XtXi
    elif cov == "cluster":
        g = pd.factorize(np.asarray(groups))[0]
        G = g.max() + 1
        M = np.zeros((k, k))
        for j in range(G):
            s = X[g == j].T @ e[g == j]
            M += np.outer(s, s)
        V = XtXi @ M @ XtXi * (G / (G - 1)) * ((n - 1) / (n - k))
    elif cov == "conley":
        xy = np.asarray(coords, float)
        D = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
        K = np.clip(1 - D / cutoff_km, 0, None)  # Bartlett kernel
        Xe = X * e[:, None]
        V = XtXi @ (Xe.T @ K @ Xe) @ XtXi * (n / (n - k))
    else:
        raise ValueError(cov)
    se = np.sqrt(np.diag(V))
    t = b / se
    p = 2 * stats.t.sf(np.abs(t), dfr) if use_t else 2 * stats.norm.sf(np.abs(t))
    names = ["Intercept"] + list(xcols)
    f = Fit()
    f.params, f.bse, f.pvalues = (pd.Series(v, names) for v in (b, se, p))
    f.nobs, f.resid, f.X, f.XtXi, f.dfr = n, e, X, XtXi, dfr
    f.rsquared = 1 - (e @ e) / ((Y - Y.mean()) @ (Y - Y.mean()))
    return f


def cooks_distance(f):
    h = np.einsum("ij,jk,ik->i", f.X, f.XtXi, f.X)
    k = f.X.shape[1]
    s2 = f.resid @ f.resid / f.dfr
    return (f.resid ** 2 / (k * s2)) * h / (1 - h) ** 2


def morans_i(values, xy, k=5, perms=999, seed=0):
    v = np.asarray(values, float) - np.mean(values)
    xy = np.asarray(xy, float)
    D = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    W = np.zeros_like(D)
    for i in range(len(D)):
        W[i, np.argsort(D[i])[1:k + 1]] = 1
    W /= W.sum(1, keepdims=True)
    n = len(v)
    I = n / W.sum() * (v @ W @ v) / (v @ v)
    rng = np.random.default_rng(seed)
    sims = np.array([(lambda p: n / W.sum() * (p @ W @ p) / (p @ p))(rng.permutation(v)) for _ in range(perms)])
    return I, (np.sum(sims >= I) + 1) / (perms + 1)


def holm(p):
    p = np.asarray(p, float)
    m, o = len(p), np.argsort(p)
    adj, cur = np.empty(m), 0.0
    for i, idx in enumerate(o):
        cur = max(cur, min(1.0, (m - i) * p[idx]))
        adj[idx] = cur
    return adj


def bh(p):
    p = np.asarray(p, float)
    m, o = len(p), np.argsort(p)[::-1]
    adj, cur = np.empty(m), 1.0
    for i, idx in enumerate(o):
        cur = min(cur, p[idx] * m / (m - i))
        adj[idx] = cur
    return adj


def norm_name(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())
