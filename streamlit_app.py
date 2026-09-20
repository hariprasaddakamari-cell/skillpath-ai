import os
import html
import textwrap
import requests
import streamlit as st

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("SKILLPATH_API_URL", "").rstrip("/")


# ============================================================
# UI / CSS
# ============================================================
CSS = """
<style>
.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: #111827;
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

[data-testid="stSidebar"] input {
    color: #111827 !important;
    background: white !important;
}

.hero {
    padding: 42px;
    border-radius: 28px;
    color: white;
    background:
        radial-gradient(circle at 90% 10%, rgba(255,255,255,.16), transparent 30%),
        linear-gradient(135deg, #111827 0%, #3730a3 55%, #6d28d9 100%);
    margin-bottom: 26px;
    box-shadow: 0 20px 50px rgba(49,46,129,.20);
}

.hero-label {
    color: #c7d2fe;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 44px;
    line-height: 1.06;
    font-weight: 850;
    margin: 10px 0 12px;
}

.hero-text {
    max-width: 760px;
    color: #e0e7ff;
    font-size: 16px;
    line-height: 1.65;
}

.section-title {
    font-size: 25px;
    font-weight: 850;
    color: #111827;
    margin: 28px 0 13px;
}

.section-subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: -7px;
    margin-bottom: 15px;
}

.metric {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 19px;
    min-height: 105px;
    box-shadow: 0 7px 22px rgba(15,23,42,.05);
}

.metric-number {
    color: #4338ca;
    font-size: 30px;
    font-weight: 850;
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
    margin-bottom: 13px;
    box-shadow: 0 6px 20px rgba(15,23,42,.04);
}

.job-title {
    font-size: 18px;
    font-weight: 800;
    color: #111827;
}

.job-meta {
    color: #64748b;
    font-size: 13px;
    margin-top: 5px;
}

.job-score {
    color: #4f46e5;
    font-size: 25px;
    font-weight: 850;
    text-align: right;
}

.progress {
    height: 8px;
    background: #e5e7eb;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 15px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
}

.chip {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3;
    border: 1px solid #c7d2fe;
    border-radius: 999px;
    padding: 6px 11px;
    margin: 3px;
    font-size: 12px;
    font-weight: 700;
}

.gap-card {
    background: linear-gradient(135deg,#fff7ed,#ffffff);
    border: 1px solid #fed7aa;
    border-radius: 17px;
    padding: 17px;
    min-height: 92px;
    box-shadow: 0 5px 17px rgba(15,23,42,.035);
}

.gap-title {
    color: #c2410c;
    font-size: 15px;
    font-weight: 800;
}

.gap-text {
    color: #64748b;
    font-size: 12px;
    margin-top: 5px;
}

.course {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 19px;
    min-height: 245px;
    box-shadow: 0 6px 18px rgba(15,23,42,.04);
}

.course-category {
    color: #6366f1;
    font-size: 11px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.course-name {
    color: #111827;
    font-size: 18px;
    line-height: 1.3;
    font-weight: 850;
    margin-top: 8px;
}

.course-provider {
    color: #64748b;
    font-size: 13px;
    margin-top: 5px;
}

.course-info {
    color: #475569;
    font-size: 12px;
    margin-top: 13px;
}

.course-skills {
    margin-top: 10px;
}

.profile-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 7px 22px rgba(15,23,42,.04);
}

.source-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 13px;
    margin-bottom: 8px;
    color: #334155;
    font-size: 13px;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 750;
}

div[data-testid="stFileUploader"] {
    border-radius: 15px;
}

@media (max-width: 800px) {
    .hero-title {
        font-size: 34px;
    }
    .hero {
        padding: 28px;
    }
}
</style>
"""

