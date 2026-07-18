import streamlit as st
import pandas as pd
import plotly.express as px

from engine.visit_manager import load_visits
from engine.comparison import compare_visits
from engine.alerts import generate_alerts
from components.sidebar import render_sidebar
# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Patient Progress",
    page_icon="📈",
    layout="wide",
)
render_sidebar()
# ==========================================================
# Title
# ==========================================================

st.title("📈 Patient Progress Dashboard")

st.markdown("---")

# ==========================================================
# Selected Patient
# ==========================================================

if "selected_patient" not in st.session_state:

    st.warning(
        "Please select a patient from the Patient Database."
    )

    st.stop()

patient = st.session_state["selected_patient"]

patient_id = patient["Patient_ID"]

# ==========================================================
# Header
# ==========================================================

st.success(
    f"""
### 👤 {patient['Full_Name']}

**Patient ID:** {patient_id}
"""
)

# ==========================================================
# Load Visits
# ==========================================================

visits = load_visits(patient_id)

if visits.empty:

    st.info(
        "No visit history available."
    )

    st.stop()

visits["Visit_Date"] = pd.to_datetime(
    visits["Visit_Date"]
)

visits = visits.sort_values(
    "Visit_Date"
)

# ==========================================================
# Clinical Alerts
# ==========================================================

alerts = generate_alerts(visits)

# ==========================================================
# Summary
# ==========================================================

latest = visits.iloc[-1]

first = visits.iloc[0]

change = latest["Probability"] - first["Probability"]

if change < -0.05:

    status = "🟢 Improving"

elif change > 0.05:

    status = "🔴 Declining"

else:

    status = "🟡 Stable"

# ==========================================================
# Dashboard Metrics
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "Total Visits",
        len(visits),
    )

with c2:

    st.metric(
        "Risk Level",
        latest["Risk"],
    )

with c3:

    st.metric(
        "CKD Probability",
        f"{latest['Probability']:.1%}",
    )

with c4:

    st.metric(
        "Overall Change",
        f"{change:.1%}",
    )

with c5:

    st.metric(
        "Clinical Status",
        status,
    )

# ==========================================================
# Improvement Score
# ==========================================================

st.markdown("---")

st.subheader("🏥 Overall Clinical Improvement")

improvement_score = max(
    0,
    min(
        100,
        (1 - latest["Probability"]) * 100,
    ),
)

st.progress(
    improvement_score / 100
)

st.caption(
    f"Clinical Improvement Score: {improvement_score:.1f}/100"
)

# ==========================================================
# Clinical Alerts
# ==========================================================

st.markdown("---")

st.header("🚨 Clinical Alerts")

if not alerts:

    st.success(
        "No active clinical alerts."
    )

else:

    for level, message in alerts:

        if level == "Critical":

            st.error(
                f"🔴 {message}"
            )

        elif level == "High":

            st.warning(
                f"🟠 {message}"
            )

        else:

            st.info(
                f"🟡 {message}"
            )

st.markdown("---")
# ==========================================================
# CKD Risk Trend
# ==========================================================

st.header("📈 CKD Risk Trend")

risk_fig = px.line(

    visits,

    x="Visit_Date",

    y="Probability",

    markers=True,

    title="Predicted CKD Probability",

)

risk_fig.update_traces(

    line_width=3,

    marker_size=8,

)

risk_fig.update_layout(

    yaxis_tickformat=".0%",

    xaxis_title="Visit Date",

    yaxis_title="CKD Probability",

)

st.plotly_chart(

    risk_fig,

    use_container_width=True,

)

# ==========================================================
# Blood Pressure Trend
# ==========================================================

st.markdown("---")

st.header("❤️ Blood Pressure Trend")

bp_fig = px.line(

    visits,

    x="Visit_Date",

    y=[

        "Mean_SBP",

        "Mean_DBP",

    ],

    markers=True,

)

bp_fig.update_traces(

    line_width=3,

    marker_size=8,

)

bp_fig.update_layout(

    xaxis_title="Visit Date",

    yaxis_title="Blood Pressure (mmHg)",

)

st.plotly_chart(

    bp_fig,

    use_container_width=True,

)

# ==========================================================
# Kidney Function Trends
# ==========================================================

st.markdown("---")

st.header("🧪 Kidney Function")

left, right = st.columns(2)

