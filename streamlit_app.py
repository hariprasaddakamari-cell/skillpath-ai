import os
import requests
import streamlit as st

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.getenv("SKILLPATH_API_URL", "").rstrip("/")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f6f7fb;
}

.block-container {
    max-width: 1180px;
    padding: 1.5rem 2rem 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    border-radius: 28px;
    padding: 2.6rem 2.8rem;
    background:
        radial-gradient(circle at 90% 15%, rgba(129,140,248,.35), transparent 28%),
        radial-gradient(circle at 15% 100%, rgba(45,212,191,.18), transparent 28%),
        linear-gradient(135deg,#111827 0%,#312e81 52%,#4c1d95 100%);
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 50px rgba(49,46,129,.18);
}

.hero-kicker {
    color: #c7d2fe;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.hero h1 {
    font-size: 3rem;
    line-height: 1.05;
    margin: .45rem 0 .8rem;
    font-weight: 800;
}

.hero p {
    color: #e0e7ff;
    max-width: 720px;
    font-size: 1.03rem;
    line-height: 1.65;
}

.card {
    background: #fff;
    border: 1px solid #e6e8ef;
    border-radius: 20px;
    padding: 1.25rem;
    box-shadow: 0 8px 25px rgba(15,23,42,.045);
}

.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #111827;
    margin: 1.4rem 0 .8rem;
}

.muted {
    color: #64748b;
}

.metric-card {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 18px;
    padding: 1rem 1.1rem;
