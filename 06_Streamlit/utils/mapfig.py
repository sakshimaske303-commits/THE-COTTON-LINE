"""Taluka maps drawn as plain filled polygons (no basemap tiles, no geo projection)."""
import math

SCALES = {
    "Blues": ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"],
    "Greens": ["#f7fcf5", "#c7e9c0", "#74c476", "#238b45", "#00441b"],
    "Oranges": ["#fff5eb", "#fdd0a2", "#fd8d3c", "#d94801", "#7f2704"],
    "Purples": ["#fcfbfd", "#dadaeb", "#9e9ac8", "#6a51a3", "#3f007d"],
    "YlOrBr": ["#ffffe5", "#fee391", "#fe9929", "#cc4c02", "#662506"],
    "Greys": ["#f7f7f7", "#bdbdbd", "#737373", "#252525"],
    "RdBu": ["#2166ac", "#92c5de", "#f7f7f7", "#f4a582", "#b2182b"],
}
KX = math.cos(math.radians(20.6))


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _color(stops, t):
    t = min(max(t, 0.0), 1.0) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    a, b = _rgb(stops[i]), _rgb(stops[i + 1])
    f = t - i
    return "#%02x%02x%02x" % tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))


def _xy(gj_feature):
    g = gj_feature["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    xs, ys = [], []
    for p in polys:
        ring = p[0]
        xs += [round(c[0] * KX, 5) for c in ring] + [None]
        ys += [round(c[1], 5) for c in ring] + [None]
    return xs, ys


def build_map(gj, line, values, labels, scale, label, base="#1d3445", edge="#ffffff", base_edge="#4a6274",
              line_color="#111111", text_color="#cee5d6", fmt=".3f", diverging=False):
    """values / labels: dicts keyed by feature id. Returns (data, layout) as plain dicts."""
    stops = SCALES[scale]
    v = [x for x in values.values() if x == x]
    lo, hi = min(v), max(v)
    if diverging:
        m = max(abs(lo), abs(hi))
        lo, hi = -m, m
    span = (hi - lo) or 1.0
    data = []
    for ft in gj["features"]:
        fid = ft["id"]
        xs, ys = _xy(ft)
        val = values.get(fid)
        has = val is not None and val == val
        data.append({"type": "scatter", "x": xs, "y": ys, "mode": "lines", "fill": "toself",
                     "fillcolor": _color(stops, (val - lo) / span) if has else base,
                     "line": {"width": 0.6 if has else 0.4, "color": edge if has else base_edge},
                     "hoveron": "fills", "hoverinfo": "text" if has else "skip",
                     "text": f"{labels.get(fid, fid)}<br>{label}: {val:{fmt}}" if has else "",
                     "showlegend": False})
    data.append({"type": "scatter", "x": [c[0] * KX for c in line], "y": [c[1] for c in line], "mode": "lines",
                 "line": {"width": 3, "color": line_color}, "hoverinfo": "skip", "showlegend": False})
    data.append({"type": "scatter", "x": [None], "y": [None], "mode": "markers", "hoverinfo": "skip",
                 "showlegend": False,
                 "marker": {"colorscale": [[i / (len(stops) - 1), c] for i, c in enumerate(stops)],
                            "cmin": lo, "cmax": hi, "color": [lo], "showscale": True,
                            "colorbar": {"tickfont": {"color": text_color}, "thickness": 14, "len": 0.8}}})
    axis = {"visible": False, "fixedrange": False}
    layout = {"xaxis": dict(axis), "yaxis": dict(axis, scaleanchor="x", scaleratio=1),
              "plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)", "hovermode": "closest",
              "dragmode": "pan", "margin": {"l": 0, "r": 0, "t": 10, "b": 0}, "showlegend": False}
    return data, layout
