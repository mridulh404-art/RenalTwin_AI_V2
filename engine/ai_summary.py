import pandas as pd


def generate_summary(patient, visits):

    if visits.empty:

        return "No visit history available."

    latest = visits.iloc[-1]

    if len(visits) > 1:

        previous = visits.iloc[-2]

    else:

        previous = latest

    probability_change = (
        latest["Probability"]
        - previous["Probability"]
    )

    creatinine_change = (
        latest["LBXSCR"]
        - previous["LBXSCR"]
    )

    egfr_change = (
        latest["eGFR"]
        - previous["eGFR"]
    )

    summary = f"""
Patient {patient['Full_Name']} ({patient['Patient_ID']}) has completed {len(visits)} clinical visit(s).

Current CKD probability is {latest['Probability']:.1%} ({latest['Risk']}).

Compared with the previous visit:

• CKD probability changed by {probability_change:.1%}

• Serum creatinine changed by {creatinine_change:.2f} mg/dL

• eGFR changed by {egfr_change:.1f} mL/min/1.73m²

Current blood pressure is
{latest['Mean_SBP']:.0f}/{latest['Mean_DBP']:.0f} mmHg.

This summary is AI-generated and should always be interpreted together with the complete clinical assessment.
"""

    return summary.strip()