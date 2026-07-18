from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.calibration import CalibrationDisplay
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

FEATURES = [

    "RIDAGEYR",
    "Female",
    "RIDRETH3",

    "BMXBMI",
    "BMXWAIST",

    "Mean_SBP",
    "Mean_DBP",

    "Diabetes",
    "Smoker",

    "LBXPLTSI",
    "LBDNENO",
    "LBDLYMNO",

    "LBXHGB",

    "SII",

    "LBXSCR",
    "LBDSALSI",

]

TARGET = "CKD"

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_model.csv"
)

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    stratify=y,
    random_state=42,
    test_size=0.20,
)

model = joblib.load(
    PROJECT_ROOT /
    "trained_models" /
    "Model_B_random_forest.pkl"
)

fig, ax = plt.subplots(figsize=(6, 6))

CalibrationDisplay.from_estimator(
    model,
    X_test,
    y_test,
    n_bins=10,
    strategy="quantile",
    ax=ax,
)

plt.title("Model B Calibration Curve")

output = PROJECT_ROOT / "outputs/figures"
output.mkdir(parents=True, exist_ok=True)

plt.savefig(
    output / "calibration_curve.png",
    dpi=300,
)

plt.close()

print("Calibration curve saved.")