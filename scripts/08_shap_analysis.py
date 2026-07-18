from pathlib import Path

import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# RenalTwin AI V2
# SHAP Explainability
# Compatible with SHAP 0.52+
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - SHAP Explainability")
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

# ----------------------------------------------------------
# Sample (for speed)
# ----------------------------------------------------------

X = df[FEATURES].sample(
    n=min(500, len(df)),
    random_state=42,
)

print(f"Using {len(X)} samples.")

# ----------------------------------------------------------
# Load Model
# ----------------------------------------------------------

model = joblib.load(
    PROJECT_ROOT /
    "trained_models" /
    "Model_B_random_forest.pkl"
)

print("\nLoaded Model:")
print(type(model))

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
# Random Forest Feature Importance
# ----------------------------------------------------------

importance = pd.DataFrame({

    "Feature": FEATURES,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False,
)

importance.to_csv(

    figure_folder /

    "feature_importance.csv",

    index=False,

)

plt.figure(figsize=(8,6))

plt.barh(

    importance["Feature"],

    importance["Importance"]

)

plt.gca().invert_yaxis()

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig(

    figure_folder /

    "rf_feature_importance.png",

    dpi=300,

)

plt.close()

print("✓ Random Forest Feature Importance saved.")

# ----------------------------------------------------------
# SHAP
# ----------------------------------------------------------

print()

print("Building TreeExplainer...")

explainer = shap.TreeExplainer(model)

print("Calculating SHAP values...")

shap_values = explainer(X)

print("✓ SHAP values calculated.")

print()

print("SHAP object type:")
print(type(shap_values))

print("SHAP values shape:")
print(shap_values.values.shape)

# ----------------------------------------------------------
# Handle Binary Classification
# ----------------------------------------------------------

values = shap_values.values

# Binary classification returns (samples, features, classes)

if values.ndim == 3:

    print("Binary classifier detected.")

    values = values[:, :, 1]

elif values.ndim == 2:

    print("Single-output SHAP detected.")

else:

    raise ValueError(
        f"Unexpected SHAP shape: {values.shape}"
    )

# ----------------------------------------------------------
# SHAP BAR
# ----------------------------------------------------------

plt.figure(figsize=(10,7))

shap.summary_plot(

    values,

    X,

    plot_type="bar",

    show=False,

)

plt.tight_layout()

plt.savefig(

    figure_folder /

    "shap_feature_importance.png",

    dpi=300,

)

plt.close()

print("✓ SHAP Feature Importance saved.")

# ----------------------------------------------------------
# SHAP SUMMARY
# ----------------------------------------------------------

plt.figure(figsize=(10,7))

shap.summary_plot(

    values,

    X,

    show=False,

)

plt.tight_layout()

plt.savefig(

    figure_folder /

    "shap_summary.png",

    dpi=300,

)

plt.close()

print("✓ SHAP Summary saved.")

# ----------------------------------------------------------
# Top 5 Dependence Plots
# ----------------------------------------------------------

top5 = importance.head(5)["Feature"].tolist()

print()

print("Generating dependence plots...")

for feature in top5:

    plt.figure(figsize=(8,6))

    shap.dependence_plot(

        feature,

        values,

        X,

        interaction_index=None,

        show=False,

    )

    plt.tight_layout()

    plt.savefig(

        figure_folder /

        f"shap_{feature}.png",

        dpi=300,

    )

    plt.close()

print("✓ Dependence plots saved.")

print()

print("=" * 80)
print("SHAP ANALYSIS COMPLETED")
print("=" * 80)

print()

print("Generated files:")

print()

print("feature_importance.csv")

print("rf_feature_importance.png")

print("shap_feature_importance.png")

print("shap_summary.png")

for feature in top5:

    print(f"shap_{feature}.png")