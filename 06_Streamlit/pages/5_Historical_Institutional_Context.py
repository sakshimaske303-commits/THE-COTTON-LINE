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
The plan was to find a digitized 1901-1931 Imperial Gazetteer map and overlay it against the
modern division line. No accessible digitized version of one exists. What answers the same
question a different way: tracing the actual district-membership lists for Berar Division and the
Central Provinces' Nagpur Division across the 1903-1956 period, checking whether the same
territory sits on each side of the modern boundary, district by district.
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
            Ellichpur absorbed into Amravati district. Wun renamed Yavatmal. Basim renamed Washim,
            folded into Akola for a stretch, recreated as its own district 1 July 1998. Net effect:
            maps district-for-district onto today's <strong>Amravati Division</strong> — same
            5-district territory, renamed and re-split internally, no actual boundary redraw.
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
            Chanda renamed Chandrapur. Gondiya (split from Bhandara, 1999) and Gadchiroli (split
            from Chandrapur, 26 Aug 1982) are later internal subdivisions, not new land. The one
            real wrinkle: <strong>Balaghat</strong> went to Madhya Pradesh's Jabalpur Division on
            1 Nov 1956 (linguistic States Reorganisation) — never a Maharashtra district, so never
            part of this project's 11-district dataset to begin with.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**Bottom line:** as far as documented district lineage can show, the modern Amravati/Nagpur
Division boundary is the same line as the historical Berar/Central Provinces boundary — confirmed
by tracing every district's administrative history, not by a literal old-map overlay. The one
caveat worth stating precisely: this project's "Central Provinces" side is specifically the
Maharashtra-Vidarbha portion of the old CP Nagpur Division, very slightly smaller than the
historical division's full extent — the missing piece (Balaghat) fell away because of a 1956
language-based state boundary redraw, unrelated to the Ryotwari/Malguzari distinction this project
actually tests. A genuine period map for visual use is still not sourced — this doesn't block the
substantive question, which now has a well-sourced yes.
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
