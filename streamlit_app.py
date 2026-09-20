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
CSS = """
<style>
.stApp { background: #f6f7fb; }
.block-container { max-width: 1150px; padding-top: 2rem; padding-bottom: 4rem; }
.hero { padding: 42px; border-radius: 26px; color: white;
        background: linear-gradient(135deg, #111827, #3730a3, #6d28d9);
        margin-bottom: 24px; box-shadow: 0 18px 45px rgba(49,46,129,.20); }
.hero-label { color: #c7d2fe; font-size: 13px; font-weight: 800;
              letter-spacing: 2px; text-transform: uppercase; }
.hero-title { font-size: 46px; line-height: 1.05; font-weight: 800; margin: 10px 0; }
.hero-text { max-width: 720px; color: #e0e7ff; font-size: 17px; line-height: 1.6; }
.section-title { font-size: 25px; font-weight: 800; color: #111827; margin: 25px 0 12px; }
.metric { background: white; border: 1px solid #e5e7eb; border-radius: 18px;
          padding: 20px; box-shadow: 0 7px 22px rgba(15,23,42,.05); }
.metric-number { color: #4338ca; font-size: 31px; font-weight: 800; }
.metric-label { color: #64748b; font-size: 13px; margin-top: 4px; }
.job { background: white; border: 1px solid #e5e7eb; border-radius: 18px;
       padding: 20px; margin-bottom: 12px; box-shadow: 0 6px 20px rgba(15,23,42,.04); }
.job-title { font-size: 18px; font-weight: 800; color: #111827; }
.job-meta { color: #64748b; font-size: 13px; margin-top: 4px; }
.job-score { color: #4f46e5; font-size: 25px; font-weight: 800; text-align: right; }
.progress { height: 8px; background: #e5e7eb; border-radius: 20px; overflow: hidden; margin-top: 14px; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#4f46e5,#7c3aed); }
.chip { display: inline-block; background: #eef2ff; color: #3730a3;
        border: 1px solid #c7d2fe; border-radius: 999px; padding: 6px 11px;
        margin: 3px; font-size: 12px; font-weight: 700; }
.gap-chip { display: inline-block; background: #fff7ed; color: #c2410c;
            border: 1px solid #fed7aa; border-radius: 999px; padding: 6px 11px;
            margin: 3px; font-size: 12px; font-weight: 700; }
.simulator { background: linear-gradient(135deg,#eef2ff,#faf5ff);
             border: 1px solid #ddd6fe; border-radius: 22px; padding: 24px; margin-top: 8px; }
.sim-title { color: #312e81; font-size: 23px; font-weight: 800; }
.course { background: white; border: 1px solid #e5e7eb; border-radius: 17px;
          padding: 18px; min-height: 120px; box-shadow: 0 6px 18px rgba(15,23,42,.04); }
.course-category { color: #6366f1; font-size: 11px; font-weight: 800; text-transform: uppercase; }
.course-name { color: #111827; font-weight: 800; margin-top: 7px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- Helpers --------------------
def score_value(job):
    try:
        return float(job.get("match_score", job.get("score", 0)))
    except (TypeError, ValueError):
        return 0.0


def show_chips(items, gap=False):
    if not items:
        return

    class_name = "gap-chip" if gap else "chip"
    html = "".join(
        f'<span class="{class_name}">{item}</span>'
        for item in items
    )
    st.markdown(html, unsafe_allow_html=True)


def flatten_courses(courses):
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


# -------------------- Hero --------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">AI Career Intelligence</div>
        <div class="hero-title">
            Turn your skills into<br>your next career move.
        </div>
        <div class="hero-text">
            SkillPath AI analyzes your resume, finds relevant jobs,
            identifies skill gaps, recommends learning paths, and
            simulates how a new skill can improve your opportunities.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("⚙️ Settings")

    configured_url = st.text_input(
        "Backend URL",
        value=API_URL,
        placeholder="https://your-app.onrender.com",
    )

    if configured_url:
        API_URL = configured_url.rstrip("/")

    location = st.text_input("Target location", "Hyderabad")
    interests = st.text_input(
        "Career interest",
        "Backend Development",
    )
    free_only = st.checkbox("Only show free courses")

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
                st.error(f"Backend returned {response.status_code}")

        except requests.RequestException:
            st.warning("Backend connection unavailable")


if not API_URL:
    st.info(
        "Set SKILLPATH_API_URL in Streamlit Secrets, "
        "or enter your Render backend URL in the sidebar."
    )
    st.stop()


# -------------------- Input --------------------
st.markdown(
    '<div class="section-title">Build your career profile</div>',
    unsafe_allow_html=True,
)

resume_tab, manual_tab = st.tabs(
    ["📄 Resume Analysis", "✍️ Manual Profile"]
)

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
                        "free_only": str(free_only).lower(),
                    },
                    timeout=180,
                )

            if response.ok:
                st.session_state["result"] = response.json()
                st.success("Career analysis completed.")
            else:
                st.error(
                    f"Analysis failed: HTTP {response.status_code}"
                )
                st.code(response.text)

        except requests.RequestException as exc:
            st.error(f"Could not reach backend: {exc}")


with manual_tab:
    name = st.text_input("Name", "Candidate")
    skills_text = st.text_input(
        "Skills",
        "Java, Spring Boot, SQL, Git, Docker",
    )

    if st.button(
        "✨ Analyze Profile",
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
            with st.spinner("Analyzing your profile..."):
                response = requests.post(
                    f"{API_URL}/api/analyze",
                    json=payload,
                    timeout=180,
                )

            if response.ok:
                st.session_state["result"] = response.json()
                st.success("Profile analysis completed.")
            else:
                st.error(
                    f"Analysis failed: HTTP {response.status_code}"
                )
                st.code(response.text)

        except requests.RequestException as exc:
            st.error(f"Could not reach backend: {exc}")


# -------------------- Results --------------------
result = st.session_state.get("result")

if result:
    profile = result.get("profile", {}) or {}
    jobs = result.get("jobs", []) or []
    gaps = result.get("skill_gaps", {}) or {}
    courses = result.get("courses", {}) or {}
    skills = profile.get("skills", []) or []

    st.divider()

    st.markdown(
        '<div class="section-title">Your career snapshot</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(4)

    metrics = [
        (len(skills), "Detected skills"),
        (len(jobs), "Matching jobs"),
        (
            len(gaps) if isinstance(gaps, dict) else 0,
            "Skill-gap areas",
        ),
        (
            len(courses) if isinstance(courses, dict) else 0,
            "Learning groups",
        ),
    ]

    for column, (number, label) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if skills:
        st.markdown(
            '<div class="section-title">Your skills</div>',
            unsafe_allow_html=True,
        )
        show_chips(skills)

    # -------------------- Jobs --------------------
    st.markdown(
        '<div class="section-title">Best-fit opportunities</div>',
        unsafe_allow_html=True,
    )

    if jobs:
        for job in jobs[:10]:
            score = max(0.0, min(100.0, score_value(job)))

            title = job.get("title", "Untitled role")
            company = job.get("company", "Company")
            job_location = job.get("location", "Location")
            required = job.get("required_skills", []) or []

            st.markdown(
                f"""
                <div class="job">
                    <div style="display:flex;justify-content:space-between;">
                        <div>
                            <div class="job-title">{title}</div>
                            <div class="job-meta">
                                🏢 {company} &nbsp; • &nbsp;
                                📍 {job_location}
                            </div>
                        </div>
                        <div>
                            <div class="job-score">{score:.0f}%</div>
                            <div class="job-meta">match</div>
                        </div>
                    </div>

                    <div class="progress">
                        <div class="progress-fill"
                             style="width:{score}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if required:
                st.caption(
                    "Required skills: "
                    + " • ".join(map(str, required))
                )
    else:
        st.info("No matching jobs were returned.")

    # -------------------- Skill gaps --------------------
    st.markdown(
        '<div class="section-title">Skills to strengthen</div>',
        unsafe_allow_html=True,
    )

    if isinstance(gaps, dict):
        gap_items = []

        for value in gaps.values():
            if isinstance(value, list):
                gap_items.extend(value)
            else:
                gap_items.append(value)

        if gap_items:
            show_chips(gap_items, gap=True)
        else:
            st.success("No major skill gaps returned.")
    elif gaps:
        st.write(gaps)
    else:
        st.success("No major skill gaps returned.")

    # -------------------- Courses --------------------
    st.markdown(
        '<div class="section-title">Recommended learning path</div>',
        unsafe_allow_html=True,
    )

    course_items = flatten_courses(courses)

    if course_items:
        columns = st.columns(min(3, len(course_items)))

        for index, (category, course) in enumerate(course_items[:9]):
            with columns[index % len(columns)]:
                st.markdown(
                    f"""
                    <div class="course">
                        <div class="course-category">{category}</div>
                        <div class="course-name">{course}</div>
                        <div class="job-meta">
                            Build this skill for stronger job matches.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No course recommendations returned.")

    # -------------------- Simulator --------------------
    st.markdown(
        '<div class="section-title">Career simulator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="simulator">
            <div class="sim-title">
                🔮 What if you learn one more skill?
            </div>
            <p>
                Test how adding a skill changes your match for a target job.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_options = {}

    for job in jobs:
        job_id = job.get("id")
        title = job.get("title")

        if job_id is not None:
            job_options[title or str(job_id)] = job_id

    if job_options:
        left, right = st.columns([1.4, 1])

        with left:
            selected_title = st.selectbox(
                "Target role",
                list(job_options.keys()),
            )

        with right:
            added_skill = st.text_input(
                "Skill to learn",
                "SQL",
            )

        if st.button(
            "🧠 Simulate Impact",
            type="primary",
            use_container_width=True,
        ):
            payload = {
                "profile": profile,
                "added_skill": added_skill,
                "job_id": job_options[selected_title],
            }

            try:
                with st.spinner(
                    "Calculating skill impact..."
                ):
                    response = requests.post(
                        f"{API_URL}/api/simulate-skill",
                        json=payload,
                        timeout=60,
                    )

                if response.ok:
                    simulation = response.json()

                    before = simulation.get(
                        "before", {}
                    ).get("match_score", "—")

                    after = simulation.get(
                        "after", {}
                    ).get("match_score", "—")

                    gain = simulation.get(
                        "match_gain", "—"
                    )

                    a, b, c = st.columns(3)

                    a.metric("Current match", before)
                    b.metric("After learning", after)
                    c.metric("Match gain", gain)

                    st.success(
                        f"Learning {simulation.get('skill', added_skill)} "
                        f"could unlock "
                        f"{simulation.get('local_jobs_with_skill', 0)} "
                        f"local job(s) requiring that skill."
                    )
                else:
                    st.error(
                        f"Simulation failed: HTTP {response.status_code}"
                    )
                    st.code(response.text)

            except requests.RequestException as exc:
                st.error(f"Could not reach backend: {exc}")
    else:
        st.info(
            "Analyze a profile with matching jobs first "
            "to use the simulator."
        )

    # -------------------- Technical proof --------------------
    with st.expander("🔎 AI pipeline & evidence"):
        st.write(
            "Loader → Splitter → Embeddings → FAISS → "
            "Retriever → LangGraph → Tools"
        )

        sources = result.get("sources", [])
        trace = result.get("trace", [])

        if sources:
            st.write("Retrieved sources:", sources)

        if trace:
            st.write("Agent trace:", trace)
