import streamlit as st
import os
from utils.theme import inject_theme, PALETTE
from utils.data import output_path, show_image_or_placeholder

st.set_page_config(page_title="Theoretical Foundations — THE COTTON LINE", page_icon="📚", layout="wide")
inject_theme()

st.markdown("<h1>📚 THEORETICAL FOUNDATIONS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Institutional Persistence, Two Land-Tenure Systems, "
    "and the Physics Behind the Data</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# DIAGRAM — left blank until an illustrative image is added
# ============================================================
col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    show_image_or_placeholder(
        output_path("Figures", "imgg1.png"),
        caption="Two Land Tenures, One Satellite Signature",
        ai_generated=True,
    )
    st.markdown(
        f"""
        <div class="recon-card" style="margin-top:6px;">
            <p style="color:{PALETTE['text_secondary']}; font-size:0.85rem; font-style:italic; margin:0; text-align:center;">
                Generated with an AI image tool from a fully-specified brief -- every process, label,
                and relationship shown was authored from my own understanding of the institutional
                theory and remote-sensing physics below; the AI was directed to illustrate it, not to
                originate it.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================
# SECTION 1 — INSTITUTIONAL PERSISTENCE THEORY
# ============================================================
st.markdown("### Why an Erased Administrative Line Might Still Matter")

st.markdown("""
**Institutional persistence** is the idea, well established in economic history, that the rules a
region was governed under can keep shaping its economy long after the institution itself is gone
-- because land-tenure arrangements set who owned what, how it could be sold or subdivided, and
what incentive a cultivator had to specialize in one cash crop versus diversify. Those incentives
compound across generations even after the formal rule is repealed. This project tests one
specific, geographically bounded version of that idea: whether the Ryotwari/Malguzari divide,
abolished in 1956, still shows up as a measurable difference in land on either side of where it
used to run.
""")

st.markdown("---")

# ============================================================
# SECTION 2 — RYOTWARI VS MALGUZARI
# ============================================================
st.markdown("### Two Land-Tenure Systems, One Shared Border")

t1, t2 = st.columns(2)
with t1:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 260px;">
        <p style="color: {PALETTE['berar']}; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 10px;">Berar — Ryotwari</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            Annexed directly by the British in 1853. Land revenue was settled directly with the
            individual cultivator (the <em>ryot</em>), who held formal, individually-titled rights
            to their plot. With the American Civil War cutting off Lancashire's usual raw-cotton
            supply in the early 1860s, Berar was pushed hard into cotton as a single, tradeable
            cash crop -- individually-owned land made that specialization administratively easy to
            enforce, plot by plot.
        </p>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 260px;">
        <p style="color: {PALETTE['cp']}; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 10px;">Central Provinces — Malguzari</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            The Central Provinces to Berar's east were instead settled under a Malguzari
            (zamindari-style) system: revenue was collected through an intermediary landholder
            (the <em>malguzar</em>) responsible for a whole estate, not directly from each
            cultivator. More land stayed under estate/forest control rather than being converted
            plot-by-plot to individually-managed cropland -- a structural difference this project's
            land-use variable picks up directly.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
The hypothesis this project tests is not that one system was better or worse -- it's narrower and
more falsifiable than that: that Ryotwari's individual-plot cotton specialization should leave a
different **vegetation phenology signature** (a sharper kharif-to-rabi decline, since a
single-cropped field goes fallow once cotton is picked) and a different **agrarian labor
structure** (more landless agricultural labor relative to cultivators, the standard indicator
associated with a cash-crop-dependent smallholding economy) than Malguzari's more mixed,
estate-managed land did -- and that both of those, if real, should still be visible today.
""")

st.markdown("---")

# ============================================================
# SECTION 3 — REMOTE SENSING PHYSICS: WHY NDVI CAN DETECT THIS
# ============================================================
st.markdown("### The Remote-Sensing Logic: Why NDVI Can Pick Up a Cropping Pattern")

st.latex(r"NDVI = \frac{NIR - RED}{NIR + RED}")

st.markdown("""
NDVI is built from real leaf optics: chlorophyll strongly absorbs red light to drive
photosynthesis, while a leaf's internal cell structure scatters near-infrared light heavily.
Healthy, chlorophyll-rich canopy therefore shows low red reflectance and high NIR reflectance --
a large positive NDVI. Because NDVI tracks canopy structure and greenness directly, it responds
to a very specific agronomic fact this project leans on: **a single-cropped field goes back to
bare or fallow soil once its one crop is harvested, while a double-cropped field gets re-sown and
stays green.** Measuring NDVI at the kharif peak (post-monsoon, cotton canopy fullest) and again
at the rabi/pre-harvest point captures exactly that difference -- a **large kharif-to-rabi
decline is this project's cotton-monoculture signature; a small one is its mixed-cropping
signature.** This is the outcome variable behind the Cotton Signature (NDVI) page.
""")

st.markdown("---")

# ============================================================
# SECTION 4 — LST AS A SECOND PHYSICAL CHANNEL
# ============================================================
st.markdown("### Land Surface Temperature: A Second, Independent Physical Channel")

st.markdown("""
Land Surface Temperature (LST), derived from Landsat's thermal band, measures the actual radiant
temperature of the ground surface rather than air temperature. Bare or sparsely-vegetated soil
heats up faster and holds less moisture than a denser, actively-transpiring canopy, so LST and
NDVI are physically linked but not redundant: NDVI describes what's growing, LST describes how
that translates into surface heat and, indirectly, moisture stress. Testing both independently --
rather than leaning on NDVI alone -- is what let this project confirm, in the full-footprint Phase
4 regression, that the same side-of-boundary distance gradient shows up in two physically distinct
measurements, not just one (see Spatial Discontinuity Regression).
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Theory Behind the Test</p>",
    unsafe_allow_html=True,
)
