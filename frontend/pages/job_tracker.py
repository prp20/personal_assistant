import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

API_URL = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("📋 Job Application Tracker")
st.caption("Track your job applications with status, links, and notes.")


def fetch_jobs():
    response = requests.get(f"{API_URL}/jobs")
    data = response.json()
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(columns=["id", "Company", "Role", "Location", "Status", "Application URL", "Notes"])


def save_job(data, job_id=None):
    payload = {}
    for k, v in data.items():
        if pd.isna(v):
            payload[k] = ""
        elif isinstance(v, (pd.Timestamp, pd.Timedelta)):
            payload[k] = str(v)
        elif isinstance(v, (float, int, str)):
            payload[k] = v
        else:
            payload[k] = str(v)

    if job_id is not None:
        payload["id"] = int(job_id)

    requests.post(f"{API_URL}/jobs", json=payload)


def delete_job(job_id):
    requests.delete(f"{API_URL}/jobs/{job_id}")


# -------------------------
# Fetch Data
df = fetch_jobs()

# -------------------------
# Editable Grid
if not df.empty:
    gb = GridOptionsBuilder.from_dataframe(df.drop(columns=["id"]))
    gb.configure_default_column(editable=True)
    gb.configure_selection('single')
    grid_options = gb.build()

    st.write("### 📝 Edit Applications Inline")
    grid_response = AgGrid(
        df.drop(columns=["id"]),
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MANUAL,
        fit_columns_on_grid_load=True,
        height=400,
        theme="streamlit"
    )

    updated_df = pd.DataFrame(grid_response["data"])

    if st.button("💾 Save All Changes"):
        for idx, row in updated_df.iterrows():
            job_id = df.iloc[idx]["id"]
            save_job(row.to_dict(), job_id=job_id)
        st.success("All changes saved to backend.")
        st.rerun()
else:
    st.info("No jobs tracked yet. Add your first one below!")

# -------------------------
# Add New Entry Form
with st.expander("➕ Add New Job Application"):
    with st.form("job_form"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        location = st.text_input("Location")
        status = st.selectbox(
            "Status", ["Applied", "Interviewing", "Rejected", "Offer", "Follow-Up"])
        application_url = st.text_input("Application URL (Optional)")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Job")
        if submitted:
            new_entry = {
                "Company": company,
                "Role": role,
                "Location": location,
                "Status": status,
                "Application URL": application_url,
                "Notes": notes
            }
            save_job(new_entry)
            st.success(f"Added {company} - {role} to your tracker.")
            st.rerun()

# -------------------------
# CSV Download
if not df.empty:
    csv = df.drop(columns=["id"]).to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv,
                       "job_applications.csv", "text/csv")
