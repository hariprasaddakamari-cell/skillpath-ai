import os
import requests
import streamlit as st

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎯",
    layout="wide"
)

API_URL = os.getenv("SKILLPATH_API_URL", "").rstrip("/")

st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    padding: 2.2rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #172554, #4338ca, #7c3aed);
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 2.7rem;
    margin-bottom: .3rem;
}

.hero p {
    color: #e0e7ff;
    font-size: 1.05rem;
}

.card {
    background: white;
    padding: 1.2rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}

.tag {
    display: inline-block;
    padding: .35rem .7rem;
    margin: .2rem;
    background: #eef2ff;
    color: #3730a3;
    border-radius: 999px;
    font-size: .8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎯 SkillPath AI</h1>
    <p>
        AI-powered career intelligence that transforms your resume
        into personalized jobs, skill gaps, courses and career paths.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    if API_URL:
        try:
            response = requests.get(
                f"{API_URL}/api/health",
                timeout=15
            )

            if response.ok:
                health = response.json()

                st.success("Backend Online")

                st.caption(
                    f"Jobs: {health.get('jobs', 0)}"
                )

                st.caption(
                    f"Courses: {health.get('courses', 0)}"
                )

            else:
                st.error(
                    f"Backend returned {response.status_code}"
                )

        except Exception as e:
            st.error("Backend connection failed")
            st.caption(str(e))

    else:
        st.warning(
            "SKILLPATH_API_URL is not configured."
        )

    st.divider()

    location = st.text_input(
        "📍 Target Location",
        "Hyderabad"
    )

    interests = st.text_input(
        "💡 Career Interest",
        "Backend Development"
    )

    free_only = st.checkbox(
        "Only recommend free courses"
    )


# --------------------------------------------------
# CHECK API
# --------------------------------------------------

if not API_URL:

    st.error(
        "Backend URL is missing. Add SKILLPATH_API_URL "
        "in Streamlit Secrets."
    )

    st.stop()


# --------------------------------------------------
# PROFILE SECTION
# --------------------------------------------------

st.subheader("1. Build Your Career Profile")

resume_tab, manual_tab = st.tabs(
    ["📄 Resume Analysis", "✍️ Manual Profile"]
)


# --------------------------------------------------
# RESUME
# --------------------------------------------------

with resume_tab:

    resume = st.file_uploader(
        "Upload your PDF resume",
        type=["pdf"]
    )

    if st.button(
        "🚀 Analyze My Resume",
        type="primary",
        use_container_width=True,
        disabled=resume is None
    ):

        try:

            with st.spinner(
                "Reading resume and analyzing your career profile..."
            ):

                response = requests.post(

                    f"{API_URL}/api/analyze-resume",

                    files={
                        "file": (
                            resume.name,
                            resume.getvalue(),
                            "application/pdf"
                        )
                    },

                    data={
                        "location": location,
                        "interests": interests,
                        "free_only": str(
                            free_only
                        ).lower()
                    },

                    timeout=180
                )

            if response.ok:

                result = response.json()

                st.session_state["result"] = result

                st.success(
                    "Resume analyzed successfully!"
                )

            else:

                st.error(
                    f"Analysis failed: "
                    f"{response.status_code}"
                )

                st.code(response.text)

        except requests.RequestException as e:

            st.error(
                f"Could not connect to backend: {e}"
            )


# --------------------------------------------------
# MANUAL PROFILE
# --------------------------------------------------

with manual_tab:

    name = st.text_input(
        "Your Name",
        "Candidate"
    )

    skills_text = st.text_input(
        "Your Skills",
        "Java, Spring Boot, SQL, Git, Docker"
    )

    if st.button(
        "✨ Analyze Profile",
        use_container_width=True
    ):

        skills = [
            x.strip()
            for x in skills_text.split(",")
            if x.strip()
        ]

        payload = {

            "profile": {

                "name": name,

                "location": location,

                "interests": [
                    x.strip()
                    for x in interests.split(",")
                    if x.strip()
                ],

                "skills": skills
            },

            "free_only": free_only
        }

        try:

            with st.spinner(
                "Finding matching career opportunities..."
            ):

                response = requests.post(

                    f"{API_URL}/api/analyze",

                    json=payload,

                    timeout=180
                )

            if response.ok:

                result = response.json()

                st.session_state["result"] = result

                st.success(
                    "Profile analyzed successfully!"
                )

            else:

                st.error(
                    f"Analysis failed: "
                    f"{response.status_code}"
                )

                st.code(response.text)

        except requests.RequestException as e:

            st.error(
                f"Could not connect to backend: {e}"
            )


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

result = st.session_state.get("result")


if result:

    profile = result.get(
        "profile",
        {}
    )

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


    st.divider()

    st.subheader(
        "2. 🎯 Career Snapshot"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Skills Detected",
        len(skills)
    )

    c2.metric(
        "Jobs Matched",
        len(jobs)
    )

    c3.metric(
        "Skill Gaps",
        len(gaps) if isinstance(
            gaps,
            dict
        ) else 0
    )

    c4.metric(
        "Course Groups",
        len(courses) if isinstance(
            courses,
            dict
        ) else 0
    )


    if skills:

        st.markdown(
            "**Your detected skills**"
        )

        tags = ""

        for skill in skills:

            tags += (
                f'<span class="tag">'
                f'{skill}'
                f'</span>'
            )

        st.markdown(
            tags,
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # JOBS
    # --------------------------------------------------

    st.subheader(
        "3. 💼 Matching Jobs"
    )

    if jobs:

        for job in jobs[:10]:

            with st.container(
                border=True
            ):

                left, right = st.columns(
                    [4, 1]
                )

                with left:

                    st.markdown(
                        f"### {job.get('title', 'Job')}"
                    )

                    st.write(
                        f"🏢 {job.get('company', '')}"
                    )

                    st.write(
                        f"📍 {job.get('location', '')}"
                    )

                    required = job.get(
                        "required_skills",
                        []
                    )

                    if required:

                        st.caption(
                            "Required skills: "
                            + ", ".join(required)
                        )

                with right:

                    score = job.get(
                        "match_score",
                        job.get(
                            "score",
                            "—"
                        )
                    )

                    st.metric(
                        "Match",
                        f"{score}%"
                        if isinstance(
                            score,
                            (int, float)
                        )
                        else str(score)
                    )

    else:

        st.info(
            "No matching jobs were returned."
        )


    # --------------------------------------------------
    # SKILL GAPS
    # --------------------------------------------------

    st.subheader(
        "4. 🧩 Skill Gaps"
    )

    if gaps:

        if isinstance(
            gaps,
            dict
        ):

            for key, value in gaps.items():

                st.markdown(
                    f"**{key}**"
                )

                if isinstance(
                    value,
                    list
                ):

                    for item in value:

                        st.write(
                            "•",
                            item
                        )

                else:

                    st.write(
                        value
                    )

        else:

            st.write(gaps)

    else:

        st.success(
            "No major skill gaps returned."
        )


    # --------------------------------------------------
    # COURSES
    # --------------------------------------------------

    st.subheader(
        "5. 📚 Recommended Learning"
    )

    if courses:

        if isinstance(
            courses,
            dict
        ):

            for key, value in courses.items():

                st.markdown(
                    f"### {key}"
                )

                if isinstance(
                    value,
                    list
                ):

                    for item in value:

                        st.write(
                            "•",
                            item
                        )

                else:

                    st.write(value)

        else:

            st.write(courses)

    else:

        st.info(
            "No course recommendations returned."
        )


    # --------------------------------------------------
    # SIMULATION
    # --------------------------------------------------

    st.subheader(
        "6. 🔮 What If I Learn a New Skill?"
    )

    job_options = {

        j.get("title", str(j.get("id"))):
        j.get("id")

        for j in jobs

        if j.get("id") is not None
    }


    if job_options:

        selected_job = st.selectbox(
            "Choose a target job",
            list(job_options.keys())
        )

        added_skill = st.text_input(
            "Skill you want to learn",
            "SQL"
        )


        if st.button(
            "🧠 Simulate Skill Impact",
            type="primary"
        ):

            payload = {

                "profile": profile,

                "added_skill": added_skill,

                "job_id": job_options[
                    selected_job
                ]
            }

            try:

                with st.spinner(
                    "Calculating career impact..."
                ):

                    response = requests.post(

                        f"{API_URL}/api/simulate-skill",

                        json=payload,

                        timeout=60
                    )

                if response.ok:

                    simulation = response.json()

                    before = simulation.get(
                        "before",
                        {}
                    ).get(
                        "match_score",
                        "—"
                    )

                    after = simulation.get(
                        "after",
                        {}
                    ).get(
                        "match_score",
                        "—"
                    )

                    gain = simulation.get(
                        "match_gain",
                        "—"
                    )

                    a, b, c = st.columns(3)

                    a.metric(
                        "Current Match",
                        before
                    )

                    b.metric(
                        "After Learning",
                        after
                    )

                    c.metric(
                        "Match Gain",
                        gain
                    )

                    st.success(
                        f"Learning "
                        f"**{simulation.get('skill', added_skill)}** "
                        f"could unlock "
                        f"**{simulation.get('local_jobs_with_skill', 0)}** "
                        f"local job(s)."
                    )

                else:

                    st.error(
                        f"Simulation failed: "
                        f"{response.status_code}"
                    )

                    st.code(
                        response.text
                    )

            except requests.RequestException as e:

                st.error(
                    f"Could not connect to backend: {e}"
                )

    else:

        st.info(
            "Analyze your profile first to use "
            "the skill simulator."
        )
