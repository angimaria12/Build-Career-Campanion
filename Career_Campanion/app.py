from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API Key (Streamlit Cloud or Local .env)
try:
    api_key = st.secrets.get("GROQ_API_KEY")
except (FileNotFoundError, KeyError):
    api_key = None

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

    # Initialize Career Chatbot

chatbot = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.4,
    api_key=api_key
)


# Check API Key
if not api_key:
    st.error("Please configure your GROQ API key.")
    st.stop()

# Set API Key
os.environ["GROQ_API_KEY"] = api_key

from utils.resume_parser import extract_resume_text
from utils.career_analyzer import analyze_resume


st.set_page_config(
    page_title="Career Companion",
    page_icon="🎯",
    layout="wide"
)

# Store chatbot conversation

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "career_context" not in st.session_state:
    st.session_state.career_context = None

if "career_report" not in st.session_state:
    st.session_state.career_report = None



# Application heading

from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Load CSS
css_path = ASSETS_DIR / "style.css"

with open(css_path, "r", encoding="utf-8") as file:
    css = file.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

# Load HTML
html_path = ASSETS_DIR / "hero.html"

with open(html_path, "r", encoding="utf-8") as file:
    hero_html = file.read()

st.html(hero_html)

st.divider()


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

                # Store career report for follow-up chatbot

            st.session_state.career_report = report

            st.session_state.career_context = report.model_dump_json(
            indent=2
              )

            st.session_state.chat_history = []

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

            # =====================================
            # LEARNING ROADMAP WITH OFFICIAL LINKS
            # =====================================

            st.divider()

            st.header("📚 Your Personalized Learning Roadmap")

            st.write(
                "Follow these recommended learning steps, "
                "explore the official resources and track "
                "your progress as you learn!"
            )

            # Official learning resources

            learning_resources = {
                "aws": [
                    (
                        "☁️ AWS Cloud Practitioner - Official Training",
                        "https://aws.amazon.com/training/digital/"
                    ),
                    (
                        "📘 AWS Cloud Practitioner Study Guide",
                        "https://d1.awsstatic.com/training-and-certification/ramp-up_guides/Ramp-Up_Guide_CloudPractitioner.pdf"
                    )
                ],

                "azure": [
                    (
                        "☁️ Azure Fundamentals - Microsoft Learn",
                        "https://learn.microsoft.com/en-us/training/azure/"
                    ),
                    (
                        "🎓 Azure Training and Certifications",
                        "https://azure.microsoft.com/en-in/resources/training-and-certifications/"
                    )
                ],

                "tensorflow": [
                    (
                        "🧠 TensorFlow Official Tutorials",
                        "https://www.tensorflow.org/tutorials"
                    )
                ],

                "pytorch": [
                    (
                        "🔥 PyTorch Official Tutorials",
                        "https://pytorch.org/tutorials/"
                    )
                ],

                "sql": [
                    (
                        "💻 MySQL Official Tutorial",
                        "https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/"
                    ),
                    (
                        "📘 PostgreSQL Official Tutorial",
                        "https://www.postgresql.org/docs/current/tutorial.html"
                    )
                ],

                "power bi": [
                    (
                        "📊 Power BI - Microsoft Learn",
                        "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"
                    )
                ],

                "docker": [
                    (
                        "🐳 Docker Official Getting Started Guide",
                        "https://docs.docker.com/get-started/"
                    )
                ],

                "mlflow": [
                    (
                        "🤖 MLflow Official Documentation",
                        "https://mlflow.org/docs/latest/"
                    )
                ],

                "github actions": [
                    (
                        "🐙 GitHub Actions Documentation",
                        "https://docs.github.com/en/actions"
                    )
                ],

                "kaggle": [
                    (
                        "🏆 Kaggle Learn",
                        "https://www.kaggle.com/learn"
                    )
                ],

                "flask": [
                    (
                        "🌐 Flask Official Quickstart",
                        "https://flask.palletsprojects.com/en/stable/quickstart/"
                    )
                ]
            }

            # Match roadmap topics with learning links

            def get_learning_links(roadmap_item):

                item_lower = roadmap_item.lower()

                matched_links = []

                for keyword, links in learning_resources.items():

                    if keyword in item_lower:

                        matched_links.extend(links)

                # Include general cloud resources
                if "cloud" in item_lower:

                    for keyword in ["aws", "azure"]:

                        for link in learning_resources[keyword]:

                            if link not in matched_links:
                                matched_links.append(link)

                return matched_links

            # Display roadmap and follow-up checklist

            total_tasks = len(report.learning_roadmap)

            for index, item in enumerate(
                report.learning_roadmap, 1
            ):

                with st.expander(
                    f"📌 Step {index}: {item}",
                    expanded=True
                ):

                    st.checkbox(
                        "Mark this learning task as completed ✅",
                        key=f"roadmap_task_{index}"
                    )

                    st.write("📖 Recommended Learning Resources:")

                    links = get_learning_links(item)

                    if links:

                        for title, url in links:

                            st.markdown(
                                f"🔗 [{title}]({url})"
                            )

                    else:

                        st.info(
                            "Explore the official documentation "
                            "for the technologies mentioned in this step."
                        )

            # Learning progress tracker

            st.divider()

            st.subheader("🎯 Your Learning Progress")

            completed_tasks = sum(
                st.session_state.get(
                    f"roadmap_task_{index}", False
                )
                for index in range(1, total_tasks + 1)
            )

            if total_tasks > 0:

                progress_percentage = (
                    completed_tasks / total_tasks
                )

                st.progress(progress_percentage)

                st.write(
                    f"✅ Completed: {completed_tasks} / {total_tasks} tasks"
                )

                st.write(
                    f"📊 Overall Progress: "
                    f"{progress_percentage * 100:.0f}%"
                )

                if completed_tasks == total_tasks:

                    st.success(
                        "🎉 Congratulations! You have completed "
                        "your entire learning roadmap!"
                    )

                elif completed_tasks > 0:

                    st.info(
                        "🚀 Great progress! Keep learning "
                        "and complete your remaining tasks."
                    )

                else:

                    st.info(
                        "🌱 Your learning journey starts here. "
                        "Complete your first task!"
                    )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:

    st.info("Please upload your resume to get started.")

