import streamlit as st
from utils.theme import inject_theme, PALETTE
from utils.data import output_path, show_image_or_placeholder, load_analysis

st.set_page_config(page_title="Study Design — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>STUDY DESIGN</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 700;'>The Line, the Three Samples, "
            "and the Test</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
I used the modern division boundary as a proxy for the old provincial line. **Amravati Division**
(Akola, Amravati, Buldhana, Washim, Yavatmal) stands for Berar, settled under Ryotwari, and
**Nagpur Division** (Nagpur, Wardha, Bhandara, Gondia, Chandrapur, Gadchiroli) for the Central
Provinces, settled under Malguzari. I dissolved the 120 talukas into these two divisions and
extracted their shared edge. District lineage from 1903 to 1956 supports the match at district
level; it is not a geometric overlay of a period map.
""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Boundary line", "384.7 km", "UTM 44N")
c2.metric("Corridor", "32 talukas", "15 Berar / 17 CP")
c3.metric("Landsat sample", "98 talukas", "56 Berar / 42 CP")
c4.metric("Census sample", "119 talukas", "56 Berar / 63 CP")
st.markdown("---")

show_image_or_placeholder(output_path("v2_fig1_study_design_map.png"),
                          caption="The boundary proxy, the 25 km corridor (hatched) and the talukas at least "
                                  "half observed by the Landsat scenes (green outline). Census outcomes use "
                                  "all 119 talukas with villages.")
st.markdown("---")

st.markdown("### Three samples, fixed before looking at results")
s1, s2, s3 = st.columns(3)
for col, title, body in [
    (s1, "Corridor — 32 talukas", "Talukas whose polygon touches a 25 km buffer of the line. The closest "
     "look at the line itself, and the least statistical power (a step must be about 2 SD to be detected)."),
    (s2, "Landsat sample — 98 talukas", "Talukas with at least half their cropland observed on both "
     "seasonal dates (Landsat paths 144-146). Every Berar taluka, to 228 km; LST uses 56 talukas."),
    (s3, "Census sample — 119 talukas", "Every taluka with Census 2011 villages, all 11 districts, "
     "reaching 228 km into Berar and 200 km into the Central Provinces."),
]:
    col.markdown(f"""
    <div class="recon-card" style="min-height: 190px;">
        <p style="color: {PALETTE['accent2']}; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px;">{title}</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">{body}</p>
    </div>""", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### The model")
st.latex(r"y = \beta_0 + \beta_1\,side + \beta_2\,dist + \beta_3\,(side \times dist) + \gamma_1\,rain + \gamma_2\,elev + \varepsilon")
st.markdown("""
- **H1 (step):** β1 ≠ 0. The outcome jumps exactly at the line.
- **H2 (slope):** β3 ≠ 0. The outcome changes with distance differently on each side.
- `dist` is the signed centroid distance to the line (positive in Berar). `rain` is WorldClim annual
  rainfall and `elev` is SRTM elevation, both at the taluka centroid.
- **Inference:** the most conservative of HC3 and Conley spatial standard errors (50 and 100 km).
  Neighbouring talukas are correlated, and with so few units neither correction alone is safe.
  Holm correction is applied over all 20 tests.
- **Checks:** local-linear RD at the line, symmetric windows, placebo lines inside each side,
  influence, coverage thresholds, and the minimum detectable step.
""")

st.markdown("### Where the hypotheses stand")
st.markdown("""
- **H1 — not supported.** No step in the corridor, the Landsat sample or local estimates at the line.
  The one exception (labour ratio, 119-taluka model, +0.96, Holm p = 0.029) is zero in the corridor
  and in local estimates: a regional difference, not a break at the line.
- **H2 — slopes differ, but not because of the line.** NDVI survives Holm in both years, because the
  line sits on the crest of a ridge; LST and labour are significant before correction. Placebo lines reproduce the NDVI and labour patterns.
- **Boundary proxy — supported at district level only.** Some Central Provinces talukas (e.g.
  Rajura) came from other jurisdictions; excluding them changes nothing.
""")
st.markdown("<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Study Design</p>",
            unsafe_allow_html=True)
