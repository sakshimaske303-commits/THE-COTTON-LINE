"""
Path resolution + data loaders for THE COTTON LINE dashboard.

Lives in 06_Streamlit/utils/ -- data itself lives one project level up,
in 03_Data_Processed/ and 07_Outputs/. BASE_DIR/ROOT_DIR resolution
matches the pattern used across the rest of the portfolio (e.g.
GREEN_POLICY_INTELLIGENCE_SYSTEM/dashboard/app.py) so it works both
running locally from inside 06_Streamlit/ and however it ends up
deployed later.
"""
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
    """Shows an image if it exists at `path`; otherwise shows a plain
    "not added yet" note instead of erroring. Used for the theory
    diagram slot on Theoretical Foundations and every output chart."""
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
