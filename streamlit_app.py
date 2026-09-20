
/* Hero */
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

/* Cards */
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

/* Metrics */
.metric-card {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 18px;
    padding: 1rem 1.1rem;
    box-shadow: 0 6px 20px rgba(15,23,42,.04);
}
.metric-number {
    font-size: 1.85rem;
    line-height: 1;
    font-weight: 800;
    color: #4338ca;
}
.metric-label {
    color: #64748b;
    font-size: .78rem;
    margin-top: .35rem;
}

/* Job cards */
.job-card {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 18px;
    padding: 1.15rem 1.25rem;
    margin-bottom: .75rem;
}
.job-title {
    font-weight: 800;
    color: #111827;
    font-size: 1.05rem;
}
.job-meta {
    color: #64748b;
    font-size: .84rem;
    margin-top: .2rem;
}
.score {
    font-size: 1.45rem;
    font-weight: 800;
    color: #4338ca;
    text-align: right;
}
.bar {
    height: 8px;
    background: #e5e7eb;
    border-radius: 99px;
    overflow: hidden;
    margin-top: .65rem;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
    border-radius: 99px;
}

/* Skill chips */
.chip {
    display: inline-block;
    padding: .38rem .65rem;
    margin: .2rem .25rem .2rem 0;
    border-radius: 999px;
    background: #eef2ff;
    color: #3730a3;
    border: 1px solid #e0e7ff;
    font-size: .78rem;
    font-weight: 600;
}
.gap-chip {
    display: inline-block;
    padding: .38rem .65rem;
    margin: .2rem .25rem .2rem 0;
    border-radius: 999px;
    background: #fff7ed;
    color: #c2410c;
    border: 1px solid #fed7aa;
    font-size: .78rem;
    font-weight: 600;
}

/* Simulator */
.simulator {
    background: linear-gradient(135deg,#eef2ff,#faf5ff);
    border: 1px solid #ddd6fe;
    border-radius: 22px;
    padding: 1.4rem;
}
.sim-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #312e81;
}

/* Upload area */
.upload-box {
    background: #fafaff;
    border: 1px dashed #a5b4fc;
    border-radius: 18px;
    padding: .6rem;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 2.7rem;
}
</style>
