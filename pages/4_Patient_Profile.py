import streamlit as st
import pandas as pd
from pathlib import Path

from components.patient_banner import patient_banner
from components.patient_actions import patient_actions
from components.sidebar import render_sidebar

from engine.visit_manager import latest_visit


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Patient Profile",
    page_icon="👤",
    layout="wide",
)


render_sidebar()


# ==========================================================
# Title
# ==========================================================

st.title("👤 Patient Profile")

st.markdown("---")


# ==========================================================
# Check Patient Selection
# ==========================================================

if "selected_patient" not in st.session_state:

    st.warning(
        "Please select a patient from Patient Database."
    )

    st.stop()


patient = st.session_state["selected_patient"]

patient_id = patient["Patient_ID"]


# ==========================================================
# Latest Visit
# ==========================================================

latest = latest_visit(patient_id)


patient_banner(
    patient,
    latest,
)


# ==========================================================
# Patient Storage
# ==========================================================

patient_folder = (
    Path("data")
    / "patients"
    / patient_id
)

visit_file = patient_folder / "visits.csv"


# ==========================================================
# Patient Header
# ==========================================================

st.markdown("---")

left, right = st.columns([1, 3])


with left:

    st.markdown(
        """
        <div style="
        font-size:90px;
        text-align:center;
        ">
        👤
        </div>
        """,
        unsafe_allow_html=True,
    )


with right:

    st.header(
        patient.get(
            "Full_Name",
            "Unknown Patient"
        )
    )


    st.write(
        f"**Patient ID:** {patient_id}"
    )

    st.write(
        f"**Age:** {patient.get('Age','-')}"
    )

    st.write(
        f"**Sex:** {patient.get('Sex','-')}"
    )

    st.write(
        f"**Blood Group:** {patient.get('Blood_Group','-')}"
    )

    st.write(
        f"**Physician:** {patient.get('Physician','-')}"
    )


# ==========================================================
# Load Visits
# ==========================================================

if visit_file.exists():

    visits = pd.read_csv(
        visit_file
    )

else:

    visits = pd.DataFrame()


total_visits = len(visits)


# ==========================================================
# Clinical Summary
# ==========================================================

st.markdown("---")

st.subheader(
    "📋 Clinical Summary"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Age",
        patient.get(
            "Age",
            "-"
        ),
    )


with c2:

    st.metric(
        "Height",
        patient.get(
            "Height",
            "-"
        ),
    )


with c3:

    st.metric(
        "Hospital",
        patient.get(
            "Hospital",
            "-"
        ),
    )


with c4:

    st.metric(
        "Total Visits",
        total_visits,
    )


# ==========================================================
# Quick Actions
# ==========================================================

st.markdown("---")

patient_actions()


# ==========================================================
# Visit History
# ==========================================================

st.markdown("---")

st.subheader(
    "📅 Recent Clinical Visits"
)


if visits.empty:

    st.info(
        "No clinical visits available."
    )

else:

    if "Visit_Date" in visits.columns:

        visits = visits.sort_values(
            "Visit_Date",
            ascending=False,
        )


    st.dataframe(
        visits,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# Patient Data
# ==========================================================

st.markdown("---")

with st.expander(
    "🔍 View Complete Patient Record"
):

    st.json(
        patient
    )