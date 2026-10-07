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
        caption="Two Land Tenures, One Satellite Signature (schematic of the hypothesised mechanism)",
    )
    st.caption("This illustration is a schematic, not real data. It shows the hypothesis, including a sharp break at the boundary. The measured results on the other pages show no sharp break, and the NDVI curves drawn here are not the observed values.")

st.markdown("---")

# ============================================================
# SECTION 1 — INSTITUTIONAL PERSISTENCE THEORY
# ============================================================
st.markdown("### Why an Erased Administrative Line Might Still Matter")

st.markdown("""
**Institutional persistence** is just a fancy way of saying that old rules can keep changing a
region's economy long after the laws themselves are gone. It happens because old land systems
decided who owned what, how property could be broken up or sold, and if a farmer had any real
reason to grow just one cash crop instead of mixing things up. These choices pile up across
generations, even after the official rule gets repealed. My project tests a very specific,
mapped-out version of this theory: I want to find out if the old Ryotwari and Malguzari split --
thrown out back in 1956 -- still shows up as a real, measurable difference on the ground today.
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
            Berar was assigned to the East India Company by a treaty with the Nizam in 1853 and
            was administered under the Ryotwari system, in which land revenue is collected
            straight from the individual farmer (the <em>ryot</em>), who held individually-titled
            rights to a specific plot. When the American Civil War cut off the normal raw-cotton
            supply to Lancashire mills in the early 1860s, cotton became increasingly important in
            Berar. The mechanism proposed here, that individual plot rights made cotton
            specialisation easier, is a hypothesis this project tests, not an established fact.
        </p>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 260px;">
        <p style="color: {PALETTE['cp']}; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 10px;">Central Provinces — Malguzari</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            The Central Provinces sat right to the east of Berar and ran on a Malguzari
            setup, which is related to zamindari but distinct from it. Instead of dealing with
            individual farmers, the government collected revenue through an intermediary landholder
            (the <em>malguzar</em>) responsible for a whole estate. Malguzari also brought cadastral
            surveys and statutory tenant protections, so it was not a simple landlord system
            (Iversen et al., 2013). Whether more land stayed under estate or forest control as a
            result is not established here; the land-use variables only describe current patterns.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
My project isn't testing whether one system was better or worse than the other. My test is much
narrower and simpler: I want to see if Ryotwari's individual-plot cotton farming left behind a
different **vegetation phenology signature** (meaning a sharper kharif-to-rabi decline, since a
single-cropped field goes fallow once cotton is picked) and a different **agrarian labor
structure** (more landless laborers relative to cultivators, the standard indicator for a
cash-crop-dependent smallholding economy) than Malguzari's mixed, estate-managed land. If these
differences are real, my data should still show them today.
""")

st.markdown("---")

# ============================================================
# SECTION 3 — REMOTE SENSING PHYSICS: WHY NDVI CAN DETECT THIS
# ============================================================
st.markdown("### The Remote-Sensing Logic: Why NDVI Can Pick Up a Cropping Pattern")

st.latex(r"NDVI = \frac{NIR - RED}{NIR + RED}")

st.markdown("""
NDVI is built from real physics and leaf optics. Chlorophyll absorbs red light to drive
photosynthesis, while the inside cell structure of a leaf bounces back near-infrared light
heavily. Because of this, healthy green plants show low red reflection and high near-infrared
reflection -- a big positive NDVI number. I rely on a very simple fact here: **single-cropped
fields go back to bare, dry dirt after one harvest, but mixed-crop fields get planted again and
stay green.** I measured NDVI at the kharif peak, just after the monsoons when leaves are
fullest, and then checked it again just before the rabi harvest to capture this exact gap. A
**huge drop in greenness is my project's signature for single-crop cotton farming, while a small
drop means farmers are mixing up their crops.** This is the outcome variable behind the Cotton
Signature (NDVI) page.
""")

st.markdown("---")

# ============================================================
# SECTION 4 — LST AS A SECOND PHYSICAL CHANNEL
# ============================================================
st.markdown("### Land Surface Temperature: A Second, Independent Physical Channel")

st.markdown("""
Land Surface Temperature (LST) comes from Landsat's thermal band and tracks the actual heat of
the ground instead of just the air temperature. Bare dirt or sparsely-vegetated fields heat up
faster and hold less moisture than a denser, actively-transpiring canopy. This is why LST and
NDVI are physically linked but not redundant: NDVI shows me what is actually growing, while LST
tells me how that translates into surface heat and, indirectly, moisture stress. I chose to test
both channels independently -- rather than leaning on NDVI alone -- and that's what let this
project confirm, in the full-footprint Phase 4 regression, that the same side-of-boundary
distance gradient shows up across two physically distinct measurements, not just one (see Spatial
Discontinuity Regression).
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Theory Behind the Test</p>",
    unsafe_allow_html=True,
)
