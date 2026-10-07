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
On the full footprint the `side × signed_dist_km` interaction is significant for **both**
Earth-observation outcomes -- NDVI decline (p = 0.035) and LST (p = 0.011). `signed_dist_km` on its
own is also strongly significant in both. The two do not share a shape: NDVI decline falls from
west to east with a flatter Berar side, while LST is highest near the line and falls with
distance on both sides. Only the LST interaction is robust to HC3 errors, symmetric windows and
removal of its most influential taluka; the NDVI interaction is not (see the robustness section
below).
""")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">
        The ag-laborer complication, explained rather than picked around
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.9rem; line-height:1.65; margin:0;">
        At full-footprint scale, the ag-laborer ratio flips: the `side` level term becomes
        significant (coef≈0.62, p≈0.014) and the slope interaction stops being significant --
        the opposite pattern from the corridor result. The full footprint is asymmetric: the
        Berar side reaches about 104 km from the boundary and the Central Provinces side about
        180 km, and only Amravati and Yavatmal contribute Berar-side census data. A symmetric-window
        test restricted to comparable distances keeps the level term significant (p = 0.004 within
        105 km, 0.008 within 80 km, 0.041 within 60 km), so asymmetry alone does not explain it.
        It is not significant under district-clustered errors (p = 0.11, only 7 clusters) and is
        absent in the corridor. It is reported as a scale-dependent result, not resolved either way.
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
        "The coefficient stays positive and in a fairly tight band across every run. The p-value "
        "moves around more, crossing back over 0.05 when Amravati, Seloo, Samudrapur, Narkhed, "
        "Korpana, or Yavatmal taluka is dropped (Amravati alone raises it to 0.138). Direction is "
        "stable, but the significance depends on a handful of talukas."
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
                               caption="Full footprint — all four outcomes (population/land-use data cover 8 of 11 districts; Akola, Buldhana and Washim are missing).")

st.markdown("---")

st.markdown("### Findings: What Held Up, What Didn't")

st.markdown("""
- **No sharp level jump at the boundary in the corridor's four headline outcomes** —
  this project set out looking for a discontinuity and didn't find one at the line itself.
  (The one exception is the full-footprint ag-laborer `side` jump, p≈0.014. It survives
  symmetric distance windows (p = 0.004 to 0.041) but not district-clustered errors, is absent in
  the corridor, and rests on two Berar districts; see the robustness section below.)
- **Land fragmentation** (Agrarian & Land Structure page) came back flat — Central Provinces
  corridor talukas run slightly *larger* holdings, the opposite of a naive "Ryotwari →
  fragmentation" story.
- **The ag-laborer ratio depends on which scale it's read at** — the level difference appears on the full footprint and the slope difference in the corridor; neither is confirmed at the other scale.
- **The one significant corridor-scale interaction is suggestive at best** — stable in direction
  across the jackknife, but the p-value crosses 0.05 in 6 of 32 runs, HC3 gives p = 0.063, and
  dropping the urban Amravati taluka gives p = 0.138.
""")

st.markdown(f"""
<div class="recon-card">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:10px;">
        The Honest Shape of This Result
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0;">
        The old Berar/Central Provinces boundary does not show up in present-day Vidarbha as a hard
        edge in NDVI decline, land surface temperature, or net cultivated area. What the data show
        instead is a regional west-to-east gradient that partly coincides with the old line. The
        temperature interaction is the most robust piece; the NDVI interaction is fragile; the
        labour ratio differs by scale; and none of the 16 tests survives a Holm correction. The
        line is also an older political frontier and a river line, so these patterns cannot be
        attributed to tenure. Read the results as exploratory.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Robustness and Multiple Testing")
st.markdown("""
Sixteen coefficients were tested (the `side` and interaction terms for four outcomes at two
scales). Four have raw p < 0.05, where chance alone would give about 0.8. None survives a Holm
correction, and the smallest Benjamini-Hochberg q-value is 0.115. Treat the results as exploratory.
The table comes from `05_Python/robustness_checks.py`.
""")
rb = safe_read_csv("Phase4", "robustness", "main_models_with_corrections.csv")
if rb is None:
    st.info("Run 05_Python/robustness_checks.py to generate the robustness tables.")
else:
    show = rb[["scale", "outcome", "n", "p_side", "p_side_HC3", "p_side_holm", "p_int", "p_int_HC3", "p_int_holm"]].round(4)
    st.dataframe(show, use_container_width=True, hide_index=True)
    st.caption("HC3 = heteroskedasticity-robust errors; Holm = corrected across all 16 tests. "
               "District-clustered p-values are in the CSV but are unreliable with 5-7 clusters.")
win = safe_read_csv("Phase4", "robustness", "symmetric_windows_full_footprint.csv")
if win is not None:
    st.markdown("**Symmetric distance windows (full footprint)**")
    st.dataframe(win.round(4), use_container_width=True, hide_index=True)
plc = safe_read_csv("Phase4", "robustness", "placebo_cutoffs_cp_side.csv")
if plc is not None:
    st.markdown("**Placebo cutoffs on the Central Provinces side only (no historical boundary there)**")
    st.dataframe(plc.round(4), use_container_width=True, hide_index=True)
    st.caption("Fake cutoffs produce significant NDVI-decline jumps, which indicates a non-linear "
               "regional gradient that the linear-in-distance model does not capture.")

st.success("""
**Field check:** the Karanja Ghadge / Sawardoh check compares field-level Sentinel-2 values with the
satellite signal on the Central Provinces side only. It is illustrative and does not validate the
Berar versus Central Provinces difference. See the Ground Truth page for details.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Spatial Discontinuity Regression &amp; Findings</p>",
    unsafe_allow_html=True,
)
