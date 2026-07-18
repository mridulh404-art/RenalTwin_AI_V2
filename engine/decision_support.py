"""
RenalTwin AI V2
Clinical Decision Support Engine

This module converts AI predictions and clinical
measurements into evidence-informed recommendations.

For clinical decision support only.
"""

from typing import Dict, List


def generate_decision_support(
    prediction: Dict,
    patient: Dict,
) -> Dict:

    probability = prediction["Probability"]
    risk = prediction["Risk"]

    egfr = patient.get("eGFR", 90)
    creatinine = patient.get("LBXSCR", 1.0)
    sbp = patient.get("Mean_SBP", 120)
    dbp = patient.get("Mean_DBP", 80)
    diabetes = patient.get("Diabetes", 0)
    smoker = patient.get("Smoker", 0)

    priority = "Routine"

    recommendations: List[str] = []

    follow_up = "12 Months"

    # ======================================================
    # AI Risk
    # ======================================================

    if probability >= 0.80:

        priority = "Critical"

        follow_up = "Within 1 Week"

        recommendations.append(
            "Urgent nephrology referral."
        )

    elif probability >= 0.60:

        priority = "High"

        follow_up = "Within 1 Month"

        recommendations.append(
            "Arrange nephrology consultation."
        )

    elif probability >= 0.40:

        priority = "Moderate"

        follow_up = "Within 3 Months"

    else:

        priority = "Low"

        follow_up = "12 Months"

    # ======================================================
    # Kidney Function
    # ======================================================

    if egfr < 60:

        recommendations.append(
            "Repeat renal function testing."
        )

    if creatinine > 1.5:

        recommendations.append(
            "Monitor serum creatinine."
        )

    # ======================================================
    # Blood Pressure
    # ======================================================

    if sbp >= 140 or dbp >= 90:

        recommendations.append(
            "Optimize blood pressure control."
        )

    # ======================================================
    # Diabetes
    # ======================================================

    if diabetes == 1:

        recommendations.append(
            "Ensure appropriate glycemic management."
        )

    # ======================================================
    # Smoking
    # ======================================================

    if smoker == 1:

        recommendations.append(
            "Provide smoking cessation counselling."
        )

    # ======================================================
    # Lifestyle
    # ======================================================

    recommendations.extend(
        [
            "Encourage regular physical activity as clinically appropriate.",
            "Recommend a kidney-friendly diet.",
            "Avoid nephrotoxic medications whenever possible.",
            "Maintain adequate hydration unless contraindicated.",
        ]
    )

    # Remove duplicates while preserving order
    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return {

        "Priority": priority,

        "Follow_Up": follow_up,

        "Recommendations": recommendations,

        "Probability": probability,

        "Risk": risk,

    }