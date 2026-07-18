from pathlib import Path
from datetime import datetime
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

HISTORY_FILE = PROJECT_ROOT / "data" / "history.csv"


def save_prediction(result):
    """
    Save prediction to history.csv
    """

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Model": result["Model"],
        "Probability": round(result["Probability"], 4),
        "Risk": result["Risk"],
        "Prediction": result["Prediction"],
    }])

    if HISTORY_FILE.exists():
        history = pd.read_csv(HISTORY_FILE)
        history = pd.concat([history, row], ignore_index=True)
    else:
        history = row

    history.to_csv(HISTORY_FILE, index=False)


def load_history():
    """
    Load prediction history.
    """

    if HISTORY_FILE.exists():
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame()