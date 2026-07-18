from datetime import datetime
import pandas as pd


def generate_alerts(visits, notes=None):

    alerts = []

    if visits.empty:
        return alerts

    latest = visits.iloc[-1]

    # ------------------------------------------------------
    # CKD Risk
    # ------------------------------------------------------

    if latest["Probability"] >= 0.80:

        alerts.append(
            (
                "Critical",
                "Very high predicted CKD risk."
            )
        )

    elif latest["Probability"] >= 0.60:

        alerts.append(
            (
                "High",
                "High predicted CKD risk."
            )
        )

    # ------------------------------------------------------
    # eGFR
    # ------------------------------------------------------

    if "eGFR" in latest.index:

        if latest["eGFR"] < 60:

            alerts.append(
                (
                    "High",
                    "Reduced kidney function (eGFR < 60)."
                )
            )

    # ------------------------------------------------------
    # Creatinine
    # ------------------------------------------------------

    if "LBXSCR" in latest.index:

        if latest["LBXSCR"] > 1.5:

            alerts.append(
                (
                    "High",
                    "Elevated serum creatinine."
                )
            )

    # ------------------------------------------------------
    # Blood Pressure
    # ------------------------------------------------------

    if latest["Mean_SBP"] >= 140:

        alerts.append(
            (
                "Medium",
                "Elevated systolic blood pressure."
            )
        )

    if latest["Mean_DBP"] >= 90:

        alerts.append(
            (
                "Medium",
                "Elevated diastolic blood pressure."
            )
        )

    # ------------------------------------------------------
    # Risk Trend
    # ------------------------------------------------------

    if len(visits) > 1:

        previous = visits.iloc[-2]

        if latest["Probability"] > previous["Probability"] + 0.10:

            alerts.append(
                (
                    "High",
                    "CKD probability increased significantly since the previous visit."
                )
            )

    return alerts