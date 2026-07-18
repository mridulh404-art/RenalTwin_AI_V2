from pathlib import Path
from datetime import datetime
import pandas as pd

# ==========================================================
# RenalTwin AI V2
# Visit Manager
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PATIENT_FOLDER = PROJECT_ROOT / "data" / "patients"


# ==========================================================
# Generate Visit ID
# ==========================================================

def generate_visit_id(patient_id):

    visit_file = (
        PATIENT_FOLDER
        / patient_id
        / "visits.csv"
    )

    if not visit_file.exists():
        return "VIS-00001"

    visits = pd.read_csv(visit_file)

    if visits.empty:
        return "VIS-00001"

    try:

        last = visits.iloc[-1]["Visit_ID"]

        number = int(
            last.split("-")[-1]
        ) + 1

    except Exception:

        number = len(visits) + 1

    return f"VIS-{number:05d}"


# ==========================================================
# Save Visit
# ==========================================================

def save_visit(

    patient_id,

    model,

    patient_data,

    prediction,

):

    patient_path = (

        PATIENT_FOLDER

        / patient_id

    )

    patient_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    visit_file = patient_path / "visits.csv"

    visit_id = generate_visit_id(
        patient_id
    )

    row = {

        "Visit_ID": visit_id,

        "Visit_Date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

        "Model": model,

        **patient_data,

        "Probability":
            prediction["Probability"],

        "Risk":
            prediction["Risk"],

        "Prediction":
            prediction["Prediction"],

    }

    visit = pd.DataFrame([row])

    if visit_file.exists():

        history = pd.read_csv(
            visit_file
        )

        history = pd.concat(

            [

                history,

                visit,

            ],

            ignore_index=True,

        )

    else:

        history = visit

    history.to_csv(

        visit_file,

        index=False,

    )

    return visit_id


# ==========================================================
# Load Visits
# ==========================================================

def load_visits(patient_id):

    visit_file = (

        PATIENT_FOLDER

        / patient_id

        / "visits.csv"

    )

    if not visit_file.exists():

        return pd.DataFrame()

    return pd.read_csv(
        visit_file
    )


# ==========================================================
# Latest Visit
# ==========================================================

def latest_visit(patient_id):

    visits = load_visits(
        patient_id
    )

    if visits.empty:

        return None

    return visits.iloc[-1]
def load_all_visits():
    """
    Load visits from every patient folder.
    """

    all_visits = []

    if not PATIENT_FOLDER.exists():

        return pd.DataFrame()

    for folder in PATIENT_FOLDER.iterdir():

        if not folder.is_dir():

            continue

        visit_file = folder / "visits.csv"

        if visit_file.exists():

            df = pd.read_csv(visit_file)

            df["Patient_ID"] = folder.name

            all_visits.append(df)

    if not all_visits:

        return pd.DataFrame()

    return pd.concat(
        all_visits,
        ignore_index=True,
    )