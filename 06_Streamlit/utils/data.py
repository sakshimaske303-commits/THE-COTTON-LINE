"""Paths and data loaders for the dashboard."""
import os
import pandas as pd

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))       # .../06_Streamlit/utils
STREAMLIT_DIR = os.path.dirname(UTILS_DIR)                     # .../06_Streamlit
PROJECT_ROOT = os.path.dirname(STREAMLIT_DIR)                  # .../THE_COTTON_LINE

DATA_DIR = os.path.join(PROJECT_ROOT, "03_Data_Processed")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "07_Outputs")


def data_path(*parts):
    return os.path.join(DATA_DIR, *parts)


def output_path(*parts):
    return os.path.join(OUTPUTS_DIR, *parts)


def safe_read_csv(*parts):
    """Read a CSV under 03_Data_Processed/, or return None if it isn't there yet."""
    path = data_path(*parts)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def show_image_or_placeholder(path, caption=None, ai_generated=False):
    """Show the image if it exists, else a short "not added yet" note."""
    import streamlit as st
    if os.path.exists(path):
        st.image(path, use_container_width=True)
        if caption:
            st.markdown(
                f"<p style='text-align:center;' class='caption-text'>{caption}</p>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Not added yet -- this slot is reserved and will fill in once the image is ready.")


# ---------------------------------------------------------------- v2.0 loaders
def load_analysis():
    """One row per taluka (120) with every variable and sample flag (built by 05_Python/run_all.py)."""
    return safe_read_csv("Phase4", "analysis_taluka_dataset.csv")


def load_result(name):
    return safe_read_csv("Phase4", "results", name)


def key_numbers():
    import json
    p = data_path("Phase4", "results", "key_numbers.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


OUTCOME_LABELS = {
    "ndvi_decline_y1": "NDVI decline, year 1",
    "ndvi_decline_y2": "NDVI decline, year 2",
    "lst_june_c": "LST, 20 June 2026",
    "ag_laborer_to_cultivator": "Labourers per cultivator",
    "net_area_pct": "Net sown area (%)",
}
SCALE_LABELS = {"corridor": "Corridor (32)", "footprint": "Landsat sample", "census_wide": "Census, 119 talukas"}
