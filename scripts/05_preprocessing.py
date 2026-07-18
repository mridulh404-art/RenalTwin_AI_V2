from pathlib import Path
import numpy as np
import pandas as pd

# ==========================================================
# RenalTwin AI Version 2
# Data Preprocessing
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Data Preprocessing")
print("=" * 80)

# ----------------------------------------------------------
# Load engineered dataset
# ----------------------------------------------------------

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_engineered.csv"
)

print(f"Original shape: {df.shape}")

# ----------------------------------------------------------
# Adults only
# ----------------------------------------------------------

df = df[df["RIDAGEYR"] >= 18].copy()

print(f"Adult dataset: {df.shape}")

# ----------------------------------------------------------
# Diabetes
# NHANES:
# 1 = Yes
# 2 = No
# others = Missing
# ----------------------------------------------------------

df["Diabetes"] = np.where(
    df["DIQ010"] == 1,
    1,
    np.where(df["DIQ010"] == 2, 0, np.nan)
)

# ----------------------------------------------------------
# Smoking
# NHANES:
# 1 = Yes
# 2 = No
# others = Missing
# ----------------------------------------------------------

df["Smoker"] = np.where(
    df["SMQ020"] == 1,
    1,
    np.where(df["SMQ020"] == 2, 0, np.nan)
)

# ----------------------------------------------------------
# Sex
# 1 = Male
# 2 = Female
# ----------------------------------------------------------

df["Female"] = np.where(
    df["RIAGENDR"] == 2,
    1,
    0
)

# ----------------------------------------------------------
# Log Transform
# ----------------------------------------------------------

df["Log_SII"] = np.log1p(df["SII"])

df["Log_UACR"] = np.log1p(df["URDACT"])

print("✓ Log transformations completed")

# ----------------------------------------------------------
# Select Model Variables
# ----------------------------------------------------------

model = df[
    [
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
        "LBXSCR",
        "LBDSALSI",
        "URDACT",
        "Log_UACR",
        "SII",
        "Log_SII",
        "eGFR",
        "CKD",
    ]
].copy()

# ----------------------------------------------------------
# Median Imputation
# ----------------------------------------------------------

numeric = model.select_dtypes(include="number").columns

for col in numeric:

    if col != "CKD":

        model[col] = model[col].fillna(
            model[col].median()
        )

print("✓ Missing values imputed")

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

output = PROJECT_ROOT / "data/processed"

model.to_csv(
    output / "renal_twin_model.csv",
    index=False
)

print()

print("=" * 80)
print("Preprocessing completed successfully.")
print("=" * 80)

print(model.shape)

print()

print(model.head())