import streamlit as st
import os
from utils.theme import inject_theme, PALETTE
from utils.data import output_path, show_image_or_placeholder

st.set_page_config(page_title="Theoretical Foundations — THE COTTON LINE", layout="wide")
inject_theme()

st.markdown("<h1>THEORETICAL FOUNDATIONS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Institutional Persistence, Two Land-Tenure Systems, "
    "and the Physics Behind the Data</h3>",
    unsafe_allow_html=True,
)
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
My project does not test whether one system was better than the other, and it cannot attribute
anything to tenure: the same line is also an older political frontier, the Wardha river and a
soil and rainfall transition. It asks a narrower, prior question: does the old line still mark a
**break** in how the land is farmed today -- in the seasonal greenness of fields, in surface
temperature, in labour structure or in land use -- or does a regional gradient simply run across it?
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
heavily, so green canopy gives a high NDVI. I measure NDVI in early November, after the monsoon,
and again in early March. Land under a single long-season crop that is picked and left fallow
loses most of its greenness between the two dates; land with a second (rabi) crop, irrigation or
perennial cover loses less. The fall is therefore a **cropping-intensity index, not a cotton
detector**: soybean is already harvested by November and rice in the east may still stand.
At district level the index tracks official cotton share (r = 0.86 for 10 districts; see Cotton
Signature).
""")

st.markdown("---")

# ============================================================
# SECTION 4 — LST AS A SECOND PHYSICAL CHANNEL
# ============================================================
st.markdown("### Land Surface Temperature: A Second Physical Channel")

st.markdown("""
Land Surface Temperature (LST) comes from Landsat's thermal band and tracks the actual heat of
the ground instead of just the air temperature. Bare dirt or sparsely-vegetated fields heat up
faster and hold less moisture than a denser, actively-transpiring canopy. This is why LST and
NDVI are physically linked but not redundant. Here LST is a single pre-monsoon date (20 June 2026),
when most fields are bare, so it mainly reflects soil and surface type -- dark black-cotton soils
heat strongly. The two channels do not show the same shape: NDVI decline falls steadily eastwards,
while LST forms a ridge at the line (see Spatial Discontinuity Regression).
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Theory Behind the Test</p>",
    unsafe_allow_html=True,
)
