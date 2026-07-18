from pathlib import Path
import pandas as pd

# ==========================================================
# RenalTwin AI V2
# Progress Analytics
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VISIT_FILE = PROJECT_ROOT / "data" / "visits.csv"


def load_patient_progress(patient_id):
    """
    Load all visits for one patient.
    """

    if not VISIT_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(VISIT_FILE)

    df = df[
        df["Patient_ID"] == patient_id
    ]

    if df.empty:
        return df

    df = df.sort_values(
        "Visit_Date"
    )

    return df


def calculate_progress(patient_id):
    """
    Compare first and latest visit.
    """

    visits = load_patient_progress(
        patient_id
    )

    if len(visits) < 2:

        return {

            "Status": "Insufficient Data",

            "Change": 0,

            "First": None,

            "Latest": None,

        }

    first = visits.iloc[0]["Probability"]

    latest = visits.iloc[-1]["Probability"]

    change = latest - first

    if change < -0.05:

        status = "Improving"

    elif change > 0.05:

        status = "Declining"

    else:

        status = "Stable"

    return {

        "Status": status,

        "Change": change,

        "First": first,

        "Latest": latest,

    }