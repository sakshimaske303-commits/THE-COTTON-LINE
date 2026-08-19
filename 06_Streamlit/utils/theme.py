import streamlit as st

# ============================================================
# THE COTTON LINE -- dashboard theme
# Palette: Prussian Blue / Teal Blue (Berar side) + Mughal Green
# (Central Provinces side) + Pastel Blue / Light Silver on a dark
# navy base. Card-and-border style matched to the rest of the
# portfolio (see BORDER_OPTICS/utils/theme.py -- closest sibling,
# same historical-institutional-persistence design).
# ============================================================
PALETTE = {
    "bg_main": "#0A1B26",       # near-black navy -- page background
    "bg_card": "#122B3C",       # card background, one step up from bg_main
    "bg_sidebar": "#071119",    # darkest -- sidebar
    "prussian": "#103A57",       # Prussian Blue -- borders / muted secondary series
    "berar": "#307B8E",          # Teal Blue -- Berar / Amravati Division side
    "cp": "#8FE8B4",             # Icy pastel green -- Central Provinces / Nagpur Division side
    "accent": "#307B8E",         # Teal Blue -- primary accent
    "accent2": "#8FE8B4",        # Icy pastel green -- secondary accent (bright, reads on dark bg;
                                  # Mughal Green itself is too dark to register against bg_main)
    "text_primary": "#CEE5D6",  # Light Silver -- main text on dark bg
    "text_secondary": "#A9D3C5",# Pastel Blue -- muted / secondary text
}


