import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="RenalTwin AI V2",
    page_icon="🩺",
    layout="wide",
)

# ==========================================================
# Custom CSS
# ==========================================================

css = Path("assets/styles.css")

if css.exists():

    st.markdown(
        f"<style>{css.read_text()}</style>",
        unsafe_allow_html=True,
    )

# ==========================================================
# Title
# ==========================================================

st.title("🩺 RenalTwin AI V2")

st.subheader(
    "AI-powered Clinical Decision Support System"
)

st.markdown("---")

# ==========================================================
# Load Data
# ==========================================================

patients_file = Path("data/patients.csv")
visits_file = Path("data/visits.csv")

patients = (
    pd.read_csv(patients_file)
    if patients_file.exists()
    else pd.DataFrame()
)

visits = (
    pd.read_csv(visits_file)
    if visits_file.exists()
    else pd.DataFrame()
)

# ==========================================================
# Dashboard Statistics
# ==========================================================

total_patients = len(patients)

total_visits = len(visits)

if visits.empty:

    avg_probability = 0

    high_risk = 0

    latest_probability = 0

else:

    avg_probability = visits["Probability"].mean()

    latest_probability = visits.iloc[-1]["Probability"]

    high_risk = len(

        visits[
            visits["Risk"].isin(
                [
                    "High",
                    "Very High",
                ]
            )
        ]

    )

# ==========================================================
# Summary Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Registered Patients",
    total_patients,
)

c2.metric(
    "Clinical Visits",
    total_visits,
)

c3.metric(
    "High Risk Cases",
    high_risk,
)

c4.metric(
    "Average CKD Probability",
    f"{avg_probability:.1%}",
)

st.markdown("---")

# ==========================================================
# Charts
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("CKD Risk Distribution")

    if visits.empty:

        st.info("No visit data available.")

    else:

        fig = px.pie(

            visits,

            names="Risk",

            title="Risk Categories",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

with right:

    st.subheader("Model Usage")

    if visits.empty:

        st.info("No prediction data available.")

    else:

        fig = px.histogram(

            visits,

            x="Model",

            title="Prediction Models",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

# ==========================================================
# Recent Patients
# ==========================================================

st.markdown("---")

left, right = st.columns([2, 1])

with left:

    st.subheader("📋 Recently Registered Patients")

    if patients.empty:

        st.info(
            "No registered patients."
        )

    else:

        st.dataframe(

            patients.tail(10),

            use_container_width=True,

            hide_index=True,

        )

with right:

    st.subheader("⚡ Quick Actions")

    st.success(
        """
👤 Register Patient

🩺 New Clinical Visit

📈 Patient Progress

📝 Clinical Notes

📄 Reports

🧬 Digital Twin

🤖 Decision Support
"""
    )

# ==========================================================
# Recent Visits
# ==========================================================

st.markdown("---")

st.subheader("🩺 Recent Clinical Visits")

if visits.empty:

    st.info(
        "No visit history available."
    )

else:

    recent = visits.sort_values(

        "Visit_Date",

        ascending=False,

    )

    st.dataframe(

        recent.head(10),

        use_container_width=True,

        hide_index=True,

    )

# ==========================================================
# High Risk Patients
# ==========================================================

st.markdown("---")

st.subheader("🚨 High Risk Cases")

if visits.empty:

    st.info(
        "No clinical predictions available."
    )

else:

    high = visits[
        visits["Risk"].isin(
            [
                "High",
                "Very High",
            ]
        )
    ]

    if high.empty:

        st.success(
            "No high-risk patients found."
        )

    else:

        st.dataframe(

            high,

            use_container_width=True,

            hide_index=True,

        )

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    """
RenalTwin AI V2

AI-powered Clinical Decision Support System

Features:
• CKD Prediction
• SHAP Explainability
• Digital Twin Simulation
• Patient Registry
• Progress Analysis
• Clinical Notes
• AI Decision Support

For research and clinical decision support purposes only.
"""
)