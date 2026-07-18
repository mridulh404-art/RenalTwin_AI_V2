from pathlib import Path
from datetime import datetime
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PATIENT_FOLDER = PROJECT_ROOT / "data" / "patients"


def save_note(

    patient_id,

    visit_id,

    diagnosis,

    medications,

    recommendations,

    followup,

    notes,

):

    patient = PATIENT_FOLDER / patient_id

    patient.mkdir(
        parents=True,
        exist_ok=True,
    )

    note_file = patient / "notes.csv"

    row = {

        "Visit_ID": visit_id,

        "Date":
            datetime.now().strftime("%Y-%m-%d"),

        "Diagnosis": diagnosis,

        "Medications": medications,

        "Recommendations": recommendations,

        "Follow_Up": followup,

        "Clinical_Notes": notes,

    }

    df = pd.DataFrame([row])

    if note_file.exists():

        history = pd.read_csv(note_file)

        history = pd.concat(

            [

                history,

                df,

            ],

            ignore_index=True,

        )

    else:

        history = df

    history.to_csv(

        note_file,

        index=False,

    )
# ==========================================================
# Load Notes
# ==========================================================

def load_notes(patient_id):

    patient = PATIENT_FOLDER / patient_id

    note_file = patient / "notes.csv"

    if not note_file.exists():

        return pd.DataFrame()

    return pd.read_csv(note_file)


# ==========================================================
# Latest Note
# ==========================================================

def latest_note(patient_id):

    notes = load_notes(patient_id)

    if notes.empty:

        return None

    return notes.iloc[-1].to_dict()