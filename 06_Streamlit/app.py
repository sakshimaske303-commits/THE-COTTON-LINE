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

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(48, 123, 142, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; margin: 10px 0 18px 0;">
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
            People always blame Vidarbha's farming trouble on bad rain, prices, or crop choices. But I
            wanted to test a much older historical reason (dating back to 1853 when the British took
            over Berar and forced farmers into the Ryotwari cotton system just to feed their own
            Lancashire mills). Did this colonial setup leave a permanent footprint on the land? The old
            line was officially wiped out in 1956. I chose to use actual satellite maps and village
            census numbers to check if this border still shows up today, rather than just guessing from
            old history textbooks.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is The Cotton Line?

    In 1853, the British took over **Berar** -- which means today's Amravati, Akola, Buldhana,
    Washim, and Yavatmal districts. They forced this specific region into a **Ryotwari** land
    system, pushing a strict cotton monoculture setup because the American Civil War suddenly
    stopped their regular supply to Lancashire cloth factories. On the other side, the six eastern
    districts (Nagpur, Wardha, Chandrapur, Bhandara, Gondia, and Gadchiroli) became the
    **Central Provinces**. Landlords there used a completely different setup called the
    **Malguzari** system.

    The old colonial line officially disappeared at Independence. But the crazy thing is that it
    runs right along our modern Amravati Division and Nagpur Division boundary line. I built this
    modern border line myself using present-day taluka shapefiles, cross-checked it by tracking
    old district lineage records, and ran a spatial-discontinuity regression test to see if things
    like cotton-signature NDVI, farm labor ratios, land use, and ground heat actually make a sharp
    jump at the border today.
    """)

with col_right:
    st.markdown(f"""
    <div class="recon-card">
        <p style="color:{PALETTE['accent']}; text-transform:uppercase; font-size:0.78rem;
                  letter-spacing:1.5px; font-weight:800; margin-bottom:12px;">Core Finding, So Far</p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0; font-weight:500;">
            My data shows absolutely no sharp jump right at the old border line. But a real
            west-to-east trend is definitely there. I verified this gradient across two independent
            annual NDVI cycles, and my land-surface temperature data shows the exact same pattern:
            both satellite metrics shift at different speeds as you move away from the boundary
            depending on which side you stand on. This is a much more honest and precise result
            than a clean step-jump (plus I reported everything exactly as it came out, even where
            the results flip or change based on the map scale). See Spatial Discontinuity
            Regression for the full breakdown.
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
    "All three documents are current. The ground-truth check closed out first -- see the Ground "
    "Truth page -- which is what let the Executive Summary get written.</p>",
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
