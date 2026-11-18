import streamlit as st
import os

# Get Google API Key
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
except FileNotFoundError:
    api_key = None

# Check API Key
if not api_key:
    st.error("Please configure your GOOGLE API key.")
    st.stop()

# Set API Key
os.environ["GOOGLE_API_KEY"] = api_key

import streamlit as st
import os

from dotenv import load_dotenv

from utils.resume_parser import extract_resume_text

from utils.career_analyzer import analyze_resume


# Load environment variables

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Please configure your GOOGLE API key in the .env file.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

st.set_page_config(
    page_title="Career Companion",
    page_icon="🎯",
    layout="wide"
)


# Application heading

st.title("🎯 Career Companion")
st.subheader("Your AI-Powered Career Advisor.")

st.write(
    "Upload your resume and discover job opportunities "
    "that match your skills, education and experience."
)

st.divider()


# API key check



# Resume upload

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)


if uploaded_file:

    st.success("Resume uploaded successfully!")

    if st.button("Analyze My Resume", type="primary"):

        try:
            with st.spinner(
                "AI is analyzing your resume..."
            ):

                resume_text = extract_resume_text(
                    uploaded_file
                )

                report = analyze_resume(resume_text)

            st.success("Resume analysis completed!")

            # Candidate summary

            st.header("👤 Candidate Profile")

            st.write(report.candidate_summary)

            # Education

            st.header("🎓 Education")

            for item in report.education:
                st.write("•", item)

            # Technical skills

            st.header("💻 Technical Skills")

            st.write(
                ", ".join(report.technical_skills)
            )

            # Soft skills

            st.header("🤝 Soft Skills")

            st.write(
                ", ".join(report.soft_skills)
            )

            # Projects and experience

            st.header("📂 Experience and Projects")

            for item in report.experience_and_projects:
                st.write("•", item)

            # Job recommendations

            st.divider()

            st.header("💼 Recommended Job Roles")

            for job in report.suitable_jobs:

                with st.expander(
                    f"{job.role} - {job.match_score}% Match"
                ):

                    st.progress(
                        min(max(job.match_score, 0), 100) / 100
                    )

                    st.write("**Why this role suits you:**")
                    st.write(job.reason)

                    st.write("**Required skills:**")
                    st.write(", ".join(job.required_skills))

                    st.write("**Skills to improve:**")
                    st.write(", ".join(job.missing_skills))

            # Improvement suggestions

            st.divider()

            st.header("🚀 Career Improvement Suggestions")

            for item in report.improvement_suggestions:
                st.write("•", item)

            # Learning roadmap

            st.header("📚 Learning Roadmap")

            for index, item in enumerate(
                report.learning_roadmap, 1
            ):
                st.write(f"{index}. {item}")

            st.balloons()

        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:

    st.info("Please upload your resume to get started.")

st.divider()

st.caption(
    "Career Companion | AI-based career guidance. "
    "Recommendations are suggestions, not hiring guarantees."
)
