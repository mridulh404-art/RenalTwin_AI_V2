import streamlit as st
import pandas as pd
from pathlib import Path

from engine.predictor import predict
from engine.visit_manager import save_visit
from engine.shap_service import get_top_features
from components.sidebar import render_sidebar
# ==========================================================
# Page
# ==========================================================

st.set_page_config(
    page_title="New Visit",
    page_icon="🩺",
    layout="wide",
)
render_sidebar()
st.title("🩺 New Clinical Visit")

st.markdown("---")

# ==========================================================
# Selected Patient
# ==========================================================

if "selected_patient" not in st.session_state:

    st.warning(
        "No patient selected."
    )

    st.stop()

patient = st.session_state["selected_patient"]

patient_id = patient["Patient_ID"]

st.success(

f"""
Current Patient

**{patient['Full_Name']}**

Patient ID : {patient_id}
"""

)

st.markdown("---")
st.subheader("Patient Information")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Age",
    patient["Age"],
)

c2.metric(
    "Sex",
    patient["Sex"],
)

c3.metric(
    "Blood Group",
    patient["Blood_Group"],
)

c4.metric(
    "Physician",
    patient["Physician"],
)

st.markdown("---")
st.subheader("Visit Information")

selected_model = st.selectbox(

    "Clinical Model",

    [

        "Model A",

        "Model B",

        "Model C",

    ],

)
st.subheader("Vital Signs")

left,right = st.columns(2)

with left:

    sbp = st.number_input(

        "Systolic BP",

        70,

        250,

        120,

    )

    dbp = st.number_input(

        "Diastolic BP",

        40,

        150,

        80,

    )

with right:

    bmi = st.number_input(

        "BMI",

        10.0,

        60.0,

        25.0,

    )

    waist = st.number_input(

        "Waist Circumference",

        40.0,

        180.0,

        90.0,

    )
st.markdown("---")

st.subheader("CBC")

c1,c2 = st.columns(2)

with c1:

    platelet = st.number_input(

        "Platelets",

        50.0,

        800.0,

        250.0,

    )

    neutrophil = st.number_input(

        "Neutrophils",

        0.1,

        20.0,

        4.5,

    )

with c2:

    lymphocyte = st.number_input(

        "Lymphocytes",

        0.1,

        10.0,

        2.0,

    )

    hemoglobin = st.number_input(

        "Hemoglobin",

        5.0,

        20.0,

        13.5,

    )

sii = st.number_input(

    "SII",

    50.0,

    5000.0,

    500.0,

)
# ==========================================================
# Kidney Biomarkers
# ==========================================================

if selected_model in ["Model B", "Model C"]:

    st.markdown("---")
    st.subheader("Kidney Biomarkers")

    col1, col2 = st.columns(2)

    with col1:

        creatinine = st.number_input(
            "Serum Creatinine (mg/dL)",
            0.2,
            15.0,
            1.0,
        )

    with col2:

        albumin = st.number_input(
            "Serum Albumin (g/L)",
            20.0,
            60.0,
            42.0,
        )

else:

    creatinine = 1.0
    albumin = 42.0
# ==========================================================
# Diagnostic Biomarkers
# ==========================================================

if selected_model == "Model C":

    st.markdown("---")

    st.subheader("Diagnostic Biomarkers")

    col1, col2 = st.columns(2)

    with col1:

        egfr = st.number_input(
            "eGFR",
            1.0,
            150.0,
            90.0,
        )

    with col2:

        uacr = st.number_input(
            "Urine Albumin-Creatinine Ratio",
            1.0,
            3000.0,
            20.0,
        )

else:

    egfr = 90
    uacr = 20
st.markdown("---")

st.subheader("Lifestyle")

left, right = st.columns(2)

with left:

    diabetes = st.selectbox(
        "Diabetes",
        ["No", "Yes"],
    )

with right:

    smoker = st.selectbox(
        "Smoking",
        ["No", "Yes"],
    )
# ==========================================================
# Patient Data
# ==========================================================

patient_data = {

    "RIDAGEYR": patient["Age"],

    "Female": 1 if patient["Sex"] == "Female" else 0,

    "RIDRETH3": 3,

    "BMXBMI": bmi,

    "BMXWAIST": waist,

    "Mean_SBP": sbp,

    "Mean_DBP": dbp,

    "Diabetes": 1 if diabetes == "Yes" else 0,

    "Smoker": 1 if smoker == "Yes" else 0,

    "LBXPLTSI": platelet,

    "LBDNENO": neutrophil,

    "LBDLYMNO": lymphocyte,

    "LBXHGB": hemoglobin,

    "SII": sii,

    "LBXSCR": creatinine,

    "LBDSALSI": albumin,

    "eGFR": egfr,

    "URDACT": uacr,

}
st.markdown("---")

predict_btn = st.button(
    "🩺 Generate AI Prediction",
    use_container_width=True,
)
if predict_btn:

    result = predict(
        patient_data,
        selected_model,
    )

    probability = result["Probability"]

    visit_id = save_visit(

        patient_id,

        selected_model,

        patient_data,

        result,

    )

    st.success(
        f"Visit Saved Successfully\n\nVisit ID: {visit_id}"
    )
    st.markdown("---")

    st.subheader("Prediction Result")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Probability",
        f"{probability:.1%}",
    )

    c2.metric(
        "Risk",
        result["Risk"],
    )

    c3.metric(
        "Prediction",
        "CKD" if result["Prediction"] else "No CKD",
    )
    top = get_top_features(
        patient_data,
        selected_model,
    )

    st.markdown("---")

    st.subheader("Top Contributing Features")

    st.dataframe(
        top,
        use_container_width=True,
        hide_index=True,
    )
