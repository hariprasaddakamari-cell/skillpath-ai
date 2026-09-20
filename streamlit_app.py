import os
import requests
import streamlit as st

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("SKILLPATH_API_URL", "").rstrip("/")

# ---------- Theme ----------
st.markdown(
    """
<style>
:root {
    --bg: #f5f7f2;
    --panel: #ffffff;
    --ink: #172018;
    --muted: #68736b;
    --green: #176b4d;
    --green2: #23845f;
    --soft: #e9f3ed;
    --line: #dfe7e1;
    --orange: #e98b42;
}

.stApp { background: var(--bg); color: var(--ink); }
.block-container { max-width: 1250px; padding-top: 1.5rem; padding-bottom: 4rem; }

[data-testid="stSidebar"] {
    background: #123b2c;
}
[data-testid="stSidebar"] * { color: #eef8f1 !important; }

.brand {
    padding: 8px 4px 24px 4px;
}
.brand-name {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: -.7px;
}
.brand-sub {
    color: #b8d8c5;
    font-size: 12px;
    margin-top: 4px;
}

.hero {
    background: linear-gradient(115deg, #153f30 0%, #1e6a4d 58%, #2c8b63 100%);
    border-radius: 28px;
    padding: 42px 44px;
    color: white;
    box-shadow: 0 20px 50px rgba(19,70,48,.18);
}
.eyebrow {
    color: #bce8ce;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero h1 {
    font-size: 46px;
    line-height: 1.04;
    margin: 10px 0 12px;
    letter-spacing: -1.5px;
}
.hero p {
    max-width: 720px;
    color: #e3f4e9;
    font-size: 16px;
    line-height: 1.65;
}

.section {
    font-size: 24px;
    font-weight: 850;
    margin: 30px 0 12px;
    color: var(--ink);
}
.subtle { color: var(--muted); font-size: 14px; }

.card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 26px rgba(21,44,31,.05);
}
.card-title { font-size: 18px; font-weight: 850; }
.card-muted { color: var(--muted); font-size: 13px; margin-top: 5px; }

.metric {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 19px;
}
.metric-value { font-size: 30px; font-weight: 900; color: var(--green); }
.metric-label { color: var(--muted); font-size: 12px; margin-top: 3px; }

.job {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 12px;
}
.job-title { font-size: 18px; font-weight: 850; }
.job-company { color: var(--muted); font-size: 13px; margin-top: 4px; }
.score { color: var(--green); font-size: 27px; font-weight: 900; }

.progress {
    background: #e7eee9;
    height: 8px;
    border-radius: 99px;
    overflow: hidden;
    margin-top: 13px;
}
.progress > div {
    height: 100%;
    background: linear-gradient(90deg, var(--green), var(--green2));
}

.chip, .gap {
    display: inline-block;
    border-radius: 999px;
    padding: 6px 10px;
    margin: 3px 4px 3px 0;
    font-size: 12px;
    font-weight: 750;
}
.chip { background: #eaf4ee; color: #176b4d; border: 1px solid #cfe5d8; }
.gap { background: #fff2e8; color: #a9561d; border: 1px solid #f4d3bc; }

.sim {
    background: linear-gradient(135deg, #edf7f0, #f9f5eb);
    border: 1px solid #d8e7dc;
    border-radius: 22px;
    padding: 25px;
}
.sim-title { font-size: 22px; font-weight: 900; color: #173c2c; }

.trace {
    background: #14271e;
    color: #d7f3e0;
    border-radius: 17px;
    padding: 18px;
    font-family: monospace;
    font-size: 12px;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 800;
    min-height: 45px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
def api_request(method, path, **kwargs):
    if not API_URL:
        return None, "Backend URL is not configured."
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=180,
            **kwargs,
        )
        if response.ok:
            return response.json(), None
        return None, f"HTTP {response.status_code}: {response.text}"
    except requests.RequestException as exc:
        return None, str(exc)


def show_chips(items, cls="chip"):
    if not items:
        return
    html = "".join(
        f'<span class="{cls}">{str(x)}</span>' for x in items
    )
    st.markdown(html, unsafe_allow_html=True)


def job_score(job):
    try:
        return max(0, min(100, float(
            job.get("match_score", job.get("score", 0))
        )))
    except (TypeError, ValueError):
        return 0


def course_items(courses):
    result = []
    if not isinstance(courses, dict):
        return result
    for category, values in courses.items():
        if isinstance(values, list):
            for value in values:
                result.append((category, value))
        else:
            result.append((category, values))
    return result


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-name">SkillPath AI</div>
            <div class="brand-sub">AI-powered career intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Your target")
    location = st.text_input("Location", "Hyderabad")
    interests = st.text_input("Career interest", "Backend Development")
    free_only = st.checkbox("Prioritize free learning")

    st.markdown("---")
    st.markdown("### Backend")
    configured = st.text_input(
        "FastAPI URL",
        value=API_URL,
        placeholder="https://your-backend.onrender.com",
    )
    if configured:
        API_URL = configured.rstrip("/")

    if API_URL:
        data, error = api_request("GET", "/api/health")
        if error:
            st.error("Backend offline")
        else:
            st.success("Backend connected")
            st.caption(
                f"{data.get('jobs', 0)} jobs • "
                f"{data.get('courses', 0)} courses"
            )

# ---------- Hero ----------
st.markdown(
    """
<div class="hero">
    <div class="eyebrow">Career intelligence platform</div>
    <h1>Turn your current skills<br>into your next opportunity.</h1>
    <p>
        Upload your resume or build a profile. SkillPath AI identifies
        relevant jobs, explains your skill gaps, recommends a focused
        learning path, and lets you simulate the impact of learning a
        new skill.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Profile builder ----------
st.markdown(
    '<div class="section">Build your profile</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtle">Start with your resume or enter your skills manually.</div>',
    unsafe_allow_html=True,
)

tab_resume, tab_manual = st.tabs(["📄 Upload resume", "✍️ Enter manually"])

with tab_resume:
    resume = st.file_uploader(
        "Drop your PDF resume here",
        type=["pdf"],
        help="PDF only, maximum 5 MB.",
    )
    if st.button(
        "Analyze my career →",
        type="primary",
        use_container_width=True,
        disabled=resume is None,
    ):
        with st.spinner("Analyzing your resume and matching opportunities..."):
            result, error = api_request(
                "POST",
                "/api/analyze-resume",
                files={
                    "file": (
                        resume.name,
                        resume.getvalue(),
                        "application/pdf",
                    )
                },
                data={
                    "location": location,
                    "interests": interests,
                    "free_only": str(free_only).lower(),
                },
            )
        if error:
            st.error(error)
        else:
            st.session_state["result"] = result
            st.success("Your career profile is ready.")

with tab_manual:
    manual_name = st.text_input("Name", "Candidate")
    manual_skills = st.text_input(
        "Skills, separated by commas",
        "Java, Spring Boot, SQL, Git, Docker",
    )
    if st.button("Build my profile →", use_container_width=True):
        skills = [
            x.strip()
            for x in manual_skills.split(",")
            if x.strip()
        ]
        payload = {
            "profile": {
                "name": manual_name,
                "location": location,
                "interests": [
                    x.strip()
                    for x in interests.split(",")
                    if x.strip()
                ],
                "skills": skills,
            },
            "free_only": free_only,
        }
        with st.spinner("Building your career profile..."):
            result, error = api_request(
                "POST", "/api/analyze", json=payload
            )
        if error:
            st.error(error)
        else:
            st.session_state["result"] = result
            st.success("Your career profile is ready.")

# ---------- Results ----------
result = st.session_state.get("result")

if result:
    profile = result.get("profile", {}) or {}
    jobs = result.get("jobs", []) or []
    gaps = result.get("skill_gaps", {}) or {}
    courses = result.get("courses", {}) or {}
    skills = profile.get("skills", []) or []

    st.markdown(
        '<div class="section">Your career snapshot</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    values = [
        (len(skills), "Skills detected"),
        (len(jobs), "Relevant jobs"),
        (len(gaps) if isinstance(gaps, dict) else 0, "Gap areas"),
        (len(course_items(courses)), "Learning options"),
    ]
    for col, (value, label) in zip(cols, values):
        with col:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if skills:
        st.markdown(
            '<div class="section">Your current skills</div>',
            unsafe_allow_html=True,
        )
        show_chips(skills)

    # ---------- Jobs ----------
    st.markdown(
        '<div class="section">Opportunities for you</div>',
        unsafe_allow_html=True,
    )

    if not jobs:
        st.info("No matching jobs were returned for this profile.")
    else:
        for job in jobs[:10]:
            score = job_score(job)
            title = job.get("title", "Untitled role")
            company = job.get("company", "Company")
            where = job.get("location", "Location")
            required = job.get("required_skills", []) or []

            st.markdown(
                f"""
                <div class="job">
                    <div style="display:flex;justify-content:space-between;gap:20px;">
                        <div>
                            <div class="job-title">{title}</div>
                            <div class="job-company">
                                {company} &nbsp; · &nbsp; {where}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div class="score">{score:.0f}%</div>
                            <div class="job-company">match</div>
                        </div>
                    </div>
                    <div class="progress">
                        <div style="width:{score}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if required:
                st.caption(
                    "Required: " + " • ".join(map(str, required))
                )

    # ---------- Skill gaps ----------
    st.markdown(
        '<div class="section">Your opportunity gaps</div>',
        unsafe_allow_html=True,
    )

    gap_list = []
    if isinstance(gaps, dict):
        for value in gaps.values():
            if isinstance(value, list):
                gap_list.extend(value)
            else:
                gap_list.append(value)

    if gap_list:
        show_chips(gap_list, "gap")
    else:
        st.success("No major skill gaps were returned.")

    # ---------- Learning path ----------
    st.markdown(
        '<div class="section">Your learning path</div>',
        unsafe_allow_html=True,
    )

    learning = course_items(courses)

    if learning:
        cols = st.columns(min(3, len(learning)))
        for index, (category, course) in enumerate(learning[:9]):
            with cols[index % len(cols)]:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="eyebrow" style="color:#23845f;">
                            {category}
                        </div>
                        <div class="card-title" style="margin-top:8px;">
                            {course}
                        </div>
                        <div class="card-muted">
                            Focus on this skill to improve job readiness.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No learning recommendations returned.")

    # ---------- Simulator ----------
    st.markdown(
        '<div class="section">Career simulator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sim">
            <div class="sim-title">What if you learn one more skill?</div>
            <div class="subtle">
                Pick a target role and test how adding a skill changes
                your match.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_map = {
        job.get("title", str(job.get("id"))): job.get("id")
        for job in jobs
        if job.get("id") is not None
    }

    if job_map:
        left, right = st.columns([1.5, 1])
        with left:
            selected = st.selectbox(
                "Target role",
                list(job_map.keys()),
            )
        with right:
            new_skill = st.text_input("Skill to learn", "SQL")

        if st.button(
            "Simulate skill impact →",
            type="primary",
            use_container_width=True,
        ):
            payload = {
                "profile": profile,
                "added_skill": new_skill,
                "job_id": job_map[selected],
            }
            with st.spinner("Calculating impact..."):
                simulation, error = api_request(
                    "POST",
                    "/api/simulate-skill",
                    json=payload,
                )

            if error:
                st.error(error)
            else:
                before = simulation.get("before", {}).get(
                    "match_score", 0
                )
                after = simulation.get("after", {}).get(
                    "match_score", 0
                )
                gain = simulation.get("match_gain", 0)

                a, b, c = st.columns(3)
                a.metric("Current match", before)
                b.metric("After learning", after, delta=gain)
                c.metric(
                    "Local jobs unlocked",
                    simulation.get("local_jobs_with_skill", 0),
                )

                st.success(
                    f"Learning {simulation.get('skill', new_skill)} "
                    "can strengthen your match for this role."
                )

    # ---------- Agent transparency ----------
    st.markdown(
        '<div class="section">How SkillPath AI reached this result</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View retrieval and agent trace"):
        st.markdown(
            """
            <div class="trace">
            Loader → Splitter → Embeddings → FAISS → Retriever
            → LangGraph → Tools
            </div>
            """,
            unsafe_allow_html=True,
        )

        sources = result.get("sources", [])
        trace = result.get("trace", [])

        if sources:
            st.write("Retrieved sources")
            st.write(sources)

        if trace:
            st.write("Agent trace")
            st.write(trace)

else:
    # Empty state designed for first-time demo.
    st.markdown(
        """
        <div class="section">How it works</div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    steps = [
        (
            "01",
            "Build your profile",
            "Upload a resume or enter your technical skills.",
        ),
        (
            "02",
            "Discover opportunities",
            "The agent matches your profile against the job knowledge base.",
        ),
        (
            "03",
            "Close the gaps",
            "Get targeted learning recommendations and simulate skill impact.",
        ),
    ]

    for col, (number, title, text) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-value">{number}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-muted">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
