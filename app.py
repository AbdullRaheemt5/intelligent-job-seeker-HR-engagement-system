# app.py

import streamlit as st
from ai_engine import analyze_jobseeker
from chat_ai import generate_chat_response
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Intelligent Jobseeker Engagement Platform",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_history_jobseeker" not in st.session_state:
    st.session_state.chat_history_jobseeker = []

if "chat_history_recruiter" not in st.session_state:
    st.session_state.chat_history_recruiter = []

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "Jobseeker Assistant"

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🤖 Intelligent Jobseeker Engagement Platform</h1>
    <p style='text-align:center;'>AI-powered resume analysis, job matching & interview readiness</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- LAYOUT ----------------
left_col, main_col, right_col = st.columns([1.2, 3, 1.5])

# ======================================================
# 📄 LEFT COLUMN — RESUME INPUT
# ======================================================
with left_col:
    st.header("📄 Resume Input")

    resume_text = ""
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""
        st.success("Resume uploaded successfully")
    else:
        resume_text = st.text_area("Or paste resume text", height=220)

    last_active_days = st.number_input(
        "Days Since Last Activity", 0, 365, 10
    )

    analyze = st.button("🚀 Analyze Profile", use_container_width=True)

# ---------------- JOB DATABASE ----------------
job_database = [
    {"job_title": "Frontend Developer", "required_skills": ["HTML", "CSS", "JavaScript", "React"]},
    {"job_title": "UI Developer", "required_skills": ["HTML", "CSS", "JavaScript"]},
    {"job_title": "Web Developer", "required_skills": ["HTML", "CSS", "JavaScript", "Node"]},
]

# ======================================================
# 🧠 ANALYSIS EXECUTION
# ======================================================
if analyze:
    if not resume_text.strip():
        st.warning("Please upload or paste your resume.")
    else:
        st.session_state.analysis_result = analyze_jobseeker(
            resume_text=resume_text,
            job_database=job_database,
            last_active_days=last_active_days
        )

# ======================================================
# 📊 MAIN COLUMN — ANALYSIS (ALWAYS VISIBLE)
# ======================================================
with main_col:
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.caption("💡 AI chat responses are based on this analysis")

        if result.get("engagement_message"):
            st.warning(f"🔔 {result['engagement_message']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Resume Score", result["resume_analysis"]["resume_strength_score"])
        col2.metric("Skills Found", len(result["resume_analysis"]["top_skills"]))
        col3.metric(
            "Top Job Match",
            f"{result['job_recommendations'][0]['match_percentage']}%"
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📄 Resume Analysis", "💼 Job Matches", "🧠 Skill Gap", "🎤 Interview Prep"]
        )

        with tab1:
            st.subheader("Extracted Skills")
            st.write(", ".join(result["resume_analysis"]["top_skills"]))

            st.subheader("Improvement Suggestions")
            for tip in result["resume_analysis"]["improvement_suggestions"]:
                st.write(f"• {tip}")

        with tab2:
            for job in result["job_recommendations"]:
                st.markdown(f"### {job['job_title']}")
                st.progress(job["match_percentage"] / 100)
                st.write(f"Match: {job['match_percentage']}%")
                st.write("Missing Skills:", ", ".join(job["missing_skills"]))
                st.divider()

        with tab3:
            st.subheader("Skill Gap Analysis")
            st.write("Target Role:", result["skill_gap_analysis"]["target_role_used"])

            gap = result["skill_gap_analysis"]["skill_gap_percentage"]
            st.progress(1 - gap / 100)

            st.write(
                "Missing Skills:",
                ", ".join(result["skill_gap_analysis"]["missing_skills"])
            )

            st.subheader("Learning Roadmap")
            for step in result["skill_gap_analysis"]["suggested_learning_roadmap"]:
                st.write(f"• {step}")

        with tab4:
            st.subheader("Technical Questions")
            for q in result["interview_prep"]["technical_questions"]:
                st.write(f"• {q}")

            st.subheader("Behavioral Questions")
            for q in result["interview_prep"]["behavioral_questions"]:
                st.write(f"• {q}")

    else:
        st.info("⬅ Upload and analyze a resume to see insights here.")

# ======================================================
# 💬 RIGHT COLUMN — AI CHATBOT
# ======================================================
with right_col:
    st.header("💬 AI Career Assistant")

    mode = st.selectbox(
        "Mode",
        ["Jobseeker Assistant", "Recruiter / HR Assistant"],
        index=0 if st.session_state.chat_mode == "Jobseeker Assistant" else 1
    )

    st.session_state.chat_mode = mode

    chat_history = (
        st.session_state.chat_history_jobseeker
        if mode == "Jobseeker Assistant"
        else st.session_state.chat_history_recruiter
    )

    chat_box = st.container(height=420)

    with chat_box:
        for role, message in chat_history:
            if role == "user":
                st.markdown(f"👤 **You:** {message}")
            else:
                st.markdown(f"🤖 **AI:** {message}")

    user_input = st.text_input("Ask something...", key="chat_input")

    if st.button("Send", use_container_width=True):
        if st.session_state.analysis_result is None:
            st.error("Analyze the resume first.")
        elif user_input.strip():

            reply = generate_chat_response(
                user_message=user_input,
                resume_data=st.session_state.analysis_result,
                mode="jobseeker" if mode == "Jobseeker Assistant" else "recruiter",
                chat_history=chat_history
            )

            chat_history.append(("user", user_input))
            chat_history.append(("assistant", reply))