import streamlit as st
import pandas as pd
import plotly.express as px


def display_scores(scores):
    k_score = int(scores['keyword_score'][0])
    s_score = int(scores['structure_score'][0])
    r_score = int(scores['readability_score'])
    readability_metric = int(scores['readability_metric'])
    f_score = int(scores['formatting_score'][0])

    total = k_score + s_score + r_score + f_score
    components = {
        "Keywords": k_score,
        "Structure": s_score,
        "Readability": r_score,
        "Formatting": f_score
    }

    st.markdown("## 📊 ATS Score Breakdown")
    st.progress(total / 100)

    for section, score in components.items():
        st.write(f"{section}: {score}/100")
        st.progress(score / 40)

    pie_df = pd.DataFrame.from_dict(components, orient='index').reset_index()
    pie_df.columns = ["Component", "Score"]
    fig = px.pie(pie_df, values="Score", names="Component",
                 title="ATS Score Breakdown")
    st.plotly_chart(fig)