# ----------------------------------------------------------
# Creatinine
# ----------------------------------------------------------

with left:

    if "LBXSCR" in visits.columns:

        creatinine_fig = px.line(

            visits,

            x="Visit_Date",

            y="LBXSCR",

            markers=True,

            title="Serum Creatinine",

        )

        creatinine_fig.update_traces(

            line_width=3,

            marker_size=8,

        )

        creatinine_fig.update_layout(

            xaxis_title="Visit Date",

            yaxis_title="Creatinine (mg/dL)",

        )

        st.plotly_chart(

            creatinine_fig,

            use_container_width=True,

        )

# ----------------------------------------------------------
# eGFR
# ----------------------------------------------------------

with right:

    if "eGFR" in visits.columns:

        egfr_fig = px.line(

            visits,

            x="Visit_Date",

            y="eGFR",

            markers=True,

            title="Estimated GFR",

        )

        egfr_fig.update_traces(

            line_width=3,

            marker_size=8,

        )

        egfr_fig.update_layout(

            xaxis_title="Visit Date",

            yaxis_title="eGFR",

        )

        st.plotly_chart(

            egfr_fig,

            use_container_width=True,

        )

# ==========================================================
# Visit History
# ==========================================================

st.markdown("---")

st.header("📋 Visit History")

history = visits.sort_values(

    "Visit_Date",

    ascending=False,

)

st.dataframe(

    history,

    use_container_width=True,

    hide_index=True,

)

# ==========================================================
# Visit Comparison
# ==========================================================

st.markdown("---")

st.header("🔬 Visit Comparison")

visit_ids = visits["Visit_ID"].tolist()

if len(visit_ids) < 2:

    st.info(
        "At least two visits are required for comparison."
    )

else:

    left, right = st.columns(2)

    with left:

        visit1 = st.selectbox(
            "Baseline Visit",
            visit_ids,
            index=0,
        )

    with right:

        visit2 = st.selectbox(
            "Comparison Visit",
            visit_ids,
            index=len(visit_ids) - 1,
        )

    if st.button(
        "🔍 Compare Visits",
        use_container_width=True,
    ):

        if visit1 == visit2:

            st.warning(
                "Please select two different visits."
            )

        else:

            comparison = compare_visits(
                visits,
                visit1,
                visit2,
            )

            st.subheader("Comparison Table")

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True,
            )

            # --------------------------------------------------
            # Clinical Interpretation
            # --------------------------------------------------

            st.markdown("---")

            st.subheader("🩺 Clinical Interpretation")

            probability_diff = comparison.loc[
                comparison["Metric"] == "Probability",
                "Difference",
            ]

            creatinine_diff = comparison.loc[
                comparison["Metric"] == "LBXSCR",
                "Difference",
            ]

            egfr_diff = comparison.loc[
                comparison["Metric"] == "eGFR",
                "Difference",
            ]

            interpretation = []

            if not probability_diff.empty:

                value = probability_diff.iloc[0]

                if value < 0:

                    interpretation.append(
                        f"✅ CKD probability decreased by {abs(value):.1%}."
                    )

                elif value > 0:

                    interpretation.append(
                        f"⚠ CKD probability increased by {value:.1%}."
                    )

            if not creatinine_diff.empty:

                value = creatinine_diff.iloc[0]

                if value < 0:

                    interpretation.append(
                        f"✅ Serum creatinine decreased by {abs(value):.2f} mg/dL."
                    )

                elif value > 0:

                    interpretation.append(
                        f"⚠ Serum creatinine increased by {value:.2f} mg/dL."
                    )

            if not egfr_diff.empty:

                value = egfr_diff.iloc[0]

                if value > 0:

                    interpretation.append(
                        f"✅ eGFR improved by {value:.1f}."
                    )

                elif value < 0:

                    interpretation.append(
                        f"⚠ eGFR decreased by {abs(value):.1f}."
                    )

            if interpretation:

                for item in interpretation:

                    st.write(item)

            else:

                st.info(
                    "No clinically meaningful changes detected."
                )

# ==========================================================
# Page Footer
# ==========================================================

st.markdown("---")

st.caption(
    """
RenalTwin AI V2

Patient Progress Analysis Module

Includes longitudinal risk assessment,
clinical alerts, trend analysis,
and visit comparison.

For research and clinical decision support purposes only.
"""
)