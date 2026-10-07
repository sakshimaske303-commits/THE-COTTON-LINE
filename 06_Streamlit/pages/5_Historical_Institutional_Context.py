import streamlit as st
from utils.theme import inject_theme, PALETTE
from utils.data import safe_read_csv

st.set_page_config(page_title="Historical & Institutional Context — THE COTTON LINE", page_icon="🏛️", layout="wide")
inject_theme()

st.markdown("<h1>🏛️ HISTORICAL &amp; INSTITUTIONAL CONTEXT</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; font-weight: 700;'>Verifying the Modern Boundary Against "
    "Documented District Lineage, and the Forest Rights Act Compilation</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# HISTORICAL BOUNDARY LINEAGE
# ============================================================
st.markdown("### Is the Modern Boundary Actually the Historical One?")

st.markdown("""
My original plan was to find an old, scanned 1901-1931 Imperial Gazetteer map and stack it
directly against my modern division layer. I failed because no accessible digitized version of
that map exists anywhere. So, I tackled the exact same problem from a different angle by
manually tracking down old district-membership archives for both Berar Division and Central
Provinces' Nagpur Division from 1903 to 1956. I sat down and cross-checked whether the exact same
piece of land sits on each side of the modern boundary, district by district.
""")

h1, h2 = st.columns(2)
with h1:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 260px;">
        <p style="color:{PALETTE['berar']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:10px;">Berar Division, 1903-1956</p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.88rem; margin:0 0 10px 0;">
            Amraoti, Akola, Ellichpur, Buldhana, Basim, Wun
        </p>
        <p style="color:{PALETTE['text_secondary']}; font-size:0.85rem; margin:0;">
            Later, Ellichpur got merged into Amravati district, Wun changed its name to Yavatmal,
            and Basim turned into Washim (which got folded into Akola for a stretch before coming
            back out as its own separate district on 1 July 1998). This district history lines up
            district-for-district with today's <strong>Amravati Division</strong> — the same
            5-district territory, just renamed and re-split internally, with no actual boundary
            redraw.
        </p>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div class="recon-card" style="min-height: 260px;">
        <p style="color:{PALETTE['cp']}; font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:10px;">CP's Nagpur Division, Historical</p>
        <p style="color:{PALETTE['text_primary']}; font-size:0.88rem; margin:0 0 10px 0;">
            Nagpur, Bhandara, Chanda, Wardha, and <strong>Balaghat</strong>
        </p>
        <p style="color:{PALETTE['text_secondary']}; font-size:0.85rem; margin:0;">
            Later on, Chanda changed its name to Chandrapur, while Gondiya split off from
            Bhandara in 1999 and Gadchiroli split from Chandrapur on 26 August 1982 (meaning these
            two are just internal boundary cuts, not new land). The one real wrinkle:
            <strong>Balaghat</strong> went to Madhya Pradesh's Jabalpur Division on 1 Nov 1956
            during the linguistic States Reorganisation — it was never a Maharashtra district, so
            it was never part of this project's 11-district dataset to begin with.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**Bottom line:** as far as documented district lineage can show, the modern Amravati-Nagpur
Division boundary is the same line as the historical Berar-Central Provinces boundary. I
checked this against the administrative lineage of each district rather than a period map, so
it is district-level evidence and not a taluka-by-taluka verification. Some talukas on the
Central Provinces side (for example Rajura, from Hyderabad State) came from other jurisdictions,
so that side is not uniformly Malguzari. One further catch: my
"Central Provinces" data side only looks at the Maharashtra-Vidarbha section of the old CP Nagpur
Division, which makes it slightly smaller than the historical footprint. The missing piece --
Balaghat -- dropped away during the 1956 language-based state reshuffle, which has nothing to do
with the Ryotwari or Malguzari farming rules I am actually testing. I still have not found a
genuine historical period map to use as a visual aid, but that does not block my main research
question, since district lineage is consistent with the line being the same, though it is not a geometric confirmation.
""")

st.markdown("---")

# ============================================================
# FRA COMPILATION
# ============================================================
st.markdown("### Forest Rights Act: A Sourced Compilation, Not a Clean Panel")

st.markdown("""
No clean taluka-level, or even consistent district-level, FRA dataset exists in the public domain
for Vidarbha — this isn't a case of not searching hard enough. What follows is fragmented across a
few documents at a few different scales, compiled here with its scope stated for every row, and
kept as a **contextual/narrative data point, not a Phase 4 regression variable** — there isn't a
consistent enough measurement across enough districts to add it to the taluka-level dataset the
way NDVI or rainfall are in there.
""")

fra = safe_read_csv("Economics", "fra_compilation_vidarbha.csv")
if fra is None:
    st.warning("fra_compilation_vidarbha.csv not found yet.")
else:
    st.dataframe(fra, use_container_width=True, hide_index=True,
                 column_config={"source_url": st.column_config.LinkColumn("source_url")})

st.markdown(f"""
<div class="recon-card" style="margin-top: 12px;">
    <p style="color:{PALETTE['accent2']}; font-weight:800; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">
        The one real district-level anchor
    </p>
    <p style="color:{PALETTE['text_primary']}; font-size:0.9rem; line-height:1.6; margin:0;">
        <strong>Gadchiroli</strong>, 2016 data: 1,355 community forest rights titles covering
        4,34,181 hectares against an estimated minimum potential of 5,57,137 hectares —
        <strong>77.9% recognized</strong>, explicitly classified "high performing" in the
        source report, against Nashik district elsewhere in the state at just 5%. A real,
        sourced, single-district figure — not generalizable to the other 7 districts, which have
        no equivalent public number.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>THE COTTON LINE — Historical &amp; Institutional Context</p>",
    unsafe_allow_html=True,
)
