import streamlit as st


def display_suggestions(suggestions: str):
    st.title("📑 ATS Suggestions & Feedback")
    with st.expander("", expanded=True):
        st.markdown(suggestions, unsafe_allow_html=False)
