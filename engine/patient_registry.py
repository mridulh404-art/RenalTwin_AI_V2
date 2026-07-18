from pathlib import Path
from datetime import datetime
import pandas as pd

# ==========================================================
# RenalTwin AI V2
# Patient Registry
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

PATIENT_FILE = DATA_FOLDER / "patients.csv"


# ==========================================================
# Generate Patient ID
# ==========================================================

def generate_patient_id():
    """
    Generate Patient IDs like:

    RT-2026-00001
    RT-2026-00002
    """

    year = datetime.now().year

    if not PATIENT_FILE.exists():
        return f"RT-{year}-00001"

    df = pd.read_csv(PATIENT_FILE)

    if df.empty:
        return f"RT-{year}-00001"

    try:
        last_id = str(df.iloc[-1]["Patient_ID"])
        last_number = int(last_id.split("-")[-1])
        new_number = last_number + 1

    except Exception:
        new_number = len(df) + 1

    return f"RT-{year}-{new_number:05d}"


# ==========================================================
# Register Patient
# ==========================================================
def register_patient(data: dict):
    """
    Register a patient.

    Creates:
    - Patient record in patients.csv
    - Individual patient folder
    - Empty visits.csv
    - reports/
    - images/
    """

    patient_id = generate_patient_id()

    # ------------------------------------------------------
    # Duplicate Check
    # ------------------------------------------------------

    if PATIENT_FILE.exists():

        patients = pd.read_csv(PATIENT_FILE)

        duplicate = patients[
            (patients["Full_Name"] == data["Full_Name"])
            &
            (patients["Date_of_Birth"] == data["Date_of_Birth"])
            &
            (patients["Phone"] == data["Phone"])
        ]

        if not duplicate.empty:

            return duplicate.iloc[0]["Patient_ID"]

    # ------------------------------------------------------
    # Registration Date
    # ------------------------------------------------------

    row = {

        "Patient_ID": patient_id,

        "Registration_Date":
            datetime.now().strftime("%Y-%m-%d"),

        **data,

    }

    new_patient = pd.DataFrame([row])

    if PATIENT_FILE.exists():

        patients = pd.read_csv(PATIENT_FILE)

        patients = pd.concat(
            [patients, new_patient],
            ignore_index=True,
        )

    else:

        patients = new_patient

    patients.to_csv(
        PATIENT_FILE,
        index=False,
    )

    # ======================================================
    # Create Patient Folder
    # ======================================================

    patient_folder = (
        PROJECT_ROOT
        / "data"
        / "patients"
        / patient_id
    )

    patient_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------
    # Profile
    # ------------------------------------------------------

    profile = patient_folder / "profile.json"

    pd.Series(row).to_json(
        profile,
        indent=4,
    )

    # ------------------------------------------------------
    # Visits
    # ------------------------------------------------------

    visits = patient_folder / "visits.csv"

    if not visits.exists():

        pd.DataFrame(
            columns=[
                "Visit_ID",
                "Visit_Date",
                "Model",
                "Probability",
                "Risk",
            ]
        ).to_csv(
            visits,
            index=False,
        )

    # ------------------------------------------------------
    # Reports
    # ------------------------------------------------------

    (
        patient_folder
        / "reports"
    ).mkdir(
        exist_ok=True,
    )

    # ------------------------------------------------------
    # Images
    # ------------------------------------------------------

    (
        patient_folder
        / "images"
    ).mkdir(
        exist_ok=True,
    )

    # ------------------------------------------------------
    # SHAP
    # ------------------------------------------------------

    (
        patient_folder
        / "shap"
    ).mkdir(
        exist_ok=True,
    )

    # ------------------------------------------------------
    # Digital Twin
    # ------------------------------------------------------

    (
        patient_folder
        / "digital_twin"
    ).mkdir(
        exist_ok=True,
    )

    return patient_id
# ==========================================================
# Load All Patients
# ==========================================================

def load_patients():

    if PATIENT_FILE.exists():
        return pd.read_csv(PATIENT_FILE)

    return pd.DataFrame()


# ==========================================================
# Search Patient
# ==========================================================

def search_patient(patient_id):

    patients = load_patients()

    if patients.empty:
        return None

    patient = patients[
        patients["Patient_ID"] == patient_id
    ]

    if patient.empty:
        return None

    return patient.iloc[0].to_dict()


# ==========================================================
# Load Patient
# ==========================================================

def load_patient(patient_id):
    """
    Alias of search_patient().
    """

    return search_patient(patient_id)


# ==========================================================
# Patient Dropdown List
# ==========================================================

def get_patient_list():

    patients = load_patients()

    if patients.empty:
        return []

    return [
        f"{row.Patient_ID} - {row.Full_Name}"
        for _, row in patients.iterrows()
    ]


# ==========================================================
# Update Patient
# ==========================================================

def update_patient(patient_id, updated_data):

    patients = load_patients()

    if patients.empty:
        return False

    idx = patients.index[
        patients["Patient_ID"] == patient_id
    ]

    if len(idx) == 0:
        return False

    for key, value in updated_data.items():

        if key in patients.columns:
            patients.loc[idx[0], key] = value

    patients.to_csv(
        PATIENT_FILE,
        index=False,
    )

    return True


# ==========================================================
# Delete Patient
# ==========================================================

def delete_patient(patient_id):

    patients = load_patients()

    if patients.empty:
        return False

    patients = patients[
        patients["Patient_ID"] != patient_id
    ]

    patients.to_csv(
        PATIENT_FILE,
        index=False,
    )

    return True


# ==========================================================
# Total Patients
# ==========================================================

def total_patients():

    patients = load_patients()

    return len(patients)