def render_markdown(content, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(content, str):
        content = textwrap.dedent(content).strip()
    return st.markdown(content, *args, **kwargs)

render_markdown(CSS, unsafe_allow_html=True)


# ============================================================
# Helpers
# ============================================================
def safe_text(value):
    """Convert values to display-safe HTML text."""
    return html.escape(str(value))


def score_value(job):
    try:
        return float(job.get("match_score", job.get("score", 0)))
    except (TypeError, ValueError):
        return 0.0


def show_chips(items):
    """Render a clean list of skill chips."""
    if not items:
        return

    cleaned = []
    for item in items:
        if isinstance(item, dict):
            item = (
                item.get("skill")
                or item.get("name")
                or item.get("title")
                or ""
            )

        item = str(item).strip()

        if item and item not in cleaned:
            cleaned.append(item)

    if not cleaned:
        return

    html_items = "".join(
        f'<span class="chip">{safe_text(item)}</span>'
        for item in cleaned
    )

    render_markdown(html_items, unsafe_allow_html=True)


def flatten_courses(courses):
    """
    Convert backend course structure into:
    [(category, course_dict), ...]
    """
    output = []

    if not isinstance(courses, dict):
        return output

    for category, values in courses.items():

        if isinstance(values, list):
            for value in values:
                output.append((category, value))
        else:
            output.append((category, values))

    return output


def extract_gap_items(gaps):
    """Flatten and clean the backend skill-gap structure."""
    items = []

    if isinstance(gaps, dict):
        for key, value in gaps.items():

            if isinstance(value, list):
                candidates = value
            else:
                candidates = [value]

            for item in candidates:

                if isinstance(item, dict):
                    item = (
                        item.get("skill")
                        or item.get("name")
                        or item.get("title")
                        or key
                    )

                if item:
                    item = str(item).strip()

                    if item and item not in items:
                        items.append(item)

    elif isinstance(gaps, list):
        for item in gaps:
            if isinstance(item, dict):
                item = (
                    item.get("skill")
                    or item.get("name")
                    or item.get("title")
                    or ""
                )

            if item:
                item = str(item).strip()
                if item and item not in items:
                    items.append(item)

    elif gaps:
        items.append(str(gaps).strip())

    return items


def course_field(course, key, default=""):
    if isinstance(course, dict):
        return course.get(key, default)
    return default


def render_course(category, course):
    """Render one course as a proper UI card."""
    if not isinstance(course, dict):
        render_markdown(
            f"""
            <div class="course">
                <div class="course-category">{safe_text(category)}</div>
                <div class="course-name">{safe_text(course)}</div>
                <div class="course-provider">
                    Recommended learning resource
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    title = course_field(course, "title", "Recommended course")
    provider = course_field(
        course,
        "provider",
        "Open Learning Catalog",
    )
    duration = course_field(course, "duration_weeks", "?")
    cost = course_field(course, "cost", 0)
    level = course_field(course, "level", "All levels")
    skills = course_field(course, "skills", [])

    if cost in (0, "0", None, ""):
        cost_text = "Free"
    else:
        cost_text = f"₹{cost}"

    skill_html = ""

    if isinstance(skills, list):
        skill_html = "".join(
            f'<span class="chip">{safe_text(skill)}</span>'
            for skill in skills[:5]
        )

    render_markdown(
        f"""
        <div class="course">
            <div class="course-category">
                {safe_text(category)}
            </div>

            <div class="course-name">
                {safe_text(title)}
            </div>

            <div class="course-provider">
                {safe_text(provider)}
            </div>

            <div class="course-info">
                <b>{safe_text(level)}</b>
                &nbsp; • &nbsp;
                {safe_text(duration)} week(s)
                &nbsp; • &nbsp;
                {safe_text(cost_text)}
            </div>

            <div class="course-skills">
                {skill_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Hero
# ============================================================
render_markdown(
    """
    <div class="hero">
        <div class="hero-label">AI CAREER INTELLIGENCE</div>

        <div class="hero-title">
            Turn your skills into<br>
            your next career move.
        </div>

        <div class="hero-text">
            SkillPath AI analyzes your resume, matches you with
            relevant opportunities, identifies skill gaps, and
            recommends a focused learning path.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:

    render_markdown("## 🎯 SkillPath AI")
    st.caption("AI-powered skill-gap and career matching")

    st.divider()

    configured_url = st.text_input(
        "Backend URL",
        value=API_URL,
        placeholder="https://your-backend.onrender.com",
    )

    if configured_url:
        API_URL = configured_url.rstrip("/")

    location = st.text_input(
        "Target location",
        "Hyderabad",
    )

    interests = st.text_input(
        "Career interest",
        "Backend Development",
    )

    free_only = st.checkbox(
        "Only show free courses",
        value=False,
    )

    st.divider()

    if API_URL:

        try:
            response = requests.get(
                f"{API_URL}/api/health",
                timeout=10,
            )

            if response.ok:
                data = response.json()

                st.success("Backend connected")

                st.caption(
                    f"{data.get('jobs', 0)} jobs • "
                    f"{data.get('courses', 0)} courses"
                )

            else:
                st.error(
                    f"Backend returned HTTP {response.status_code}"
                )

        except requests.RequestException:
            st.warning(
                "Backend connection unavailable."
            )

    st.caption("SkillPath AI • Career Intelligence")


if not API_URL:

    st.info(
        "Set SKILLPATH_API_URL in Streamlit Secrets "
        "or enter your Render backend URL in the sidebar."
    )

    st.stop()


# ============================================================
# Input
# ============================================================
render_markdown(
    '<div class="section-title">Build your career profile</div>',
    unsafe_allow_html=True,
)

render_markdown(
    """
    <div class="section-subtitle">
        Upload a resume for automatic skill extraction,
        or enter your skills manually.
    </div>
    """,
    unsafe_allow_html=True,
)

resume_tab, manual_tab = st.tabs(
    ["📄 Resume Analysis", "✍️ Manual Profile"]
)


# ============================================================
# Resume analysis
# ============================================================
with resume_tab:

    resume = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        help="PDF only. Maximum size: 5 MB.",
    )

    if st.button(
        "🚀 Analyze My Career",
        type="primary",
        use_container_width=True,
        disabled=resume is None,
    ):

        try:

            with st.spinner(
                "Reading your resume and finding opportunities..."
            ):

                response = requests.post(
                    f"{API_URL}/api/analyze-resume",
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
                        "free_only": str(
                            free_only
                        ).lower(),
                    },
                    timeout=180,
                )

            if response.ok:

                st.session_state["result"] = response.json()

                st.success(
                    "Career analysis completed."
                )

            else:

                st.error(
                    f"Analysis failed: HTTP "
                    f"{response.status_code}"
                )

                with st.expander("Backend response"):
                    st.code(response.text)

        except requests.RequestException as exc:

            st.error(
                f"Could not reach backend: {exc}"
            )


# ============================================================
# Manual profile
# ============================================================
with manual_tab:

    name = st.text_input(
        "Name",
        "Candidate",
    )

    skills_text = st.text_input(
        "Skills",
        "Java, Spring Boot, SQL, Git, Docker",
    )

    if st.button(
        "✨ Analyze Profile",
        type="primary",
        use_container_width=True,
    ):

        skills = [
            item.strip()
            for item in skills_text.split(",")
            if item.strip()
        ]

        payload = {
            "profile": {
                "name": name,
                "location": location,
                "interests": [
                    item.strip()
                    for item in interests.split(",")
                    if item.strip()
                ],
                "skills": skills,
            },
            "free_only": free_only,
        }

        try:

            with st.spinner(
                "Analyzing your profile..."
            ):

                response = requests.post(
                    f"{API_URL}/api/analyze",
                    json=payload,
                    timeout=180,
                )

            if response.ok:

                st.session_state["result"] = response.json()

                st.success(
                    "Profile analysis completed."
                )

            else:

                st.error(
                    f"Analysis failed: HTTP "
                    f"{response.status_code}"
                )

                with st.expander("Backend response"):
                    st.code(response.text)

        except requests.RequestException as exc:

            st.error(
                f"Could not reach backend: {exc}"
            )


# ============================================================
# Results
# ============================================================
result = st.session_state.get("result")


if result:

    profile = result.get(
        "profile",
        {}
    ) or {}

    jobs = result.get(
        "jobs",
        []
    ) or []

    gaps = result.get(
        "skill_gaps",
        {}
    ) or {}

    courses = result.get(
        "courses",
        {}
    ) or {}

    skills = profile.get(
        "skills",
        []
    ) or []


    # --------------------------------------------------------
    # Career snapshot
    # --------------------------------------------------------
    st.divider()

    render_markdown(
        '<div class="section-title">Your career snapshot</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(4)

    gap_items = extract_gap_items(gaps)
    course_items = flatten_courses(courses)

    metrics = [
        (
            len(skills),
            "Detected skills",
        ),
        (
            len(jobs),
            "Matching jobs",
        ),
        (
            len(gap_items),
            "Skill gaps",
        ),
        (
            len(course_items),
            "Learning resources",
        ),
    ]

    for column, (number, label) in zip(
        columns,
        metrics,
    ):

        with column:

            render_markdown(
                f"""
                <div class="metric">
                    <div class="metric-number">
                        {safe_text(number)}
                    </div>

                    <div class="metric-label">
                        {safe_text(label)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    # --------------------------------------------------------
    # Candidate skills
    # --------------------------------------------------------
    if skills:

        render_markdown(
            '<div class="section-title">Your skills</div>',
            unsafe_allow_html=True,
        )

        show_chips(skills)


    # --------------------------------------------------------
    # Jobs
    # --------------------------------------------------------
    render_markdown(
        '<div class="section-title">Best-fit opportunities</div>',
        unsafe_allow_html=True,
    )

    render_markdown(
        """
        <div class="section-subtitle">
            Roles ranked using the skills detected from your profile.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if jobs:

        for job in jobs[:10]:

            score = max(
                0.0,
                min(
                    100.0,
                    score_value(job),
                ),
            )

            title = job.get(
                "title",
                "Untitled role",
            )

            company = job.get(
                "company",
                "Company",
            )

            job_location = job.get(
                "location",
                "Location",
            )

            required = job.get(
                "required_skills",
                [],
            ) or []

            render_markdown(
                f"""
                <div class="job">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        gap:20px;
                    ">

                        <div>
                            <div class="job-title">
                                {safe_text(title)}
                            </div>

                            <div class="job-meta">
                                🏢 {safe_text(company)}
                                &nbsp; • &nbsp;
                                📍 {safe_text(job_location)}
                            </div>
                        </div>

                        <div>
                            <div class="job-score">
                                {score:.0f}%
                            </div>

                            <div class="job-meta">
                                match
                            </div>
                        </div>

                    </div>

                    <div class="progress">
                        <div
                            class="progress-fill"
                            style="width:{score}%;"
                        ></div>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            if required:

                st.caption(
                    "Required skills: "
                    + " • ".join(
                        safe_text(skill)
                        for skill in required
                    )
                )

    else:

        st.info(
            "No matching jobs were returned."
        )


    # --------------------------------------------------------
    # Skill gaps
    # --------------------------------------------------------
    render_markdown(
        '<div class="section-title">Your opportunity gaps</div>',
        unsafe_allow_html=True,
    )

    render_markdown(
        """
        <div class="section-subtitle">
            Skills that can improve your readiness for the
            available opportunities.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if gap_items:

        gap_columns = st.columns(
            min(3, len(gap_items))
        )

        for index, gap in enumerate(
            gap_items[:12]
        ):

            with gap_columns[
                index % len(gap_columns)
            ]:

                render_markdown(
                    f"""
                    <div class="gap-card">

                        <div class="gap-title">
                            🎯 {safe_text(gap)}
                        </div>

                        <div class="gap-text">
                            Recommended skill to strengthen
                            your job match.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:

        st.success(
            "No major skill gaps were identified."
        )


    # --------------------------------------------------------
    # Learning path
    # --------------------------------------------------------
    render_markdown(
        '<div class="section-title">Your learning path</div>',
        unsafe_allow_html=True,
    )

    render_markdown(
        """
        <div class="section-subtitle">
            Focused learning resources based on the skills
            identified by the career analysis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if course_items:

        course_columns = st.columns(
            min(3, len(course_items))
        )

        for index, (category, course) in enumerate(
            course_items[:9]
        ):

            with course_columns[
                index % len(course_columns)
            ]:

                render_course(
                    category,
                    course,
                )

    else:

        st.info(
            "No learning recommendations returned."
        )


    # --------------------------------------------------------
    # AI pipeline / evidence
    # --------------------------------------------------------
    render_markdown(
        '<div class="section-title">How SkillPath AI works</div>',
        unsafe_allow_html=True,
    )

    with st.expander(
        "🔎 AI pipeline & evidence",
        expanded=False,
    ):

        render_markdown(
            """
            **Pipeline**

            Loader → Splitter → Embeddings → FAISS →
            Retriever → LangGraph → Tools
            """
        )

        sources = result.get(
            "sources",
            []
        ) or []

        trace = result.get(
            "trace",
            []
        ) or []

        if sources:

            render_markdown("**Retrieved evidence**")

            for source in sources[:10]:

                if isinstance(source, dict):

                    title = (
                        source.get("title")
                        or source.get("name")
                        or source.get("id")
                        or "Retrieved source"
                    )

                    render_markdown(
                        f"""
                        <div class="source-card">
                            {safe_text(title)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    render_markdown(
                        f"""
                        <div class="source-card">
                            {safe_text(source)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        if trace:

            render_markdown("**Agent trace**")

            for item in trace[:15]:
                st.caption(str(item))
