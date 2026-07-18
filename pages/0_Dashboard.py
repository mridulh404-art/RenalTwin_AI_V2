import streamlit as st
import pandas as pd
import plotly.express as px

from engine.patient_registry import load_patients
from engine.visit_manager import load_all_visits

# ==========================================================
# Page
# ==========================================================

st.set_page_config(
    page_title="RenalTwin Dashboard",
    page_icon="🏥",
    layout="wide",
)
st.title("🏥 RenalTwin AI V2")

st.subheader("Clinical Dashboard")

st.markdown("---")
patients = load_patients()

visits = load_all_visits()
total_patients = len(patients)

total_visits = len(visits)

if visits.empty:

    average_probability = 0

    high_risk = 0

else:

    average_probability = visits[
        "Probability"
    ].mean()

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

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Patients",
    total_patients,
)

c2.metric(
    "Visits",
    total_visits,
)

c3.metric(
    "High Risk",
    high_risk,
)

c4.metric(
    "Average CKD Risk",
    f"{average_probability:.1%}",
)
st.markdown("---")

st.header("Risk Distribution")

if not visits.empty:

    chart = px.pie(

        visits,

        names="Risk",

        title="CKD Risk Levels",

    )

    st.plotly_chart(

        chart,

        use_container_width=True,

    )
st.markdown("---")

st.header("Model Usage")

if not visits.empty:

    model_chart = px.histogram(

        visits,

        x="Model",

    )

    st.plotly_chart(

        model_chart,

        use_container_width=True,

    )
st.markdown("---")

st.header("Recent Clinical Visits")

if visits.empty:

    st.info(
        "No visits recorded."
    )

else:

    recent = visits.sort_values(

        "Visit_Date",

        ascending=False,

    )

    st.dataframe(

        recent.head(15),

        use_container_width=True,

        hide_index=True,

    )
st.markdown("---")

st.header("🚨 High Risk Patients")

if visits.empty:

    st.info("No data.")

else:

    high = visits[

        visits["Risk"].isin(
            [
                "High",
                "Very High",
            ]
        )

    ]

    st.dataframe(

        high,

        use_container_width=True,

        hide_index=True,

    )
