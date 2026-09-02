import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import statsmodels.formula.api as smf
from utils.theme import inject_theme, plotly_layout, PALETTE
from utils.data import safe_read_csv, output_path, show_image_or_placeholder

st.set_page_config(page_title="Spatial Discontinuity Regression — THE COTTON LINE", page_icon="📊", layout="wide")
inject_theme()

st.markdown("<h1>📊 SPATIAL DISCONTINUITY REGRESSION</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>The Actual Phase 4 Test, Its Climate Controls, "
    "Robustness, and What It All Adds Up To</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Does each outcome jump right at the historical boundary once distance-to-boundary, rainfall, and
elevation are controlled for, or is the region-wide contrast seen on the earlier pages just a
broad gradient that happens to look different on either side? Model, run live below via
`statsmodels` OLS on the same data pulled from the earlier pages:
""")
st.latex(r"\text{outcome} = \beta_0 + \beta_1 \cdot side + \beta_2 \cdot signed\_dist\_km + \beta_3 \cdot (side \times signed\_dist\_km) + rainfall + elevation + \varepsilon")

DIV_COLORS = {"Amravati (Berar)": PALETTE["berar"], "Nagpur (Central Provinces)": PALETTE["cp"]}

st.markdown("### Climate controls, for context — LST and the rainfall gradient behind `annual_total_mm` and `elevation_m`")
st.markdown("""
Neither variable here is a finding about the historical boundary — both are the natural
geography of Vidarbha (wetter/lower to the east, drier/higher to the west) that predates
Ryotwari and Malguzari by geological time. Flagged because if Berar is both historically
cotton-monoculture *and* drier, a "Berar looks more drought-stressed" result could just be
reflecting less rainfall rather than the land-tenure legacy — both are netted out as controls
in the model above.
""")
lst = safe_read_csv("Vegetation", "corridor_taluka_lst_ndvi_stats.csv")
rain_corridor = safe_read_csv("Hydrology", "corridor_taluka_precipitation_stats.csv")
rain_full = safe_read_csv("Hydrology", "taluka_precipitation_stats.csv")

cc1, cc2 = st.columns(2)
with cc1:
    if lst is not None:
        means = lst.groupby("division")["lst_mean_c"].mean()
        st.metric("LST — Berar", f"{means.get('Amravati (Berar)', float('nan')):.1f}°C")
        st.metric("LST — Central Provinces", f"{means.get('Nagpur (Central Provinces)', float('nan')):.1f}°C")
        st.caption("June (pre-sowing) snapshot — see Methodology & Data for the DN=0 fix.")
    else:
        st.warning("corridor_taluka_lst_ndvi_stats.csv not found yet.")
with cc2:
    if rain_corridor is not None and rain_full is not None:
        c_means = rain_corridor.groupby("division")["annual_total_mm"].mean()
        f_means = rain_full.groupby("division")["annual_total_mm"].mean()
        st.metric("Rainfall — Berar", f"{c_means.get('Amravati (Berar)', float('nan')):.0f}mm",
                   f"District-wide: {f_means.get('Amravati (Berar)', float('nan')):.0f}mm")
        st.metric("Rainfall — Central Provinces", f"{c_means.get('Nagpur (Central Provinces)', float('nan')):.0f}mm",
                   f"District-wide: {f_means.get('Nagpur (Central Provinces)', float('nan')):.0f}mm")
        st.caption("WorldClim 10 arc-min grid (~18.5km/pixel) — good for the regional gradient, "
                   "not taluka-by-taluka precision. Monsoon share (~88% Jun-Sep) is nearly "
                   "identical both sides; the difference is total volume.")
    else:
        st.warning("Precipitation CSVs not found yet.")

col_a, col_b, col_c = st.columns([0.1, 5.9, 0.1])
with col_b:
    show_image_or_placeholder(output_path("lst_ndvi_corridor_comparison.png"))
    show_image_or_placeholder(output_path("precipitation_corridor_comparison.png"))

st.markdown("---")

FORMULA_TMPL = "{outcome} ~ side + signed_dist_km + side:signed_dist_km + annual_total_mm + elevation_m"
OUTCOMES = [
    ("kharif_to_rabi_decline", "Kharif-to-rabi NDVI decline"),
    ("ag_laborer_to_cultivator", "Ag-laborer-to-cultivator ratio"),
    ("net_area_pct", "Net cultivated area %"),
    ("lst_mean_c", "Land surface temperature"),
]


def fit_all(df):
    rows = []
    for col, label in OUTCOMES:
        if col not in df.columns:
            continue
        try:
            model = smf.ols(FORMULA_TMPL.format(outcome=col), data=df).fit()
            rows.append({
                "Outcome": label,
                "n": int(model.nobs),
                "side (level jump) coef": model.params.get("side", float("nan")),
                "side p-value": model.pvalues.get("side", float("nan")),
                "side × dist (slope diff) coef": model.params.get("side:signed_dist_km", float("nan")),
                "side × dist p-value": model.pvalues.get("side:signed_dist_km", float("nan")),
            })
        except Exception as e:
            rows.append({"Outcome": label, "n": None, "side (level jump) coef": None,
                         "side p-value": None, "side × dist (slope diff) coef": None,
                         "side × dist p-value": None})
    return pd.DataFrame(rows)


def style_pvals(df):
    def highlight(v):
        if isinstance(v, float) and v == v and v < 0.05:
            return f"color: {PALETTE['accent2']}; font-weight: 800;"
        return ""
    styler = df.style.format({
        "side (level jump) coef": "{:.3f}", "side p-value": "{:.3f}",
        "side × dist (slope diff) coef": "{:.4f}", "side × dist p-value": "{:.3f}",
    }, na_rep="—")
    subset = ["side p-value", "side × dist p-value"]
    if hasattr(styler, "map"):
        return styler.map(highlight, subset=subset)
    return styler.applymap(highlight, subset=subset)


# ============================================================
# CORRIDOR (32 TALUKAS)
# ============================================================
st.markdown("### 32-Taluka Corridor")

corridor = safe_read_csv("Phase4", "phase4_master_dataset.csv")
if corridor is None:
    st.warning("Phase4/phase4_master_dataset.csv not found yet.")
else:
    st.dataframe(style_pvals(fit_all(corridor)), use_container_width=True, hide_index=True)
    st.caption("Bold = p < 0.05. Sample sizes vary by outcome (n≈28-32) since not every corridor "
               "taluka has usable coverage on every variable.")

st.markdown("""
**Being straight about what came back:** at this sample size, none of the `side` level-jump
coefficients clear significance -- no outcome shows a clean jump right at the boundary once
controls are in. The one result that did clear significance was the `side × signed_dist_km`
*slope* interaction on the ag-laborer ratio -- not a level jump, a difference in how the ratio
changes with distance from the boundary depending on which side you're on.
""")

st.markdown("---")

# ============================================================
# FULL FOOTPRINT (68 TALUKAS)
# ============================================================
st.markdown("### 68-Taluka Full Footprint")

full = safe_read_csv("Phase4", "phase4_fullfootprint_dataset.csv")
if full is None:
    st.warning("Phase4/phase4_fullfootprint_dataset.csv not found yet.")
else:
    st.dataframe(style_pvals(fit_all(full)), use_container_width=True, hide_index=True)
    st.caption("Bold = p < 0.05. Full footprint is lopsided -- 49 Central Provinces talukas to "
               "19 Berar talukas, since the Landsat scene simply covers more CP-side territory.")

st.markdown("""
With more power, the `side × signed_dist_km` interaction becomes significant for **both**
Earth-observation outcomes -- NDVI decline and LST -- not just the one variable that showed it at
the corridor scale. `signed_dist_km` on its own is also strongly significant in both. Two
independent outcome variables showing the same shape of result, with real statistical power behind
it, is the strongest evidence in the project for **"gradient, not discontinuity."**
""")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">
        The ag-laborer complication, explained rather than picked around
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.9rem; line-height:1.65; margin:0;">
        At full-footprint scale, the ag-laborer ratio flips: the `side` level jump becomes
        significant (coef≈0.62, p≈0.01) and the slope interaction stops being significant --
        the opposite pattern from the corridor result. This traces to an asymmetric sample: in
        this particular Landsat scene, the Berar side barely extends past ~20km from the boundary
        (only Amravati district falls inside the footprint), while the Central Provinces side
        reaches out past 160km (Bhandara, Gondiya). A "level jump near the boundary" read is more
        defensible under those conditions than a "different slope across the whole range" read,
        since only one side actually has much range to have a slope over. The corridor-only
        interaction result is trusted more for what's happening right at the line; the
        full-footprint level jump is read as suggestive of a broader regional gap, not a
        competing measurement of the same thing.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# ROBUSTNESS: LEAVE-ONE-OUT JACKKNIFE
# ============================================================
st.markdown("### Robustness: Leave-One-Out Jackknife on the Corridor Interaction")

jk = safe_read_csv("Phase4", "phase4_robustness_jackknife.csv")
if jk is None:
    st.warning("Phase4/phase4_robustness_jackknife.csv not found yet.")
else:
    n_sig = (jk["p"] < 0.05).sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Coefficient range", f"{jk['coef'].min():.3f} – {jk['coef'].max():.3f}", "Across 32 leave-one-out runs")
    c2.metric("Stays p < 0.05", f"{n_sig} / {len(jk)}", "Runs")
    c3.metric("Max p-value seen", f"{jk['p'].max():.3f}", "When a driving taluka is dropped")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=jk["dropped_dtname"] + " — " + jk["dropped_sdtname"], y=jk["p"],
                          marker_color=[PALETTE["accent2"] if p < 0.05 else PALETTE["berar"] for p in jk["p"]]))
    fig.add_hline(y=0.05, line_dash="dash", line_color=PALETTE["text_secondary"])
    fig.update_layout(yaxis_title="p-value with this taluka dropped", xaxis_title="",
                       xaxis_tickangle=-60)
    st.plotly_chart(plotly_layout(fig, height=450), use_container_width=True)
    st.caption(
        "The coefficient stays positive and in a tight band across every single run -- no one "
        "taluka is secretly driving the whole thing. The p-value moves around more, crossing back "
        "over 0.05 when Amravati, Seloo, Samudrapur, Narkhed, Korpana, or Yavatmal taluka is "
        "dropped. Direction and rough size of the effect is stable; statistical significance is "
        "right on the edge. Called 'suggestive but not bulletproof' rather than dismissed or oversold."
    )

st.markdown("---")

# ============================================================
# STATIC PLOTS
# ============================================================
st.markdown("### Outcome vs. Distance-to-Boundary, Fitted by Side")

col_a, col_b, col_c = st.columns([0.1, 5.9, 0.1])
with col_b:
    show_image_or_placeholder(output_path("phase4_discontinuity_plots.png"),
                               caption="Corridor scale — the four headline outcomes.")
    show_image_or_placeholder(output_path("phase4_fullfootprint_plots.png"),
                               caption="Full footprint — NDVI decline and LST.")
    show_image_or_placeholder(output_path("phase4_fullfootprint_all4_plots.png"),
                               caption="Full footprint — all four outcomes, once population/land-use data covered all 11 districts.")

st.markdown("---")

st.markdown("### Findings: What Held Up, What Didn't")

st.markdown("""
- **No sharp level jump at the boundary**, in any of the four headline outcomes, at either scale —
  this project set out looking for a discontinuity and didn't find one at the line itself.
- **Land fragmentation** (Agrarian & Land Structure page) came back flat — Central Provinces
  corridor talukas run slightly *larger* holdings, the opposite of a naive "Ryotwari →
  fragmentation" story.
- **The ag-laborer ratio depends on which scale it's read at** — explained above, not picked around.
- **The one significant corridor-scale interaction is "suggestive, not bulletproof"** — stable in
  direction and size across the full jackknife, edge-of-significance on the p-value.
""")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:10px;">
        The Honest Shape of This Result
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0;">
        A 150-year-old colonial land-tenure boundary, erased in 1956, does not show up in
        present-day Vidarbha as a hard edge in cotton dependency, land use, or agrarian labor
        structure. What it shows up as instead is a genuine, statistically real east-west gradient
        that strengthens with distance from where that line used to run — present in two
        independently-measured Earth-observation variables, confirmed across two separate growing
        years (Cotton Signature NDVI). That's a different, more interesting result than a clean
        discontinuity would have been: institutional persistence here looks less like a fence and
        more like a slope.
    </p>
</div>
""", unsafe_allow_html=True)

st.success("""
**Ground-truthed:** the Karanja Ghadge / Sawardoh field check — comparing actual photographed
field patches against their NDVI/LST pixel values as a direct sanity-check on the remote-sensing
signal this whole project rests on — is now complete. See the Ground Truth page for details.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Spatial Discontinuity Regression &amp; Findings</p>",
    unsafe_allow_html=True,
)
