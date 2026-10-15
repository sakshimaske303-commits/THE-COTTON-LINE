import streamlit as st
import pandas as pd
from utils.theme import inject_theme, PALETTE
from utils.data import load_result, key_numbers, output_path, show_image_or_placeholder, OUTCOME_LABELS, SCALE_LABELS

st.set_page_config(page_title="Spatial Discontinuity Regression — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>SPATIAL DISCONTINUITY REGRESSION</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>Step (H1) and Slope (H2) Tests, "
            "Robustness, and What They Add Up To</h3>", unsafe_allow_html=True)
st.markdown("---")

st.latex(r"y = \beta_0 + \beta_1\,side + \beta_2\,dist + \beta_3\,(side \times dist) + \gamma_1\,rain + \gamma_2\,elev + \varepsilon")
st.markdown("""
All numbers on this page are read from `03_Data_Processed/Phase4/results/`, written by
`05_Python/robustness_checks.py`.

- **Primary p-value:** the largest of the HC3, Conley-50 km and Conley-100 km p-values.
- **Holm:** corrected across all 20 tests.
""")

main = load_result("main_models.csv")
K = key_numbers()
if main is None:
    st.warning("Run `python 05_Python/run_all.py` to produce the results.")
    st.stop()

t = main.copy()
t["Outcome"] = t.outcome.map(OUTCOME_LABELS)
t["Sample"] = t.scale.map(SCALE_LABELS)
show = t[["Outcome", "Sample", "n", "n_berar", "side_coef", "p_side_primary", "p_side_holm",
          "int_coef", "p_int_ols", "p_int_primary", "p_int_holm", "mde_in_sd"]].rename(columns={
    "n_berar": "n Berar", "side_coef": "Step", "p_side_primary": "Step p", "p_side_holm": "Step Holm",
    "int_coef": "Slope change /km", "p_int_ols": "Slope p (OLS)", "p_int_primary": "Slope p",
    "p_int_holm": "Slope Holm", "mde_in_sd": "Detectable step (SD)"})
st.dataframe(show.style.format({"Step": "{:.3f}", "Step p": "{:.3f}", "Step Holm": "{:.3f}",
                                "Slope change /km": "{:.4f}", "Slope p (OLS)": "{:.3f}", "Slope p": "{:.3f}",
                                "Slope Holm": "{:.3f}", "Detectable step (SD)": "{:.2f}"}),
             use_container_width=True, hide_index=True)
st.caption(f"{K.get('n_raw_sig_primary', '?')} of {K.get('n_tests', 20)} tests have primary p < 0.05; "
           f"{K.get('n_holm_sig', '?')} survive Holm. 'Detectable step' = minimum step detectable at 80 % "
           "power, in SD of the outcome.")

show_image_or_placeholder(output_path("v2_fig5_test_summary.png"))
show_image_or_placeholder(output_path("v2_fig4_outcome_vs_distance.png"),
                          caption="Per-side linear fits for display; p-values from the full model.")
st.markdown("---")

st.markdown("### What held up and what didn't")
st.markdown("""
- **No step at the line (H1).** None in the corridor, the Landsat sample, or local-linear estimates
  at 40-80 km (all p ≥ 0.16).
- **The one exception is regional.** The labour ratio steps by +0.96 in the 119-taluka model (Holm
  p = 0.029), but it is 0.02 in the corridor (p = 0.97), is not significant within 60 km, and does
  not appear in local estimates. It is concentrated in Amravati district.
- **Slopes differ (H2), and fake lines do too.** NDVI survives Holm in both years (p < 0.001): the
  line sits on the crest of a ridge. LST and labour are significant before correction. Placebo cutoffs inside each side reproduce the NDVI and labour
  slope changes. Only LST passes the placebo test, and it is a single pre-monsoon date that most
  likely reflects the black-soil belt along the line.
- **Power.** The corridor can only detect a step of about 1.6-2.1 SD. The larger samples detect about
  1 SD, or 0.6-0.7 SD for NDVI year 2 and net sown area.
""")
st.markdown(f"""
<div class="recon-card">
<p style="color:{PALETTE['accent2']}; font-weight:800; text-transform:uppercase; font-size:0.85rem;">The honest shape of the result</p>
<p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.6; margin:0;">
Vidarbha's cotton core straddles the old Berar/Central Provinces line; the line itself leaves no
measurable break. The pattern is real — the satellite index tracks district cotton share — but it
cannot be attributed to land tenure, because the line is also a
pre-colonial frontier, a river and a soil and rainfall transition.</p></div>
""", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### Robustness tables")
for title, name, note in [
    ("Local-linear RD at the line (triangular kernel)", "local_linear_rd.csv", "No jump at any bandwidth."),
    ("Placebo cutoffs inside each side", "placebo_cutoffs.csv",
     "Fake lines produce NDVI and labour 'effects': a non-linear regional gradient."),
    ("Symmetric distance windows", "symmetric_windows.csv", "Slope changes appear only in 80-105 km windows."),
    ("Coverage thresholds (Landsat)", "coverage_sensitivity.csv", "NDVI and LST slope results stable from any-pixel to 90 %."),
    ("Influence and exclusions", "influence_and_exclusions.csv", "Dropping the most influential taluka; excluding Rajura/Korpana/Jiwati."),
    ("Moran's I of residuals", "morans_i_residuals.csv", "LST and census residuals are spatially correlated: hence Conley errors."),
]:
    r = load_result(name)
    if r is not None:
        with st.expander(title):
            st.dataframe(r.round(4), use_container_width=True, hide_index=True)
            st.caption(note)

st.markdown("<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Regression</p>",
            unsafe_allow_html=True)
