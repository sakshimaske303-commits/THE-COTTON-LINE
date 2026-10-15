import streamlit as st
import os
from utils.theme import inject_theme, PALETTE
from utils.data import PROJECT_ROOT

st.set_page_config(
    page_title="THE COTTON LINE",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_theme()

st.markdown("<h1>THE COTTON LINE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700; margin-top: -10px;'>"
    "Is an Erased Colonial Land-Revenue Boundary Still Visible in Vidarbha's "
    "Satellite and Census Record?</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(48, 123, 142, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin: 10px 0 18px 0;">
        <a href="https://eartharxiv.org/repository/view/14802/" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['bg_sidebar']}, {PALETTE['bg_card']});
                border: 2px solid {PALETTE['accent']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(48, 123, 142, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{PALETTE['accent2']}; font-family:'Poppins',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>PREPRINT ON EARTHARXIV</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        Read the preprint
                    </div>
                </div>
            </div>
        </a>
        <a href="https://doi.org/10.5281/zenodo.22111298" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['bg_sidebar']}, {PALETTE['bg_card']});
                border: 2px solid {PALETTE['accent']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(48, 123, 142, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{PALETTE['accent2']}; font-family:'Poppins',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.22111298
                    </div>
                </div>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Census Talukas", "119", "all 11 districts")
with col2:
    st.metric("Boundary Line", "384.7 km", "Amravati / Nagpur Division")
with col3:
    st.metric("Corridor Talukas", "32", "intersect the 25 km buffer")
with col4:
    st.metric("Landsat Talukas", "56", ">= 50 % observed; 2 NDVI years")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(48, 123, 142, 0.08);
                border: 1px solid rgba(48, 123, 142, 0.3); border-left: 4px solid {PALETTE['accent2']};
                border-radius: 10px;">
        <p style="color:{PALETTE['accent2']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:800; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_primary']}; font-size:1rem; line-height:1.6; margin:0;">
            Vidarbha's farm distress is usually explained by rain, prices and crop choice. I wanted to
            test an older possibility: that the nineteenth-century line between Berar (Ryotwari) and the
            Central Provinces (Malguzari), abolished in 1956, still marks a break in the land. I used
            Landsat imagery and village census data to check, with tests designed to tell a real
            boundary from a regional gradient that merely crosses it.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is The Cotton Line?

    In 1853, **Berar** -- today's Amravati, Akola, Buldhana, Washim, and Yavatmal districts -- was
    assigned to the East India Company by a treaty with the Nizam of Hyderabad, and it was
    administered under the **Ryotwari** land system. Cotton grew in importance there in the
    1860s, when the American Civil War disrupted Lancashire's supply. Berar merged with the
    Central Provinces in 1903. The six eastern districts (Nagpur, Wardha, Chandrapur, Bhandara,
    Gondia, and Gadchiroli) belonged to the **Central Provinces** and were settled under the
    **Malguzari** system, in which an intermediary landholder answered for the estate. Nagpur
    was also annexed in 1853, so 1853 is not a Berar-only date.

    The old provincial line was abolished in 1956. At district level it corresponds to the modern
    Amravati Division and Nagpur Division boundary line. I built this
    modern border line myself using present-day taluka shapefiles, cross-checked it by tracking
    old district lineage records, and ran a spatial-discontinuity regression test to see if things
    like cotton-signature NDVI, farm labor ratios, land use, and ground heat actually make a sharp
    jump at the border today.
    """)

with col_right:
    st.markdown(f"""
    <div class="recon-card">
        <p style="color:{PALETTE['accent']}; text-transform:uppercase; font-size:0.78rem;
                  letter-spacing:1.5px; font-weight:800; margin-bottom:12px;">Core Finding</p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0; font-weight:500;">
            No outcome steps at the old line -- not in the 32-taluka corridor, not in the Landsat
            sample, not in local estimates at the line. Vidarbha's cotton core straddles the line: the
            satellite cropping index is highest within 50 km of it on both sides (0.29) and falls away
            in both directions, and it tracks district cotton share (r = 0.86). Slopes differ across
            the line because it sits on that crest, and fake boundaries inside each side reproduce the
            NDVI and labour patterns. The result is a regional pattern, not a boundary effect, and it
            cannot be attributed to tenure. 20 tests; 3 survive Holm correction.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Research Question")
st.markdown("""
**After controlling for rainfall, elevation and distance, is the former Berar/Central Provinces
boundary detectable as a spatial discontinuity in present-day satellite and census indicators of
agriculture?**

- **H1 -- step:** the outcome jumps at the line.
- **H2 -- slope:** the outcome changes with distance differently on the two sides.

Outcomes: Landsat NDVI decline (November to March, two years, a cropping-intensity index), June
land surface temperature, and Census 2011 labour structure and net sown area.
""")

st.markdown("---")

st.markdown("### Explore the Evidence")

nav_items = [
    ("Study Design", "The boundary, the corridor, and the spatial-discontinuity model"),
    ("Theoretical Foundations", "Institutional persistence theory and the remote-sensing physics behind the data"),
    ("Cotton Signature (NDVI)", "The November-to-March decline, two years, and its check against cotton statistics"),
    ("Agrarian & Land Structure", "Cotton share, ag-laborer ratio, land use, holding size"),
    ("Spatial Discontinuity Regression", "The actual Phase 4 test, climate controls, robustness, and the honest findings"),
    ("Historical & Institutional Context", "District-lineage boundary verification and the FRA compilation"),
    ("Interactive Maps", "The boundary, corridor, and taluka data, explorable directly"),
    ("Methodology & Data", "Sources, the DN=0 fix, and scene-footprint scope"),
    ("Ground Truth", "Link to Roots & Reflectance: seven fields on the Central Provinces side (illustrative)"),
]

cols = st.columns(3)
for i, (title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="recon-card" style="margin-bottom: 14px; min-height: 120px;">
            <p style="color: {PALETTE['text_primary']}; font-weight: 800; font-size: 0.95rem; margin: 0 0 4px 0;">{title}</p>
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.8rem; margin: 0; font-weight: 600;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
st.markdown("### Full Project Documentation")
st.markdown(
    f"<p style='color:{PALETTE['text_secondary']}; font-weight:600;'>"
    "Version 2.1 (October 2026). The PDFs are exported from the Markdown files in the repository.</p>",
    unsafe_allow_html=True,
)

DOCS = [
    ("Research Paper (PDF)", "CL_Research_Paper.pdf"),
    ("Development Log (PDF)", "CL_Development_Log.pdf"),
    ("Executive Summary (PDF)", "CL_Executive_Summary.pdf"),
]

doc_cols = st.columns(3)
for col, (label, fname) in zip(doc_cols, DOCS):
    with col:
        fpath = os.path.join(PROJECT_ROOT, fname)
        try:
            with open(fpath, "rb") as f:
                st.download_button(
                    label=label,
                    data=f,
                    file_name=fname,
                    mime="application/pdf",
                    use_container_width=True,
                )
        except FileNotFoundError:
            st.warning(f"{fname} not added yet.")

st.markdown(
    f"""
    <div style="text-align:center; margin: 22px 0 6px 0;">
        <a href="https://github.com/sakshimaske303-commits/THE-COTTON-LINE" target="_blank" style="text-decoration:none;">
            <span style="display:inline-block; background: linear-gradient(90deg, {PALETTE['accent']}, {PALETTE['accent2']}); color:{PALETTE['bg_main']}; font-weight:800; font-size:0.95rem; padding:12px 28px; border-radius:8px;">
                View Full Project on GitHub
            </span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    f"""
    <div style="text-align: center; padding: 25px;" class="recon-card">
        <p style="color: {PALETTE['text_secondary']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 700;">Developed by</p>
        <h2 style="color: {PALETTE['accent2']}; margin: 5px 0; border: none; padding: 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['accent']}; font-weight: 700;">Independent Geospatial Researcher</p>
    </div>
    """,
    unsafe_allow_html=True,
)
