from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

# ==========================================================
# RenalTwin AI V2
# Threshold Optimization
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Threshold Optimization")
print("=" * 80)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_model.csv"
)

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

X = df[FEATURES]

y = df[TARGET].astype(int)

# ----------------------------------------------------------
# Train/Test Split
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y,

)

# ----------------------------------------------------------
# Load Best Model
# ----------------------------------------------------------

model = joblib.load(

    PROJECT_ROOT /

    "trained_models" /

    "Model_B_random_forest.pkl"

)

probabilities = model.predict_proba(X_test)[:,1]

# ----------------------------------------------------------
# Evaluate Thresholds
# ----------------------------------------------------------

results = []

thresholds = [i / 100 for i in range(10, 91, 5)]

for threshold in thresholds:

    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
    ).ravel()

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    specificity = tn / (tn + fp)

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    youden = recall + specificity - 1

    results.append({

        "Threshold": threshold,

        "Precision": precision,

        "Recall": recall,

        "Specificity": specificity,

        "F1": f1,

        "Youden": youden,

    })

# ----------------------------------------------------------
# Results
# ----------------------------------------------------------

results_df = pd.DataFrame(results)

print()
print(results_df)

# ----------------------------------------------------------
# Best Threshold
# ----------------------------------------------------------

best = results_df.loc[
    results_df["Youden"].idxmax()
]

print()

print("=" * 80)
print("Recommended Threshold")
print("=" * 80)

print(best)

# ----------------------------------------------------------
# Save CSV
# ----------------------------------------------------------

metrics_folder = (
    PROJECT_ROOT /
    "outputs" /
    "metrics"
)

metrics_folder.mkdir(
    parents=True,
    exist_ok=True,
)

results_df.to_csv(

    metrics_folder /

    "threshold_optimization.csv",

    index=False,

)

# ----------------------------------------------------------
# Plot
# ----------------------------------------------------------

figure_folder = (
    PROJECT_ROOT /
    "outputs" /
    "figures"
)

figure_folder.mkdir(
    parents=True,
    exist_ok=True,
)

plt.figure(figsize=(10,6))

plt.plot(
    results_df["Threshold"],
    results_df["Recall"],
    label="Recall"
)

plt.plot(
    results_df["Threshold"],
    results_df["Precision"],
    label="Precision"
)

plt.plot(
    results_df["Threshold"],
    results_df["F1"],
    label="F1 Score"
)

plt.plot(
    results_df["Threshold"],
    results_df["Specificity"],
    label="Specificity"
)

plt.axvline(
    best["Threshold"],
    linestyle="--",
    label=f'Best ({best["Threshold"]:.2f})'
)

plt.xlabel("Probability Threshold")

plt.ylabel("Metric")

plt.title("Threshold Optimization")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(

    figure_folder /

    "threshold_optimization.png",

    dpi=300,

)

plt.close()

print()

print("✓ Threshold optimization figure saved.")

print("✓ Threshold table saved.")

print("=" * 80)