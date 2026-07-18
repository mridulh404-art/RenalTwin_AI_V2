import streamlit as st
import pandas as pd
from pathlib import Path
from components.sidebar import render_sidebar
from engine.patient_registry import (
    load_patients,
)

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Patient Database",
    page_icon="🗂",
    layout="wide",
)
render_sidebar()
st.title("🗂 Patient Database")

st.markdown("---")

# ==========================================================
# Load Patients
# ==========================================================

patients = load_patients()

if patients.empty:

    st.warning("No patients registered.")

    st.stop()

# ==========================================================
# Search
# ==========================================================

st.subheader("🔍 Search Patient")

c1, c2 = st.columns(2)

with c1:

    search_name = st.text_input(
        "Patient Name"
    )

with c2:

    search_id = st.text_input(
        "Patient ID"
    )

filtered = patients.copy()

if search_name:

    filtered = filtered[
        filtered["Full_Name"]
        .str.contains(
            search_name,
            case=False,
            na=False,
        )
    ]

if search_id:

    filtered = filtered[
        filtered["Patient_ID"]
        .str.contains(
            search_id,
            case=False,
            na=False,
        )
    ]

st.markdown("---")

# ==========================================================
# Statistics
# ==========================================================

a,b,c,d = st.columns(4)

a.metric(
    "Patients",
    len(filtered),
)

male = len(
    filtered[
        filtered["Sex"]=="Male"
    ]
)

female = len(
    filtered[
        filtered["Sex"]=="Female"
    ]
)

b.metric(
    "Male",
    male,
)

c.metric(
    "Female",
    female,
)

avg_age = round(
    filtered["Age"].mean(),
    1,
)

d.metric(
    "Average Age",
    avg_age,
)

st.markdown("---")

# ==========================================================
# Database
# ==========================================================

st.subheader("Registered Patients")

st.dataframe(

    filtered,

    use_container_width=True,

    hide_index=True,

)

st.markdown("---")

st.subheader("👤 Patient Details")

patient = st.selectbox(

    "Select Patient",

    filtered["Patient_ID"]

    + " - "

    + filtered["Full_Name"]

)

if patient:

    patient_id = patient.split(" - ")[0]

    selected = filtered[

        filtered["Patient_ID"]==patient_id

    ].iloc[0]

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Patient ID",
        selected["Patient_ID"],
    )

    c2.metric(
        "Age",
        selected["Age"],
    )

    c3.metric(
        "Sex",
        selected["Sex"],
    )

    st.info(

f"""
Name:
{selected["Full_Name"]}

Phone:
{selected["Phone"]}

Physician:
{selected["Physician"]}
"""

    )
st.session_state["selected_patient"] = (
    selected.to_dict()
)
if st.button(
    "👤 Open Patient Profile",
    use_container_width=True,
):

    st.switch_page(
        "pages/4_Patient_Profile.py"
    )