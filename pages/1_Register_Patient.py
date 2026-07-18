import streamlit as st
from datetime import date
from components.sidebar import render_sidebar
from engine.patient_registry import register_patient


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Register Patient",
    page_icon="👤",
    layout="wide",
)

render_sidebar()


# ==========================================================
# Title
# ==========================================================

st.title("👤 Patient Registration")

st.caption(
    "Create a new patient record in RenalTwin AI"
)

st.markdown("---")


# ==========================================================
# Patient Information
# ==========================================================

st.header("Patient Information")


col1, col2 = st.columns(2)


with col1:

    full_name = st.text_input(
        "Full Name"
    )

    dob = st.date_input(
        "Date of Birth",
        value=date.today()
    )

    sex = st.selectbox(
        "Sex",
        [
            "Male",
            "Female",
            "Other",
        ]
    )

    phone = st.text_input(
        "Phone Number"
    )


with col2:

    email = st.text_input(
        "Email"
    )

    physician = st.text_input(
        "Consulting Physician"
    )

    hospital = st.text_input(
        "Hospital / Clinic"
    )

    address = st.text_area(
        "Address"
    )


# ==========================================================
# Additional Information
# ==========================================================

st.markdown("---")

st.header("Medical Background")


c1, c2 = st.columns(2)


with c1:

    diabetes = st.selectbox(
        "Diabetes History",
        [
            "No",
            "Yes",
        ]
    )


    hypertension = st.selectbox(
        "Hypertension History",
        [
            "No",
            "Yes",
        ]
    )


with c2:

    smoking = st.selectbox(
        "Smoking Status",
        [
            "No",
            "Yes",
        ]
    )


    family_history = st.selectbox(
        "Family History of Kidney Disease",
        [
            "No",
            "Yes",
        ]
    )


# ==========================================================
# Register Button
# ==========================================================

st.markdown("---")


if st.button(
    "💾 Register Patient",
    use_container_width=True,
):

    if not full_name:

        st.error(
            "Please enter patient name."
        )

    else:

        patient_data = {

            "Full_Name": full_name,

            "Date_of_Birth": str(dob),

            "Sex": sex,

            "Phone": phone,

            "Email": email,

            "Physician": physician,

            "Hospital": hospital,

            "Address": address,

            "Diabetes": diabetes,

            "Hypertension": hypertension,

            "Smoking": smoking,

            "Family_History": family_history,

        }


        patient_id = register_patient(
            patient_data
        )


        st.success(
            f"""
✅ Patient Registered Successfully

Patient ID:

**{patient_id}**
"""
        )


        st.session_state["patient_id"] = patient_id