st.divider()

st.caption(
    "Career Companion | AI-based career guidance. "
    "Recommendations are suggestions, not hiring guarantees."
)



# =====================================
# AI CAREER FOLLOW-UP CHATBOT
# =====================================

st.divider()

st.header("🤖 Career AI Assistant")

st.write(
    "Have questions about your career? "
    "Ask me anything related to your resume, "
    "skills, job opportunities or learning path!"
)

if st.session_state.career_report is not None:

    # Prepare a compact version of resume information

    report = st.session_state.career_report

    career_context = f"""
    Candidate Summary:
    {report.candidate_summary[:700]}

    Education:
    {', '.join(report.education[:4])}

    Technical Skills:
    {', '.join(report.technical_skills[:12])}

    Soft Skills:
    {', '.join(report.soft_skills[:10])}

    Experience and Projects:
    {'; '.join(report.experience_and_projects[:4])}

    Suitable Jobs:
    {'; '.join([job.role + ' (Match: ' + str(job.match_score) + '%)' for job in report.suitable_jobs[:5]])}

    Improvement Suggestions:
    {'; '.join(report.improvement_suggestions[:5])}

    Learning Roadmap:
    {'; '.join(report.learning_roadmap[:5])}
    """

    # Display previous conversation

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input

    user_question = st.chat_input(
        "Ask your career-related question here..."
    )

    if user_question:

        # Display user question

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        # Prepare AI response

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    messages = [
                        SystemMessage(
                            content=f"""
                            You are Career Companion, a friendly
                            and intelligent AI career advisor.

                            Candidate Resume Information:
                            {career_context}

                            Instructions:

                            1. Give short, simple and clear answers.
                            2. Personalize answers using the resume.
                            3. Give practical career advice.
                            4. Recommend useful learning resources
                               with official links whenever relevant.
                            5. Help with job preparation,
                               interviews and skill development.
                            6. Understand follow-up questions
                               using recent conversation history.
                            7. Never invent candidate qualifications.
                            8. For unrelated questions, politely
                               guide the user towards career topics.

                            Response Guidelines:
                            - Keep answers concise and useful.
                            - Prefer bullet points where appropriate.
                            - Avoid unnecessary explanations.
                            - Give examples when helpful.
                            - Normally keep answers within 150 words.
                            """
                        )
                    ]

                    # Include only the latest 6 previous messages

                    recent_history = st.session_state.chat_history[:-1][-6:]

                    for message in recent_history:

                        content = message["content"][:700]

                        if message["role"] == "user":
                            messages.append(
                                HumanMessage(content=content)
                            )

                        else:
                            messages.append(
                                AIMessage(content=content)
                            )

                    # Add current question

                    messages.append(
                        HumanMessage(
                            content=user_question[:1500]
                        )
                    )

                    # Generate a shorter response

                    response = chatbot.bind(
                        max_tokens=700
                    ).invoke(messages)

                    answer = response.content

                    st.markdown(answer)

                    # Save chatbot response

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(
                        f"Chatbot error: {e}"
                    )

else:

    st.info(
        "📄 Please upload and analyse your resume "
        "to start chatting with your Career AI Assistant."
    )
