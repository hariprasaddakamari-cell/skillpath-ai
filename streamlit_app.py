import os
import requests
import streamlit as st

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎯",
    layout="wide",
)

API_URL = os.getenv("SKILLPATH_API_URL", "").rstrip("/")

# -------------------- UI CSS --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #f6f7fb;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 42px;
        border-radius: 26px;
        color: white;
        background: linear-gradient(135deg, #111827, #3730a3, #6d28d9);
        margin-bottom: 24px;
        box-shadow: 0 18px 45px rgba(49, 46, 129, 0.20);
    }

    .hero-label {
        color: #c7d2fe;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.05;
        font-weight: 800;
        margin: 10px 0;
    }

    .hero-text {
        max-width: 720px;
        color: #e0e7ff;
        font-size: 17px;
        line-height: 1.6;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
        margin: 25px 0 12px;
    }

    .metric {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 7px 22px rgba(15, 23, 42, 0.05);
    }

    .metric-number {
        color: #4338ca;
        font-size: 31px;
        font-weight: 800;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    .job {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
    }

    .job-title {
        font-size: 18px;
        font-weight: 800;
