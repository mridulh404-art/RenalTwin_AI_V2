import streamlit as st
from pathlib import Path
import pandas as pd

from components.sidebar import render_sidebar

from engine.ai_summary import generate_summary
from engine.visit_manager import load_visits
from engine.clinical_notes import load_notes
from engine.pdf_report import generate_report


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Patient Reports",
    page_icon="📄",
    layout="wide",
)


render_sidebar()


# ==========================================================
# Patient Check
# ==========================================================

if "selected_patient" not in st.session_state:

    st.warning(
        "Please select a patient first."
    )

    st.stop()


patient = st.session_state["selected_patient"]

patient_id = patient["Patient_ID"]


# ==========================================================
# Patient Folder
# ==========================================================

patient_folder = (
    Path("data")
    / "patients"
    / patient_id
)

reports_folder = (
    patient_folder
    / "reports"
)

reports_folder.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Title
# ==========================================================

st.title(
    "📄 Patient Clinical Report"
)

st.caption(
    "RenalTwin AI generated clinical summary"
)

st.markdown("---")


# ==========================================================
# Patient Information
# ==========================================================

st.subheader(
    "👤 Patient Information"
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Patient ID",
        patient_id
    )


with c2:

    st.metric(
        "Name",
        patient.get(
            "Full_Name",
            "-"
        )
    )


with c3:

    st.metric(
        "Physician",
        patient.get(
            "Physician",
            "-"
        )
    )


# ==========================================================
# Load Data
# ==========================================================

visits = load_visits(
    patient_id
)

notes = load_notes(
    patient_id
)


# ==========================================================
# Clinical Summary
# ==========================================================

st.markdown("---")

st.subheader(
    "🩺 Clinical Summary"
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Total Visits",
        len(visits)
    )


latest = None


if not visits.empty:

    latest = visits.iloc[-1]


    with c2:

        st.metric(
            "Latest Risk",
            latest.get(
                "Risk",
                "-"
            )
        )


    with c3:

        probability = latest.get(
            "Probability",
            0
        )

        st.metric(
            "CKD Probability",
            f"{probability:.1%}"
        )


else:

    with c2:

        st.metric(
            "Latest Risk",
            "-"
        )


    with c3:

        st.metric(
            "CKD Probability",
            "-"
        )


# ==========================================================
# Visit History
# ==========================================================

st.markdown("---")

st.header(
    "📅 Visit History"
)


if visits.empty:

    st.info(
        "No visit history available."
    )

else:

    columns = [
        "Visit_ID",
        "Visit_Date",
        "Model",
        "Probability",
        "Risk",
    ]

    available = [
        c for c in columns
        if c in visits.columns
    ]

    st.dataframe(
        visits[available],
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# Clinical Notes
# ==========================================================

st.markdown("---")

st.header(
    "📝 Clinical Notes"
)


if notes.empty:

    st.info(
        "No clinical notes available."
    )

else:

    st.dataframe(
        notes,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# AI Summary
# ==========================================================

st.markdown("---")

st.header(
    "🤖 AI Clinical Summary"
)


summary = generate_summary(
    patient,
    visits,
)


st.info(
    summary
)


# ==========================================================
# PDF Report Generation
# ==========================================================

st.markdown("---")

st.header(
    "📥 Download Report"
)


if st.button(
    "Generate Clinical PDF Report",
    use_container_width=True,
):

    report_file = (
        reports_folder
        /
        "RenalTwin_Clinical_Report.pdf"
    )


    patient_report = {

        "Patient ID": patient_id,

        "Name": patient.get(
            "Full_Name",
            "-"
        ),

        "Age": patient.get(
            "Age",
            "-"
        ),

        "Sex": patient.get(
            "Sex",
            "-"
        ),

        "Physician": patient.get(
            "Physician",
            "-"
        ),

    }


    prediction_report = {

        "Risk": "-",

        "Probability": "-",

        "Summary": summary,

    }


    if latest is not None:

        prediction_report["Risk"] = latest.get(
            "Risk",
            "-"
        )

        prediction_report["Probability"] = latest.get(
            "Probability",
            "-"
        )


    generate_report(

        patient_report,

        prediction_report,

        report_file,

    )


    st.success(
        "Clinical report generated successfully."
    )


    with open(
        report_file,
        "rb"
    ) as file:


        st.download_button(

            label="📄 Download PDF",

            data=file,

            file_name="RenalTwin_Clinical_Report.pdf",

            mime="application/pdf",

            use_container_width=True,

        )