def inject_theme():
    p = PALETTE
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif;
        }}

        .stApp {{
            background: {p['bg_main']};
            color: {p['text_primary']};
            font-family: 'Poppins', sans-serif;
        }}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }}

        /* ---- Keep header visible (needed for sidebar open/close)
        but hide only the Deploy button ---- */
        [data-testid="stHeader"] {{
            background-color: {p['bg_main']} !important;
            height: 3rem !important;
        }}
        [data-testid="stAppDeployButton"] {{ display: none !important; }}
        [data-testid="stDecoration"] {{ display: none !important; }}
        #MainMenu {{ visibility: hidden !important; }}

        /* ---- Sidebar collapse/expand button -- visible on dark theme ---- */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="baseButton-header"],
        [data-testid="stHeader"] button,
        [data-testid*="ollapse" i],
        button[kind="header"] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;
        }}
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            background: {p['bg_sidebar']} !important;
            border: 1.5px solid {p['accent']} !important;
            border-radius: 8px !important;
            padding: 4px !important;
        }}
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="baseButton-header"] svg,
        [data-testid="stHeader"] button svg,
        button[kind="header"] svg {{
            fill: {p['accent']} !important;
            stroke: {p['accent']} !important;
            opacity: 1 !important;
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {p['bg_sidebar']} 0%, {p['bg_main']} 100%);
            border-right: 1px solid rgba(48, 123, 142, 0.25);
        }}
        section[data-testid="stSidebar"] * {{ color: {p['text_primary']} !important; }}
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{ font-weight: 500; }}

        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
        section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a,
        section[data-testid="stSidebar"] nav a,
        section[data-testid="stSidebar"] ul li a {{
            border-radius: 8px !important;
            padding: 8px 14px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }}
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover,
        section[data-testid="stSidebar"] nav a:hover,
        section[data-testid="stSidebar"] ul li a:hover {{
            background: rgba(48, 123, 142, 0.14) !important;
            border-left: 3px solid {p['accent']};
        }}
        section[data-testid="stSidebar"] [aria-selected="true"],
        section[data-testid="stSidebar"] [aria-current="page"] {{
            background: rgba(54, 107, 43, 0.22) !important;
            border-left: 3px solid {p['accent2']};
            font-weight: 800 !important;
        }}

        /* ---- Headers ---- */
        h1 {{
            color: {p['accent2']} !important;
            font-weight: 800 !important;
            font-size: 2.9rem !important;
            border-bottom: 3px solid {p['accent']};
            text-align: center !important;
            padding-bottom: 0.4rem;
        }}
        h2 {{
            color: {p['accent']} !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-top: 1.5rem !important;
        }}
        h3 {{
            color: {p['accent2']} !important;
            text-align: center !important;
            font-weight: 600 !important;
        }}
        p, li {{ color: {p['text_primary']}; font-weight: 500; }}
        strong, b {{ color: {p['accent']}; font-weight: 700; }}

        /* ---- Metric cards ---- */
        div[data-testid="stMetric"] {{
            background-color: {p['bg_card']};
            border: 1px solid {p['accent']};
            border-left: 5px solid {p['accent2']};
            border-radius: 8px;
            padding: 16px 18px;
        }}
        div[data-testid="stMetricValue"] {{
            color: {p['text_primary']} !important;
            font-weight: 800 !important;
            font-size: 1.6rem !important;
        }}
        div[data-testid="stMetricLabel"] {{
            color: {p['accent']} !important;
            text-transform: uppercase;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px;
        }}

        /* ---- Buttons ---- */
        .stButton>button {{
            background-color: {p['accent']};
            color: #EAF3EF;
            border-radius: 6px;
            border: none;
            font-weight: 700;
        }}
        .stButton>button:hover {{ background-color: {p['accent2']}; color: {p['bg_main']}; }}

        div[data-testid="stDownloadButton"] > button {{
            background-color: {p['accent']};
            color: #0A1B26;
            border-radius: 6px;
            border: none;
            font-weight: 700;
        }}
        div[data-testid="stDownloadButton"] > button:hover {{ background-color: {p['accent2']}; }}
        div[data-testid="stDownloadButton"] > button p {{ color: #0A1B26 !important; }}

        /* ---- Selectbox / inputs ---- */
        div[data-baseweb="select"] > div {{
            background-color: {p['bg_card']} !important;
            border-color: {p['accent']} !important;
        }}

        /* ---- Info / warning / success callouts ---- */
        div[data-testid="stAlert"] {{
            background-color: {p['bg_card']} !important;
            border-radius: 8px;
            border-left: 5px solid {p['accent']};
            color: {p['text_primary']} !important;
            font-weight: 600;
        }}

        hr {{ border: none; border-top: 2px solid {p['accent']}; margin: 1.8rem 0; }}

        .caption-text {{
            color: {p['text_secondary']};
            font-size: 0.88rem;
            font-weight: 600;
        }}

        /* ---- Tables / dataframes ---- */
        div[data-testid="stDataFrame"] {{ border: 1px solid {p['accent']}; border-radius: 6px; }}

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
        .stTabs [data-baseweb="tab"] {{ color: {p['text_secondary']}; font-weight: 700; }}
        .stTabs [aria-selected="true"] {{
            color: {p['accent2']} !important;
            font-weight: 800;
            border-bottom: 3px solid {p['accent']} !important;
        }}

        /* ---- Custom content cards (used throughout app.py/pages) ---- */
        .recon-card {{
            background-color: {p['bg_card']};
            border: 1px solid {p['accent']};
            border-left: 5px solid {p['accent2']};
            border-radius: 10px;
            padding: 22px;
        }}

        [data-testid="stExpander"] {{
            background-color: {p['bg_card']} !important;
            border: 1px solid {p['accent']} !important;
            border-radius: 8px !important;
        }}
        [data-testid="stExpander"] summary {{ background-color: {p['bg_card']} !important; }}
        [data-testid="stExpander"] summary p {{
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: {p['accent2']} !important;
        }}
        [data-testid="stExpanderDetails"] {{ background-color: {p['bg_card']} !important; }}
        [data-testid="stExpanderDetails"] p, [data-testid="stExpanderDetails"] li {{
            color: {p['text_primary']} !important;
        }}
        [data-testid="stExpander"] summary svg, [data-testid="stExpander"] svg {{
            fill: {p['accent']} !important; stroke: {p['accent']} !important; color: {p['accent']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def plotly_layout(fig, height=None):
    """Apply the dashboard's dark theme to a Plotly figure -- used on every chart page."""
    p = PALETTE
    fig.update_layout(
        paper_bgcolor=p["bg_main"],
        plot_bgcolor=p["bg_card"],
        font=dict(color=p["text_primary"], family="Poppins, sans-serif"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig.update_xaxes(gridcolor="rgba(169,211,197,0.15)", zerolinecolor="rgba(169,211,197,0.25)")
    fig.update_yaxes(gridcolor="rgba(169,211,197,0.15)", zerolinecolor="rgba(169,211,197,0.25)")
    if height:
        fig.update_layout(height=height)
    return fig
