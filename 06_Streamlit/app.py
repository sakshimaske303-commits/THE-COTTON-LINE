import streamlit as st
import os
from utils.theme import inject_theme, PALETTE
from utils.data import PROJECT_ROOT

st.set_page_config(
    page_title="THE COTTON LINE",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_theme()

st.markdown("<h1>🧵 THE COTTON LINE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700; margin-top: -10px;'>"
    "Does a 150-Year-Old Colonial Land-Tenure Boundary Still Register as a Measurable "
    "Spatial Signature in Present-Day Vidarbha?</h3>",
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Districts Covered", "11", "Full Vidarbha")
with col2:
    st.metric("Boundary Line", "384.7 km", "Amravati / Nagpur Division")
with col3:
    st.metric("Corridor Talukas", "32", "±25 km of the line")
with col4:
    st.metric("Full-Footprint Talukas", "68", "2 independent NDVI years")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(48, 123, 142, 0.08);
                border: 1px solid rgba(48, 123, 142, 0.3); border-left: 4px solid {PALETTE['accent2']};
                border-radius: 10px;">
        <p style="color:{PALETTE['accent2']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:800; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_primary']}; font-size:1rem; line-height:1.6; margin:0;">
            Vidarbha's farmer-distress geography is usually explained by rainfall, market prices, or
            crop choice alone. This project tests a different, longer-running explanation: that the
            1853 British annexation of Berar -- and the Ryotwari land-tenure system pushed onto it to
            feed cotton into Lancashire's mills -- left an institutional mark on this land that a
            century of shared statehood since Independence hasn't erased. That boundary was formally
            abolished in 1956. This project checks, directly against satellite and census data rather
            than assuming it from the history alone, whether it still shows up.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is The Cotton Line?

    In 1853 the British annexed the province of **Berar** -- the five districts that are today
    Amravati, Akola, Buldhana, Washim, and Yavatmal -- directly into colonial administration,
    settled it under a **Ryotwari** land-tenure system, and pushed it hard into cotton monoculture
    once the American Civil War cut off Lancashire's usual supply. The six districts to its east
    -- Nagpur, Wardha, Chandrapur, Bhandara, Gondia, Gadchiroli -- were instead the core of the
    **Central Provinces**, settled under the very different **Malguzari** system.

    That administrative line was erased at Independence, but it runs almost exactly along the
    modern Amravati Division / Nagpur Division boundary. This project builds that modern boundary
    from present-day taluka shapefiles, verifies it against the actual historical district lineage,
    and tests -- via a spatial-discontinuity design, not a before/after or synthetic-control one --
    whether cotton-signature NDVI, agrarian labor structure, land use, and land-surface temperature
    still jump at that line today.
    """)

with col_right:
    st.markdown(f"""
    <div class="recon-card">
        <p style="color:{PALETTE['accent']}; text-transform:uppercase; font-size:0.78rem;
                  letter-spacing:1.5px; font-weight:800; margin-bottom:12px;">Core Finding, So Far</p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0; font-weight:500;">
            No sharp jump in level shows up right at the historical line -- but a real east-west
            gradient does, confirmed independently in two full annual NDVI cycles and echoed in the
            land-surface-temperature signal: both decline differently with distance from the
            boundary depending on which side you're on. That's a different, more honest shape of
            result than a clean discontinuity would have been, and it's reported as such. See
            Spatial Discontinuity Regression for the full breakdown, including where the results
            genuinely disagree by scale.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Research Questions")
st.markdown("""
1. **Does cotton-signature NDVI** -- the size of a taluka's kharif-to-rabi vegetation decline, a
   monoculture-vs-mixed-cropping signature -- **jump at the historical Berar/Central Provinces
   line**, once distance-to-boundary, rainfall, and elevation are controlled for?
2. **Does agrarian labor structure** -- the ratio of agricultural laborers to cultivators, a
   standard landlessness indicator -- **show the same pattern**, and does it hold at both the
   immediate boundary corridor and the full regional footprint?
3. **Is the modern administrative boundary actually the same line** as the historical
   Berar/Central Provinces one, verified by documented district lineage rather than assumed?
""")

st.markdown("---")

st.markdown("### Explore the Evidence")

nav_items = [
    ("Study Design", "The boundary, the corridor, and the spatial-discontinuity model"),
    ("Theoretical Foundations", "Institutional persistence theory and the remote-sensing physics behind the data"),
    ("Cotton Signature (NDVI)", "The kharif-to-rabi decline test, confirmed across 2 independent years"),
    ("Agrarian & Land Structure", "Cotton share, ag-laborer ratio, land use, holding size"),
    ("Spatial Discontinuity Regression", "The actual Phase 4 test, climate controls, robustness, and the honest findings"),
    ("Historical & Institutional Context", "District-lineage boundary verification and the FRA compilation"),
    ("Interactive Maps", "The boundary, corridor, and taluka data, explorable directly"),
    ("Methodology & Data", "Sources, the DN=0 fix, and scene-footprint scope"),
    ("Ground Truth", "Karanja Ghadge / Sawardoh field verification -- complete, 7 fields"),
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
    "All four documents are current. The ground-truth check closed out first -- see the Ground "
    "Truth page -- which is what let the Project Report and Executive Summary get written.</p>",
    unsafe_allow_html=True,
)

DOCS = [
    ("Research Paper (PDF)", "CL_Research_Paper.pdf"),
    ("Development Log (PDF)", "CL_Development_Log.pdf"),
    ("Executive Summary (PDF)", "CL_Executive_Summary.pdf"),
    ("Project Report (PDF)", "CL_Project_Report.pdf"),
]

doc_cols = st.columns(4)
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
