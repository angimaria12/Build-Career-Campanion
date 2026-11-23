
import re


def is_resume(text):

    if not text or len(text.strip()) < 100:
        return False

    text = text.lower()

    # Common sections found in resumes
    resume_sections = [
        "education",
        "experience",
        "work experience",
        "professional experience",
        "skills",
        "technical skills",
        "projects",
        "certifications",
        "career objective",
        "professional summary",
        "internship",
        "employment history"
    ]

    # Common personal and professional details
    resume_details = [
        "email",
        "phone",
        "linkedin",
        "github",
        "qualification",
        "bachelor",
        "master",
        "university",
        "college",
        "programming",
        "developer"
    ]

    section_count = sum(
        1 for word in resume_sections if word in text
    )

    detail_count = sum(
        1 for word in resume_details if word in text
    )

    # Check for email address
    has_email = bool(
        re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    )

    # A resume should contain multiple relevant indicators
    if section_count >= 2 and detail_count >= 2:
        return True

    if section_count >= 3 and has_email:
        return True

    return False
