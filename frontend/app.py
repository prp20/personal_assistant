import streamlit as st
import requests
from components.file_upload import load_resume_text, load_job_description_text
from components.score_display import display_scores
from components.suggestion_display import display_suggestions

API_URL = "http://localhost:5000/api"


def get_scores(resume_text, jd_text):
    response = requests.post(
        f"{API_URL}/score", json={"resume_text": resume_text, "jd_text": jd_text})
    return response.json()


def get_suggestions(resume_text, jd_text):
    response = requests.post(
        f"{API_URL}/suggestions", json={"resume_text": resume_text, "jd_text": jd_text})
    return response.json()["suggestions"]


st.title("📄 ATS Resume Tracker")
resume_text = load_resume_text()
jd_text, keywords = load_job_description_text()

if st.button("Analyze"):
    if resume_text and jd_text:
        scores = get_scores(resume_text, jd_text)
        suggestions = get_suggestions(resume_text, jd_text)

        display_scores(scores)
        display_suggestions(suggestions)
    else:
        st.warning("Please provide both Resume and Job Description")
