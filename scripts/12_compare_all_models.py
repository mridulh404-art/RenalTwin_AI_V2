from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# RenalTwin AI V2
# Compare All Models
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Final Model Comparison")
print("=" * 80)

# ----------------------------------------------------------
# Load Results
# ----------------------------------------------------------

model_a = pd.read_csv(
    PROJECT_ROOT /
    "outputs" /
    "metrics" /
    "Model_A_comparison.csv"
)

model_b = pd.read_csv(
    PROJECT_ROOT /
    "outputs" /
    "metrics" /
    "Model_B_comparison.csv"
)

model_c = pd.read_csv(
    PROJECT_ROOT /
    "outputs" /
    "metrics" /
    "Model_C_comparison.csv"
)

best_a = model_a.iloc[0]
best_b = model_b.iloc[0]
best_c = model_c.iloc[0]

# ----------------------------------------------------------
# Summary Table
# ----------------------------------------------------------

summary = pd.DataFrame({

    "Model":[
        "Model A",
        "Model B",
        "Model C",
    ],

    "Purpose":[
        "Early Screening",
        "Clinical Screening",
        "Diagnostic Support",
    ],

    "Features":[
        14,
        16,
        18,
    ],

    "Best Algorithm":[
        best_a["Model"],
        best_b["Model"],
        best_c["Model"],
    ],

    "Accuracy":[
        best_a["Accuracy"],
        best_b["Accuracy"],
        best_c["Accuracy"],
    ],

    "Precision":[
        best_a["Precision"],
        best_b["Precision"],
        best_c["Precision"],
    ],

    "Recall":[
        best_a["Recall"],
        best_b["Recall"],
        best_c["Recall"],
    ],

    "F1":[
        best_a["F1"],
        best_b["F1"],
        best_c["F1"],
    ],

    "ROC_AUC":[
        best_a["ROC_AUC"],
        best_b["ROC_AUC"],
        best_c["ROC_AUC"],
    ]

})

summary = summary.round(4)

print()
print(summary)

# ----------------------------------------------------------
# Save CSV
# ----------------------------------------------------------

metrics_folder = (
    PROJECT_ROOT /
    "outputs" /
    "metrics"
)

summary.to_csv(

    metrics_folder /

    "Final_Model_Comparison.csv",

    index=False,

)

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
# ROC-AUC Comparison
# ----------------------------------------------------------

plt.figure(figsize=(8,6))

plt.bar(

    summary["Model"],

    summary["ROC_AUC"]

)

plt.ylim(0,1.05)

plt.ylabel("ROC-AUC")

plt.title("RenalTwin AI V2 Model Comparison")

for i, value in enumerate(summary["ROC_AUC"]):

    plt.text(
        i,
        value + 0.02,
        f"{value:.3f}",
        ha="center",
    )

plt.tight_layout()

plt.savefig(

    figure_folder /

    "model_comparison_auc.png",

    dpi=300,

)

plt.close()

# ----------------------------------------------------------
# F1 Comparison
# ----------------------------------------------------------

plt.figure(figsize=(8,6))

plt.bar(

    summary["Model"],

    summary["F1"]

)

plt.ylim(0,1.05)

plt.ylabel("F1 Score")

plt.title("F1 Score Comparison")

for i, value in enumerate(summary["F1"]):

    plt.text(
        i,
        value + 0.02,
        f"{value:.3f}",
        ha="center",
    )

plt.tight_layout()

plt.savefig(

    figure_folder /

    "model_comparison_f1.png",

    dpi=300,

)

plt.close()

print()

print("=" * 80)
print("COMPARISON COMPLETED")
print("=" * 80)

print()

print("Files generated:")

print("Final_Model_Comparison.csv")
print("model_comparison_auc.png")
print("model_comparison_f1.png")