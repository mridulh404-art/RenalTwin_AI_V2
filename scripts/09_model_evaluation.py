from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,

    confusion_matrix,
    ConfusionMatrixDisplay,

    RocCurveDisplay,
    PrecisionRecallDisplay,

    classification_report,
)

# ==========================================================
# RenalTwin AI V2
# Clinical Model Evaluation
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Clinical Model Evaluation")
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

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

# ----------------------------------------------------------
# Metrics
# ----------------------------------------------------------

accuracy = accuracy_score(y_test, predictions)

precision = precision_score(y_test, predictions)

recall = recall_score(y_test, predictions)

f1 = f1_score(y_test, predictions)

roc_auc = roc_auc_score(y_test, probabilities)

pr_auc = average_precision_score(y_test, probabilities)

brier = brier_score_loss(y_test, probabilities)

cm = confusion_matrix(y_test, predictions)

tn, fp, fn, tp = cm.ravel()

specificity = tn / (tn + fp)

npv = tn / (tn + fn)

ppv = tp / (tp + fp)

# ----------------------------------------------------------
# Print Results
# ----------------------------------------------------------

print()

print(f"Accuracy     : {accuracy:.4f}")
print(f"Precision    : {precision:.4f}")
print(f"Recall       : {recall:.4f}")
print(f"Specificity  : {specificity:.4f}")
print(f"F1 Score     : {f1:.4f}")
print(f"ROC-AUC      : {roc_auc:.4f}")
print(f"PR-AUC       : {pr_auc:.4f}")
print(f"Brier Score  : {brier:.4f}")
print(f"NPV          : {npv:.4f}")
print(f"PPV          : {ppv:.4f}")

print()

print(classification_report(
    y_test,
    predictions,
))

# ----------------------------------------------------------
# Output Folder
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

# ----------------------------------------------------------
# ROC Curve
# ----------------------------------------------------------

RocCurveDisplay.from_predictions(
    y_test,
    probabilities,
)

plt.savefig(
    figure_folder / "roc_curve.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

# ----------------------------------------------------------
# Precision Recall Curve
# ----------------------------------------------------------

PrecisionRecallDisplay.from_predictions(
    y_test,
    probabilities,
)

plt.savefig(
    figure_folder / "precision_recall_curve.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

ConfusionMatrixDisplay(
    confusion_matrix=cm
).plot()

plt.savefig(
    figure_folder / "confusion_matrix.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print()
print("Evaluation figures saved.")
print("=" * 80)