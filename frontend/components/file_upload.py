import streamlit as st
from .pdf_parser import parse_pdf


def load_resume_text():
    resume_file = st.file_uploader("Upload Resume (.pdf)", type=["pdf"])
    if resume_file:
        # Extract text from PDF (frontend responsibility)
        resume_text = parse_pdf(resume_file)
        return resume_text
    return None


def load_job_description_text():
    jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
    if jd_file:
        jd_text = jd_file.read().decode("utf-8")
        # Extract top 20 words for demo
        keywords = jd_text.lower().split()[:20]
        return jd_text, keywords
    return None, None
