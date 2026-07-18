import streamlit as st
from components.sidebar import render_sidebar
from engine.visit_manager import latest_visit
from engine.clinical_notes import (
    save_note,
    load_notes,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Clinical Notes",
    page_icon="📝",
    layout="wide",
)
render_sidebar()
# ==========================================================
# Check Selected Patient
# ==========================================================

if "selected_patient" not in st.session_state:

    st.warning(
        "Please select a patient from the Patient Database."
    )

    st.stop()

patient = st.session_state["selected_patient"]

patient_id = patient["Patient_ID"]

# ==========================================================
# Latest Visit
# ==========================================================

visit = latest_visit(patient_id)

if visit is None:

    st.warning(
        "This patient has no clinical visits yet.\n\nPlease create a new visit first."
    )

    st.stop()

visit_id = visit["Visit_ID"]


# ==========================================================
# Title
# ==========================================================

st.title("📝 Clinical Notes")

st.markdown("---")

# ==========================================================
# Patient Information
# ==========================================================

st.subheader("Patient Information")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Patient ID",
        patient_id,
    )

with c2:

    st.metric(
        "Patient",
        patient["Full_Name"],
    )

with c3:

    st.metric(
        "Visit ID",
        visit_id,
    )

with c4:

    st.metric(
        "Physician",
        patient.get(
            "Physician",
            "-",
        ),
    )

st.info(
    f"""
**Hospital:** {patient.get('Hospital','-')}

**Age:** {patient.get('Age','-')} Years

**Sex:** {patient.get('Sex','-')}
"""
)

st.markdown("---")

# ==========================================================
# Diagnosis
# ==========================================================

st.subheader("Diagnosis")

diagnosis = st.text_area(
    "Clinical Diagnosis",
    placeholder="Enter diagnosis...",
    height=100,
)

# ==========================================================
# Medication
# ==========================================================

st.subheader("Current Medications")

medications = st.text_area(
    "Medication List",
    placeholder="Example:\nLosartan 50 mg\nEmpagliflozin 10 mg",
    height=120,
)

# ==========================================================
# Recommendations
# ==========================================================

st.subheader("Treatment Recommendations")

recommendations = st.text_area(
    "Recommendations",
    placeholder="Lifestyle modification, repeat labs after 3 months...",
    height=120,
)

# ==========================================================
# Follow-up
# ==========================================================

st.subheader("Follow-up")

followup = st.date_input(
    "Next Follow-up Date",
)

# ==========================================================
# Clinical Notes
# ==========================================================

st.subheader("Clinical Notes")

notes = st.text_area(
    "Additional Clinical Notes",
    height=220,
)

# ==========================================================
# Save
# ==========================================================

st.markdown("---")

if st.button(
    "💾 Save Clinical Notes",
    use_container_width=True,
):

    if diagnosis.strip() == "":

        st.error(
            "Diagnosis cannot be empty."
        )

    else:

        save_note(

            patient_id=patient_id,

            visit_id=visit_id,

            diagnosis=diagnosis,

            medications=medications,

            recommendations=recommendations,

            followup=str(followup),

            notes=notes,

        )

        st.success(
            "Clinical notes saved successfully."
        )

        st.balloons()

# ==========================================================
# Previous Notes
# ==========================================================

st.markdown("---")

st.header("📜 Previous Clinical Notes")

history = load_notes(patient_id)

if history.empty:

    st.info(
        "No previous clinical notes found."
    )

else:

    history = history.sort_values(
        "Date",
        ascending=False,
    )

    for _, row in history.iterrows():

        with st.expander(
            f"{row['Date']} | {row['Diagnosis']}"
        ):

            st.markdown(
                f"""
### Diagnosis

{row['Diagnosis']}

---

### Medications

{row['Medications']}

---

### Recommendations

{row['Recommendations']}

---

### Follow-up

{row['Follow_Up']}

---

### Clinical Notes

{row['Clinical_Notes']}
"""
            )

# ==========================================================
# Summary
# ==========================================================

st.markdown("---")

st.caption(
    """
RenalTwin AI V2

Clinical Notes Module

All notes are stored with the corresponding patient and visit history.
"""
)