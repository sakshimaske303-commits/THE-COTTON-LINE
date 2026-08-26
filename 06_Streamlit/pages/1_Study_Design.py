import os
import streamlit as st
import streamlit.components.v1 as components
from utils.theme import inject_theme, PALETTE
from utils.data import data_path, show_image_or_placeholder

st.set_page_config(page_title="Study Design — THE COTTON LINE", page_icon="🗺️", layout="wide")
inject_theme()

st.markdown("<h1>🗺️ STUDY DESIGN</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Building the Modern Boundary, "
    "the Discontinuity Corridor, and the Test Itself</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
I used modern division boundaries to stand in for the two old colonial zones. For the old Berar
Ryotwari territory, I picked **Amravati Division** (Akola, Amravati, Buldhana, Washim, and
Yavatmal), while for the old Central Provinces Malguzari land, I used **Nagpur Division** (Nagpur,
Wardha, Bhandara, Gondia, Chandrapur, and Gadchiroli). I didn't just guess this part -- I verified
it completely using old records on the Historical & Institutional Context page. Next, I chose to
dissolve all 120 talukas across the 11 districts into these two division shapes, and then I
extracted the exact shared edge where they touch to make my boundary line.
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Boundary Line Length", "384.7 km", "Akola/Amravati/Wardha → Yavatmal/Chandrapur")
with col2:
    st.metric("Corridor Width", "±25 km", "Either side of the line")
with col3:
    st.metric("Berar-Side Corridor Area", "7,387 km²", "Amravati Division")
with col4:
    st.metric("CP-Side Corridor Area", "7,987 km²", "Nagpur Division")

st.markdown("---")

col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    interactive_map_path = data_path("Administrative", "boundary_verification_map.html")
    if os.path.exists(interactive_map_path):
        with open(interactive_map_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=520)
        st.markdown(
            "<p style='text-align:center;' class='caption-text'>Figure. The two dissolved divisions, "
            "the 384.7 km boundary line, and the 25 km discontinuity corridor, checked against the "
            "full taluka grid for gaps or overlaps at the seam. Toggle layers top-right.</p>",
            unsafe_allow_html=True,
        )
    else:
        show_image_or_placeholder(
            data_path("Administrative", "boundary_verification_map.png"),
            caption="Figure. The two dissolved divisions, the 384.7 km boundary line, and the 25 km "
                    "discontinuity corridor, checked against the full taluka grid for gaps or overlaps at the seam.",
        )

st.markdown("---")

st.markdown("### Two Sample Scales, Used Deliberately")

s1, s2 = st.columns(2)
with s1:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 210px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px;">32-Taluka Corridor</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            Out of my total dataset, 32 talukas sit right inside the narrow ±25 km buffer zone
            (which includes 15 on the Berar side and 17 on the Central Provinces side). I chose
            this corridor because it gives the tightest, most direct test to check if the colonial
            effect actually jumps right at the historical line. This is my smallest sample, meaning
            it has limited statistical power. But it definitely provides the most honest spatial
            look at what happens right at the boundary itself.
        </p>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 210px;">
        <p style="color: {PALETTE['accent2']}; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px;">68-Taluka Full Footprint</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
            I used the full area covered by my two main Landsat scenes (specifically WRS-2 path
            144, rows 045 and 046) to grab the complete NDVI and LST numbers. This wider dataset
            covers 68 talukas across the whole satellite view instead of sticking just to the
            narrow corridor line. My models get much better statistical power here, though it
            moves away from that strict "right at the border" test. I ran this setup on purpose as
            a robustness check to double-check my corridor results, not to replace them.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### The Model")

st.latex(r"\text{outcome} = \beta_0 + \beta_1 \cdot side + \beta_2 \cdot signed\_dist\_km + \beta_3 \cdot (side \times signed\_dist\_km) + controls + \varepsilon")

st.markdown("""
I picked a standard spatial-discontinuity model and ran it using OLS (via the Python
`statsmodels` library). This is not an event-study, difference-in-differences, or
synthetic-control model because I do not have a treatment date here -- just a fixed line on a
map. My `side` variable (where 1 means Berar and 0 means Central Provinces) checks for a level
jump right at the boundary. Then, the `side × signed_dist_km` interaction checks if the slope
changes differently as you move further away on either side. To get `signed_dist_km`, I
calculated the distance from each taluka center to my merged border line using UTM 44N (and
wrote it as positive for the Berar side). Finally, I threw in total annual rain and elevation as
control variables. My data back in Entry 8 already confirmed that Vidarbha has a natural
west-drier and east-wetter climate trend that nature made on its own, so I had to block this out
completely before trusting any colonial law effect.
""")

st.markdown("---")

st.markdown("### Hypotheses")

h1, h2, h3 = st.columns(3)
with h1:
    st.info("**H1**\n\nCotton-signature NDVI decline jumps at the boundary (`side` significant), "
            "once rainfall and elevation are controlled for.")
with h2:
    st.info("**H2**\n\nAgrarian labor structure (ag-laborer-to-cultivator ratio) shows the same "
            "level jump, and it holds at both the corridor and full-footprint scale.")
with h3:
    st.info("**H3**\n\nThe modern Amravati/Nagpur Division boundary is, in fact, the same line "
            "as the historical Berar/Central Provinces one -- not just a convenient stand-in.")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Study Design</p>",
    unsafe_allow_html=True,
)
